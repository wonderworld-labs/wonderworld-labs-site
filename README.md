# Wonderworld Labs website

A responsive static site for free GitHub Pages hosting. No build step or paid Squarespace website subscription is required. Existing domain registration/renewal is separate.

## Pages

### App discovery (October 2026)

- `/apps/`: app directory with category comparison and download access.
- `/apps/melody-garden/`, `/apps/arrow-unleashed/`, `/apps/whispering-diary/`: dedicated app pages with supported features, FAQs, and download access sections.
- `/categories/music-learning/`, `/categories/puzzle-games/`, `/categories/ai-character-conversations/`: category entry pages linking to the relevant app.
- `sitemap.xml` lists canonical pages; `robots.txt` allows crawling. HTML contains canonical metadata, social previews, and structured data without requiring JavaScript.

The three package-based Google Play listing URLs returned HTTP 404 during verification on 26 October 2026. App pages explicitly mark public availability as unconfirmed and offer support for access. Replace the access wording and URLs when production or closed-test links are confirmed. Do not add prices, ratings, or availability claims without verification.

Run `python check_site.py` to verify internal links, anchors, structured data, sitemap coverage, and preservation of existing policy paragraphs. Privacy URLs and the legacy `/privacy-policy.html` remain unchanged. Submit the sitemap in your search engine webmaster accounts if available; publication does not guarantee indexing or AI recommendations.

- `/`: Wonderworld Labs homepage.
- `/privacy/`: directory of policies for Wonderworld Labs apps and games.
- `/privacy/melody-garden/`: primary Melody Garden Android privacy policy.
- `/privacy-policy.html`: working legacy address for the same Melody Garden policy, with support at contact@wonderworldlabs.com. App disclosures match the current ad-free, offline Android release. Website-hosting information is disclosed separately on the page.

## Publish

1. Push this checkout to `https://github.com/wonderworld-labs/wonderworld-labs-site` using an account with write access.
2. Settings → Pages → Deploy from a branch. Select the branch containing these files and `/(root)`, then Save. No paid plan is needed because this repository is public.
3. Pages → Custom domain: set `wonderworldlabs.com`, matching CNAME. Verify domain ownership in GitHub; GitHub supplies the unique verification TXT record.
4. In Squarespace Domains → wonderworldlabs.com → DNS settings, set four A records for `@`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153. For `www`, use CNAME `wonderworld-labs.github.io`. Resolve conflicts for these web-host records without changing email MX/TXT records.
5. Wait for DNS and HTTPS certificate provisioning, then enable Enforce HTTPS. Public DNS returned NXDOMAIN on 16 October 2026; confirm the domain is active and its nameservers are correct in Squarespace if that persists.
6. Confirm `https://wonderworldlabs.com/privacy/melody-garden/` opens signed out before entering it in Play Console. The URL is a deployment target, not evidence that publication has succeeded.

## Closed testing

Use the policy URL above after verification. The app release and closed-testing materials stay in the Melody Garden project repository. Testers Google Group: testers-community@googlegroups.com. Select the Google Groups access method in the closed track; members still need to opt in to the test.

## Verification

The homepage links to the policy; support links use contact@wonderworldlabs.com. The policy contains all six sections from the app's current privacy JSON plus a website-hosting disclosure. There are no external fonts, analytics or tracking scripts on the policy page.

## References

- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Adding future products

Create `privacy/<app-slug>/index.html` for each real app, add it to `privacy/index.html`, and put that exact app-specific URL in its Play Console listing. Describe its actual permissions, SDKs, advertising, accounts, data sharing, retention, deletion and children’s use. Do not copy Melody Garden’s no-ads/no-upload claims into a game that uses ads or analytics. A shared policy is possible when it clearly identifies every covered app and accurately distinguishes their practices; separate product pages are the structure used here. No policies have been invented for unreleased or unspecified products.

The old `/privacy-policy.html` remains usable with a canonical link to Melody Garden’s dedicated page. Keep it available for previous links. The site icon sources and raster exports are in assets/, with usage notes in assets/BRAND.md.
