# SPDX-License-Identifier: GPL-2.0-or-later
"""Executed ONLY by an explicit Blender executable; imports real bundled bpy."""
import argparse
import importlib
import json
from pathlib import Path
import sys
import traceback

import bpy
from mathutils import Vector


class Unsupported(Exception):
    pass


def near(actual, expected, tolerance=1e-5):
    assert len(actual) == len(expected)
    assert all(abs(a - b) <= tolerance for a, b in zip(actual, expected)), (list(actual), expected)


def cube():
    obj = bpy.data.objects.get('Cube')
    assert obj is not None and obj.type == 'MESH', 'Factory cube missing'
    assert len(obj.data.vertices) == 8 and len(obj.data.polygons) == 6
    assert bpy.context.scene.camera is not None
    return obj


def transform(obj):
    obj.location = (0.25, -0.5, 0.75)
    obj.rotation_euler = (0.1, 0.2, 0.3)
    obj.scale = (1.1, 0.9, 1.2)
    bpy.context.view_layer.update()
    near(obj.location, (0.25, -0.5, 0.75))
    near(obj.rotation_euler, (0.1, 0.2, 0.3))
    near(obj.scale, (1.1, 0.9, 1.2))
    near(obj.matrix_world.translation, (0.25, -0.5, 0.75))


