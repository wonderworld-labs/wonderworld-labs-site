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
 # Keep the block board and piece tray together in the player's viewport.
 if slug=='block-blasting':
  index=out/'play'/slug/'index.html';index.write_text(index.read_text(encoding='utf-8').replace('href="style.css"','href="style.css?v=portal-7"'),encoding='utf-8')
  css=out/'play'/slug/'style.css'
  with css.open('a',encoding='utf-8') as f:f.write('''
body.arcade-embedded #app:has(>.board){display:grid;grid-template-columns:minmax(0,1fr) 160px;column-gap:22px;align-content:start}
body.arcade-embedded #app:has(>.board)>.row{grid-column:1/-1}
body.arcade-embedded #app:has(>.board)>.row h2{font-size:23px;margin:10px 0}
body.arcade-embedded #app:has(>.board)>.board{grid-column:1;grid-row:3/span 4;width:min(100%,calc(100dvh - 170px));max-width:420px;margin:0 auto}
body.arcade-embedded #app:has(>.board)>.tray{grid-column:2;grid-row:3;flex-direction:column;gap:8px;min-height:0;align-self:start}
body.arcade-embedded #app:has(>.board) .piece{width:100%;height:75px}
body.arcade-embedded #app:has(>.board) .mini span{width:18px;height:18px}
body.arcade-embedded #app:has(>.board)>p{grid-column:2;font-size:11px;margin:10px 0}
body.arcade-embedded #app:has(>.board)>button{grid-column:2;font-size:12px;padding:8px}
@media(max-width:600px){body.arcade-embedded #app:has(>.board){display:block}body.arcade-embedded #app:has(>.board)>.board{width:min(100%,max(185px,calc(100dvh - 285px)))}body.arcade-embedded #app:has(>.board)>.tray{flex-direction:row;margin-top:10px}body.arcade-embedded #app:has(>.board) .piece{width:30%;height:75px}body.arcade-embedded #app:has(>.board)>p{margin:6px 0}}
''')
print('Assembled portal and six game runtimes in dist/.')

