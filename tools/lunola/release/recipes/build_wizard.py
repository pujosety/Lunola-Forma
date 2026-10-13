# SPDX-License-Identifier: GPL-2.0-or-later
"""Build a separate MSI with the real native WixUI_InstallDir wizard."""
from pathlib import Path
import json,subprocess,uuid,xml.etree.ElementTree as E
R=Path('D:/Lunola/Forma');A=R/'audit/installer-wizard';prior=R/'audit/release-installer'
name='Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64-Setup'
out=R/'packages'/name;assert not out.exists();out.mkdir()
license_text=(prior/'payload/license/spdx/GPL-3.0-or-later.txt').read_text()
rtf=[]
for ch in license_text:
 if ch in '\\{}':rtf.append('\\'+ch)
 elif ch=='\n':rtf.append('\\par\n')
 elif ch=='\r':continue
 elif ord(ch)<128:rtf.append(ch)
 else:
  for i in range(0,len(ch.encode('utf-16-le')),2):
   unit=int.from_bytes(ch.encode('utf-16-le')[i:i+2],'little');rtf.append('\\u'+str(unit if unit<32768 else unit-65536)+'?')
license_rtf=A/'Lunola-License.rtf';license_rtf.write_text('{\\rtf1\\ansi\\deff0{\\fonttbl{\\f0 Segoe UI;}}\\f0\\fs18 '+''.join(rtf)+'}',encoding='ascii')
ns='http://schemas.microsoft.com/wix/2006/wi';E.register_namespace('',ns)
tree=E.parse(prior/'LunolaForma.wxs');product=tree.getroot().find('{'+ns+'}Product')
base_manifest=json.loads((prior/'payload-manifest.json').read_text())
product.set('Id','{'+str(uuid.uuid5(uuid.UUID(product.get('UpgradeCode').strip('{}')),'setup-ui-revision-1:'+base_manifest['binary_commit'])).upper()+'}')
product.find('{'+ns+'}MajorUpgrade').set('AllowSameVersionUpgrades','yes')
for node in list(product):
 if node.tag=='{'+ns+'}Upgrade' and any(v.get('Property')=='LUNOLA_SAME_VERSION_INSTALLED' for v in node):product.remove(node)
 if node.tag=='{'+ns+'}Condition' and 'LUNOLA_SAME_VERSION_INSTALLED' in (node.text or ''):product.remove(node)
for p in list(product.findall('{'+ns+'}Property')):
 if p.get('Id')=='ARPNOMODIFY':product.remove(p)
E.SubElement(product,'{'+ns+'}Property',{'Id':'WIXUI_INSTALLDIR','Value':'LUNOLA_INSTALLFOLDER'})
E.SubElement(product,'{'+ns+'}UIRef',{'Id':'WixUI_InstallDir'})
E.SubElement(product,'{'+ns+'}UIRef',{'Id':'WixUI_ErrorProgressText'})
E.SubElement(product,'{'+ns+'}WixVariable',{'Id':'WixUILicenseRtf','Value':str(license_rtf)})
E.indent(tree);source=A/'LunolaForma-Setup.wxs';tree.write(source,encoding='utf-8',xml_declaration=True)
manifest=json.loads((prior/'payload-manifest.json').read_text());manifest['installer']=str(out/(name+'.msi'));manifest['previous_product_code']=manifest['product_code'];manifest['product_code']=product.get('Id');manifest['ui_revision']='1'
(A/'payload-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
tools=Path('D:/DevTools/WiX/3.14.1/bin');obj=A/'LunolaForma-Setup.wixobj'
for label,args in [('candle',['-nologo','-arch','x64','-out',str(obj),str(source)]),('light',['-nologo','-ext',str(tools/'WixUIExtension.dll'),'-cc',str(prior),'-reusecab','-out',manifest['installer'],str(obj)])]:
 print('BUILD '+label,flush=True)
 with (A/(label+'.log')).open('w') as log:code=subprocess.call([str(tools/(label+'.exe'))]+args,stdout=log,stderr=subprocess.STDOUT,cwd=A)
 if code!=0:
  print('\n'.join(line for line in (A/(label+'.log')).read_text(errors='replace').splitlines() if ' : error ' in line),flush=True)
  raise RuntimeError(label+' failed; see its full log')
print('WIZARD MSI BUILT: '+manifest['installer'],flush=True)