def material(obj):
    mat = bpy.data.materials.new('QA_Material')
    mat.use_nodes = True
    shader = next(n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    shader.inputs['Base Color'].default_value = (0.8, 0.15, 0.05, 1.0)
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    assert obj.data.materials[0] == mat
    near(shader.inputs['Base Color'].default_value, (0.8, 0.15, 0.05, 1.0))


def modifier(obj):
    mod = obj.modifiers.new('QA_Subdivision', 'SUBSURF')
    mod.levels = 1
    mod.render_levels = 1
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    try:
        assert len(mesh.vertices) > len(obj.data.vertices), 'Modifier did not evaluate'
    finally:
        evaluated.to_mesh_clear()


def geometry(obj):
    if bpy.app.version < (2, 92, 0):
        raise Unsupported('Geometry Nodes requires Blender >= 2.92')
    group = bpy.data.node_groups.new('QA_Geometry', 'GeometryNodeTree')
    if hasattr(group, 'interface'):
        group.interface.new_socket(name='Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
        group.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    else:
        group.inputs.new('NodeSocketGeometry', 'Geometry')
        group.outputs.new('NodeSocketGeometry', 'Geometry')
    inp = group.nodes.new('NodeGroupInput')
    out = group.nodes.new('NodeGroupOutput')
    out.is_active_output = True
    group.links.new(inp.outputs['Geometry'], out.inputs['Geometry'])
    mod = obj.modifiers.new('QA_GeometryNodes', 'NODES')
    mod.node_group = group
    bpy.context.view_layer.update()
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    try:
        assert len(mesh.vertices) >= 8 and len(mesh.polygons) >= 6
        assert len(group.links) == 1
    finally:
        evaluated.to_mesh_clear()


def animation(obj):
    scene = bpy.context.scene
    obj.location = (0, 0, 0)
    assert obj.keyframe_insert(data_path='location', frame=1)
    obj.location = (1, 2, 3)
    assert obj.keyframe_insert(data_path='location', frame=10)
    assert obj.animation_data is not None and obj.animation_data.action is not None
    scene.frame_set(1)
    near(obj.location, (0, 0, 0))
    scene.frame_set(10)
    near(obj.location, (1, 2, 3))
    scene.frame_set(5)
    assert 0 < obj.location.x < 1, 'Animation interpolation not evaluated'
    scene.frame_set(1)


def addon(output):
    import addon_utils
    directory = output / 'temporary_addon'
    directory.mkdir()
    name = 'qa_temporary_addon'
    source = '''import bpy
bl_info = {"name": "QA Temporary", "blender": (2, 80, 0), "category": "Development"}
class QA_OT_probe(bpy.types.Operator):
    bl_idname = "qa.smoke_probe"
    bl_label = "QA Smoke Probe"
    def execute(self, context):
        context.scene["qa_addon_executed"] = True
        return {'FINISHED'}
def register():
    bpy.utils.register_class(QA_OT_probe)
def unregister():
    bpy.utils.unregister_class(QA_OT_probe)
'''
    (directory / (name + '.py')).write_text(source, encoding='utf-8')
    sys.path.insert(0, str(directory))
    importlib.invalidate_caches()
    try:
        module = addon_utils.enable(name, default_set=False, persistent=False)
        assert module is not None, 'Temporary add-on failed to enable'
        assert addon_utils.check(name)[1]
        assert bpy.ops.qa.smoke_probe() == {'FINISHED'}
        assert bpy.context.scene['qa_addon_executed'] is True
    finally:
        addon_utils.disable(name, default_set=False)
        sys.path.remove(str(directory))
    assert not addon_utils.check(name)[1]
    assert bpy.types.Operator.bl_rna_get_subclass_py('QA_OT_probe', None) is None
    assert name not in bpy.context.preferences.addons, 'Unexpected preference registration'


def obj_export(output):
    obj = cube()
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = output / 'cube.obj'
    try:
        bpy.ops.wm.obj_export.get_rna_type()
    except (AttributeError, RuntimeError):
        try:
            bpy.ops.export_scene.obj.get_rna_type()
        except (AttributeError, RuntimeError):
            raise RuntimeError('No supported OBJ exporter registered in this build')
        result = bpy.ops.export_scene.obj(filepath=str(path), use_selection=True)
    else:
        result = bpy.ops.wm.obj_export(filepath=str(path), export_selected_objects=True)
    assert result == {'FINISHED'}
    text = path.read_text(encoding='utf-8')
    assert sum(line.startswith('v ') for line in text.splitlines()) >= 8
    assert sum(line.startswith('f ') for line in text.splitlines()) >= 6


def save(output):
    obj = cube()
    transform(obj)
    material(obj)
    modifier(obj)
    if bpy.app.version >= (2, 92, 0):
        geometry(obj)
    animation(obj)
    bpy.context.scene['qa_saved_marker'] = 'separate-process-v1'
    path = output / 'compatibility.blend'
    assert bpy.ops.wm.save_as_mainfile(filepath=str(path), check_existing=False) == {'FINISHED'}
    assert path.is_file() and path.stat().st_size > 0


def reopen(output):
    path = output / 'compatibility.blend'
    assert path.is_file()
    assert bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False) == {'FINISHED'}
    assert Path(bpy.data.filepath).resolve() == path.resolve()
    assert bpy.context.scene['qa_saved_marker'] == 'separate-process-v1'
    obj = cube()
    near(obj.rotation_euler, (0.1, 0.2, 0.3))
    near(obj.scale, (1.1, 0.9, 1.2))
    assert obj.data.materials[0].name == 'QA_Material'
    shader = next(n for n in obj.data.materials[0].node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    near(shader.inputs['Base Color'].default_value, (0.8, 0.15, 0.05, 1))
    assert obj.modifiers['QA_Subdivision'].type == 'SUBSURF'
    assert obj.modifiers['QA_Subdivision'].levels == 1
    if bpy.app.version >= (2, 92, 0):
        group = obj.modifiers['QA_GeometryNodes'].node_group
        assert group.name == 'QA_Geometry' and len(group.links) == 1
    evaluated = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh = evaluated.to_mesh()
    try:
        assert len(mesh.vertices) > 8, 'Saved modifier stack did not evaluate after reopen'
    finally:
        evaluated.to_mesh_clear()
    bpy.context.scene.frame_set(10)
    near(obj.location, (1, 2, 3))
    bpy.context.scene.frame_set(1)
    near(obj.location, (0, 0, 0))


def render(output, engine):
    scene = bpy.context.scene
    if engine == 'eevee':
        chosen = None
        for candidate in ('BLENDER_EEVEE_NEXT', 'BLENDER_EEVEE'):
            try:
                scene.render.engine = candidate
            except (TypeError, ValueError):
                continue
            chosen = candidate
            break
        assert chosen is not None, 'Eevee not available in build'
    else:
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'CPU'
        scene.cycles.samples = 4
        scene.cycles.use_denoising = False
        assert scene.cycles.device == 'CPU'
        chosen = 'CYCLES'
    scene.camera.location = (5, -5, 4)
    scene.camera.rotation_euler = (-scene.camera.location).to_track_quat('-Z', 'Y').to_euler()
    scene.render.resolution_x = 32
    scene.render.resolution_y = 32
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    path = output / (engine + '.png')
    scene.render.filepath = str(path)
    scene.render.use_file_extension = True
    assert bpy.ops.render.render(write_still=True) == {'FINISHED'}
    assert path.is_file() and path.stat().st_size > 0
    image = bpy.data.images.load(str(path), check_existing=False)
    try:
        assert tuple(image.size) == (32, 32)
        pixels = list(image.pixels[:])
        assert len(pixels) == 32 * 32 * 4
        assert max(pixels[0::4]) - min(pixels[0::4]) > 1e-4, 'Render appears uniform'
    finally:
        bpy.data.images.remove(image)
    return {'engine': chosen, 'device': 'CPU' if engine == 'cycles' else 'Eevee graphics context',
            'image': str(path), 'resolution': [32, 32]}


def api():
    assert isinstance(bpy.app.version, tuple) and len(bpy.app.version) == 3
    assert bpy.app.background is True
    assert bpy.context.scene is not None
    assert callable(bpy.utils.register_class)
    assert bpy.ops.wm.save_as_mainfile.get_rna_type() is not None
    cube()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', required=True)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--result', required=True, type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
    output = args.output.resolve()
    root = Path(__file__).resolve().parent
    assert output.is_relative_to(root) and output != root
    assert args.result.resolve().parent == output
    result = {'case': args.case, 'status': 'FAIL', 'version': list(bpy.app.version),
              'version_string': bpy.app.version_string,
              'build_hash': bpy.app.build_hash.decode('ascii', errors='replace'),
              'binary_path': bpy.app.binary_path}
    cases = {'api': api, 'cube_transform': lambda: transform(cube()),
             'material': lambda: material(cube()), 'modifier': lambda: modifier(cube()),
             'geometry_nodes': lambda: geometry(cube()), 'animation': lambda: animation(cube()),
             'addon': lambda: addon(output), 'obj_export': lambda: obj_export(output),
             'blend_save': lambda: save(output), 'blend_reopen': lambda: reopen(output),
             'eevee_render': lambda: render(output, 'eevee'),
             'cycles_cpu_render': lambda: render(output, 'cycles')}
    try:
        details = cases[args.case]()
        result.update(status='PASS', details=details)
    except Unsupported as error:
        result.update(status='SKIP', reason=str(error))
    except Exception as error:
        result.update(reason=str(error), traceback=traceback.format_exc())
        raise
    finally:
        args.result.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
