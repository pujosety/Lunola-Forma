# SPDX-License-Identifier: GPL-2.0-or-later
"""Host-side contract tests; never imports or mocks bpy."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent
CASES = ['api', 'cube_transform', 'material', 'modifier', 'geometry_nodes',
         'animation', 'addon', 'obj_export', 'blend_save', 'blend_reopen',
         'eevee_render', 'cycles_cpu_render']

class RunnerContract(unittest.TestCase):
    def test_missing_executable_records_not_run(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as work:
            result = subprocess.run([sys.executable, str(ROOT / 'run_smoke.py'),
                '--blender', str(Path(work) / 'nonexistent.exe'), '--output', work],
                capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2, result.stderr)
            report = json.loads((Path(work) / 'summary.json').read_text())
            self.assertEqual(report['status'], 'NOT RUN')
            self.assertEqual([c['case'] for c in report['cases']], CASES)
            self.assertTrue(all(c['status'] == 'NOT RUN' for c in report['cases']))
            self.assertIn('not a file', report['error'])

    def test_executable_argument_required(self):
        result = subprocess.run([sys.executable, str(ROOT / 'run_smoke.py')],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertIn('--blender', result.stderr)

if __name__ == '__main__':
    unittest.main()
