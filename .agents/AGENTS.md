# AI Agent Guidelines — loadsmith-lab-canonical-data

> Source of truth for this repository, for any AI agent (Claude, Codex, Gemini,
> …). The root `CLAUDE.md` is only a pointer to this folder.

## Golden Rule (the `.agents/` folder prevails)

The `.agents/` folder is the source of truth. If existing code conflicts with
what is documented here, the documented standard prevails — surface the conflict
to the user before diverging.

## Authoring rule — how to extend this (all agents MUST follow)

This `.agents/` folder is the **single source of truth for every AI agent**
(Claude, Codex, Gemini, …) — not a reference copy. When you add or change agent
guidance, you MUST keep that truth here:

- **A new directive / convention / rule** → add it to **this file**
  (`.agents/AGENTS.md`). Do **not** put it in `CLAUDE.md` or any other per-agent
  file — those are pointers, not content.
- **A new skill / command** → write the real, agent-agnostic logic in
  **`.agents/skills/<name>.md`**. Then wire each agent's native entry point as a
  **thin stub** that only redirects here:
  - Claude: `.claude/commands/<name>.md` — keep its frontmatter (`description`,
    `argument-hint`, `allowed-tools`) so the slash command registers, then a body
    that says "read and follow `.agents/skills/<name>.md`".
  - Other agents: their own command/skill mechanism, with the same redirect.
- **Never** duplicate real instructions or skill logic into `CLAUDE.md` or into a
  stub. If a per-agent file ever starts holding real content, move it here and
  leave a pointer behind.
- Committed files stay in **English** (repo rule), even when chatting in another
  language.

These are **operating instructions only** — for what this repo is and the schema
it defines, read [README.md](../README.md), or `generate.py` itself. Don't guess
at "why" — go read it.

## Conventions

- **English only.** All artifacts committed to this repo — `generate.py`,
  README, commit messages, identifiers — must be in English, even when the
  user writes in Portuguese.
- **Stdlib only, no dependencies.** `generate.py` must run with a bare
  `python3` — no `pip install`, no `requirements.txt`. This is what lets
  service images in [`loadsmith-lab-canonical-images`](../../loadsmith-lab-canonical-images) generate
  the dataset in a minimal `python:3-slim` build stage.
- **Deterministic, always.** The generator is seeded (`seed = 42`). Any change
  must preserve byte-for-byte reproducibility for a given seed — the whole
  point is that the CSV is never committed because it's a pure function of
  this source.

## Hard rules — read before changing the schema

- **This repo is the schema source of truth.** The 34 columns, their order,
  types, and null rates in [README.md](../README.md) are canonical. Every
  consumer — every image's `init.sql` in `loadsmith-lab-canonical-images` — must match
  exactly (column order = CSV column order; empty string = NULL).
- **This repo owns the dataset version.** The [`VERSION`](../VERSION) file holds
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
  3. Update every image's `init.sql` in `loadsmith-lab-canonical-images` to match, and
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
[`loadsmith-lab-canonical-images/.agents/AGENTS.md`](../../loadsmith-lab-canonical-images/.agents/AGENTS.md).
