"""Build only the arcade shell. Games stay exclusively on their original subdomains."""
from pathlib import Path
import shutil
root=Path(__file__).parent;front=root/'public' if (root/'public').exists() else root;out=root/'dist'
for name in ['index.html','style.css','app.js','icon.svg','_headers','privacy.html','robots.txt','sitemap.xml','art']:
 source=front/name;dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True)
 if source.is_dir():shutil.copytree(source,dest,dirs_exist_ok=True)
 else:shutil.copy2(source,dest)
print('Built arcade shell only. No game code is copied.')

