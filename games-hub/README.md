# Wonderworld Arcade

Live: https://games.wonderworldlabs.com/

An immersive static game portal. A game opens immediately in a large player; six illustrated game tiles switch between retained frames. Includes favorites, search, shuffle, previous/next, cinema mode and fullscreen where supported. No marketing hero or long introductory copy.

## Build and deploy

The shell is in `public/` in the working workspace, or directly in `games-hub/` in the company source repository. Original game implementations remain in their respective private repositories. Runtime copies are assembled for hosting; do not commit `dist/` to the public company repository.

Run `python build.py --source-root D:\push\projects\wonderworld-labs` with the game checkouts available under `game-projects/<slug>` and `android-web-projects/<slug>/public`. This assembles `dist/`. Publish that folder to Cloudflare Pages project `wonderworld-games`.

Latest deployment: https://20604225.wonderworld-games.pages.dev/

The arcade runtimes share the portal origin and use distinct game save keys. Portal saves are separate from saves on the individual game subdomains. The individual game sites remain available.

## Validation

Checked all six boards/entry flows inside the portal, a real arrow-removal interaction, and retained in-progress state after switching games. Block Blasting rendered all 64 cells. HintHunt retains its original explicit model-download choice. Cinema mode works; browser automation could not grant the user activation needed for native fullscreen, so that remains a manual check. Games still expose their original navigation and settings.

## Game source revisions

- Arrow unleashed: `05233d7e79fd5db106bf32fd61fb07db5762b5a5`
- Block Blasting: `b3e583b0921560f523bf73faffd125483038f432`
- Ladderday: `292b8b300a4caed6b87793dda0cb1dc381909a41`
- HintHunt: `cabd1f5a7bcfbb5ed93e299d969a959ef8551107`
- Linkloom: `a85075447af2aa702910ae3e5d7369ad4f163a13`
- Scale Safari: `8f070df8b987ba6bda1fca1901e2e303b85715d8`

