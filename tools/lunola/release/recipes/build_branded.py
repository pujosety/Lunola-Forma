# SPDX-License-Identifier: GPL-2.0-or-later
"""Build branded UI revision 2; never run an installer on this host."""
from pathlib import Path
import hashlib,json,subprocess,uuid,xml.etree.ElementTree as E
R=Path('D:/Lunola/Forma');A=R/'audit/installer-branding';prior=R/'audit/installer-wizard'
art=R/'publication/release/windows/installer_lunola';name='Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64-Setup-r2'
out=R/'packages'/name;assert not out.exists(),'Never overwrite released or previously inspected candidates'
assets=json.loads((art/'manifest.json').read_text())
for file in ['LunolaDialog.bmp','LunolaBanner.bmp']:
 with (art/file).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==assets['derivatives'][file]['sha256'],file
ns='http://schemas.microsoft.com/wix/2006/wi';E.register_namespace('',ns)
tree=E.parse(prior/'LunolaForma-Setup.wxs');product=tree.getroot().find('{'+ns+'}Product')
base=json.loads((prior/'payload-manifest.json').read_text());previous=product.get('Id')
assert previous==base['product_code']=='{425A1781-FC04-5D6F-BA22-C56AFD2B6FE4}'
code='{'+str(uuid.uuid5(uuid.UUID(product.get('UpgradeCode').strip('{}')),'setup-ui-revision-2:'+base['binary_commit'])).upper()+'}'
product.set('Id',code)
for key,file in [('WixUIDialogBmp','LunolaDialog.bmp'),('WixUIBannerBmp','LunolaBanner.bmp')]:
 assert not any(p.get('Id')==key for p in product.findall('{'+ns+'}WixVariable'))
 E.SubElement(product,'{'+ns+'}WixVariable',{'Id':key,'Value':str(art/file)})
E.indent(tree);source=A/'LunolaForma-Branded-Setup.wxs';tree.write(source,encoding='utf-8',xml_declaration=True)
out.mkdir();base.update(installer=str(out/(name+'.msi')),previous_product_code=previous,product_code=code,ui_revision='2')
(A/'payload-manifest.json').write_text(json.dumps(base,indent=2)+'\n')
tools=Path('D:/DevTools/WiX/3.14.1/bin');obj=A/'LunolaForma-Branded-Setup.wixobj'
for label,args in [('candle',['-nologo','-arch','x64','-out',str(obj),str(source)]),('light',['-nologo','-ext',str(tools/'WixUIExtension.dll'),'-cc',str(R/'audit/release-installer'),'-reusecab','-out',base['installer'],str(obj)])]:
 print('BUILD '+label,flush=True)
 with (A/(label+'.log')).open('w') as log:ret=subprocess.call([str(tools/(label+'.exe'))]+args,stdout=log,stderr=subprocess.STDOUT,cwd=A)
 if ret:
  print('\n'.join(s for s in (A/(label+'.log')).read_text(errors='replace').splitlines() if ' : error ' in s),flush=True)
  raise RuntimeError(label+' failed; no install or release performed')
print('BRANDED REVISION 2 MSI BUILT: '+base['installer'],flush=True)
