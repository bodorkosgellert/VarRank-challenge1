# VarRank — Challenge 1: End the diagnostic odyssey

ClawBio + Nebius Hackathon Berlin, 18 August 2026.

Public teaching pack from the Corpas family genome (Corpasome, [DOI 10.6084/m9.figshare.693052.v3](https://doi.org/10.6084/m9.figshare.693052.v3), CC BY 4.0). Four people: son, father, mother, sister. Genome build GRCh37. This is research teaching data, not a clinical diagnosis.

## Slack demo form (one message, five bullets)

Copy this into `#berlin-demos`:

- **team name:** VarRank
- **challenge:** Challenge 1, End the diagnostic odyssey
- **repo:** this repository
- **what it does:** Counts 30 paternal and 38 maternal labels on the 68-row Corpas GRCh37 table and adds a gnomAD v2 world-frequency layer, showing most HIGH teaching sites are common in the population.
- **what it refused:** Refused to call variants rare from family `AF`, refused a diagnosis without phenotype, refused de novo / compound-het from unphased teaching labels, and refused to run the GRCh38 VCF annotator on this GRCh37 pack.

## Start here

- [CHALLENGE1-REPORT.md](CHALLENGE1-REPORT.md) — full narrative
- [CHALLENGE1-RESULTS-EXPORT.md](CHALLENGE1-RESULTS-EXPORT.md) — spreadsheet notes
- [challenge1-results-export.tsv](challenge1-results-export.tsv) — one row per variant
- [DEMO-SCRIPT-PLAIN-ENGLISH.md](DEMO-SCRIPT-PLAIN-ENGLISH.md) — spoken two-minute script

## What we counted

| Label | Count |
|---|---|
| Paternal (from the father) | 30 |
| Maternal (from the mother) | 38 |
| Total variant rows | 68 |

Official table: https://docs.clawbio.ai/hackathon/berlin/data/challenge1-b37-segregation.tsv

## What we refused

- Rare from family `AF` (that field is frequency inside these four people, not gnomAD)
- Pathogenic / diagnostic from historical `EFF` with no phenotype / HPO
- De novo (a parent carries every site)
- Compound het from unphased teaching tags
- Autosomal dominant / recessive of a disease
- A clinical diagnosis
- Running `vcf-annotator` on this GRCh37 pack with GRCh38 defaults

## gnomAD v2 (GRCh37) layer

66 of 68 sites found. 52 of 66 have AF ≥ 1%. Most HIGH teaching sites are common in the world. Two sites still need follow-up (BDKRB1 stop-gain with no gnomAD hit; BAGE indel with rs ID shift). See [GNOMAD-LAYER-NOTE.md](GNOMAD-LAYER-NOTE.md).

Local ClawBio `--demo` skill outputs (`rhiv/`, `acmg/`, `cnv/`, `vcfann/`) are method checks on bundled toy data, not calls on the family table.
