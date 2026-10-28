"""Render reviewed guide content and refresh discovery links; no network calls."""
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BASE = 'https://wonderworldlabs.com'
guides = json.loads((ROOT/'content/guides.json').read_text(encoding='utf-8'))
esc = html.escape

def page(path, title, description, body, graph):
    template = (ROOT/'templates/guide-shell.tpl').read_text(encoding='utf-8')
    template = re.sub(r'<title>.*?</title>', '<title>'+esc(title)+' | Wonderworld Labs</title>', template)
    template = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m:m[1]+esc(description,quote=True), template)
    template = re.sub(r'(<meta (?:name|property)="(?:og:title|twitter:title)" content=")[^"]*', lambda m:m[1]+esc(title,quote=True), template)
    template = template.replace(BASE+'/apps/"', BASE+path+'"')
    template = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)+'</script>', template)
    template = re.sub(r'<main class="wrap">.*?</main>', '<main class="wrap">'+body+'</main>', template)
    target=ROOT/path.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(template,encoding='utf-8')

def guide_link(g):
    return '<li><a href="/guides/'+g['slug']+'/">'+esc(g['title'])+'</a></li>'

seen=set()
for g in guides:
    assert re.fullmatch(r'[a-z0-9-]+',g['slug']) and g['slug'] not in seen
    seen.add(g['slug'])
    path='/guides/'+g['slug']+'/'
    body=f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/apps/{g["app"]}/">{esc(g["name"])}</a> / <a href="/guides/">Guides</a></nav><article><div class="hero"><p class="eyebrow">{esc(g["name"])} guide · Android</p><h1>{esc(g["title"])}</h1><p class="meta">By Wonderworld Labs · Published <time datetime="{g["date"]}">{g["date"]}</time></p><p class="lead">{esc(g["answer"])}</p></div>'
    body+='<nav aria-label="On this page"><ul>'+''.join(f'<li><a href="#section-{i}">{esc(s["heading"])}</a></li>' for i,s in enumerate(g['sections']))+'</ul></nav>'
    for i,s in enumerate(g['sections']):
        body+=f'<section class="faq" id="section-{i}"><h2>{esc(s["heading"])}</h2>'
        if s.get('steps'):
            body+='<ol>'+''.join('<li>'+esc(v)+'</li>' for v in s['steps'])+'</ol>'
        body+=''.join('<p>'+esc(p)+'</p>' for p in s.get('paragraphs',[]))+'</section>'
    body+='<section class="faq"><h2>Questions and answers</h2>'+''.join('<h3>'+esc(q)+'</h3><p>'+esc(a)+'</p>' for q,a in g['faq'])+'</section>'
    if g.get('sources'):
        body+='<section class="faq"><h2>Further reading</h2><ul>'+''.join('<li><a href="'+esc(s['url'],quote=True)+'">'+esc(s['title'])+'</a></li>' for s in g['sources'])+'</ul></section>'
    body+=f'<section class="notice"><h2>Explore {esc(g["name"])}</h2><p>See the app features and current download access. Availability may depend on release or testing access.</p><a class="button" href="/apps/{g["app"]}/#download">{esc(g["name"])} download options</a><p>App details in this guide are based on the <a href="/privacy/{g["app"]}/">current {esc(g["name"])} privacy policy</a>. Suggested routines and checks are editorial guidance.</p></section></article>'
    graph=[{'@type':'Article','@id':BASE+path+'#article','headline':g['title'],'description':g['description'],'datePublished':g['date'],'dateModified':g.get('updated',g['date']),'mainEntityOfPage':BASE+path,'author':{'@type':'Organization','name':'Wonderworld Labs','url':BASE+'/'},'publisher':{'@type':'Organization','name':'Wonderworld Labs','url':BASE+'/'},'about':{'@type':'SoftwareApplication','name':g['name'],'url':BASE+'/apps/'+g['app']+'/','operatingSystem':'Android'}}, {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Guides','item':BASE+'/guides/'},{'@type':'ListItem','position':2,'name':g['title'],'item':BASE+path}]}]
    page(path,g['title'],g['description'],body,graph)

# Article lists belong in the blog hub, not the product landing pages.

body='<div class="hero"><p class="eyebrow">Practical help</p><h1>Android app guides</h1><p class="lead">Plan an offline music practice session, choose an arrow puzzle game, or understand local AI conversations.</p></div>'
for app in sorted({g['app'] for g in guides}):
    group=[g for g in guides if g['app']==app]
    body+='<section><h2>'+esc(group[0]['name'])+'</h2><ul>'+''.join(guide_link(g) for g in group)+'</ul></section>'
page('/guides/','Android App Guides','Practical guides to Melody Garden, Arrow unleashed, and The Whispering Diary: offline learning, puzzles, and AI character conversations.',body,[{'@type':'CollectionPage','name':'Android app guides','url':BASE+'/guides/'}])
namespace='http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('',namespace)
tree=ET.parse(ROOT/'sitemap.xml');urls={el.text for el in tree.findall('{*}url/{*}loc')}
for path in ['/guides/']+['/guides/'+g['slug']+'/' for g in guides]:
    if BASE+path not in urls:
        entry=ET.SubElement(tree.getroot(),'{'+namespace+'}url')
        ET.SubElement(entry,'{'+namespace+'}loc').text=BASE+path
tree.write(ROOT/'sitemap.xml',encoding='UTF-8',xml_declaration=True)
print(f'Rendered {len(guides)} guides and refreshed guide index and sitemap.')
