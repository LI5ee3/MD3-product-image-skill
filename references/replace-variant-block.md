# REPLACE_VARIANT block

Read this file only when building an SKU scene prompt (state `REPLACE_VARIANT`).
Append the block below with its exact words after the `CORE_SCENE_BLOCK`; never
rewrite, paraphrase, or expand it.

```text
Lock ORIGINAL MASTER geometry, shape placement, depth, material roles,
relative light-dark hierarchy, composition, and primary light direction. Use
CURRENT SKU as the only authoritative product; do not show the master product.

Do not lock master hues. When CURRENT SKU visibly differs in dominant color,
re-derive the background base and secondary colors from CURRENT SKU. At least
one large field and one secondary field must change visibly at thumbnail size;
a product-only change does not count. Re-establish the controlled contrast
family instead of collapsing the adapted fields into one near-identical hue
family. Preserve separation from every adjacent field.

Lock version-text size, position, and typography. Its solid lightness may adapt
only for legibility against the SKU-adaptive background; never add a backing.
```
