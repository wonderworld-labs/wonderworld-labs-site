# Wonderworld Labs website

A responsive static site for free GitHub Pages hosting. No build step or paid Squarespace website subscription is required. Existing domain registration/renewal is separate.

## Pages

- `/`: Wonderworld Labs homepage.
- `/privacy-policy.html`: Melody Garden Android privacy policy, with support at contact@wonderworldlabs.com. App disclosures match the current ad-free, offline Android release. Website-hosting information is disclosed separately on the page.

## Publish

1. Push this checkout to `https://github.com/wonderworld-labs/wonderworld-labs-site` using an account with write access.
2. Settings → Pages → Deploy from a branch. Select the branch containing these files and `/(root)`, then Save. No paid plan is needed because this repository is public.
3. Pages → Custom domain: set `wonderworldlabs.com`, matching CNAME. Verify domain ownership in GitHub; GitHub supplies the unique verification TXT record.
4. In Squarespace Domains → wonderworldlabs.com → DNS settings, set four A records for `@`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153. For `www`, use CNAME `wonderworld-labs.github.io`. Resolve conflicts for these web-host records without changing email MX/TXT records.
5. Wait for DNS and HTTPS certificate provisioning, then enable Enforce HTTPS. Public DNS returned NXDOMAIN on 16 October 2026; confirm the domain is active and its nameservers are correct in Squarespace if that persists.
6. Confirm `https://wonderworldlabs.com/privacy-policy.html` opens signed out before entering it in Play Console. The URL is a deployment target, not evidence that publication has succeeded.

## Closed testing

Use the policy URL above after verification. The app release and closed-testing materials stay in the Melody Garden project repository. Testers Google Group: testers-community@googlegroups.com. Select the Google Groups access method in the closed track; members still need to opt in to the test.

## Verification

The homepage links to the policy; support links use contact@wonderworldlabs.com. The policy contains all six sections from the app's current privacy JSON plus a website-hosting disclosure. There are no external fonts, analytics or tracking scripts on the policy page.

## References

- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
