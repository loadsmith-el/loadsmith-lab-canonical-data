# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository. It is **operating instructions only** — for what this
repo is and the schema it defines, read [README.md](README.md), or
`generate.py` itself. Don't guess at "why" — go read it.

## Conventions

- **English only.** All artifacts committed to this repo — `generate.py`,
  README, commit messages, identifiers — must be in English, even when the
  user writes in Portuguese.
- **Stdlib only, no dependencies.** `generate.py` must run with a bare
  `python3` — no `pip install`, no `requirements.txt`. This is what lets
  service images in [`loadsmith-lab-images`](../loadsmith-lab-images) generate
  the dataset in a minimal `python:3-slim` build stage.
- **Deterministic, always.** The generator is seeded (`seed = 42`). Any change
  must preserve byte-for-byte reproducibility for a given seed — the whole
  point is that the CSV is never committed because it's a pure function of
  this source.

## Hard rules — read before changing the schema

- **This repo is the schema source of truth.** The 34 columns, their order,
  types, and null rates in [README.md](README.md) are canonical. Every
  consumer — every image's `init.sql` in `loadsmith-lab-images` — must match
  exactly (column order = CSV column order; empty string = NULL).
- **This repo owns the dataset version.** The [`VERSION`](VERSION) file holds
  the canonical revision string (e.g. `v1`). It is the single source of truth
  for "which dataset is this": the git tag, this `VERSION` file, and each
  consuming image's Dockerfile `ARG DATA_REF` must all be the same string. The
  image CI derives its published `:data-<ref>` tag from `DATA_REF`, so a drift
  here makes that tag lie.
- **Never commit the generated CSV.** It's gitignored
  (`spacecraft_telemetry_events.csv`) — service images clone this repo at
  build time and run `generate.py` themselves.
- **Changing the schema is a breaking change for every image.** If you add,
  remove, reorder, or retype a column:
  1. Update `generate.py` and the schema table/SQL in `README.md`.
  2. **Bump `VERSION`** (e.g. `v1` → `v2`), commit, then create the matching
     git tag (`v2`) on that commit — tag name == `VERSION` content.
  3. Update every image's `init.sql` in `loadsmith-lab-images` to match, and
     bump that image's Dockerfile `ARG DATA_REF` to the new tag.

  Skipping step 2/3 leaves images pinned to the old schema silently working
  against new generator output (or vice versa) — always bump and re-pin
  together.

## Verifying a change

```bash
python3 generate.py   # → spacecraft_telemetry_events.csv (gitignored)
md5sum spacecraft_telemetry_events.csv   # compare before/after a change to confirm determinism for unrelated edits
```

To verify an image still builds against this schema, see
[`loadsmith-lab-images/CLAUDE.md`](../loadsmith-lab-images/CLAUDE.md).
