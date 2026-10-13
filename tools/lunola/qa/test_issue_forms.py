# SPDX-License-Identifier: GPL-2.0-or-later
"""Independently validate real issue-form YAML and product documentation.
Run with PyYAML available, e.g. uv run --with PyYAML python this_script.py.
"""
from pathlib import Path
import json
import re
import subprocess
import yaml
ROOT = Path(__file__).resolve().parents[3]
checks = []
def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})

expected = ['bug_report.yml', 'feature_request.yml', 'performance_issue.yml', 'compatibility_issue.yml']
forms = ROOT / '.github/ISSUE_TEMPLATE'
check('exactly_four_form_files', sorted(p.name for p in forms.glob('*.yml')) == sorted(expected))
for filename in expected:
    path = forms / filename
    form = yaml.safe_load(path.read_text(encoding='utf-8'))
    check(filename + ':mapping', isinstance(form, dict))
    for field in ['name', 'description', 'title']:
        check(filename + ':' + field, isinstance(form.get(field), str) and bool(form[field]))
    for forbidden in ['labels', 'assignees', 'projects']:
        check(filename + ':no_default_' + forbidden, forbidden not in form)
    body = form['body']; ids = []
    check(filename + ':body', isinstance(body, list) and bool(body))
    for index, item in enumerate(body):
        prefix = filename + ':body:' + str(index)
        check(prefix + ':mapping', isinstance(item, dict))
        check(prefix + ':supported_type', item['type'] in ['markdown', 'input', 'textarea', 'checkboxes', 'dropdown'])
        attributes = item['attributes']
        check(prefix + ':attributes', isinstance(attributes, dict))
        if item['type'] == 'markdown':
            check(prefix + ':privacy_disclosure', 'never collected' in attributes['value'] and 'public' in attributes['value'])
        else:
            ids.append(item['id'])
            check(prefix + ':id', bool(re.fullmatch('[a-z][a-z0-9_]*', item['id'])))
            check(prefix + ':label', isinstance(attributes.get('label'), str) and bool(attributes['label']))
            if item['type'] in ['input', 'textarea']:
                check(prefix + ':description', isinstance(attributes.get('description'), str) and bool(attributes['description']))
                check(prefix + ':required_flag', isinstance(item.get('validations', {}).get('required'), bool))
    check(filename + ':unique_ids', len(ids) == len(set(ids)))
    by_id = {item['id']: item for item in body if 'id' in item}
    for required in ['version', 'os', 'gpu_driver', 'reproduction', 'expected', 'actual']:
        check(filename + ':required:' + required, by_id[required]['validations']['required'] is True)
    check(filename + ':logs_optional', by_id['logs']['validations']['required'] is False)
    check(filename + ':review_required', by_id['privacy']['attributes']['options'][0]['required'] is True)
    ignored = subprocess.run(['git', 'check-ignore', str(path.relative_to(ROOT))], cwd=ROOT, capture_output=True)
    check(filename + ':not_ignored', ignored.returncode == 1)

readme = (ROOT / 'README.md').read_text(encoding='utf-8')
for heading in ['Overview', 'Features', 'Screenshots', 'Installation', 'System requirements', 'Build from source', 'Documentation', 'Issues', 'Contributing', 'Releases', 'Attribution', 'License']:
    check('README:section:' + heading, '## ' + heading in readme)
for name in ['README.md', 'CHANGELOG.md', 'docs/lunola/ISSUE_REPORTING.md', 'docs/lunola/product/TUTORIALS.md']:
    path = ROOT / name
    for index, target in enumerate(re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8'))):
        if not target.startswith(('https:', 'http:', '#', 'mailto:')):
            check(name + ':local_link:' + str(index), (path.parent / target.split('#')[0]).exists())
for name in ['COPYING', 'AUTHORS']:
    original = subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT).replace(b'\r\n', b'\n')
    check(name + ':preserved', (ROOT / name).read_bytes().replace(b'\r\n', b'\n') == original)
check('credentials_remain_ignored', subprocess.run(['git', 'check-ignore', '.env'], cwd=ROOT, capture_output=True).returncode == 0)
failed = [item for item in checks if not item['passed']]
report = {'scope': 'Independent host/schema/source checks; not rebuild or GUI', 'checks': len(checks), 'passed': len(checks) - len(failed), 'failed': failed}
print(json.dumps(report, indent=2))
raise SystemExit(bool(failed))
