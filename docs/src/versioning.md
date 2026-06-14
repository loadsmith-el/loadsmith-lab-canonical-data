# Versioning

The `VERSION` file is the source of truth for the dataset revision (currently
`v1`). By convention this string is mirrored in three places that **must always
agree**:

- this `VERSION` file,
- the git **tag** on the same commit (`v1`),
- each consuming image's Dockerfile `ARG DATA_REF` in
  [`loadsmith-lab-canonical-images`](https://loadsmith-el.github.io/loadsmith-lab-canonical-images/).

Service images pin a specific `DATA_REF`, and the image CI publishes a derived
`:data-<ref>` tag — so an image's data revision is an explicit, independent
choice (decoupled from the service version). A drift between these three makes
that published tag lie.

## Cutting a new revision

This repo owns the dataset version. **Changing the schema is a breaking change
for every image.** If you add, remove, reorder, or retype a column:

1. Update `generate.py` and the schema table/SQL on the [Schema](./schema.md)
   page (and the repo `README.md`).
2. **Bump `VERSION`** (e.g. `v1` → `v2`), commit, then create the matching git
   **tag** (`v2`) on that commit — tag name == `VERSION` content.
3. Update every image's `init.sql` in
   [`loadsmith-lab-canonical-images`](https://loadsmith-el.github.io/loadsmith-lab-canonical-images/)
   to match, and bump that image's Dockerfile `ARG DATA_REF` to the new tag.

Skipping steps 2/3 leaves images pinned to the old schema silently working
against new generator output (or vice versa) — always bump and re-pin together.
