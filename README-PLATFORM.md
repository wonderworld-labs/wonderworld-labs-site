# Hosting architecture

Company catalogue: wonderworldlabs.com, Cloudflare Pages, wonderworld-labs-site repository.

Craftlane: craftlane.wonderworldlabs.com, Cloudflare Pages, craftlane repository.

Signal & Scale: signal-and-scale.wonderworldlabs.com, existing Cloudflare Worker, signal-and-scale repository.

Sarkarijob Search: sarkarijob.work, existing Cloudflare Pages and alerts Worker, sarkarimatch repository.

/apps/ lists products. /games/ lists Android games and future browser editions. Keep existing /apps/game-slug/ URLs for established links. Add independent game repositories and Cloudflare projects when browser editions are ready; only show Play buttons after verification.

One AdSense publisher account can manage these properties. Distinct registered domains need their own site review. Each deployment serving ads needs the publisher code, ads.txt handling and appropriate privacy/consent setup.
