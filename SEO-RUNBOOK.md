# Daily SEO and answer-focused publishing

Owner instruction: public search research for now; target one new useful guide per app per day at 05:00 Asia/Kolkata. Commit and push verified changes to the existing GitHub Pages site. Preserve policy URLs and text. Do not enable authenticated services until the owner completes setup and requests connection.

## Evidence and private history

Run `python seo_research.py --suggestions`. It uses Python's standard library to collect public Google autocomplete suggestions for English/India. This endpoint is unofficial and can change; on failure use ordinary public web research and record the source. Suggestions establish candidate wording, not search volume, rankings, or impressions. Raw results go to the sibling `../seo-private/YYYY-MM-DD/` directory, never the public Pages repository.

Review the previous private daily report and `content/guides.json` before choosing topics. Save sources, date, query, language, country, relevant findings, rejected phrases, and publication commit in the private report. Keep exports, credentials, account identifiers, and raw query analytics there or in a credential manager, not under this repository. Google Console access is currently unavailable; missing metrics must remain null/unavailable.

## Keyword selection

1. Refresh the seed set using supported app features and public query suggestions. Broaden gradually beyond the initial 12 seeds. Search relevant phrases and examine primary sources; record observations without pretending the search tool's ordering is a Google organic rank.
2. Group related wording by reader intent. Select one useful unanswered problem per app. Map one guide to that intent; synonyms belong on the same page. Exclude unrelated local classes, crossword books, mod APKs, unlimited-hint claims, unsupported free pricing, and unsupported medical or professional uses.
3. Target three original guides daily, one per app, but update an existing guide when the intent overlaps. Do not manufacture thin pages to hit the target. Record skipped targets and why. A rerun on the same IST date must not duplicate publication.
4. Each guide needs a concise answer, specific supported information, useful steps or distinctions, suitable FAQs, the app name and Android platform, source links, and a direct link to its app's `#download` section. No fabricated app screenshots, experience, tests, ratings, search demand, or guarantees of chatbot citations.

## Build and publish

Add reviewed content to `content/guides.json`, including the actual publication date. Only change `updated` for a substantive edit. Run `python build_guides.py` to generate the article and guide index, app links, and sitemap. The builder is repeatable; avoid manually editing generated guide HTML. Keep titles/descriptions unique and structured data aligned with visible content. The guide body must be useful without JavaScript. Article markup helps describe content but is not a promise of a special search result.

Run `python check_site.py`, `python -m py_compile build_guides.py seo_research.py`, and `git diff --check`. Inspect a representative rendered page when browser tools are available. Check Git status before staging: preserve other work. Fetch the remote and reconcile changes without overwriting someone else's edits. Commit only reviewed task files; push `origin main`. Wait for GitHub Pages success for that commit, verify the new guide URLs and edited app pages with HTTP 200 and expected content, and record results privately. Do not report a push alone as verified publication.

## Measurement: public-only phase

Use the same documented public search queries over time and record provider, date, market/language if controllable, result URLs, and whether a site URL was observed. A result absent from a search sample is not proof of deindexing or a rank below any particular number. Public autocomplete does not show who saw this site or clicked it. Web results cannot establish a Google position unless the provider explicitly supplies an organic position and matching query context. Record ranking, CTR, and click change as unavailable until a comparable source exists.

Track site availability and deployment as separate measurements. Recheck app download destinations: all three public Play listing URLs returned 404 during the previous update; do not claim production availability without checking again. No download click tracking has been installed.

## Measurement after the owner connects Search Console

Use a verified property and read-only OAuth. `python seo_research.py --search-console` accepts a short-lived `GOOGLE_SEARCH_CONSOLE_ACCESS_TOKEN` and optional `GSC_SITE_URL`; it never prints the token. This is a manual-token adapter, not a completed unattended OAuth connection. Configure refresh-token handling through an approved credential provider before calling it unattended.

The collector fetches final Web data with a three-day buffer and compares adjacent 7-day and 28-day windows by query, page, country, and device. Its candidate filter is at least 10 impressions, zero clicks, and average position greater than 10; this is a triage threshold, not evidence that low position caused the lack of clicks. Search Console's row limits and anonymized queries mean even paginated data is not all keywords. Validate coverage and data freshness before reporting.

Compare matching cohorts and like-for-like dimensions. For new pages, establish a baseline first. Separately evaluate the pre-update pages published in commit `fe5290247b3e7cea297d0d03a17de7c362f51ed2`, then each new publication cohort. Report impressions, clicks, CTR, average position, date windows, and sample sizes. Do not average CTR or positions across rows without appropriate weighting. A positive prior-position minus current-position delta indicates improvement for that matching row. Missing rows are not zeros. Describe changes after publication as association, not proof that the edit caused them.

Keyword Planner estimates are separate from site performance and advertising competition is not organic SEO difficulty. Chatbot citations are a separate, sampled observation: record the exact prompt, engine, date, and cited URL if observed; do not invent an AEO score or equate Google rank with chatbot visibility.

## Sources

- [Google's helpful-content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google AI features and websites](https://developers.google.com/search/docs/appearance/ai-features)
- [Search Analytics API limitations and dimensions](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [Gum Search Console support](https://gumcli.dev/services/searchconsole)
- [Gum installation platforms](https://gumcli.dev/install)

The user setup guide is stored outside the website at `../SEO-SETUP-GUIDE.md`.

## Current owner instructions (31 October 2026)

The owner authorized live read-only Google Search Console and Keyword Planner access on 27 October; this supersedes the earlier public-only statements above. Use the private refresh/collection workflow and never expose credentials. Read LANDING-PAGE-GUIDELINES.md before every content update. Keep the owner-selected Vaultaire reference structure in app pages, with verified app-specific facts, concise product sections, honest artwork and download availability. Long educational content belongs in /guides/; do not append guide lists to landing pages.

