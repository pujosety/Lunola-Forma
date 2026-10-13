# SPDX-License-Identifier: GPL-2.0-or-later
"""Archive an exact Git ref with hydrated, hash-verified LFS contents."""
import argparse,hashlib,json,re,subprocess,tarfile,zipfile
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--ref',required=True);p.add_argument('--lfs-objects',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 repo=a.repo.resolve();out=a.output.resolve();assert not out.exists() and not out.is_relative_to(repo),'Fresh output outside source required'
 ref=subprocess.check_output(['git','rev-parse',a.ref+'^{commit}'],cwd=repo,text=True).strip();prefix='Lunola-Forma-'+a.ref.replace('/','-')+'-Source/';out.parent.mkdir(parents=True,exist_ok=True)
 records=[];lfs_count=0;process=subprocess.Popen(['git','archive','--format=tar','--prefix='+prefix,ref],cwd=repo,stdout=subprocess.PIPE)
 try:
  with tarfile.open(fileobj=process.stdout,mode='r|') as tar,zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
   for member in tar:
    assert member.name.startswith(prefix) and '..' not in Path(member.name).parts
    if member.isdir():continue
    info=zipfile.ZipInfo(member.name);info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=((member.mode| (0o120000 if member.issym() else 0o100000))<<16);info.create_system=3
    if member.issym():data=member.linkname.encode();z.writestr(info,data);records.append({'path':member.name,'sha256':hashlib.sha256(data).hexdigest(),'kind':'symlink'});continue
    assert member.isfile(),member.name
    data=tar.extractfile(member).read();match=re.fullmatch(rb'version https://git-lfs.github.com/spec/v1\noid sha256:([a-f0-9]{64})\nsize (\d+)\n?',data)
    if match:
     oid=match[1].decode();expected_size=int(match[2]);source=a.lfs_objects/oid[:2]/oid[2:4]/oid;assert source.is_file() and source.stat().st_size==expected_size,member.name
     digest=hashlib.sha256()
     with source.open('rb') as f,z.open(info,'w',force_zip64=True) as dest:
      while block:=f.read(1024*1024):digest.update(block);dest.write(block)
     assert digest.hexdigest()==oid,member.name;lfs_count+=1;records.append({'path':member.name,'sha256':oid,'kind':'hydrated_lfs'})
    else:z.writestr(info,data);records.append({'path':member.name,'sha256':hashlib.sha256(data).hexdigest(),'kind':'git_blob'})
  assert process.wait()==0,'Git archive failed'
 except BaseException:
  process.stdout.close();process.wait();raise
 with zipfile.ZipFile(out) as z:
  assert len(z.namelist())==len(records) and len(set(z.namelist()))==len(records)
  for rec in records:
   digest=hashlib.sha256()
   with z.open(rec['path']) as f:
    while block:=f.read(1024*1024):digest.update(block)
   assert digest.hexdigest()==rec['sha256'],rec['path']
 with out.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
 links=subprocess.check_output(['git','ls-tree',ref,'lib/'],cwd=repo,text=True).splitlines();links=[s for s in links if s.startswith('160000')]
 result={'source_commit':ref,'archive':str(out),'bytes':out.stat().st_size,'sha256':sha,'verified_files':len(records),'hydrated_lfs_files':lfs_count,'dependency_gitlinks':links,'scope':'Complete tracked application source/assets; platform-library contents are separately pinned dependencies, not fabricated source'}
 out.with_suffix('.verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
