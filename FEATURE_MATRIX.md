# Depths 3D v5.0 — Feature and gap matrix

The implementation is verified against the provided v4.9.0 game and preserves existing gameplay. "Implemented" means an executable mechanic exists and has passed at least a code path or targeted simulated-browser test where one is listed, not that final player tuning and real-GPU visual acceptance are complete.

| Domain | Implemented in v5.0 | Partial / not yet implemented |
|---|---|---|
| Weapons | All eight retained, live bullet/grenade physics, per-weapon magazine/reload, automatic and burst AK, projectile hit/weak-zone, shotgun falloff, flamethrower burn, distinct synthetic audio, weapon damage and technology upgrades | No full per-weapon recoil animation suite with real-world measured values; no manual shell-by-shell shotgun reload; no complete per-surface impact library |
| Melee | Katana/saber sweep damage, follow-through, directional combo, guard/parry, saber ignition and timed energy wave, impact feedback and lightweight severing | No full-body inverse-kinematics sword fencing, dynamic parry targeting or rigid-body ragdoll |
| Enemies | Stalker, armored, crawler, necromancer variants, LOS, noise response, patrols, flanking/retreat, summoning/healing, pathfinding, grounded leg animation, stagger/knockback | Crawlers do not physically climb ceilings, squad tactics and cover-seeking are limited, no mocap |
| Procedural dungeons | Nine distinct theme palettes, navigable generated mazes, seeded reproducibility, set-piece rooms, key-gated exits, rune interaction, breakable secret walls, hazards, boss arenas, decorative cathedrals | No advanced multi-stage lock/door system, physical collapsing floors, rescue quests or authored room storytelling |
| Bosses | Four names/forms, 20-floor cadence, three phases, health bar, warning rings, more aggressive phases, different special attacks, minions/wards/arena hazards | Boss attacks share procedural skeletons, not bespoke mocap or polished cinematic cut-scenes |
| Progression | Soul coins, medkits, armor, stamina, random perks, weapon damage and 5 gun-tech categories, inventory, Survival, New Game+ | Permanent cross-run unlock trees and equipment loadout slots not fully implemented |
| Sound/graphics | Weapon profiles, layered explosion VFX, fire/smoke, spatial creature cues, theme palette, procedural wall detail, level cleanup, manual graphics scale, volume settings | No imported high-quality recordings, physically based scanned textures, volumetric light or high-end renderer benchmarks |
| UI/Save | Cinematic launch, main menu, pause, inventory, 8-weapon quick panel, HUD objectives/minimap, boss health, campaign save/continue, reset saved campaign | No fully freehand radial mouse wheel; browser persistence not tested in actual Colab origin; no cloud synchronization |
| QA | Syntax, browser interaction with Three.js mock, actual projectile damage math, grenade drop/explosion, maze reachability, boss phases, shop/save data, local HTTP launcher | Real WebGL fidelity, GPU fps, actual user Colab rendering and spatial audio output require external testing |

## Consolidated v5.0.0 interface and katana correction

Katana: slimmer curved blade, modeled guard/hilt/edge, camera repositioning, single circumferential gripping hand, combo cuts and heavy/thrust moves, guard and sweep-timed melee contact. These features passed mock-browser behavioral tests; real GPU render quality remains unverified.


The main and title screens were simplified without removing features. Loadout selection, detailed controls, game modes, audio/video settings, records and save controls are reachable in focused submenus. Destructive save actions request confirmation. These changes do not modify the deferred gameplay capabilities listed above.
