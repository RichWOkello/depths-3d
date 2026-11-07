# DEPTHS 3D v6.0.0 — Test Report

**Build date:** 2026-11-07  
**Status:** GitHub-ready release candidate; real GPU/WebGL certification pending.

## Automated tests run on the integrated v6.0.0 source

| Test | Result | Scope |
|---|---|---|
| JavaScript syntax (`node --check src/game.js`) | PASS | Source parses; does not guarantee runtime rendering |
| Rebuild (`python build.py`) | PASS | Regenerates playable HTML, GitHub Pages source, bestiary viewer and Colab notebook |
| Notebook validation | PASS | Eight notebook cells, including two Python code cells |
| Necromancer-specific model test | PASS | Hood, skull, robe layers, belt ornaments, staff crown, five spell wisps and casting state in simulated Three.js |
| Five-creature anatomy/LOD test | PASS | Five species, cache reuse, finite geometry, LOD switches and preserved Necromancer model |
| Integration regression test | PASS | Reload, projectile updates, AI alerts, portal gating, saved progress, boss phase transitions |
| v5.2 UI regression test on integrated v6 source | PASS | 47 SVG symbols, eight gun viewmodels with hands, 800×700 HUD, two-step Soul Forge actions |
| Actual WebGL on user's machine | NOT VERIFIED | Requires Chrome/Edge/Colab |
| Sustained 60 FPS, 40 monsters | NOT VERIFIED | Real GPU draw-call benchmark not available |
| Reference-exact photorealistic likeness | NOT ACHIEVED | Procedural geometry is an approximation, optional GLB replacement path available |

These results reflect tests actually executed against the v6.0.0 code; tests labeled v5/v5.2 in their filenames are **regression tests** of earlier systems, not evidence that the release remains at those versions. Structural/mock WebGL tests do not prove photorealism, accurate clipping-free animations, or live browser performance.

## Known performance gap

Uncached high-detail procedural geometry generation for some species can exceed the 150 ms target, although geometry is cached thereafter. Draw calls may be high with large enemy groups. Quality settings and distance-based detail reductions exist but have not been certified on mid-range hardware.

## CI

`.github/workflows/verify.yml` runs JavaScript syntax, a deterministic rebuild and notebook validation when pushed to GitHub. Passing CI will not certify full GPU visual quality.
