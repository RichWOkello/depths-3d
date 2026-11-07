# CHANGELOG

## v5.2.0 — Creature Sculpting Refinement (development, 2026-11-07)

- Replaced ellipsoid-stacked core bodies for **Grave Brute, Crypt Crawler, Flesh Ghoul, Dusk Stalker, Ashen Necromancer and Winged Horror** with continuous procedural organic surfaces generated through a cached smooth-union implicit field and marching tetrahedra.
- Created six different locally generated flesh materials containing per-species color variation, scars, capillaries, pore relief, bump mapping and roughness variation. Added deeper eye sockets, layered eyes and double-toothed open mouths.
- Replaced the three-piece dangling arms with continuous tapered muscle surfaces while retaining animated shoulders, wrists, claws and attack telegraphs; tapered ground-leg geometry and arched wing membranes.
- Reused core geometry and texture resources across identical creatures while keeping per-instance material state separate, fixing shared damage-emissive changes between monsters.
- Rebuilt `CREATURE_GALLERY.html` from actual game model code with species-specific skins and rotation/zoom controls.
- Verified six models using simulated Three.js, tested closed two-manifold core mesh topology, and reran v5.2.0 gameplay, progression and boss regression checks.
- **Remaining:** exact photorealism of the supplied images, authored skeletal models, true in-browser WebGL appearance, 60 FPS and hosted Colab runtime have not been validated. This is a substantial procedural improvement, not a production photogrammetry/character-art replacement.


## v5.2.0 — Post-build integration pass (development candidate)

- Replaced camera-attached first-person geometry with a second viewmodel render scene and tighter 58° FOV.
- Distinct katana/saber idle hold state and secondary-hand engagement for saber guard/heavy.
- Added transform-based per-phalanx articulation (4x3 fingers + thumb chain) to firearm hand rigs.
- Added 47 reusable stroke-based inline SVG symbols and removed last extended-pictographic character.
- Added responsive recoil crosshair, compact weapon panel, transient numeric hotbar, 800×700 viewport.
- Added zoom and rotation to minimap, themed light/shadow flashlight and Low/Medium/High quality presets.
- Improved infernal map/roughness/emissive crack material and reduced monster white damage flash.
- Added pooled sprite VFX, lower-quality particle budgets, irregular wet blood decals.
- Fixed Soul Forge perk-review back navigation; added pause/explosion music ducking.
- Added deterministic browser-mock QA, refreshed honest acceptance matrix and test report.

hangelog — Depths 3D

## v5.2.0 — Portal & Presentation Development Build (2026-11-07)

**Not a fully accepted release.** This is an integrated, source-complete development revision, pending real browser/WebGL verification and additional requested feature work.

### Implemented
- Procedural gateway with carved stone arch, pillars, orbiting shards, rune band and a GLSL polar vortex (FBM turbulence, radial swirl, tunnel brightness, pulsing).
- Nine portal palettes with blue/violet Royal Catacombs, orange/red Infernal Sanctum and green/gold variants; enlarged gate on fifth-floor boss levels.
- State-aware portal shader/light updates, opening animation, rune illumination, sealed objective prompt, and deliberate E interaction after activation.
- Portal transition overlay, audio cue, FOV expansion, level-name interstitial and delayed floor load.
- Lower renderer tone-map exposure and ambient light, change Infernal wall/floor palette to charred-basalt colors.
- Soul Forge split into choose-perk and shop views, five categories, page-ready card grid and unspent-currency confirmation.
- New procedural combat/boss sound layers driven by alert and boss state; persistent mute setting.
- High-DPI minimap canvas, facing arrow, FOV cone and M enlargement.
- Removed emoji glyphs from generated game HTML; replaced with readable plain text (a complete SVG icon overhaul remains outstanding).
- Eight-code-cell, fully readable Colab output (seven plain game-string cells and an HTTP iframe launcher), with repeat-execution server cleanup.
- Automated JS syntax checks; notebook parsing and exact-part reconstruction; Colab HTTP handoff mock; static HTTP file serving.

### Not yet implemented or verified against full request
- Production-quality models for all eight weapons, finger-by-finger anatomically correct hands, distinct full weapon animation rigs and IK.
- Screen-space refraction, actual bloom postprocessing, lens distortion and volumetric shafts.
- Entire dungeon material overhaul, full physically based normal/AO procedural map set, torch shadow budget, and realistic monsters.
- Minimap north-up rotation and full-map legend, complete responsive HUD zone redesign, full SVG sprite icon set and universal gamepad UI navigation.
- Real-world Colab GPU/WebGL playthrough, FPS measurement and full boss/weapon regression acceptance.

### Compatibility
- Source retains v5.1.0 combat, campaigns, weapon slots, difficulty, progression and browser storage format; compatibility is intended but full live regressions remain unverified.

---

# Changelog

## [5.1.0] — 2026-11-06 · Integrated development build (NOT acceptance-complete)

