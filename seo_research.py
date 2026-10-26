"""Read-only SEO research. Private outputs live OUTSIDE the public Pages repo.

Usage: python seo_research.py --suggestions
       python seo_research.py --search-console
Search Console requires GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN in the environment
with webmasters.readonly scope and access to GSC_SITE_URL (defaults to domain).
"""
import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT.parent / 'seo-private'
IST = timezone(timedelta(hours=5, minutes=30))
SEEDS = {
    'melody-garden': ['offline piano learning app', 'learn guitar offline', 'piano app without microphone', 'piano guitar learning app android'],
    'arrow-unleashed': ['offline arrow puzzle game', 'arrow puzzle hints', 'daily arrow puzzle', 'arrow puzzle no ads'],
    'whispering-diary': ['offline ai chat android', 'offline ai character chat', 'private ai diary', 'local ai chat without internet'],
}

def request(url, body=None, token=None):
    headers = {'User-Agent': 'WonderworldLabs-SEO-Research/1.0'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    if body is not None:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

def save(name, value):
    folder = PRIVATE / datetime.now(IST).date().isoformat()
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')

def suggestions():
    result = {'source': 'Google public autocomplete (undocumented endpoint; may be unavailable)',
              'market': 'IN', 'language': 'en', 'observed_at': datetime.now(IST).isoformat(),
              'limitation': 'Suggestions are candidate phrases, not search volumes, organic rankings, or site impressions.', 'apps': {}}
    for app, seeds in SEEDS.items():
        rows = []
        for seed in seeds:
            try:
                data = request('https://suggestqueries.google.com/complete/search?' + urllib.parse.urlencode({'client':'firefox','hl':'en','gl':'in','q':seed}))
                rows.append({'seed':seed, 'suggestions':data[1]})
            except (urllib.error.URLError, ValueError, TimeoutError) as error:
                rows.append({'seed':seed, 'status':'unavailable', 'error_type':type(error).__name__})
        result['apps'][app] = rows
    save('keyword-suggestions.json', result)
    for app, rows in result['apps'].items():
        phrases = sorted({p for row in rows for p in row.get('suggestions', [])})
        print(app + ': ' + json.dumps(phrases, ensure_ascii=False))

def fetch_period(token, site, start, end):
    url = 'https://www.googleapis.com/webmasters/v3/sites/' + urllib.parse.quote(site, safe='') + '/searchAnalytics/query'
    rows = []
    for offset in range(0, 100000, 25000):
        response = request(url, {'startDate':str(start), 'endDate':str(end), 'dimensions':['query','page','country','device'], 'type':'web', 'dataState':'final', 'rowLimit':25000, 'startRow':offset}, token)
        batch = response.get('rows', [])
        rows.extend(batch)
        if len(batch) < 25000:
            break
    return {'start':str(start), 'end':str(end), 'dimensions':['query','page','country','device'], 'rows':rows,
            'limitation':'Search Console omits anonymized queries and may return only top rows. Results are not all searches. Pagination safety cap: 100000 rows.'}

def compare(before, after):
    old = {tuple(r['keys']):r for r in before['rows']}
    result = []
    for row in after['rows']:
        prior = old.get(tuple(row['keys']))
        result.append({'keys':row['keys'], 'clicks':row['clicks'], 'impressions':row['impressions'], 'ctr':row['ctr'], 'position':row['position'],
                       'prior':prior, 'position_improvement':prior['position']-row['position'] if prior else None,
                       'click_delta':row['clicks']-prior['clicks'] if prior else None,
                       'opportunity':row['impressions'] >= 10 and row['clicks'] == 0 and row['position'] > 10})
    return sorted(result, key=lambda x:(not x['opportunity'], -x['impressions']))

def search_console():
    token = os.environ.get('GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN')
    if not token:
        save('search-console-status.json', {'status':'unavailable','reason':'No authorized Search Console access token configured','metrics':None})
        print('Search Console unavailable: account authorization needed. No rankings or clicks inferred.')
        return
    site = os.environ.get('GSC_SITE_URL', 'sc-domain:wonderworldlabs.com')
    # Use final data and a three-day reporting buffer. GSC dates use Pacific Time.
    end = datetime.now(timezone.utc).date() - timedelta(days=3)
    for days in [7,28]:
        current = fetch_period(token, site, end-timedelta(days=days-1), end)
        previous = fetch_period(token, site, end-timedelta(days=2*days-1), end-timedelta(days=days))
        save(f'gsc-{days}d.json', {'site':site,'current':current,'previous':previous,'comparison':compare(previous,current),
                               'interpretation':'Association only. Low position does not establish why clicks were absent. Missing rows are not zero.'})
        print(f'Saved {days}-day comparison privately: {len(current["rows"])} current rows; {len(previous["rows"])} previous rows.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--suggestions', action='store_true')
    parser.add_argument('--search-console', action='store_true')
    args = parser.parse_args()
    if args.suggestions:
        suggestions()
    if args.search_console:
        try:
            search_console()
        except urllib.error.HTTPError as error:
            save('search-console-status.json', {'status':'unavailable','http_status':error.code,'metrics':None})
            raise SystemExit(f'Search Console returned HTTP {error.code}; no credentials or response body logged.')
