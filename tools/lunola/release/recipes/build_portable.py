# SPDX-License-Identifier: GPL-2.0-or-later
"""Create a local CPack ZIP from the exact verified runtime, then read it back."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,zipfile
R=Path('D:/Lunola/Forma');A=R/'audit/release-portable'
SOURCE=R/'publication';runtime=R/'Lunola-Forma-complete-identity-final'
state=json.loads((R/'audit/complete-identity-final/build-state.json').read_text())
assert state['commit']=='d373d95263ee1824ac864ab9f0478274754c0b4a'
assert state['qa_pass_count']==12
name='Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64'
out=R/'packages'/name;stage=A/'stage'/name
assert not out.exists(),'Never overwrite a previous package'
assert not stage.exists(),'Never reuse a stale stage'
config=R/'build-phase-c/CPackConfig.cmake'
config_text=config.read_text()
for variable,value in [('CPACK_PACKAGE_NAME','Lunola Forma'),('CPACK_PACKAGE_VENDOR','Pujo Setyo'),('CPACK_PACKAGE_VERSION','5.4.0')]:
 assert f'set({variable} "{value}")' in config_text,variable
version=subprocess.check_output([str(runtime/'blender.exe'),'--version'],text=True)
assert 'd373d95263ee' in version and '5.4.0 Alpha' in version
out.mkdir(parents=True);stage.mkdir(parents=True)
manifest={};excluded=[]
for p in sorted(runtime.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(runtime).as_posix()
 if p.suffix.lower() in {'.pdb','.lib'}:excluded.append(rel);continue
 assert not p.is_symlink(),rel
 target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
 with p.open('rb') as stream:manifest[rel]=hashlib.file_digest(stream,'sha256').hexdigest()
for legal in ['COPYING','AUTHORS']:
 shutil.copy2(SOURCE/legal,stage/legal)
info={'product_name':'Lunola Forma','byline':'by Pujo Setyo','vendor':'Pujo Setyo','engine_version':'5.4.0 Alpha','binary_commit':state['commit'],'package_type':'Windows x64 portable development build','remote_publication':False,'distribution_status':'Local verification only; not approved for public redistribution','source_publication_status':'Modified source exists locally; this identity commit has not been pushed','remaining_gates':['Corresponding modified source publication','Artwork/dependency redistribution review','Signed installer and coexistence','Clean-machine validation','Native OS DPI/hardware coverage']}
(stage/'LUNOLA_PACKAGE_INFO.json').write_text(json.dumps(info,indent=2)+'\n')
(stage/'LUNOLA_README.txt').write_text('Lunola Forma\nby Pujo Setyo\n\nWindows x64 portable development build, based on Blender 5.4.0 Alpha.\nExtract the complete folder; run blender-launcher.exe or blender.exe.\nNo installation, registry changes or file associations are performed by this ZIP.\nThe internal executable name is retained for compatibility.\n\nLocal verification package only: NOT a public release.\nModified source publication and redistribution reviews are pending.\nSee LUNOLA_PACKAGE_INFO.json and the preserved license directory, COPYING and AUTHORS.\n')
cpack=Path('D:/DevTools/VisualStudio/2022/Community/Common7/IDE/CommonExtensions/Microsoft/CMake/CMake/bin/cpack.exe')
command=[str(cpack),'--config',str(config),'-G','ZIP','-D','CPACK_INSTALL_CMAKE_PROJECTS=','-D',f'CPACK_INSTALLED_DIRECTORIES={stage.as_posix()};/','-D',f'CPACK_PACKAGE_FILE_NAME={name}','-D',f'CPACK_PACKAGE_DIRECTORY={out.as_posix()}','-D','CPACK_INCLUDE_TOPLEVEL_DIRECTORY=ON']
(A/'effective-package-settings.json').write_text(json.dumps({'command':command,'source_config':str(config),'product_name':'Lunola Forma','vendor':'Pujo Setyo','archive_name':name+'.zip','installation_performed':False},indent=2))
print('CPACK ZIP: '+name,flush=True)
with (A/'cpack.log').open('w') as log:result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,cwd=A)
assert result.returncode==0,(A/'cpack.log').read_text()
archive=out/(name+'.zip');assert archive.is_file()
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 files={n for n in z.namelist() if not n.endswith('/')}
 expected={name+'/'+p for p in manifest}|{name+'/'+p for p in ['COPYING','AUTHORS','LUNOLA_PACKAGE_INFO.json','LUNOLA_README.txt']}
 assert files==expected,{'extra':list(files-expected),'missing':list(expected-files)}
 for rel,digest in manifest.items():assert hashlib.sha256(z.read(name+'/'+rel)).hexdigest()==digest,rel
 extract=A/'extracted';assert not extract.exists()
 z.extractall(extract)
with archive.open('rb') as stream:archive_sha=hashlib.file_digest(stream,'sha256').hexdigest()
(out/'SHA256SUMS.txt').write_text(archive_sha+'  '+archive.name+'\n')
report={**info,'archive':str(archive),'archive_bytes':archive.stat().st_size,'archive_sha256':archive_sha,'runtime_file_count':len(manifest),'runtime_sha256':manifest,'excluded_developer_files':excluded,'crc_check':'PASS','archive_roundtrip_hash_check':'PASS','extracted_executable':str(extract/name/'blender.exe'),'status':'PACKAGED_AND_CONTENT_VERIFIED; runtime execution pending'}
(out/'package-verification.json').write_text(json.dumps(report,indent=2)+'\n')
(A/'latest-package.json').write_text(json.dumps({'out':str(out),'archive':str(archive),'executable':report['extracted_executable']},indent=2))
print(json.dumps({k:report[k] for k in ['archive','archive_bytes','archive_sha256','runtime_file_count','status']},indent=2),flush=True)
