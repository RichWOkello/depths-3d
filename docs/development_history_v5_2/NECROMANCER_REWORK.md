# Depths 3D v5.2.0 — Necromancer Rework

This is a **targeted art-and-animation update to the existing Bestiary Pass**. It is not a new release number, a direct copy of the reference artwork, or a replacement for a professionally sculpted GLB model.

## Reference characteristics and implementation

| Reference requirement | Implementation status |
|---|---|
| Long pale skull face hidden in a hood | Reworked with layered cheekbones, recessed dark eye sockets, narrow nasal cavity, exposed teeth, and an open hood opening; visual match not certified |
| Deep, jagged hood | Generated an open bevel-like hood shell, double edge stitching, hood brow and fabric tails; partial approximation |
| Tall maroon-black robes | Two procedural robe surfaces with vertex-color pleats and uneven hems; partial approximation |
| Metal spiked pauldrons | Four spike pieces on each shoulder, two-toned metallic trim; partial approximation |
| Skull trophies attached to belt | Three miniature skull face ornaments with sockets, nose, teeth and hanging chains; implemented |
| Ancient carved staff on character's left in the image | Staff moved to left hand and extended towards the floor, thorn crown and rings added; partial approximation |
| Violet energy orb and bloom | Separate bright orb, halo, point light and orbiting runic motes; real compositor bloom NOT implemented by this patch |
| Purple runes on robes | 16 glowing runic strokes that pulse in casting state; implemented |
| Raised free hand throwing magical wisps | Right-hand magic with five animated strands and timing tied to attack state; implemented |
| Cloth and ornament reaction to movement | Existing sprung strips plus subtle belt skull motion; partial physics approximation |

The other five Bestiary creatures, original bosses, eight weapons, game progression, menus, and Colab launcher are retained. The model is procedural and uses the same cached 17-bone skinned-body and 3-LOD engine as before.

## Performance controls

Animated wisps and the staff light are disabled beyond 16 m; runic details fade out by 22 m; halo by 24 m; miniature trophy skulls by 26 m. The game engine still limits character animation beyond 40 m. These are coarse visibility switches, not proof of 60 FPS.

## Running

- **Colab:** open `depths_3d_bestiary_pass.ipynb`, run the primary code cell and click inside the resulting iframe.
- **Browser:** open `PLAY_DIRECTLY.html` in a WebGL-capable desktop browser with internet connectivity for Three.js CDN.
- **Visual inspection:** open `BESTIARY_VIEWER.html`; the Necromancer is now selected by default. Rotate it and toggle attack/idle and silhouette overlay.
- **GitHub:** copy the contents of this package into an existing local repo but preserve its hidden `.git` directory; review/test before pushing.

## Testing and limitations

Automated syntax, mocked Three.js instantiation, animation-state progression, Colab compilation, and gameplay regression tests pass. There was **no genuine GPU/WebGL visual approval**; exact likeness, actual animation smoothness, real Colab browser rendering, mobile behavior, and 60 FPS remain unverified. The enlarged decorative silhouette increases mesh/draw-call count at close range, so frame rate must be checked in a real play session. More accurate matching requires a sculpted GLB model and production rigging; an optional GLB loader adapter remains available in the Bestiary source.
