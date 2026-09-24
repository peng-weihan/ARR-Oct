# arr-Oct version control

This repository records the current ARR paper workspace, including LaTeX sources,
bibliography and figures, manuscript PDFs, the extracted benchmark dataset,
review notes, and analysis documentation.

The initial snapshot was created on 2026-09-24. It does not rewrite or merge the
previous Overleaf history. The original paper repository metadata is preserved
locally outside this repository at:

`../.git-backups/20260924-160531/arr-Oct/69c7ffb776a8821cc0f99c65/.git`

The original remote configuration is kept in that backup; this repository has no
remote configured. The backup is not included when cloning this repository.

Ignored files remain on disk:

- Dataset `.tar.gz` / `.tgz` bundles duplicate the extracted dataset.
- `tmp/` and `output/` contain temporary builds, rendered pages, and trial outputs.
- LaTeX intermediate files, logs, Python caches, local configuration, and secrets.

The largest retained file is `HEART-BENCH-dataset/data/characters.parquet`
(approximately 23.9 MiB). It is retained as benchmark data, rather than treated as
a disposable cache. PDFs used by the paper and `main.pdf` are retained.
The dataset's inherited Hugging Face LFS attributes have been replaced with
ordinary Git binary attributes for Parquet files; no Git LFS setup is required.

Some research utilities, including the evidence-review script, refer to sibling
directories in the larger `human-like` workspace; a clone of this repository
alone does not include those external experiment outputs.
