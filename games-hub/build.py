"""Assemble deployable arcade assets without publishing game sources to the hub repository."""
from pathlib import Path
import shutil,argparse
root=Path(__file__).parent
parser=argparse.ArgumentParser();parser.add_argument('--source-root',type=Path,default=root.parents[1]);args=parser.parse_args()
workspace=args.source_root;out=root/'dist';front=root/'public' if (root/'public').exists() else root
for name in ['index.html','style.css','app.js','icon.svg','_headers','privacy.html','robots.txt','sitemap.xml','art']:
 source=front/name;dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True)
 if source.is_dir():shutil.copytree(source,dest,dirs_exist_ok=True)
 else:shutil.copy2(source,dest)
for slug in ['arrow-unleashed','block-blasting','ladderday','hinthunt','linkloom','scale-safari']:
 source=workspace/'android-web-projects'/slug/'public' if slug in ['arrow-unleashed','block-blasting'] else workspace/'game-projects'/slug
 if not source.is_dir():raise SystemExit(f'Missing game source: {source}')
 for f in source.rglob('*'):
  rel=f.relative_to(source)
  if not f.is_file() or any(part.startswith('.') for part in rel.parts) or f.name in ['_headers','README.md','wrangler.jsonc','extra-mysteries.txt','robots.txt','sitemap.xml']:continue
  dest=out/'play'/slug/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
print('Assembled portal and six game runtimes in dist/.')

