# Changelog

## [5.0.0] — Katana and Light Saber corrected build (2026-11-06)

- Rebuilt the katana as a thinner, curved tapered blade with a modeled tsuba, wrapped hilt, pommel and reflective metallic edge.
- Replaced its generic melee hand with one handle-locked anatomical grip: four fingers curve *around* the hilt, with an opposable thumb and tapered forearm.
- Repositioned the katana in the lower-right camera foreground with restrained walk/run sway and limited camera obstruction.
- Added keyed horizontal/diagonal combo cuts, G heavy vertical slash, T thrust and C guard/parry; matched slash trails and sweep-timed hit windows, with stamina and cooldown checks.
- Preserved all eight weapons, other viewmodels, HUD, menus, save format and Colab/static hosting outputs.
- Rebuilt the Light Saber as a compact, detailed metallic hilt with emitter, grip ridges, pommel and slim layered luminous blade.
- Replaced the Light Saber’s offset glove with one anatomical hand locked to the hilt. Four fingers wrap around its circumference and the thumb opposes them; the forearm no longer drifts during attacks.
- Corrected the saber ignition transform: extending cylinder length along local **Y** while the blade faces world **Z**, keeping the near end fixed at the emitter.
- Added a distinct lower-right Light Saber ready stance, restrained walking/running sway, guard animation and style-specific horizontal/diagonal/heavy/thrust attacks with matching sweep paths and resource costs.
- Kept the katana corrections and other seven weapons, combat, menus, saves, Colab and static hosting outputs intact.
- Tested with Chromium and a simulated Three.js renderer; real WebGL presentation still requires hardware review.

## Previous v5.0.0 feature history

## [5.1.0] — 2026-11-06 · Minimal Interface

- Redesigned the start screen with a clear hierarchy, restrained typography and reusable Gothic artwork.
- Kept the cinematic intro → title → difficulty → main menu flow, while removing the crowded armory, mode and controls lists from the main menu.
- Introduced dedicated Loadout, Records, and Settings pages. Settings now opens Audio, Display, Controls, Gameplay and Saved Data subpages.
- Redesigned pause, quick weapon selection and victory/failure screens using the same visual language.
- Made New Expedition and Delete Save require explicit confirmation when a saved campaign exists.
- Reduced footer control labels to essential shortcuts; complete controls remain available within Settings.
- Verified menu navigation, settings changes, save confirmation, start/resume, combat controls and six legacy physics/world tests in simulated Chromium.
- Rebuilt the Colab, single HTML and static-hosting entry points from the same source. Nothing was uploaded to GitHub.

## [5.0.0] — 2026-11-06 · The Abyssal Expansion

### Combat and physics
- Replaced firearm precomputed instant hits with simulated moving projectiles, sub-stepped wall/enemy collision and M79 gravity.
- Added firearm magazines and reload timing, burst/auto AK mode, vertical aim, head-height and weak-zone bonuses, damage falloff and physics-based knockback.
- Added timed katana guarding/parries and a charged energy-saber wave, plus melee combo scaling and persistent flamethrower burning patches.

### Enemy behavior and bosses
- Added distinct stalkers, armored demons, crawlers and necromancers with stealth/retreat, resistance, leg rigs, summoning, healing and investigative behaviors.
- Added noise events, patrols, navigation and wind-up melee strikes.
- Four named boss encounters with multi-phase health bars, danger telegraphs, shield/ritual and elemental variants, and carved boss arenas.

### Dungeons and progression
- Extended the environment rotation to nine Gothic/temple/crypt/fortress/library themes.
- Added functional rune switches, recurring crypt-key objectives, secret breakable walls, discoverable soul rewards, hazards and different decorated room types.
- Added coin economy, inventory/medkits, stamina and armor, a Soul Forge between floors, five firearm technology upgrades, campaign save/continue, Survival and New Game+.

### UI and architecture
- Added a weapon selection screen, objective/armor/energy HUD readouts, save/continue/inventory panels, boss meters and expanded settings.
- Improved level-bound resource disposal and prevented duplicate Colab HTTP servers on cell rerun.
- Generated browser, Colab and GitHub Pages-ready formats from the same game source. No automatic publication.