- Added directional stamina dodge, collision-aware travel, cooldown and recovery.
- Added direction-sensitive melee guard cost, timed parry differentiation and guard-break exhaustion.
- Added stamina consumption for ordinary melee attacks.
- Changed both blade viewmodels from one procedural grip to two weapon-attached procedural grips.
- Added functional helmet, chest, gauntlet and leg armour tiers, three relic modifiers, and Soul Forge purchases.
- Made weapon mastery tiers affect damage and firearm cadence.
- Extended schema 5 saves with optional equipment/relic fields, retaining v5.0.0 compatibility.
- Regenerated browser, standalone HTML and Colab bundles; expanded automated tests.
- **Not finished:** complete professional skeletal characters, IK, photorealistic weapon assets, extensive animations, new dungeon/campaign expansions, full GPU and Colab gameplay acceptance.



## [5.0.0] — 2026-11-06 · The Abyssal Expansion

Major update from v4.0.0, combining the improvements developed through the v4.x and v5.0 development passes under one public **v5.0.0** release.

### Combat and weapon models
- Expanded to eight weapon slots, including a katana and Light Saber alongside six real-world-inspired firearms and launchers.
- Added simulated projectile movement, ballistic grenades, collision-based impacts, weapon recoil, reloads, weak points, burns, guard/parry, and distinct melee attacks.
- Corrected the first-person katana and energy-saber models, one-hand hilt grips, camera stances, attack arcs, and gradual saber ignition.
- Added layered explosions, flames, hit reactions, sound effects and attack trails.

### Enemies and dungeons
- Added varied monster archetypes, maze navigation, procedural grounded gait, detection/retreat/flanking behavior, and named multi-phase bosses.
- Expanded the Gothic environments with stone architecture, stained glass, ossuaries, chained skeletons, pools, hazards, room set pieces, hidden passages and mechanisms.
- Added keys, ritual switches and other exploration objectives in the campaign.

### Player systems and user interface
- Added progression, equipment upgrades, inventory, Soul Forge, campaign saving, Survival mode and New Game+.
- Reorganized the cinematic introduction, New Expedition / Continue navigation, Loadout, Records, Settings and pause interfaces into minimal dedicated screens.
- Retained quick weapons, minimap, checkpoints and difficulty selection.

### Cross-platform release
- One canonical source in `src/game.js`, rebuilt into GitHub Pages `index.html`, standalone `PLAY_DIRECTLY.html`, and the self-contained Colab notebook.
- Added professional README, release notes, update guide and build verification workflow for the existing GitHub repository.

### Validation
- See `TEST_REPORT.md` and `FEATURE_MATRIX.md`. Automated tests validate source behavior with simulated rendering; real hardware WebGL and Colab acceptance require manual testing.

## Previous public releases

Development before the v5.0.0 release included v4.0.0 and earlier versions. The detailed internal intermediate notes are archived in [docs/DEVELOPMENT_HISTORY.md](docs/DEVELOPMENT_HISTORY.md). Those intermediate build labels are not separate v5.x GitHub releases.

## v5.2.0 — Monster Evolution update (development iteration, 2026-11-07)

- Unique procedural silhouettes for stalkers (lean biped, extended forearms), crawlers (six grounded articulated legs and low body), and necromancers (hood, skeletal limbs and staff). Previously these three archetypes shared other monsters' appearance.
- Four existing boss identities have distinct palette, shoulder regalia, crest and Bone King crown details, while preserving their encounter logic.
- Enemy attack windups now drive jaw, forelimb and staff animation; supporting AI state labels include flank, charge, stagger, attack and investigate.
- Crawlers steer around toward player flanks, necromancers attempt to maintain distance, and brutes gain a short collision-aware charge with cooldown.
- All changes are procedural; no external creature assets added.
- Verified in Three.js mock/browser simulations and existing integration tests. Real GPU visual QA, frame-time profiling, and professional rigged 3D model quality have **not** been verified.

## v5.2.0 — Original Creature Designs Implementation (development iteration)

- Reworked **Grave Brute, Crypt Crawler, Flesh Ghoul, Dusk Stalker, and Ashen Necromancer** to have individually recognizable, grotesque procedural anatomy, scar/tendon detail, faces, claws, and distinct coloration.
- Added the **Winged Horror** as a new enemy type in the existing monster selection system, starting in floor 3 pools, with flapping wing geometry, wing folding in narrow passages, hovering and telegraphed dive attacks.
- Added procedural creature albedo and roughness detail with shared materials, quality/distance microdetail LOD, positional creature sounds, and short capped death animations.
- Preserved all four existing bosses and existing combat, progression and save logic. Rebuilt both web distributions and the readable eight-cell Colab notebook, with an interactive `CREATURE_GALLERY.html` generated from the exact same source models.
- Automated syntax and simulated gameplay regressions passed; real WebGL image quality, actual Google Colab execution, and 60 FPS **not verified**.

## v5.2.0 — Necromancer face, hood and ritual detail refinement (development candidate)
- Rebuilt recessed skull face, teeth, eye sockets and an actual open fabric hood.
- Added double-layer pleated robes, violet rune paths, spiked pauldrons and three belt skull trophies.
- Rebuilt the gnarled left-hand staff with a thorn crown, orb, halo and localized light.
- Added five moving wisps around the right casting hand and responsive casting pose/light effects.
- Added distance culling for minor magic props and updated the Necromancer-first Bestiary Viewer.
- Retained original Bestiary creature roster, gameplay, save system, bosses and Colab flow.
- Real GPU visuals and 60 FPS still require verification.
