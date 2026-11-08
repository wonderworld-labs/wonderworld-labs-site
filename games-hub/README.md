# Wonderworld Arcade

Live: https://games.wonderworldlabs.com/

The portal is a static shell. It embeds the six original games directly from their existing Wonderworld subdomains. It must not copy, bundle or host game implementations. Original game repositories and sites are the sole game sources and deployments.

Games open immediately in a large player. Illustrated tiles switch between retained frames. The shell includes search, favorites, shuffle, previous/next and cinema/fullscreen controls.

## Build and deploy

Run `python build.py` to copy the shell into `dist/`. This does not include game code. Deploy `public/` in the working workspace, or `dist/`, to Cloudflare Pages project `wonderworld-games`.

Keep the portal and original games' COOP/COEP/CORP settings aligned. Game CSP permits `https://games.wonderworldlabs.com` as a frame ancestor. Embedded document URLs include a release identifier to avoid cached old framing policies.

Game progress stays on each original game's origin. The portal only stores favorites and recent game IDs. Embedded storage behavior can vary with browser privacy settings; the portal does not synchronize saves.

## Cleanup

The temporary runtime-copy deployments `20604225`, `44c62cf5`, and `f68d838c` were deleted from Cloudflare. The local runtime-copy build directory was removed. Future builds contain only the shell and its six SVG thumbnails.