### Testing and known gaps
- Added specialized integration tests for projectile collisions, boss phases, reloads, saves, world reachability and controls.
- See `TEST_REPORT.md` for tests that were actually executed and `FEATURE_MATRIX.md` for unimplemented/partial features. No full live WebGL or real-user Colab acceptance test has been performed.


## [4.9.0] — 2026-11-06

### First-person handling pass
- Reworked firearm hand placement to better match realistic first-person handling, including a true support hand for the pistol and more natural trigger/foregrip placement for long guns.
- Refined the katana and energy-saber holding poses with stacked two-hand grips and stronger wrist alignment.
- Added more readable melee swing presentation with side-dependent slash arcs, fuller wind-up, clearer follow-through, and improved hand/weapon motion during attacks.

### Validation
- Rebuilt browser and Colab outputs from the shared source.
- Updated delivery checks for the new version and reran automated tests.

## [4.8.0] — 2026-11-06

### Grounded locomotion and navigation
- Replaced rigid swinging legs on chasers, brutes, and bosses with jointed thigh/shin/knee/ankle/foot rigs solved by procedural two-bone IK.
- Replaced static crawler appendages with six IK legs using an alternating tripod gait. Shooters and teleporters retain appropriate hovering motion.
- World-space stance foot pinning, lifted swing phase and footfall-triggered positional sound; increased cadence when creatures move faster.
- Smoothed acceleration, braking and facing, plus shared BFS path navigation around dungeon walls and corners.

### Gothic architecture
- Added instanced carved wall bays, base plinths, stone buttresses, vertical columns, pointed arch tracery, dark recesses, and cornice reliefs.
- Preserved six distinct floor themes, high cathedral ceilings, chained skeletons, stained glass, altars and other decorations.

### Validation
- Passed game navigation and locomotion regression tests for knee movement, stable planted feet, swing clearance, foot contacts and six-legged creatures.
- Passed existing gameplay, melee physics, theme and Colab launcher tests using mock 3D geometry.
- JavaScript and notebook builds share one source. No GitHub publication.

## [4.7.0] — 2026-11-06

### Anatomical hand rigs
- Shared procedural first-person hand rig across all eight weapon slots: asymmetrical palms, separate thumbs, jointed curved finger segments, skin/leather/cloth microtextures, knuckles and nails.
- Two-handed katana and energy-saber stances; distinct recoil reaction for firearms, swing follow-through and finger-grip movement for blades.

### Combat physics
- Angular sweep-sampled blade collision and per-swing hit tracking rather than instantaneous cone damage.
- Directional knockback, friction, stagger, hit tilt, wound curves, swing-specific audiovisual feedback.
- Finishing blows can detach articulated monster limbs into short-lived physics approximations (gravity, angular motion, bounce and settling).
- Gradual energy-saber ignition with delayed attack readiness.

### Cathedral environment
- Pointed gothic arches with masonry ribs and layered columns, stained-glass recesses, rose tracery and ornamental mullions.
- Rib-vaulted ceilings, hanging iron chandeliers, gargoyles and sculpted stone tombs, alongside existing skulls, chained skeletons, blood pools and six contrasting dungeon themes.
- Architectural set pieces are capped per level to limit geometry load in browser/Colab use.

### Validation
- JavaScript syntax, Python notebook compilation, local server delivery, six-theme smoke tests, UI navigation and dedicated hand/melee/knockback/severing regression tests.
- All entrypoints rebuilt from the shared `src/game.js` source. No GitHub deployment.

## [4.6.0] — 2026-11-06

### Physics and animation pass
- Reworked melee presentation with distinct katana and energy-saber stances, improved swing arcs and more logical recovery motion.
- Added two-handed support grips for both melee weapons, plus slow saber blade ignition when the weapon is drawn.
- Strengthened katana/saber slash audio and impact feedback.

### Hands, monsters and environment
- Rebuilt weapon hands to look more anatomical, with curled gripping fingers, separate thumbs, wrist cuffs and glove structure.
- Enemy locomotion now uses smoothed facing, stride-driven gait motion and reduced floatiness for more believable movement.
- Cathedral walls and floors were repainted procedurally for taller, more gothic stonework with arches, stains and heavier masonry detail.
- Improved the loadout panel presentation while keeping all eight weapon slots visible.

