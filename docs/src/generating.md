# Generating

```bash
python generate.py     # → spacecraft_telemetry_events.csv (next to the script)
```

No dependencies, no `pip install` — Python 3 standard library only. This is what
lets service images in
[`loadsmith-lab-canonical-images`](https://loadsmith-el.github.io/loadsmith-lab-canonical-images/)
generate the dataset in a minimal `python:3-slim` build stage.

## Determinism is a hard guarantee

The generator is seeded (`seed = 42`). Any change **must** preserve byte-for-byte
reproducibility for a given seed — the whole point is that the CSV is never
committed because it's a pure function of this source.

To confirm an unrelated edit didn't perturb the output:

```bash
python3 generate.py
md5sum spacecraft_telemetry_events.csv   # compare before/after the change
```

The generated CSV is gitignored (`spacecraft_telemetry_events.csv`) — **never
commit it**.

## Conventions

- **Stdlib only, no dependencies.** `generate.py` must run with a bare `python3`
  — no `pip install`, no `requirements.txt`.
- **English only** for all committed artifacts.
