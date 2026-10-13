# SPDX-License-Identifier: GPL-2.0-or-later
"""Build an isolated per-user MSI candidate. Never execute an installer."""
from pathlib import Path
import hashlib,json,shutil,subprocess,uuid,xml.etree.ElementTree as ET
R=Path('D:/Lunola/Forma');A=R/'audit/release-installer';S=R/'publication'
name='Lunola-Forma-5.4.0-Alpha-gitd373d95263ee-Windows-x64'
out=R/'packages'/(name+'-installer');payload=A/'payload'
assert not out.exists() and not payload.exists(),'Never overwrite prior candidate evidence'
portable=json.loads((R/'audit/release-portable/latest-package.json').read_text())
source=R/'audit/release-portable/stage'/name
pinfo=json.loads((Path(portable['out'])/'package-verification.json').read_text())
for rel,digest in pinfo['runtime_sha256'].items():
 with (source/rel).open('rb') as f:assert hashlib.file_digest(f,'sha256').hexdigest()==digest,rel
assert pinfo['runtime_pass_count']==12 and pinfo['binary_commit']=='d373d95263ee1824ac864ab9f0478274754c0b4a'
shutil.copytree(source,payload)
info={k:v for k,v in pinfo.items() if k in ['product_name','vendor','byline','engine_version','binary_commit','remote_publication','remaining_gates']}
info.update(package_type='Windows x64 per-user MSI candidate',distribution_status='Local validation only; install/uninstall and clean-machine tests NOT RUN',profile_isolation='Upstream user preference paths preserved; independent profile coexistence NOT certified',file_associations='Not authored or registered')
(payload/'LUNOLA_PACKAGE_INFO.json').write_text(json.dumps(info,indent=2)+'\n')
(payload/'LUNOLA_README.txt').write_text('Lunola Forma\nby Pujo Setyo\n\nWindows x64 MSI development candidate based on Blender 5.4.0 Alpha.\nThis candidate is NOT approved as a public release.\nPer-user target: LocalAppData\\Programs\\Lunola Forma 5.4.\nStart Menu entry: Lunola Forma 5.4.\nNo .blend associations, thumbnail registration, or Blender installer upgrades are authored.\nApplication preference paths remain upstream-compatible and are NOT independently isolated.\nMatching modified source publication, redistribution reviews, signing, install/uninstall and clean-machine testing are pending.\nPreserve this entire runtime folder and included COPYING, AUTHORS and license directory.\n')
out.mkdir();ns='http://schemas.microsoft.com/wix/2006/wi';ET.register_namespace('',ns)
def elem(parent,tag,**attrs):return ET.SubElement(parent,'{'+ns+'}'+tag,{k:str(v) for k,v in attrs.items()})
def ident(prefix,text):return prefix+hashlib.sha1(text.encode()).hexdigest()
namespace=uuid.uuid5(uuid.NAMESPACE_URL,'https://github.com/pujosety/Lunola-Forma/installer/windows-x64/per-user')
def guid(text):return '{'+str(uuid.uuid5(namespace,text)).upper()+'}'
upgrade=guid('upgrade-lineage');product_code=guid('5.4.0:'+pinfo['binary_commit'])
root=ET.Element('{'+ns+'}Wix');product=elem(root,'Product',Id=product_code,Name='Lunola Forma',Language='1033',Version='5.4.0',Manufacturer='Pujo Setyo',UpgradeCode=upgrade)
elem(product,'Package',Id='*',InstallerVersion='500',Compressed='yes',InstallScope='perUser',InstallPrivileges='limited',Platform='x64',Description='Lunola Forma 5.4.0 Alpha - Windows x64 local candidate',Comments='by Pujo Setyo; local development candidate; not public release')
elem(product,'MediaTemplate',EmbedCab='yes',CompressionLevel='mszip',CabinetTemplate='payload{0}.cab')
elem(product,'MajorUpgrade',DowngradeErrorMessage='A newer Lunola Forma version is already installed.',Schedule='afterInstallInitialize')
# Block parallel same-numeric-version alpha candidates instead of replacing their files blindly.
u=elem(product,'Upgrade',Id=upgrade)
elem(u,'UpgradeVersion',Minimum='5.4.0',Maximum='5.4.0',IncludeMinimum='yes',IncludeMaximum='yes',OnlyDetect='yes',Property='LUNOLA_SAME_VERSION_INSTALLED')
condition=elem(product,'Condition',Message='This Lunola Forma candidate supports current-user installation only.');condition.text='NOT ALLUSERS'
condition=elem(product,'Condition',Message='Uninstall the existing Lunola Forma 5.4.0 alpha before installing another alpha candidate.');condition.text='Installed OR NOT LUNOLA_SAME_VERSION_INSTALLED'
elem(product,'Property',Id='ARPCOMMENTS',Value='Lunola Forma 5.4.0 Alpha by Pujo Setyo - local candidate')
elem(product,'Property',Id='ARPNOMODIFY',Value='1')
elem(product,'Icon',Id='LunolaProductIcon',SourceFile=str(S/'release/windows/icons/winblender.ico'))
elem(product,'Property',Id='ARPPRODUCTICON',Value='LunolaProductIcon')
target=elem(product,'Directory',Id='TARGETDIR',Name='SourceDir')
local=elem(target,'Directory',Id='LocalAppDataFolder')
programs=elem(local,'Directory',Id='LunolaPrograms',Name='Programs')
install=elem(programs,'Directory',Id='LUNOLA_INSTALLFOLDER',Name='Lunola Forma 5.4')
menu=elem(target,'Directory',Id='ProgramMenuFolder');menudir=elem(menu,'Directory',Id='LunolaMenuFolder',Name='Lunola Forma 5.4')
feature=elem(product,'Feature',Id='LunolaRuntime',Title='Lunola Forma',Level='1',Absent='disallow',Display='hidden')
directories={'':install};mapping={}
files=sorted(p for p in payload.rglob('*') if p.is_file())
for p in files:
 rel=p.relative_to(payload).as_posix();parent=p.relative_to(payload).parent.as_posix();parent='' if parent=='.' else parent
 current='';node=install
 for part in parent.split('/') if parent else []:
  current=(current+'/'+part).strip('/')
  if current not in directories:directories[current]=elem(node,'Directory',Id=ident('D_',current),Name=part)
  node=directories[current]
 cid=ident('C_',rel);fid=ident('F_',rel);comp=elem(node,'Component',Id=cid,Guid=guid('file:'+rel),Win64='yes')
 elem(comp,'File',Id=fid,Name=p.name,Source=str(p),KeyPath='no')
 elem(comp,'RegistryValue',Id=ident('R_',rel),Root='HKCU',Key='Software\\Lunola\\Forma\\Installer\\5.4\\Components',Name=cid,Type='integer',Value='1',KeyPath='yes')
 elem(feature,'ComponentRef',Id=cid)
 with p.open('rb') as stream:mapping[fid]={'path':rel,'sha256':hashlib.file_digest(stream,'sha256').hexdigest()}