### Validation
- Source rebuilt into HTML and Colab outputs from the same JavaScript.
- Delivery test rerun successfully after the rebuild.

## [4.5.0] — 2026-11-06

### Melee combat
- New motion-timed melee attack contact, blade-specific wind-up and recovery; katana and energy saber no longer share firearm recoil movement.
- Animated, camera-space ribbon slash with bright cutting edge plus impact streaks, particles and hit response.
- Unique katana steel swish/clang and saber energy sweep/sizzle sound synthesis, including on-contact variations.
- Organic segmented protective glove fingers, opposable thumbs, pads, articulated wrist and arm sleeves on every weapon.

### Dungeon art
- Six rotating cathedral/crypt environments with distinct procedural stonework, tiled flooring, color lighting, fog and atmosphere.
- Blood pools, skull collections, skeletal prisoners chained to walls, high stone arches, altars, collapsed rubble, stained glass, water patches and infernal fissures.
- Higher ceilings and cathedral scale; themed environmental audio cues.

### Enemies and HUD
- Extra bone anatomy, facial fangs, muscle tendon details, scar-like features and torso breathing animations.
- Compact two-row weapon selector with equipped name, icon and 1–8 shortcuts.

### Validation
- Syntax check and simulated-browser intro/PLAY/pause/weapon tests, six-theme generation test and time-delayed melee action test.
- Colab and HTML output rebuilt from the exact shared source. No GitHub upload.

## [4.4.0] - 2026-11-06

### Added
- Four-stage cinematic launch: intro, title, difficulty, then main menu.
- Game-themed background artwork embedded in every delivery format.
- New usable Katana and Energy Saber melee weapons with models, hands, slash damage, swing animations and differentiated audio.
- Original synthesized ambient background music and menu selection feedback (user-gesture initiated).
- A continuous flamethrower combustion sound layer.

### Changed
- Eight-weapon switching with digit keys 1–8 and mouse wheel.
- Compact, translucent in-game weapon selection display, designed not to obscure the center of the scene.
- Self-contained Colab notebook, playable single HTML, and GitHub Pages source rebuilt from one shared JavaScript file.

## [4.3.0] — 2026-11-06

### Visual effects
- Added textured GPU-facing fire, rolling smoke plumes, glowing sparks, timed impact lights, shockwaves and scorch marks to grenade and barrel explosions.
- Replaced the flamethrower's small sphere projectiles with brighter animated flame textures and smoke; added first-person nozzle fire and distinctive flame audio.
- Applied effects cleanup, opacity curves, motion turbulence, and an overall particle-count budget for browser and Colab performance.

### Monsters and sound
- Redesigned imp, eye-demon, ogre, teleporter, splitter, mini and demon lord models with smooth shared organic meshes, horns, eyes, jaws, tendrils, and wings.
- Added type-specific stereo-positioned procedural vocalizations and revised non-neon creature materials.

### Interface and pickups
- Redesigned the main menu, loadout cards, difficulty/mode controls, stats, settings, pause, perk and death screens.
- Restyled in-game score, status, ammo, minimap, and hotbar panels.
- Redesigned medical, ammunition, and soul relic pickups with floating identification labels when nearby.

### Compatibility and validation
- Kept the Colab HTTP iframe approach and regenerated both notebook and web builds from the same source.
- Added `PLAY_DIRECTLY.html`, a single-file browser edition that still loads Three.js from a CDN.
- Passed Node syntax and mock-browser interaction tests. Actual WebGL/Colab iframe rendering remains dependent on the end user's environment.

## [4.2.1] — 2026-11-06
- Fixed missing material helper (`GM is not defined`) and improved game startup.

## [4.2.0] — 2026-11-06
- Unified Colab web-server iframe and browser editions.

## [4.1.0] — 2026-11-06
- Added more detailed real-world-inspired Desert Eagle, Remington 870, UMP9, AK-pattern rifle, M79 and flamethrower first-person models.
