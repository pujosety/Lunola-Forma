# SPDX-License-Identifier: GPL-2.0-or-later
"""Stdlib-only launcher. Blender executes blender_smoke.py with its own Python."""
import argparse
import datetime
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
CASES = ['api', 'cube_transform', 'material', 'modifier', 'geometry_nodes',
         'animation', 'addon', 'obj_export', 'blend_save', 'blend_reopen',
         'eevee_render', 'cycles_cpu_render']


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', required=True, help='Explicit executable path; never PATH lookup')
    parser.add_argument('--output', type=Path, default=None, help='New/empty directory beneath tools/lunola/qa')
    parser.add_argument('--timeout', type=float, default=180, help='Seconds per non-render process')
    parser.add_argument('--render-timeout', type=float, default=300)
    args = parser.parse_args()
    if not all(math.isfinite(v) and v > 0 for v in (args.timeout, args.render_timeout)):
        parser.error('timeouts must be finite and positive')
    output = (args.output or ROOT / 'results' / datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')).resolve()
    if not output.is_relative_to(ROOT) or output == ROOT:
        parser.error('--output must be a child directory beneath tools/lunola/qa')
    if output.exists() and any(output.iterdir()):
        parser.error('--output must be empty (prevents stale-result success)')
    output.mkdir(parents=True, exist_ok=True)
    executable = Path(args.blender).expanduser().resolve()
    report = {'schema': 1, 'status': 'NOT RUN', 'executable': str(executable),
              'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'cases': [{'case': c, 'status': 'NOT RUN'} for c in CASES]}
    if not executable.is_file():
        report['error'] = 'Explicit Blender executable is not a file: ' + str(executable)
        dump(output / 'summary.json', report)
        print(report['error'], file=sys.stderr)
        return 2
    env = os.environ.copy()
    for key in ('BLENDER_USER_CONFIG', 'BLENDER_USER_SCRIPTS', 'BLENDER_USER_DATAFILES',
                'BLENDER_USER_EXTENSIONS', 'TMP', 'TEMP', 'TMPDIR'):
        directory = output / 'isolated' / key.lower()
        directory.mkdir(parents=True, exist_ok=True)
        env[key] = str(directory)
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    for item in report['cases']:
        case = item['case']
        if case == 'blend_reopen' and next(c for c in report['cases'] if c['case'] == 'blend_save')['status'] != 'PASS':
            item['reason'] = 'Dependency blend_save did not pass'
            continue
        result_file = output / (case + '.json')
        command = [str(executable), '--background', '--factory-startup', '--disable-autoexec',
                   '--threads', '1', '--python-exit-code', '17',
                   '--python', str(ROOT / 'blender_smoke.py'), '--',
                   '--case', case, '--output', str(output), '--result', str(result_file)]
        item['command'] = command
        limit = args.render_timeout if case.endswith('_render') else args.timeout
        item['timeout_seconds'] = limit
        start = time.monotonic()
        try:
            with (output / (case + '.log')).open('wb') as log:
                process = subprocess.run(command, cwd=output, env=env, stdout=log,
                                         stderr=subprocess.STDOUT, timeout=limit, check=False)
            item['returncode'] = process.returncode
            if result_file.is_file():
                child = json.loads(result_file.read_text(encoding='utf-8'))
                if child.get('case') != case or child.get('status') not in ('PASS', 'FAIL', 'SKIP'):
                    raise ValueError('Invalid child report')
                item['blender_result'] = child
                item['status'] = child['status']
            else:
                item['status'] = 'FAIL'
                item['reason'] = 'Blender produced no result JSON'
            if process.returncode != 0:
                item['status'] = 'FAIL'
                item['reason'] = 'Blender process exited nonzero'
        except subprocess.TimeoutExpired:
            item.update(status='FAIL', reason='Process timeout; subprocess killed and waited')
        except (OSError, ValueError) as error:
            item.update(status='FAIL', reason=str(error))
        item['duration_seconds'] = round(time.monotonic() - start, 3)
        dump(output / 'summary.json', report)
        print(case + ': ' + item['status'])
    statuses = [item['status'] for item in report['cases']]
    report['status'] = 'FAIL' if any(s in ('FAIL', 'NOT RUN') for s in statuses) else ('PASS WITH SKIPS' if 'SKIP' in statuses else 'PASS')
    report['finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    dump(output / 'summary.json', report)
    print('Report: ' + str(output / 'summary.json'))
    return 1 if report['status'] == 'FAIL' else 0


if __name__ == '__main__':
    sys.exit(main())
