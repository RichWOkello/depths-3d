# Depths 3D v5.2.0 — Five-creature fidelity review

**Source references:** the six cropped images supplied for the Bestiary Pass. The successful Necromancer design was kept intact.

**Status definitions:** *Modeled* means an actual mesh/material/animation path has been added or retained; *Partial* means the behavior or anatomical feature is approximated; *Unverified* means no real WebGL visual or GPU test has established the result. A modeled feature is **not** a declaration that it resembles the reference perfectly.

## Flesh Brute

| Reference element | Actual implementation | Status |
|---|---|---|
| Broad asymmetrical shoulders | Anatomical overlays + cached body surface | Modeled |
| Enormous protruding belly | Original fused SDF body + breathing scale | Modeled |
| Small recessed head | Low skull mount and cranial shell | Modeled |
| Deep roar cavity | Jaw rig and dark mouth geometry | Modeled |
| Sunken eyes and facial creases | Socket shapes, cheek muscles and scars | Modeled |
| Seamed/stapled skin | Stitched scar seams in head and chest | Modeled |
| Long heavy arms | Existing skinned arm rig retained | Modeled |
| Worn leather forearm bindings | Multiple curved brown straps per arm | Modeled |
| Dirty ragged loincloth | Existing spring cloth retained | Modeled |
| Weighted gait and wind-up | Brute shoulder, head and chest attack response | Modeled |
| True independent belly spring | Not implemented; breathing scale only | Partial |
| Photorealistic body/face matching | Not verified; requires sculpted/GLB model | Unverified |

## Crypt Crawler

| Reference element | Actual implementation | Status |
|---|---|---|
| Low long quadruped | Existing fused four-limb crawler | Modeled |
| Long spidery forearms | Existing skinned slender limbs | Modeled |
| Visible external rib cage | 18 curved bone-rib elements | Modeled |
| Ridged arched back | Existing dorsal spikes plus 6 new details | Modeled |
| Recessed skull-like muzzle | Organic cranium and bony snout | Modeled |
| Hooked teeth | Side fangs and jaw teeth | Modeled |
| Long planting claws | Finger claws and new foot talons | Modeled |
| Sinewy flesh and veins | Forearm tendon strips and canvas bump | Modeled |
| Diagonal scuttling gait | Existing crawl IK and spine wave retained | Modeled |
| Ambush or leap behavior | Prior gameplay retained, not separately played | Unverified |
| Grounded foot planting in live WebGL | Not visually verified | Modeled |
| Exact photorealistic likeness | Not verified; sculpted GLB needed | Unverified |

## Flesh Imp

| Reference element | Actual implementation | Status |
|---|---|---|
| Huge disproportionately bulbous head | Asymmetric cranial loft | Modeled |
| Two glossy oversized eyes | PBR eyeballs and iris geometry | Modeled |
| Fleshy orbital rims | Curved rings + upper eyelids | Modeled |
| Blink and pupil dilation | Existing animation + fixed per-lid base heights | Modeled |
| Wrinkled cheeks and folded skin | Curved layered crease lines | Modeled |
| Small distorted nose | Two recessed nostrils | Modeled |
| Crooked fleshy lips | Irregular lip arch and chin | Modeled |
| Tiny needle teeth | Original jaw teeth | Modeled |
| Wet mottled red skin | Five-species procedural map and roughness | Modeled |
| Low crouching hands and talons | Existing rig plus foot claws | Modeled |
| Swarm spawns and scale variation | Game source preserves group spawns + scale | Modeled |
| Independent facial muscle rig | Not implemented; eye and jaw animation only | Partial |
| Exact photorealistic likeness | Not verified; sculpted GLB needed | Unverified |

## Gaunt Hooded Wraith

| Reference element | Actual implementation | Status |
|---|---|---|
| Tall emaciated silhouette | Original narrow skinned body retained | Modeled |
| Hollow-eyed elongated head | New organic cranial shell | Modeled |
| Mostly exposed skeletal torso | Reduced solid head hood coverage | Modeled |
| Conspicuous ribs | 16 curved exposed rib elements | Modeled |
| Long tendon-covered arms | Six new arm cord details | Modeled |
| Long curved claws | Original hand claws remain | Modeled |
| Ragged partial shroud | Torn strips at head and waist | Modeled |
| Grey-brown sinewy skin | Retuned dry procedural skin material | Modeled |
| Floating eerie gait | Existing gliding spine and arm animation | Modeled |
| Teleport and orb abilities | Existing enemy type and effects preserved | Modeled |
| True alpha dissolving body | Prior opacity fade; not a vertex dissolve shader | Partial |
| Exact photorealistic likeness | Not verified; sculpted GLB needed | Unverified |

## Winged Gargoyle

| Reference element | Actual implementation | Status |
|---|---|---|
| Wide bat-like wings | Two skinned wing membranes | Modeled |
| Anatomical wing finger supports | Original elbow/wrist/finger bone hierarchy | Modeled |
| More irregular ragged wing edges | Contour scallops and procedural holes | Modeled |
| Birdlike predatory skull | Organic elongated cranium | Modeled |
| Prominent hooked beak | Raised central curved beak | Modeled |
| Jagged horns | Additional curved horns and skull ridges | Modeled |
| Thin but powerful arms | Skinned limbs plus tendon strips | Modeled |
| Curled gripping toes | New toe claws and nails | Modeled |
| Six-segment bony tail | New animated articulated tail groups | Modeled |
| Perched / swoop behavior | Prior AI and wing folding preserved | Modeled |
| Rock perch and flight corridor collision | Existing game geometry; not visually verified | Unverified |
| Exact photorealistic likeness | Not verified; sculpted GLB needed | Unverified |

## Necromancer preservation

Its open hood, skull, layered robes, staff crown, purple orb, three belt skulls and five wisps are retained. Its original procedural skin-map algorithm is also preserved, while the general low-level geometry creation helper now reuses cached primitives. The dedicated Necromancer structural and animation regression passed.

## Real-device acceptance that remains open

- Inspect all five models beside their reference art in a WebGL-capable browser, from the front, side and 3/4 angle.
- Verify jaws, claws, eyes, wing positions, shoulders, tails, hoods and cloth never intersect unnaturally during idle, walk, attack, hit and death.
- Run actual Colab iframe and desktop HTML, with live Three.js from its supported CDNs.
- Verify GPU frame times and memory at 10, 20 and 40 enemies, not only headless simulated movement.
- For exact high-frequency facial detail, create Blender/GLB replacements using the provided GLB loading fallback; purely procedural detail still looks less realistic than the image references.