for rel,node in {'SHARED_PROGRAMS':programs, **directories}.items():
 cid=ident('Clean_',rel or 'ROOT');comp=elem(node,'Component',Id=cid,Guid=guid('directory:'+rel),Win64='yes')
 elem(comp,'RemoveFolder',Id=ident('Remove_',rel or 'ROOT'),On='uninstall')
 elem(comp,'RegistryValue',Id=ident('DirReg_',rel or 'ROOT'),Root='HKCU',Key='Software\\Lunola\\Forma\\Installer\\5.4\\Directories',Name=cid,Type='integer',Value='1',KeyPath='yes');elem(feature,'ComponentRef',Id=cid)
comp=elem(menudir,'Component',Id='LunolaShortcut',Guid=guid('start-menu'),Win64='yes')
elem(comp,'Shortcut',Id='LunolaStartMenuShortcut',Name='Lunola Forma 5.4',Description='Lunola Forma by Pujo Setyo',Target='[LUNOLA_INSTALLFOLDER]blender-launcher.exe',WorkingDirectory='LUNOLA_INSTALLFOLDER',Icon='LunolaProductIcon',IconIndex='0')
elem(comp,'RemoveFolder',Id='LunolaRemoveMenu',On='uninstall')
elem(comp,'RegistryValue',Id='LunolaShortcutKey',Root='HKCU',Key='Software\\Lunola\\Forma\\Installer\\5.4',Name='StartMenuShortcut',Type='integer',Value='1',KeyPath='yes');elem(feature,'ComponentRef',Id='LunolaShortcut')
wxs=A/'LunolaForma.wxs';ET.indent(root);ET.ElementTree(root).write(wxs,encoding='utf-8',xml_declaration=True)
(A/'payload-manifest.json').write_text(json.dumps({'file_map':mapping,'upgrade_code':upgrade,'product_code':product_code,'runtime_file_count':len(pinfo['runtime_sha256']),'runtime_sha256':pinfo['runtime_sha256'],'binary_commit':pinfo['binary_commit'],'installer':str(out/(name+'.msi'))},indent=2))
tools=Path('D:/DevTools/WiX/3.14.1/bin');obj=A/'LunolaForma.wixobj'
for label,command in [('candle',[str(tools/'candle.exe'),'-nologo','-arch','x64','-out',str(obj),str(wxs)]),('light',[str(tools/'light.exe'),'-nologo','-out',str(out/(name+'.msi')),str(obj)])]:
 print('BUILD '+label,flush=True)
 with (A/(label+'.log')).open('w') as log:result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,cwd=A)
 assert result.returncode==0,(A/(label+'.log')).read_text(errors='replace')
print('MSI BUILT; installer has not been executed: '+str(out/(name+'.msi')),flush=True)
