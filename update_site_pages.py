"""Update website pages to emphasize browser play with real gameplay screenshots and state Android apps coming soon without download buttons."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent

# --- 1. ARROW UNLEASHED ---
p_arrow = ROOT / 'apps/arrow-unleashed/index.html'
if p_arrow.exists():
    c = p_arrow.read_text(encoding='utf-8')
    c = c.replace('<a href="/apps/">Android apps</a>', '<a href="/apps/">Apps</a>')
    c = re.sub(r'<p class="eyebrow">Arrow unleashed · [^<]*</p>', '<p class="eyebrow">Arrow unleashed · Play in Browser · Android Coming Soon</p>', c)
    c = c.replace('Play offline on Android.', 'Play instantly in your browser.')
    c = c.replace('An offline arrow puzzle game without ads: what to check', 'An offline arrow puzzle game: play in browser, Android coming soon')
    
    # Replace hero actions
    old_actions = re.search(r'<div class="hero-actions">.*?</div>\s*<p class="micro">.*?</p>', c, re.S)
    new_actions = (
        '<div class="hero-actions">'
        '<a class="button" href="https://arrow-unleashed.wonderworldlabs.com/">Play Arrow unleashed in your browser ↗</a>'
        '<span class="badge-coming-soon">Android app coming soon</span>'
        '<a class="text-link" href="#how-it-works">Explore the features ↓</a>'
        '</div>'
        '<p class="micro">Play free right in your browser on mobile or desktop without installing anything. Native Android app coming soon.</p>'
    )
    if old_actions:
        c = c.replace(old_actions.group(0), new_actions)
        
    # Replace hero art with mobile gameplay screenshot in a good stage of play
    old_art = re.search(r'<div class="art" style="--accent:#ffaf8f">.*?<p class="art-caption">.*?</p>', c, re.S)
    new_art = (
        '<div class="hero-screenshot-col">'
        '<a class="screenshot-showcase" href="https://arrow-unleashed.wonderworldlabs.com/" title="Click to play Arrow unleashed in your browser">'
        '<div class="phone-mockup">'
        '<img src="/assets/gameplay-arrow-unleashed.png" width="370" height="740" alt="Arrow unleashed mobile gameplay puzzle in a good stage of play" loading="eager">'
        '<span class="play-overlay-badge">▶ Play in Browser</span>'
        '</div>'
        '</a>'
        '<p class="art-caption">Arrow unleashed browser gameplay · Click to play now</p>'
        '</div>'
    )
    if old_art:
        c = c.replace(old_art.group(0), new_art)
        
    c = re.sub(
        r'Arrow unleashed is an Android arrow puzzle game for offline play, with daily challenges, hints and local milestones\.',
        'Arrow unleashed is an arrow puzzle game available to play free in your web browser, with 360 levels, daily challenges, hints and local milestones. The native Android app is coming soon.',
        c
    )
    c = c.replace('<span>Offline play</span><span>No ads</span><span>No account</span>', '<span>Browser play</span><span>360 Levels</span><span>No ads</span><span>Android coming soon</span>')
    
    # Download section
    old_dl = re.search(r'<section id="download" class="download">.*?</section>', c, re.S)
    new_dl = (
        '<section id="download" class="download">'
        '<div>'
        '<p class="eyebrow" style="color:inherit">Ready for your next puzzle?</p>'
        '<h2>Untangle your first arrow board.</h2>'
        '<p>Play Arrow unleashed directly in your browser today with 360 levels and daily challenges. Android app coming soon.</p>'
        '</div>'
        '<div>'
        '<a class="button" href="https://arrow-unleashed.wonderworldlabs.com/">Play Arrow unleashed in your browser ↗</a>'
        '<p class="micro">Android app coming soon · No installation required for web play</p>'
        '</div>'
        '</section>'
    )
    if old_dl:
        c = c.replace(old_dl.group(0), new_dl)
        
    p_arrow.write_text(c, encoding='utf-8')
    print('Updated arrow-unleashed.')

# --- 2. BLOCK BLASTING ---
p_blocks = ROOT / 'apps/block-blasting/index.html'
if p_blocks.exists():
    c = p_blocks.read_text(encoding='utf-8')
    c = c.replace('<a href="/apps/">Android apps</a>', '<a href="/apps/">Apps</a>')
    c = re.sub(r'<p class="eyebrow">Block Blasting · [^<]*</p>', '<p class="eyebrow">Block Blasting · Play in Browser · Android Coming Soon</p>', c)
    c = c.replace('Play offline block puzzles in Classic mode or explore 24 Adventure levels on Android.', 'Play block puzzles in Classic mode or explore 24 Adventure levels directly in your browser.')
    
    old_actions = re.search(r'<div class="hero-actions">.*?</div>\s*<p class="micro">.*?</p>', c, re.S)
    new_actions = (
        '<div class="hero-actions">'
        '<a class="button" href="https://block-blasting.wonderworldlabs.com/">Play Block Blasting in your browser ↗</a>'
        '<span class="badge-coming-soon">Android app coming soon</span>'
        '<a class="text-link" href="#how-it-works">Explore the features ↓</a>'
        '</div>'
        '<p class="micro">Play free right in your browser on mobile or desktop without installing anything. Native Android app coming soon.</p>'
    )
    if old_actions:
        c = c.replace(old_actions.group(0), new_actions)
        
    old_art = re.search(r'<div class="art" style="--accent:#f8cf79">.*?<p class="art-caption">.*?</p>', c, re.S)
    new_art = (
        '<div class="hero-screenshot-col">'
        '<a class="screenshot-showcase" href="https://block-blasting.wonderworldlabs.com/" title="Click to play Block Blasting in your browser">'
        '<div class="phone-mockup">'
        '<img src="/assets/gameplay-block-blasting.png" width="370" height="740" alt="Block Blasting mobile puzzle gameplay in action" loading="eager">'
        '<span class="play-overlay-badge">▶ Play in Browser</span>'
        '</div>'
        '</a>'
        '<p class="art-caption">Block Blasting browser gameplay · Click to play now</p>'
        '</div>'
    )
    if old_art:
        c = c.replace(old_art.group(0), new_art)
        
    c = re.sub(
        r'Block Blasting is an offline Android block puzzle game with Classic mode and 24 Adventure levels\.',
        'Block Blasting is a block puzzle game available to play free in your browser with Classic mode and 24 Adventure levels. Native Android app coming soon.',
        c
    )
    c = c.replace('<span>Classic + Adventure</span><span>No ads</span><span>Local progress</span>', '<span>Browser play</span><span>Classic + Adventure</span><span>No ads</span><span>Android coming soon</span>')
    
    old_dl = re.search(r'<section id="download" class="download">.*?</section>', c, re.S)
    new_dl = (
        '<section id="download" class="download">'
        '<div>'
        '<p class="eyebrow" style="color:inherit">Make your next move</p>'
        '<h2>A fresh board. Your next bright idea.</h2>'
        '<p>Play Block Blasting directly in your browser today with Classic mode and Adventure levels. Android app coming soon.</p>'
        '</div>'
        '<div>'
        '<a class="button" href="https://block-blasting.wonderworldlabs.com/">Play Block Blasting in your browser ↗</a>'
        '<p class="micro">Android app coming soon · No installation required for web play</p>'
        '</div>'
        '</section>'
    )
    if old_dl:
        c = c.replace(old_dl.group(0), new_dl)
        
    p_blocks.write_text(c, encoding='utf-8')
    print('Updated block-blasting.')

# --- 3. MELODY GARDEN ---
p_melody = ROOT / 'apps/melody-garden/index.html'
if p_melody.exists():
    c = p_melody.read_text(encoding='utf-8')
    c = c.replace('<a href="/apps/">Android apps</a>', '<a href="/apps/">Apps</a>')
    c = re.sub(r'<p class="eyebrow">Melody Garden · [^<]*</p>', '<p class="eyebrow">Melody Garden · Open in Browser · Android Coming Soon</p>', c)
    c = c.replace('Find an easy first step on Android.', 'Start learning right in your web browser.')
    
    old_actions = re.search(r'<div class="hero-actions">.*?</div>\s*<p class="micro">.*?</p>', c, re.S)
    new_actions = (
        '<div class="hero-actions">'
        '<a class="button" href="https://melody-garden.wonderworldlabs.com/">Open Melody Garden in your browser ↗</a>'
        '<span class="badge-coming-soon">Android app coming soon</span>'
        '<a class="text-link" href="#how-it-works">Explore the features ↓</a>'
        '</div>'
        '<p class="micro">Learn piano and guitar directly in your browser. Native Android app coming soon without any download required today.</p>'
    )
    if old_actions:
        c = c.replace(old_actions.group(0), new_actions)
        
    old_art = re.search(r'<div class="art" style="--accent:#c8bbfa">.*?<p class="art-caption">.*?</p>', c, re.S)
    new_art = (
        '<div class="hero-screenshot-col">'
        '<a class="screenshot-showcase" href="https://melody-garden.wonderworldlabs.com/" title="Click to open Melody Garden in your browser">'
        '<div class="phone-mockup">'
        '<img src="/assets/gameplay-melody-garden.png" width="370" height="740" alt="Melody Garden mobile practice in action" loading="eager">'
        '<span class="play-overlay-badge">▶ Practice in Browser</span>'
        '</div>'
        '</a>'
        '<p class="art-caption">Melody Garden browser edition · Click to open now</p>'
        '</div>'
    )
    if old_art:
        c = c.replace(old_art.group(0), new_art)
        
    c = c.replace('<span>Piano & guitar</span><span>Offline lessons</span><span>No ads</span>', '<span>Piano & guitar</span><span>Browser learning</span><span>No ads</span><span>Android coming soon</span>')
    
    old_dl = re.search(r'<section id="download" class="download">.*?</section>', c, re.S)
    new_dl = (
        '<section id="download" class="download">'
        '<div>'
        '<p class="eyebrow" style="color:inherit">Start playing today</p>'
        '<h2>Your musical journey begins here.</h2>'
        '<p>Open Melody Garden directly in your browser for on-screen piano and guitar practice. Android app coming soon.</p>'
        '</div>'
        '<div>'
        '<a class="button" href="https://melody-garden.wonderworldlabs.com/">Open Melody Garden in your browser ↗</a>'
        '<p class="micro">Android app coming soon · No installation required for web practice</p>'
        '</div>'
        '</section>'
    )
    if old_dl:
        c = c.replace(old_dl.group(0), new_dl)
        
    p_melody.write_text(c, encoding='utf-8')
    print('Updated melody-garden.')

# --- 4. WHISPERING DIARY ---
p_diary = ROOT / 'apps/whispering-diary/index.html'
if p_diary.exists():
    c = p_diary.read_text(encoding='utf-8')
    c = c.replace('<a href="/apps/">Android apps</a>', '<a href="/apps/">Apps</a>')
    c = re.sub(r'<p class="eyebrow">The Whispering Diary · [^<]*</p>', '<p class="eyebrow">The Whispering Diary · Open in Browser · Android Coming Soon</p>', c)
    c = c.replace('Fictional character conversations on Android.', 'Fictional character conversations right in your browser.')
    
    old_actions = re.search(r'<div class="hero-actions">.*?</div>\s*<p class="micro">.*?</p>', c, re.S)
    new_actions = (
        '<div class="hero-actions">'
        '<a class="button" href="https://whispering-diary.wonderworldlabs.com/">Open the diary in your browser ↗</a>'
        '<span class="badge-coming-soon">Android app coming soon</span>'
        '<a class="text-link" href="#how-it-works">Explore the features ↓</a>'
        '</div>'
        '<p class="micro">Open directly in your web browser. Adults 18+ only. Native Android app coming soon.</p>'
    )
    if old_actions:
        c = c.replace(old_actions.group(0), new_actions)
        
    old_art = re.search(r'<div class="art" style="--accent:#a9c5fa">.*?<p class="art-caption">.*?</p>', c, re.S)
    new_art = (
        '<div class="hero-screenshot-col">'
        '<a class="screenshot-showcase" href="https://whispering-diary.wonderworldlabs.com/" title="Click to open The Whispering Diary in your browser">'
        '<div class="phone-mockup">'
        '<img src="/assets/gameplay-whispering-diary.png" width="370" height="740" alt="The Whispering Diary character chat in action" loading="eager">'
        '<span class="play-overlay-badge">▶ Open in Browser</span>'
        '</div>'
        '</a>'
        '<p class="art-caption">The Whispering Diary browser edition · Click to open now</p>'
        '</div>'
    )
    if old_art:
        c = c.replace(old_art.group(0), new_art)
        
    c = c.replace('<span>Fictional AI</span><span>Local conversations</span><span>18+</span>', '<span>Fictional AI</span><span>Browser edition</span><span>18+</span><span>Android coming soon</span>')
    
    old_dl = re.search(r'<section id="download" class="download">.*?</section>', c, re.S)
    new_dl = (
        '<section id="download" class="download">'
        '<div>'
        '<p class="eyebrow" style="color:inherit">A quiet page is waiting</p>'
        '<h2>Share a thought. Hear a response.</h2>'
        '<p>Open The Whispering Diary directly in your browser. Fictional local AI conversations. Android app coming soon.</p>'
        '</div>'
        '<div>'
        '<a class="button" href="https://whispering-diary.wonderworldlabs.com/">Open the diary in your browser ↗</a>'
        '<p class="micro">Android app coming soon · Adults 18+ only</p>'
        '</div>'
        '</section>'
    )
    if old_dl:
        c = c.replace(old_dl.group(0), new_dl)
        
    p_diary.write_text(c, encoding='utf-8')
    print('Updated whispering-diary.')

# --- 5. EXPLAIN STUDIO ---
p_studio = ROOT / 'apps/explain-studio/index.html'
if p_studio.exists():
    c = p_studio.read_text(encoding='utf-8')
    c = c.replace('<a href="/apps/">Android apps</a>', '<a href="/apps/">Apps</a>')
    c = re.sub(r'<p class="eyebrow">Explain Studio · [^<]*</p>', '<p class="eyebrow">Explain Studio · Open in Browser · Android Coming Soon</p>', c)
    c = c.replace('Record clean camera video with a built-in teleprompter on Android.', 'Record clean video with an on-screen teleprompter directly in your browser.')
    
    old_actions = re.search(r'<div class="hero-actions">.*?</div>\s*<p class="micro">.*?</p>', c, re.S)
    new_actions = (
        '<div class="hero-actions">'
        '<a class="button" href="https://explain-studio.wonderworldlabs.com/">Open Explain Studio in your browser ↗</a>'
        '<span class="badge-coming-soon">Android app coming soon</span>'
        '<a class="text-link" href="#how-it-works">Explore the features ↓</a>'
        '</div>'
        '<p class="micro">Use the teleprompter and camera right in your browser. Native Android app coming soon.</p>'
    )
    if old_actions:
        c = c.replace(old_actions.group(0), new_actions)
        
    old_art = re.search(r'<div class="art" style="--accent:#b4ddd1">.*?<p class="art-caption">.*?</p>', c, re.S)
    new_art = (
        '<div class="hero-screenshot-col">'
        '<a class="screenshot-showcase" href="https://explain-studio.wonderworldlabs.com/" title="Click to open Explain Studio in your browser">'
        '<div class="phone-mockup">'
        '<img src="/assets/gameplay-explain-studio.png" width="370" height="740" alt="Explain Studio teleprompter in action" loading="eager">'
        '<span class="play-overlay-badge">▶ Open in Browser</span>'
        '</div>'
        '</a>'
        '<p class="art-caption">Explain Studio browser edition · Click to open now</p>'
        '</div>'
    )
    if old_art:
        c = c.replace(old_art.group(0), new_art)
        
    c = c.replace('<span>Camera + prompter</span><span>Offline recording</span><span>Local videos</span>', '<span>Camera + prompter</span><span>Browser studio</span><span>Android coming soon</span>')
    
    old_dl = re.search(r'<section id="download" class="download">.*?</section>', c, re.S)
    new_dl = (
        '<section id="download" class="download">'
        '<div>'
        '<p class="eyebrow" style="color:inherit">Ready to explain?</p>'
        '<h2>Share what you know with confidence.</h2>'
        '<p>Open Explain Studio directly in your browser today. Android app coming soon.</p>'
        '</div>'
        '<div>'
        '<a class="button" href="https://explain-studio.wonderworldlabs.com/">Open Explain Studio in your browser ↗</a>'
        '<p class="micro">Android app coming soon · No installation required for web use</p>'
        '</div>'
        '</section>'
    )
    if old_dl:
        c = c.replace(old_dl.group(0), new_dl)
        
    p_studio.write_text(c, encoding='utf-8')
    print('Updated explain-studio.')

# --- 6. PHOTO FILE VAULT ---
p_vault = ROOT / 'apps/photo-file-vault/index.html'
if p_vault.exists():
    c = p_vault.read_text(encoding='utf-8')
    c = c.replace('<a href="/apps/">Android apps</a>', '<a href="/apps/">Apps</a>')
    c = re.sub(r'<p class="eyebrow">Photo &amp; File Vault · [^<]*</p>', '<p class="eyebrow">Photo &amp; File Vault · Android App Coming Soon</p>', c)
    
    old_actions = re.search(r'<div class="hero-actions">.*?</div>\s*<p class="micro">.*?</p>', c, re.S)
    new_actions = (
        '<div class="hero-actions">'
        '<span class="badge-coming-soon">Android app coming soon</span>'
        '<a class="text-link" href="#how-it-works">Explore the features ↓</a>'
        '</div>'
        '<p class="micro">Native Android app coming soon. Encrypted offline storage for sensitive photos and documents.</p>'
    )
    if old_actions:
        c = c.replace(old_actions.group(0), new_actions)
        
    old_dl = re.search(r'<section id="download" class="download">.*?</section>', c, re.S)
    new_dl = (
        '<section id="download" class="download">'
        '<div>'
        '<p class="eyebrow" style="color:inherit">Keep your private memories safe</p>'
        '<h2>Photo &amp; File Vault</h2>'
        '<p>Encrypted on-device storage designed with privacy in mind.</p>'
        '</div>'
        '<div>'
        '<span class="badge-coming-soon" style="font-size:15px;padding:12px 24px">Android app coming soon</span>'
        '</div>'
        '</section>'
    )
    if old_dl:
        c = c.replace(old_dl.group(0), new_dl)
        
    p_vault.write_text(c, encoding='utf-8')
    print('Updated photo-file-vault.')

# --- 7. GAMES HUB / GAMES PAGE (games/index.html) ---
p_games = ROOT / 'games/index.html'
if p_games.exists():
    c = p_games.read_text(encoding='utf-8')
    # Update Arrow Unleashed and Block Blasting cards
    c = c.replace(
        '<div class="product-info"><h3>Arrow unleashed <span aria-hidden="true">↗</span></h3><p>Arrow puzzles · Android</p></div>',
        '<div class="product-info"><h3>Arrow unleashed <span aria-hidden="true">↗</span></h3><p>Arrow puzzles · Play in browser · Android coming soon</p></div>'
    )
    c = c.replace(
        '<div class="product-info"><h3>Block Blasting <span aria-hidden="true">↗</span></h3><p>Block puzzles · Android</p></div>',
        '<div class="product-info"><h3>Block Blasting <span aria-hidden="true">↗</span></h3><p>Block puzzles · Play in browser · Android coming soon</p></div>'
    )
    c = c.replace(
        'Arrow unleashed and Block Blasting are separate Android games; their browser editions remain planned.',
        'Arrow unleashed and Block Blasting are playable directly in your browser. Native Android versions are coming soon.'
    )
    p_games.write_text(c, encoding='utf-8')
    print('Updated games/index.html.')

# --- 8. APPS HUB (apps/index.html) ---
p_apps = ROOT / 'apps/index.html'
if p_apps.exists():
    c = p_apps.read_text(encoding='utf-8')
    c = c.replace('Android apps', 'Apps')
    p_apps.write_text(c, encoding='utf-8')
    print('Updated apps/index.html.')

# --- 9. HOME (index.html) ---
p_home = ROOT / 'index.html'
if p_home.exists():
    c = p_home.read_text(encoding='utf-8')
    c = c.replace('Android apps', 'Apps')
    p_home.write_text(c, encoding='utf-8')
    print('Updated index.html.')

print('All site pages updated successfully!')
