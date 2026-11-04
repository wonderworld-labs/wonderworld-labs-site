"""Offline checks for SEO and answer-engine metadata on the static website."""
from pathlib import Path
from html.parser import HTMLParser
import json, re, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
BASE='https://wonderworldlabs.com'
APPS={'melody-garden','arrow-unleashed','whispering-diary','photo-file-vault','block-blasting','explain-studio'}
class Meta(HTMLParser):
 def __init__(self):
  super().__init__();self.h1=0;self.canonical=[];self.desc=[];self.robots=[];self.image=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
  if tag=='meta' and a.get('name')=='description':self.desc.append(a.get('content'))
  if tag=='meta' and a.get('name')=='robots':self.robots.append(a.get('content'))
  if tag=='meta' and a.get('property')=='og:image':self.image.append(a.get('content'))
urls=set();total=0
for p in ROOT.rglob('*.html'):
 s=p.read_text(encoding='utf8');a=Meta();a.feed(s);total+=1
 assert a.h1==1,(p,'h1');assert len(a.canonical)==1,(p,'canonical');assert len(a.desc)==1,(p,'description')
 assert len(a.robots)==1 and 'index' in a.robots[0],(p,'robots')
 assert len(a.image)==1,(p,'og:image')
 graph=[]
 for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>',s):
  d=json.loads(m.group(1));assert d.get('@context')=='https://schema.org';graph+=d.get('@graph',[d])
 assert any(g.get('@type')=='WebPage' for g in graph),(p,'webpage schema')
 if p.parent.parent.name=='apps' and p.parent.name in APPS:
  assert 'id="app-overview"' in s,(p,'answer summary')
  assert any(g.get('@type')=='SoftwareApplication' and g.get('applicationCategory') for g in graph),(p,'app schema')
  assert any(g.get('@type')=='BreadcrumbList' for g in graph),(p,'breadcrumbs')
 urls.add(a.canonical[0])
# Guide discovery coverage: every published article must be linked from the guide hub
# and its parent app, and supply visible, matching Article metadata.
guide_index=(ROOT/'guides/index.html').read_text(encoding='utf8')
guides=json.loads((ROOT/'content/guides.json').read_text(encoding='utf8'))
for g in guides:
 path='/guides/'+g['slug']+'/'
 assert 'href="'+path+'"' in guide_index,(g['slug'],'not on guide hub')
 app_html=(ROOT/'apps'/g['app']/'index.html').read_text(encoding='utf8')
 assert 'href="'+path+'"' in app_html,(g['slug'],'not linked from app')
 article_html=(ROOT/'guides'/g['slug']/'index.html').read_text(encoding='utf8')
 assert '<h1>'+g['title'].replace('&','&amp;')+'</h1>' in article_html,(g['slug'],'h1 mismatch')
 assert '\"@type\":\"Article\"' in article_html or '\"@type\": \"Article\"' in article_html,(g['slug'],'Article schema missing')
for app in APPS:
 assert 'id="guides"' in (ROOT/'apps'/app/'index.html').read_text(encoding='utf8'),(app,'guide section missing')
listed={e.text for e in ET.parse(ROOT/'sitemap.xml').findall('{*}url/{*}loc')}
assert listed==urls,('sitemap coverage',listed-urls,urls-listed)
assert 'Sitemap: '+BASE+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
print(f'PASS: {total} HTML pages, {len(urls)} canonical URLs; SEO metadata, schema, sitemap and app summaries.')
