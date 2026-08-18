# Challenge 1 — what we present (freeze 16:10)

## One line for #berlin-demos

Challenge 1: reproduced 30 paternal / 38 maternal on the Corpas 68-row TSV and an explicit abstention list (no rare / no diagnosis / no de novo). BioNeMo counted the TSV; ClawBio `--demo` in Cursor showed the no-AF blind spot.

## What we measured

- File: official `challenge1-b37-segregation.tsv` (11 columns, 1 header + 68 rows)
- Count `PARENT_OF_ORIGIN_UNPHASED` → **30 paternal, 38 maternal**
- Same numbers in Cursor and in BioNeMo (`curl` to disk + Python `Counter`)
- Attribution: Corpasome, DOI 10.6084/m9.figshare.693052.v3, CC BY 4.0

## Method check (not the family VCF)

Local: `python skills/rare-high-impact-variants/rare_high_impact_variants.py --demo`  
→ 3 documented-rare; **GENE2 has no AF → not called rare**  
BioNeMo could not run that skill in the hosted image.

## Abstention list (use this, not BioNeMo’s generic text)

1. Not **rare** — no valid population AF in this pack.
2. Not **pathogenic / diagnostic** — historical `EFF` only; no phenotype / HPO.
3. Not **de novo** — son + exactly one parent at every site.
4. Not **compound het / not molecular phase** — unphased teaching labels.
5. Not a **clinical diagnosis or AD/AR call**.

Do not say: “no parental genotypes” (we have them) or “synthetic data” (it is public Corpas).

## Do not demo

OpenFold, EGFR, BioNeMo NVIDIA models, dumping the TSV, a diagnosis.
