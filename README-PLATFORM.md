# Independent app hosting

The company catalogue is deployed from this repository to the wonderworld-labs Cloudflare Pages project at https://wonderworldlabs.com. www redirects to the apex domain. DNS is managed by Cloudflare; registration remains with Squarespace. Google Workspace MX, SPF, DKIM and verification records are preserved.

Products:
- Craftlane: https://craftlane.wonderworldlabs.com, craftlane repository, separate Cloudflare Pages project. This company repo contains its product and legacy privacy pages, not the studio runtime.
- Signal & Scale: https://signal-and-scale.wonderworldlabs.com, signal-and-scale repository, separate static Cloudflare Worker.
- Sarkarijob Search: https://sarkarijob.work, sarkarimatch repository, existing Cloudflare Pages and alerts Worker. Preserve its domain and refresh schedules.

/apps/ lists products. /games/ lists Android games and future browser editions. Preserve established /apps/game-slug/ URLs; create independent repositories and Cloudflare projects for browser editions. Add Play links only after deployment is verified. Never label planned web games as playable.

Pushes to each product's repository deploy only that product. Product links, directories and company guides are maintained here. Default Pages hostnames redirect to branded production addresses. Keep Google Workspace mail records intact during DNS changes.

One AdSense publisher account manages the properties. Distinct registered domains such as sarkarijob.work require their own site approval within the same account. Each deployment serving ads needs the publisher code, ads.txt handling and appropriate privacy/consent integration. A company-directory listing does not itself enable ads.

GitHub Pages may temporarily remain as a fallback while old DNS caches expire; Cloudflare is the authoritative production destination.
