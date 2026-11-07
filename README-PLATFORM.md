# Hosting architecture

Company catalogue source: wonderworld-labs-site repository. The Cloudflare Pages project is deployed at https://wonderworld-labs.pages.dev. The wonderworldlabs.com DNS cutover is pending Squarespace identity verification; the existing GitHub Pages domain still serves the same catalogue source meanwhile.

Craftlane source: craftlane repository. Live standalone studio: https://craftlane-4ke.pages.dev. Planned custom hostname: craftlane.wonderworldlabs.com. No studio runtime is duplicated in the company repo. Legacy privacy URL remains and Cloudflare redirects are prepared for old tool URLs.

Signal & Scale source: signal-and-scale repository. Existing static Cloudflare Worker: https://signal-and-scale.pushpendra-dahiya.workers.dev. Custom domain signal-and-scale.wonderworldlabs.com is bound in Cloudflare, pending authoritative DNS cutover.

Sarkarijob Search: https://sarkarijob.work, sarkarimatch repository, existing Pages project and alerts Worker. Preserve its domain and job refresh schedules.

/apps/ lists products; /games/ lists Android games with browser editions marked planned. Preserve existing /apps/game-slug/ URLs. Add independent repositories, Cloudflare projects and verified Play links when web games are ready.

DNS migration: all 10 original records were imported; compare MX, SPF, DKIM and verification records before switching. Assigned Cloudflare nameservers: fiona.ns.cloudflare.com and hassan.ns.cloudflare.com. Complete DNSSEC transition and verify its final status. After zone activation, bind wonderworldlabs.com and www to the company Pages project; finish Craftlane custom-domain verification; update product and legacy links to branded addresses, canonical URLs and redirect the default app hostname only after the custom hostname works. Update Signal & Scale's build SITE_URL after hostname activation.

One AdSense publisher account can manage all these properties. Distinct registered domains such as sarkarijob.work need separate site review in that account. Each app serving ads needs its own publisher code and consent integration; listing it in the company directory does not enable advertising automatically.
