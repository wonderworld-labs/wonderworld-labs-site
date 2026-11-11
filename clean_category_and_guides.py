import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# 1. Update content/guides.json
guides_path = ROOT / 'content/guides.json'
raw_text = guides_path.read_text(encoding='utf-8')

raw_text = raw_text.replace(
    "Downloading and installing an app through Google Play still needs a connection; offline gameplay refers",
    "Downloading and installing an Android app in the future still needs a connection; offline gameplay refers"
)
raw_text = raw_text.replace(
    "This is separate from whether Google Play currently makes the app available to your account",
    "This is separate from Android app availability; you can also play directly in your web browser"
)
raw_text = raw_text.replace(
    "unleashed app page linked below to check current Google Play access or contact Wonderworld Labs.",
    "unleashed app page linked below to play in your browser or contact Wonderworld Labs."
)

guides_path.write_text(raw_text, encoding='utf-8')
print("Updated content/guides.json")

# 2. Update category pages
# Puzzle Games
puz_path = ROOT / 'categories/puzzle-games/index.html'
puz_html = puz_path.read_text(encoding='utf-8')
puz_html = puz_html.replace(
    "Check the current Google Play access on the app page before planning to download. Availability may depend on release or testing access; this page is not a playable browser game.",
    "Arrow unleashed is available to play directly in your browser with 360 levels and daily challenges. Android app release is coming soon."
)
puz_html = puz_html.replace(
    '<a href="/apps/arrow-unleashed/#download">See download access ↗</a>',
    '<a href="/apps/arrow-unleashed/#download">Play in browser / Android release ↗</a>'
)
puz_html = puz_html.replace(
    'current download options and release details.',
    'browser play and upcoming Android release details.'
)
puz_path.write_text(puz_html, encoding='utf-8')
print("Updated categories/puzzle-games/index.html")

# Music Learning
mus_path = ROOT / 'categories/music-learning/index.html'
mus_html = mus_path.read_text(encoding='utf-8')
mus_html = mus_html.replace(
    "The planned Melody Garden web version is not currently a playable online keyboard on this site. Public Android download access may depend on release or testing availability.",
    "Melody Garden is available to open directly in your web browser for interactive piano and guitar lessons, with Android app release coming soon."
)
mus_html = mus_html.replace(
    '<a href="/apps/melody-garden/#download">See current Android download access ↗</a>',
    '<a href="/apps/melody-garden/#download">Open in browser / Android release ↗</a>'
)
mus_html = mus_html.replace(
    'current download options on the app page.',
    'browser practice and upcoming Android release details.'
)
mus_path.write_text(mus_html, encoding='utf-8')
print("Updated categories/music-learning/index.html")

# AI Character Conversations
ai_path = ROOT / 'categories/ai-character-conversations/index.html'
ai_html = ai_path.read_text(encoding='utf-8')
ai_html = ai_html.replace(
    "Public download access may depend on release or testing availability.",
    "The Whispering Diary is available to experience in your web browser, with Android app release coming soon."
)
ai_html = ai_html.replace(
    '<a href="/apps/whispering-diary/#download">See download access ↗</a>',
    '<a href="/apps/whispering-diary/#download">Open in browser / Android release ↗</a>'
)
ai_html = ai_html.replace(
    'Check the app page for verified features and current download access.',
    'Check the app page for verified features, browser experience, and Android release details.'
)
ai_path.write_text(ai_html, encoding='utf-8')
print("Updated categories/ai-character-conversations/index.html")
