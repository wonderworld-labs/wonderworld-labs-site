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
        'badge': 'Android app coming soon'
    },
    'block-blasting': {
        'url': 'https://block-blasting.wonderworldlabs.com/',
        'play_text': 'Play Block Blasting in your browser ↗',
        'heading': 'Play Block Blasting in your browser',
        'lead': 'Enjoy Classic block puzzles and 24 Adventure levels instantly in your browser. Android app coming soon.',
        'screenshot': '/assets/gameplay-block-blasting.png',
        'alt': 'Block Blasting mobile puzzle gameplay in progress',
        'badge': 'Android app coming soon'
    },
    'ladderday': {
        'url': 'https://games.wonderworldlabs.com/ladderday/',
        'play_text': 'Play Ladderday in your browser ↗',
        'heading': 'Play Ladderday in your browser',
        'lead': 'A compact daily word challenge: change one letter at a time to find your way to GOLD. Free in your browser with no account needed.',
        'screenshot': '/assets/gameplay-ladderday.png',
        'alt': 'Ladderday daily word journey mobile gameplay in progress',
        'badge': 'Free browser game'
    },
    'scale-safari': {
        'url': 'https://games.wonderworldlabs.com/scale-safari/',
        'play_text': 'Play Scale Safari in your browser ↗',
        'heading': 'Play Scale Safari in your browser',
        'lead': 'Visual estimation & size puzzles: compare real-world objects and test your intuition directly in your browser.',
        'screenshot': '/assets/gameplay-scale-safari.png',
        'alt': 'Scale Safari visual estimation comparison gameplay',
        'badge': 'Free browser game'
    },
    'linkloom': {
        'url': 'https://games.wonderworldlabs.com/linkloom/',
        'play_text': 'Play Linkloom in your browser ↗',
        'heading': 'Play Linkloom in your browser',
        'lead': 'Pyramid word & number puzzles: discover six compound-word connections in your browser with daily starts.',
        'screenshot': '/assets/gameplay-linkloom.png',
        'alt': 'Linkloom phrase pyramid connections mobile gameplay',
        'badge': 'Free browser game'
    },
    'hinthunt': {
        'url': 'https://games.wonderworldlabs.com/hinthunt/',
        'play_text': 'Play HintHunt in your browser ↗',
        'heading': 'Play HintHunt in your browser',
        'lead': 'Semantic mystery-word game: use 10 darts to home in on the daily secret word with private on-device AI embeddings.',
        'screenshot': '/assets/gameplay-hinthunt.png',
        'alt': 'HintHunt semantic bullseye mystery word mobile gameplay',
        'badge': 'Free browser game'
    },
    'melody-garden': {
        'url': 'https://melody-garden.wonderworldlabs.com/',
        'play_text': 'Open Melody Garden in your browser ↗',
        'heading': 'Practice piano & guitar in your browser',
        'lead': 'Learn piano and guitar with interactive on-screen lessons and pitch practice right in your browser. Android app coming soon.',
        'screenshot': '/assets/gameplay-melody-garden.png',
        'alt': 'Melody Garden mobile practice in action',
        'badge': 'Android app coming soon'
    },
    'whispering-diary': {
        'url': 'https://whispering-diary.wonderworldlabs.com/',
        'play_text': 'Open The Whispering Diary in your browser ↗',
        'heading': 'Experience The Whispering Diary in your browser',
        'lead': 'Private, on-device fictional AI character conversations. Android app coming soon.',
        'screenshot': '/assets/gameplay-whispering-diary.png',
        'alt': 'The Whispering Diary character chat in progress',
        'badge': 'Android app coming soon'
    },
    'explain-studio': {
        'url': 'https://explain-studio.wonderworldlabs.com/',
        'play_text': 'Open Explain Studio in your browser ↗',
        'heading': 'Try Explain Studio in your browser',
        'lead': 'Teleprompter and camera video recording right in your web browser. Android app coming soon.',
        'screenshot': '/assets/gameplay-explain-studio.png',
        'alt': 'Explain Studio teleprompter in action',
        'badge': 'Android app coming soon'
    },
    'photo-file-vault': {
        'url': '/apps/photo-file-vault/',
        'play_text': 'Explore Photo & File Vault ↗',
        'heading': 'Photo & File Vault',
        'lead': 'Encrypted on-device storage for photos and sensitive files. Android app coming soon.',
        'screenshot': '/assets/wonderworld-icon-512.png',
        'alt': 'Photo and File Vault',
        'badge': 'Android app coming soon'
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
    badge = game.get('badge', 'Android app coming soon')
    is_game = (ROOT / 'games' / g['app']).exists()
    parent_path = f'/games/{g["app"]}/' if is_game else f'/apps/{g["app"]}/'
    play_anchor = f'/games/{g["app"]}/#play' if is_game else f'/apps/{g["app"]}/#download'

    # Top Region: Left half has blog heading, metadata & text; Right half has game screenshot mockup & direct play link!
    body = f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="{parent_path}">{esc(g["name"])}</a> / <a href="/guides/">Guides</a></nav><article>'
    body += f'<div class="guide-hero-split">'
    body += f'  <div class="guide-hero-left">'
    body += f'    <p class="eyebrow">{esc(g["name"])} guide · Play in browser</p>'
    body += f'    <h1>{esc(g["title"])}</h1>'
    body += f'    <p class="meta">By Wonderworld Labs · Published <time datetime="{g["date"]}">{g["date"]}</time></p>'
    body += f'    <p class="lead">{esc(g["answer"])}</p>'
    body += f'    <div class="guide-hero-actions">'
    body += f'      <a class="button" href="{esc(game["url"],quote=True)}">{esc(game["play_text"])}</a>'
    body += f'      <span class="badge-coming-soon">{esc(badge)}</span>'
    body += f'    </div>'
    body += f'  </div>'
    body += f'  <div class="guide-hero-right">'
    body += f'    <div class="screenshot-showcase">'
    body += f'      <a href="{esc(game["url"],quote=True)}" class="phone-mockup" title="Play {esc(g["name"])} in browser">'
    body += f'        <img src="{esc(game["screenshot"],quote=True)}" alt="{esc(game["alt"],quote=True)}" width="280" height="560">'
    body += f'        <span class="play-overlay-badge">▶ Play in Browser</span>'
    body += f'      </a>'
    body += f'      <span class="mockup-caption">Playable right now in your browser</span>'
    body += f'    </div>'
    body += f'  </div>'
    body += f'</div>'

    body += '<nav aria-label="On this page"><ul>'+''.join(f'<li><a href="#section-{i}">{esc(s["heading"])}</a></li>' for i,s in enumerate(g['sections']))+'</ul></nav>'
    for i,s in enumerate(g['sections']):
        body += f'<section class="faq" id="section-{i}"><h2>{esc(s["heading"])}</h2>'
        if s.get('steps'):
            body += '<ol>'+''.join('<li>'+esc(v)+'</li>' for v in s['steps'])+'</ol>'
        body += ''.join('<p>'+esc(p)+'</p>' for p in s.get('paragraphs',[]))+'</section>'

    body += '<section class="faq"><h2>Questions and answers</h2>'+''.join('<h3>'+esc(q)+'</h3><p>'+esc(a)+'</p>' for q,a in g['faq'])+'</section>'
    if g.get('sources'):
        body += '<section class="faq"><h2>Further reading</h2><ul>'+''.join('<li><a href="'+esc(s['url'],quote=True)+'">'+esc(s['title'])+'</a></li>' for s in g['sources'])+'</ul></section>'
    related = [item for item in guides if item['app']==g['app'] and item['slug']!=g['slug']][:3]
    if related:
        body += '<section class="faq"><h2>Related guides</h2><ul>'+''.join(guide_link(item) for item in related)+'</ul></section>'
    body += f'<section class="notice"><h2>Explore {esc(g["name"])}</h2><p>Play free directly in your web browser with no download or setup required.</p><div style="display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin:18px 0"><a class="button" href="{esc(game["url"],quote=True)}">{esc(game["play_text"])}</a><span class="badge-coming-soon">{esc(badge)}</span></div><p><a href="{play_anchor}">Explore {esc(g["name"])} details ↗</a></p><p>Game details in this guide are based on current web and mobile releases. Suggested strategies and routines are editorial guidance.</p></section></article>'
    parent_type = 'VideoGame' if is_game else 'SoftwareApplication'
    parent_url = BASE + parent_path
    graph = [{'@type':'Article','@id':BASE+path+'#article','headline':g['title'],'description':g['description'],'datePublished':g['date'],'dateModified':g.get('updated',g['date']),'mainEntityOfPage':BASE+path,'author':{'@type':'Organization','name':'Wonderworld Labs','url':BASE+'/'},'publisher':{'@type':'Organization','name':'Wonderworld Labs','url':BASE+'/'},'about':{'@type':parent_type,'name':g['name'],'url':parent_url,'operatingSystem':'Web browser, Android'}}, {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Guides','item':BASE+'/guides/'},{'@type':'ListItem','position':2,'name':g['title'],'item':BASE+path}]}]
    page(path,g['title'],g['description'],body,graph)

# Keep every guide discoverable from its parent app or game without copying article bodies.
for app in sorted({g['app'] for g in guides}):
    group=[g for g in guides if g['app']==app]
    is_game = (ROOT / 'games' / app).exists()
    target = (ROOT / 'games' / app / 'index.html') if is_game else (ROOT / 'apps' / app / 'index.html')
    if not target.exists():
        continue
    content = target.read_text(encoding='utf-8')
    resources = '<section class="app-resources" id="guides"><div><p class="eyebrow">Explore &amp; learn</p><h2>More from '+esc(group[0]['name'])+'.</h2><p>Practical answers, setup help, and ideas for your next session.</p></div><ul>'+''.join(guide_link(g) for g in group)+'</ul></section>'
    block = '<!-- app-guides:start -->' + resources + '<!-- app-guides:end -->'
    if '<!-- app-guides:start -->' in content:
        content = re.sub(r'<!-- app-guides:start -->.*?<!-- app-guides:end -->', lambda m:block, content, flags=re.S)
    else:
        if '<section id="download"' in content:
            content = content.replace('<section id="download"', block + '<section id="download"')
        elif '<section class="download"' in content:
            content = content.replace('<section class="download"', block + '<section class="download"')
    target.write_text(content, encoding='utf-8')

# Render guides hub index
body = '<div class="hero"><p class="eyebrow">Practical help</p><h1>App &amp; game guides</h1><p class="lead">Step-by-step guides for browser games, music practice, puzzles, local AI chats, and teleprompter recording. Play instantly in your browser — Android apps coming soon.</p></div>'
for app in sorted({g['app'] for g in guides}):
    group = [g for g in guides if g['app']==app]
    body += '<section><h2>'+esc(group[0]['name'])+'</h2><ul>'+''.join(guide_link(g) for g in group)+'</ul></section>'
page('/guides/','App & Game Guides','Practical guides for browser games, offline music learning, puzzle games, encrypted photo storage, fictional AI chat and video recording with a teleprompter.',body,[{'@type':'CollectionPage','name':'App and game guides','url':BASE+'/guides/'}])

# Update sitemap.xml to include all guides
sitemap_path = ROOT / 'sitemap.xml'
sitemap_text = sitemap_path.read_text(encoding='utf-8')
for g in guides:
    loc = f'<url><loc>https://wonderworldlabs.com/guides/{g["slug"]}/</loc></url>'
    loc_alt = f'<loc>https://wonderworldlabs.com/guides/{g["slug"]}/</loc>'
    if loc_alt not in sitemap_text:
        sitemap_text = sitemap_text.replace('</urlset>', f'{loc}\n</urlset>')

sitemap_path.write_text(sitemap_text, encoding='utf-8')

print(f'Rendered {len(guides)} guides and refreshed guide index and sitemap.')
