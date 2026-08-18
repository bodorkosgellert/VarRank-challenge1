# Track 1 local run — what we have, and what we did not use

**Short answer for the team:** these files come from a **local ClawBio Python skill** on **bundled demo data**. We have **not** used NVIDIA BioNeMo, the hosted OpenClaw / BioNeMo Research Agent, or Nebius GPUs.

Date: 18 August 2026 (Berlin hackathon, Challenge 1).
Machine: Windows, Cursor, clone at `C:\Users\galla\OneDrive\Documents\ClawBio`.

## Did we use BioNeMo?

**No.**

| Thing | Used? |
|---|---|
| ClawBio skill `rare-high-impact-variants` (local Python) | Yes |
| Bundled demo VCF-like input in the repo | Yes |
| Challenge 1 Corpas pedigree TSV (downloaded) | Downloaded, **not** fed into this skill yet |
| Nebius Token Factory (LLM) | Key is saved; **this report did not need it** |
| Hosted BioNeMo Research Agent / OpenClaw on Nebius | **No** |
| Deploy BioNeMo Agent (Serverless GPU) | **No** |
| Tavily | **No** (separate web-search credits) |

BioNeMo is the **hosted** agent UI on Nebius (template **Deploy BioNeMo Agent**). Promo codes failed, so we ran the official **local** fallback from the challenge brief instead.

## Command that produced the files

```powershell
cd C:\Users\galla\OneDrive\Documents\ClawBio
python skills\rare-high-impact-variants\rare_high_impact_variants.py --demo --output output\track1-demo\rhiv
```

That is the same command as in the challenge docs (`--demo`). No API call. No GPU.

We also downloaded:

`https://docs.clawbio.ai/hackathon/berlin/data/challenge1-b37-segregation.tsv`

to `output\track1-demo\challenge1-b37-segregation.tsv` for the 30 paternal / 38 maternal split. That file is **not** the input to `report.md` / `result.json`.

## What is in `report.md`

Human-readable summary. Path:

`output\track1-demo\rhiv\report.md`

It says:

- Input was **`skills/rare-high-impact-variants/demo_input.txt`** (toy teaching genome, not the Corpas family VCF)
- Rarity threshold: population AF **< 0.01**
- 6 carried annotated variants, 5 high-impact (LoF)
- **3 rare** with a documented frequency below 0.01
- **1 common**
- **1 with no population frequency** — **not called rare** (this is the track 1 point: absence of AF is not evidence of rarity)

The 3 listed “rare” rows are fake teaching genes: **GENE1, GENE7, GENE5**.

## What is in `result.json`

Machine-readable copy of the same run. Path:

`output\track1-demo\rhiv\result.json`

Useful fields:

- `rare_high_impact_count`: 3
- `high_impact_common`: 1
- `high_impact_frequency_unknown`: 1
- `frequency_unknown_genes`: `["GENE2"]` — the variant we must **not** call rare
- `findings`: the 3 documented-rare variants with AF and ClinVar

Share **both** files: `report.md` for slides, `result.json` for the numbers.

## How this maps to Challenge 1

Hour-one win in the brief: show documented-rare vs **no-frequency**, then abstain on diagnosis because there is no phenotype.

This run covers **step 2** of the paste-prompt (skill demo on bundled data). It does **not** yet:

- count 30 paternal / 38 maternal on the real TSV
- rank the Corpas quartet
- use BioNeMo / a Token Factory model to chain skills

Next local commands from the brief (still not BioNeMo):

```powershell
python skills\vcf-annotator\vcf_annotator.py --demo --output output\track1-demo\vcfann
python skills\clinical-variant-reporter\clinical_variant_reporter.py --demo --output output\track1-demo\acmg
python skills\cnv-acmg-classifier\cnv_acmg_classifier.py --demo --output output\track1-demo\cnv
```

Do **not** feed the full Corpas VCF into `vcf-annotator` (serial network calls, GRCh38). Do **not** feed the historical quartet into `rare-high-impact-variants` (it does not parse legacy `EFF`).

## If someone asks “so we used an AI?”

For **these two files**: no. A Python script counted rows in demo input.

An LLM (Token Factory, or BioNeMo if we get the hosted endpoint) is only needed when we want a model to **choose** skills and write the abstention narrative. The science in `report.md` is already the demo slide: **GENE2 has no AF, so we refuse to call it rare.**
