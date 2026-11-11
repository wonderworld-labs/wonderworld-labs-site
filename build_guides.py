"""Render reviewed guide content and refresh discovery links; no network calls."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parent
BASE = 'https://wonderworldlabs.com'
guides = json.loads((ROOT/'content/guides.json').read_text(encoding='utf-8'))
esc = html.escape

APP_GAMES = {
    'arrow-unleashed': {
        'url': 'https://arrow-unleashed.wonderworldlabs.com/',
        'play_text': 'Play Arrow unleashed in your browser ↗',
        'heading': 'Play Arrow unleashed in your browser',
        'lead': 'Untangle colorful arrow puzzles with 360 levels, daily challenges, and local milestones directly in your browser. Android app coming soon.',
        'screenshot': '/assets/gameplay-arrow-unleashed.png',
        'alt': 'Arrow unleashed mobile gameplay puzzle in a good stage of play',
    },
    'block-blasting': {
        'url': 'https://block-blasting.wonderworldlabs.com/',
        'play_text': 'Play Block Blasting in your browser ↗',
        'heading': 'Play Block Blasting in your browser',
        'lead': 'Enjoy Classic block puzzles and 24 Adventure levels instantly in your browser. Android app coming soon.',
        'screenshot': '/assets/gameplay-block-blasting.png',
        'alt': 'Block Blasting mobile puzzle gameplay in progress',
    },
    'melody-garden': {
        'url': 'https://melody-garden.wonderworldlabs.com/',
        'play_text': 'Open Melody Garden in your browser ↗',
        'heading': 'Practice piano & guitar in your browser',
        'lead': 'Learn piano and guitar with interactive on-screen lessons and pitch practice right in your browser. Android app coming soon.',
        'screenshot': '/assets/gameplay-melody-garden.png',
        'alt': 'Melody Garden mobile practice in action',
    },
    'whispering-diary': {
        'url': 'https://whispering-diary.wonderworldlabs.com/',
        'play_text': 'Open The Whispering Diary in your browser ↗',
        'heading': 'Experience The Whispering Diary in your browser',
        'lead': 'Private, on-device fictional AI character conversations. Android app coming soon.',
        'screenshot': '/assets/gameplay-whispering-diary.png',
        'alt': 'The Whispering Diary character chat in progress',
    },
    'explain-studio': {
        'url': 'https://explain-studio.wonderworldlabs.com/',
        'play_text': 'Open Explain Studio in your browser ↗',
        'heading': 'Try Explain Studio in your browser',
        'lead': 'Teleprompter and camera video recording right in your web browser. Android app coming soon.',
        'screenshot': '/assets/gameplay-explain-studio.png',
        'alt': 'Explain Studio teleprompter in action',
    },
    'photo-file-vault': {
        'url': '/apps/photo-file-vault/',
        'play_text': 'Explore Photo & File Vault ↗',
        'heading': 'Photo & File Vault',
        'lead': 'Encrypted on-device storage for photos and sensitive files. Android app coming soon.',
        'screenshot': '/assets/wonderworld-icon-512.png',
        'alt': 'Photo and File Vault',
    }
}

def page(path, title, description, body, graph):
    template = (ROOT/'templates/guide-shell.tpl').read_text(encoding='utf-8')
    template = re.sub(r'<title>.*?</title>', '<title>'+esc(title)+' | Wonderworld Labs</title>', template)
    template = re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*', lambda m:m[1]+esc(description,quote=True), template)
    template = re.sub(r'(<meta (?:name|property)="(?:og:title|twitter:title)" content=")[^"]*', lambda m:m[1]+esc(title,quote=True), template)
    template = template.replace(BASE+'/apps/"', BASE+path+'"')
    # Keep article and collection-page entity metadata in generated HTML.
    webpage = {'@type':'WebPage','@id':BASE+path+'#webpage','url':BASE+path,'name':title+' | Wonderworld Labs','description':description,'isPartOf':{'@id':BASE+'/#website'},'publisher':{'@id':BASE+'/#organization'}}
    if path.startswith('/guides/') and path != '/guides/':
        webpage['mainEntity'] = {'@id':BASE+path+'#article'}
        template = template.replace('property="og:type" content="website"','property="og:type" content="article"')
    graph.append(webpage)
    if path == '/guides/':
        graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},{'@type':'ListItem','position':2,'name':'Guides','item':BASE+'/guides/'}]})
    template = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)+'</script>', template)
    template = re.sub(r'<main class="wrap" id="content">.*?</main>', '<main class="wrap" id="content">'+body+'</main>', template)
    target=ROOT/path.strip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(template,encoding='utf-8')

def guide_link(g):
    return '<li><a href="/guides/'+g['slug']+'/">'+esc(g['title'])+'</a></li>'

seen=set()
for g in guides:
    assert re.fullmatch(r'[a-z0-9-]+',g['slug']) and g['slug'] not in seen
    seen.add(g['slug'])
    path='/guides/'+g['slug']+'/'
    game = APP_GAMES.get(g['app'], APP_GAMES['arrow-unleashed'])
    body=f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/apps/{g["app"]}/">{esc(g["name"])}</a> / <a href="/guides/">Guides</a></nav><article><div class="hero"><p class="eyebrow">{esc(g["name"])} guide · Play in browser · Android coming soon</p><h1>{esc(g["title"])}</h1><p class="meta">By Wonderworld Labs · Published <time datetime="{g["date"]}">{g["date"]}</time></p><p class="lead">{esc(g["answer"])}</p></div>'
    body+='<nav aria-label="On this page"><ul>'+''.join(f'<li><a href="#section-{i}">{esc(s["heading"])}</a></li>' for i,s in enumerate(g['sections']))+'</ul></nav>'
    for i,s in enumerate(g['sections']):
        body+=f'<section class="faq" id="section-{i}"><h2>{esc(s["heading"])}</h2>'
        if s.get('steps'):
            body+='<ol>'+''.join('<li>'+esc(v)+'</li>' for v in s['steps'])+'</ol>'
        body+=''.join('<p>'+esc(p)+'</p>' for p in s.get('paragraphs',[]))+'</section>'

    # Highlight Play in Browser with gameplay screenshot in a good stage of play!
    body+=f'<section class="guide-play-cta" id="play-in-browser"><div class="guide-play-content"><p class="eyebrow">Play in your browser</p><h2>{esc(game["heading"])}</h2><p>{esc(game["lead"])}</p><div class="guide-play-actions"><a class="button" href="{esc(game["url"],quote=True)}">{esc(game["play_text"])}</a><span class="badge-coming-soon">Android app coming soon</span></div></div><div class="guide-play-media"><a href="{esc(game["url"],quote=True)}" class="guide-gameplay-link" title="Click to play {esc(g["name"])} in your browser"><img src="{esc(game["screenshot"],quote=True)}" alt="{esc(game["alt"],quote=True)}" width="250" height="500" loading="lazy"><span class="play-overlay-badge">▶ Play in Browser</span></a><p class="media-caption">Browser gameplay · Click to play now</p></div></section>'

    body+='<section class="faq"><h2>Questions and answers</h2>'+''.join('<h3>'+esc(q)+'</h3><p>'+esc(a)+'</p>' for q,a in g['faq'])+'</section>'
    if g.get('sources'):
        body+='<section class="faq"><h2>Further reading</h2><ul>'+''.join('<li><a href="'+esc(s['url'],quote=True)+'">'+esc(s['title'])+'</a></li>' for s in g['sources'])+'</ul></section>'
    related=[item for item in guides if item['app']==g['app'] and item['slug']!=g['slug']][:3]
    if related:
        body+='<section class="faq"><h2>Related guides</h2><ul>'+''.join(guide_link(item) for item in related)+'</ul></section>'
    body+=f'<section class="notice"><h2>Explore {esc(g["name"])}</h2><p>Play free directly in your web browser with no download or setup required. Native Android app is coming soon.</p><div style="display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin:18px 0"><a class="button" href="{esc(game["url"],quote=True)}">{esc(game["play_text"])}</a><span class="badge-coming-soon">Android app coming soon</span></div><p><a href="/apps/{g["app"]}/#download">Explore {esc(g["name"])} app details &amp; coming soon info ↗</a></p><p>App details in this guide are based on the <a href="/privacy/{g["app"]}/">current {esc(g["name"])} privacy policy</a> and web release. Suggested routines and checks are editorial guidance.</p></section></article>'
    graph=[{'@type':'Article','@id':BASE+path+'#article','headline':g['title'],'description':g['description'],'datePublished':g['date'],'dateModified':g.get('updated',g['date']),'mainEntityOfPage':BASE+path,'author':{'@type':'Organization','name':'Wonderworld Labs','url':BASE+'/'},'publisher':{'@type':'Organization','name':'Wonderworld Labs','url':BASE+'/'},'about':{'@type':'SoftwareApplication','name':g['name'],'url':BASE+'/apps/'+g['app']+'/','operatingSystem':'Web browser, Android'}}, {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Guides','item':BASE+'/guides/'},{'@type':'ListItem','position':2,'name':g['title'],'item':BASE+path}]}]
    page(path,g['title'],g['description'],body,graph)

# Keep every guide discoverable from its parent app without copying article bodies.
for app in sorted({g['app'] for g in guides}):
    group=[g for g in guides if g['app']==app]
    target=ROOT/'apps'/app/'index.html'
    if not target.exists():
        continue
    content=target.read_text(encoding='utf-8')
    resources='<section class="app-resources" id="guides"><div><p class="eyebrow">Explore &amp; learn</p><h2>More from '+esc(group[0]['name'])+'.</h2><p>Practical answers, setup help, and ideas for your next session.</p></div><ul>'+''.join(guide_link(g) for g in group)+'</ul></section>'
    block='<!-- app-guides:start -->'+resources+'<!-- app-guides:end -->'
    if '<!-- app-guides:start -->' in content:
        content=re.sub(r'<!-- app-guides:start -->.*?<!-- app-guides:end -->',lambda m:block,content,flags=re.S)
    else:
        content=content.replace('<section id="download"',block+'<section id="download"')
    target.write_text(content,encoding='utf-8')

body='<div class="hero"><p class="eyebrow">Practical help</p><h1>App &amp; game guides</h1><p class="lead">Step-by-step guides for browser games, music practice, puzzles, local AI chats, and teleprompter recording. Play instantly in your browser — Android apps coming soon.</p></div>'
for app in sorted({g['app'] for g in guides}):
    group=[g for g in guides if g['app']==app]
    body+='<section><h2>'+esc(group[0]['name'])+'</h2><ul>'+''.join(guide_link(g) for g in group)+'</ul></section>'
page('/guides/','App & Game Guides','Practical guides for browser games, offline music learning, puzzle games, encrypted photo storage, fictional AI chat and video recording with a teleprompter.',body,[{'@type':'CollectionPage','name':'App and game guides','url':BASE+'/guides/'}])
print(f'Rendered {len(guides)} guides and refreshed guide index.')
