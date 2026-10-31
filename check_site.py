"""Check internal links, metadata, structured data, and preserved policy copy."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BASE = 'https://wonderworldlabs.com'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links, self.ids, self.canonical = [], set(), []
        self.h1 = self.description = 0
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.add(a['id'])
        if tag == 'a' and 'href' in a:
            self.links.append(a['href'])
        if tag == 'link' and a.get('rel') == 'canonical':
            self.canonical.append(a['href'])
        if tag == 'h1':
            self.h1 += 1
        if tag == 'meta' and a.get('name') == 'description':
            self.description += 1

pages = {}
for p in ROOT.rglob('*.html'):
    text = p.read_text(encoding='utf-8')
    page = pages[p] = Page(text)
    assert page.h1 == 1, p
    assert len(page.canonical) == 1, p
    if p.name != 'privacy-policy.html':
        assert page.description == 1, p
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
        assert json.loads(block)['@context'] == 'https://schema.org', p

for p, page in pages.items():
    for link in page.links:
        u = urlsplit(link)
        if u.scheme and not link.startswith(BASE + '/'):
            continue
        if u.netloc and u.netloc != 'wonderworldlabs.com':
            continue
        target = ROOT / u.path.lstrip('/') if u.path else p
        if target.is_dir():
            target /= 'index.html'
        assert target.exists(), (p, link)
        if u.fragment:
            assert u.fragment in pages[target].ids, (p, link)

urls = ET.parse(ROOT / 'sitemap.xml').findall('{*}url/{*}loc')
assert len(urls) == len({url.text for url in urls}), 'Duplicate sitemap URL'
assert {url.text for url in urls} == {page.canonical[0] for page in pages.values()}, 'Sitemap coverage differs from canonical pages'
for url in urls:
    target = ROOT / urlsplit(url.text).path.lstrip('/') / 'index.html'
    assert target in pages and pages[target].canonical == [url.text], url.text

for guide in json.loads((ROOT / 'content/guides.json').read_text(encoding='utf-8')):
    parent = pages[ROOT / 'apps' / guide['app'] / 'index.html']
    assert '/guides/' + guide['slug'] + '/' in parent.links, ('Guide missing from app home', guide['slug'])
    article = pages[ROOT / 'guides' / guide['slug'] / 'index.html']
    assert '/apps/' + guide['app'] + '/#download' in article.links, guide['slug']

for slug in ['melody-garden', 'arrow-unleashed', 'whispering-diary']:
    rel = f'privacy/{slug}/index.html'
    old = subprocess.check_output(['git', 'show', f'21b16ef:{rel}'], cwd=ROOT).decode()
    current = (ROOT / rel).read_text(encoding='utf-8')
    # All existing policy paragraphs remain verbatim; only navigation is appended.
    for paragraph in re.findall(r'<p\b[^>]*>.*?</p>', old, re.S):
        assert paragraph in current, (slug, paragraph)
assert (ROOT / 'privacy-policy.html').read_bytes() == subprocess.check_output(
    ['git', 'show', '21b16ef:privacy-policy.html'], cwd=ROOT)
print(f'PASS: {len(pages)} pages; internal links and anchors; JSON-LD; {len(urls)} sitemap URLs; original privacy copy and legacy policy preserved.')
