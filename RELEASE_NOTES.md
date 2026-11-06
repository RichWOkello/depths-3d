# Depths 3D v5.0.0 — The Abyssal Expansion

**Release date:** 6 November 2026  
**Release type:** Major update to the existing `RichWOkello/depths-3d` project  
**Platforms:** GitHub Pages, standalone browser, Google Colab

## Highlights

- **Eight-weapon arsenal** with six firearm/launcher weapons and two melee weapons (katana and Light Saber).
- **Improved melee presentation:** corrected single-hand grip, improved katana proportions, layered saber ignition, timed strikes, guard and knockback.
- **Richer combat:** ballistic projectiles, grenade gravity, reloads, recoil, burns, head-height damage and impact effects.
- **More intelligent dungeon enemies** with differentiated behaviors, improved gait, navigation and boss phases.
- **Larger Gothic dungeon variety** with atmospheric architecture, hazards, crypt keys, rune switches and secrets.
- **Player progression** with medkits, stamina/armour, inventory, Soul Forge upgrades, campaign continuation, Survival and New Game+.
- **Cleaner cinematic UI** with a simplified start flow and separate settings, loadout and records pages.
- **One game source / three ways to play:** GitHub Pages, single-file HTML, and a self-contained Colab notebook.

## Playing

Use [the GitHub Pages site](https://richwokello.github.io/depths-3d/) after the v5.0.0 commit deploys, or launch [`depths_3d.ipynb`](depths_3d.ipynb) in Google Colab. For local play open `PLAY_DIRECTLY.html` in Chrome or Edge.

## Compatibility and limitations

- WebGL and an internet connection to fetch Three.js r128 are required.
- The hands, monsters, weapons and environments are still procedural 3D assets; they are **not photorealistic models**.
- Real WebGL hardware rendering and long Colab sessions are not fully validated by the automated test suite.
- Browser storage is origin-specific; a Colab save may not transfer to GitHub Pages.
- Full ragdoll physics, real wall/ceiling crawler locomotion, and motion-captured animation remain outside this release.

Read [TEST_REPORT.md](TEST_REPORT.md) and [FEATURE_MATRIX.md](FEATURE_MATRIX.md) for the precise verification scope.

## Release checklist

- [ ] Replace files in the existing local repository using [UPDATE_LOCAL_REPO.md](UPDATE_LOCAL_REPO.md)
- [ ] Run the build and syntax checks locally
- [ ] Verify `index.html` and `depths_3d.ipynb` in a real browser/Colab
- [ ] Commit the v5.0.0 files to `main`
- [ ] Check the existing GitHub Pages site after deployment
- [ ] Create the `v5.0.0` Git tag and GitHub Release, if desired

This package is **prepared for publishing**; it has not been pushed to GitHub.
