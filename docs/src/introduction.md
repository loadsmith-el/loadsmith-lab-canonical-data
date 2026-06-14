# Introduction

This repository is the **canonical seed dataset** for
[loadsmith-lab](https://loadsmith-el.github.io/loadsmith-lab/): **100,000 rows of
synthetic spacecraft telemetry**, 34 columns covering every Arrow-representable
type, generated deterministically with `seed = 42`.

It holds only the **generator** — never a committed CSV. Because `generate.py` is
stdlib-only and fully deterministic, the CSV is a pure function of this source:
every run reproduces it byte-for-byte, so there's nothing to store. Service
images in
[`loadsmith-lab-canonical-images`](https://loadsmith-el.github.io/loadsmith-lab-canonical-images/)
clone this repo at **build time**, run `generate.py`, and bake the resulting CSV
into the image.

## Two roles, one source of truth

This repo is authoritative for two things, and both must stay in lockstep with
every consumer:

- **The dataset** — the generator and its output (see [Generating](./generating.md)).
- **The schema** — the 34 columns, their order, types, and null rates (see
  [Schema](./schema.md)). Every image's `init.sql` must recreate exactly this
  schema.

Changing the schema is a **breaking change for every image** — it always comes
with a version bump. See [Versioning](./versioning.md).

## Where to go next

- [Generating](./generating.md) — running the generator.
- [Versioning](./versioning.md) — the `VERSION` file, the three places that must
  agree, and the bump procedure.
- [Schema](./schema.md) — the canonical 34-column schema, column by column.
- [Data Pools](./data-pools.md) — the value pools the generator draws from.
