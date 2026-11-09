import shutil
from rcommon import CANDIDATES, utf8_stdout
from suites_loader import load_suite
utf8_stdout()
c=load_suite('C01_CPM_EFFECTIVE')
for name in CANDIDATES:
    root=c.build(name,{'backend/Directory.Packages.props':c.central(c.T,'<PackageVersion Include="A.B" Version="1.2.3" />'),c.PROJ:c.proj(c.REF)})
    code,out=c.check(name,root)
    print(name,'exit',code,'|',out.strip().replace('\n',' ')[-300:])
    shutil.rmtree(root,ignore_errors=True)
