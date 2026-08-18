# What to automate next (plain English for the team)

VarRank, Challenge 1, ClawBio + Nebius Hackathon Berlin, 18 August 2026.

This note answers the glossary questions and lays out a four-layer lookup agent. It is a design, not a finished skill. We have **not** built this loop yet. The 30/38 count and the gnomAD version 2 table are already done.

ClawBio is a research and educational tool. It is not a medical device and does not provide clinical diagnoses. Consult a healthcare professional before making any medical decisions.

---

## Glossary

### Abstention (in most cases)

**Abstention** means we **refuse a claim** the file cannot support, and we write that refusal down. It is the product of this challenge, not a gap in the work.

In most cases here, abstention is:

| We will not say | Why |
|---|---|
| Rare in the world | Family `AF` is how often the allele appears in these four people (example `AF=0.25` means two of eight copies). That is not gnomAD. Missing from a catalogue is also not rarity. |
| Pathogenic or diagnostic | The `EFF` column is old SnpEff text, not a current clinical classification. There is no phenotype and no HPO list. |
| De novo (new in the child) | A parent carries the same allele at every one of the 68 sites. |
| Compound heterozygous | The parent-of-origin tags are unphased teaching labels, not molecular phase. |
| Autosomal dominant or recessive of a disease | There is no disease described. Thirty sites are labelled from the father, thirty eight from the mother. |
| A clinical diagnosis | Same reasons as above. |

The hosted BioNeMo agent wrote a generic abstention that was wrong in places (it claimed missing parental genotypes). **Do not use that text.** We have genotypes for son, father, mother, and sister in every row.

### The BDKRB1 site

One of the **two sites gnomAD version 2 did not return**.

- Place: chromosome 14, position 96730313, G to A, GRCh37
- No rs number in the family table (`id` is `.`)
- Gene: **BDKRB1** (bradykinin receptor B1)
- Effect in the teaching column: stop-gain, protein change W98* (tryptophan 98 becomes a stop)
- Label: maternal (son and mother carry it; father does not)
- Our gnomAD v2 query as `14-96730313-G-A` came back empty

Empty here means **this query missed it**, not that the variant is rare. Ensembl VEP still calls it a stop-gain. Lift to GRCh38 is `14:96263976`. Follow-up catalogues (other gnomAD releases, dbSNP by position, ClinVar `BDKRB1 W98*`) are the next job. A COSMIC / somatic hit must be tagged somatic and must not be copied into a germline frequency cell.

### Indel

An **indel** is an insertion or a deletion: the sequence length changes. It is not a single-letter swap (those are SNVs).

The other gnomAD miss is an indel:

- Family table: chromosome 21, position 11029596, `AC` to `A` (one C deleted), id `rs138714104`
- Genes: BAGE family
- Label: maternal

Indels are often **left-shifted**: two files can write the same DNA change at neighbouring positions with different allele strings. Ensembl GRCh37 maps this to **`rs60459764`** at **21:11029597–11029598**, alleles CC to C, with 1000 Genomes evidence. Synonyms include `rs796536508`, `rs376100218`, `rs144469422`.

That is why a lookup as `21-11029596-AC-A` can miss a variant that exists under another spelling. The agent must normalise alleles, then retry.

### Existing rs (rsID)

An **rs number** (`rs` + digits) is the public name of a variant in dbSNP, for example `rs138714104`. “Existing rs” means Ensembl or VEP already knows a catalogue id for that change.

- If an rs exists, federated tools such as ClawBio `gwas-lookup` can take it as `--rsid`.
- If there is **no** rs (BDKRB1 in this pack), those tools cannot be pointed at the site. Use gene + protein HGVS instead (`BDKRB1` and `p.Trp98Ter` / W98*).

An rs on the family row can still be the **wrong spelling** of an indel. Then the existing rs is a clue, not the final query. That is the `rs138714104` → `rs60459764` case.

---

## Did BioNeMo run the ClawBio skills?

**No.** You did not need OpenClaw from a terminal either.

| Path | What happened |
|---|---|
| Hosted BioNeMo Research Agent (Nebius template **Deploy BioNeMo Agent**, endpoint `yellow-boa-endpoint-9`) | Counted the table after `curl` to disk. Pasting the whole TSV into chat crashed it. `clawbio__run_skill` for `rare-high-impact-variants` failed: **`demo is not qualified in this image`**. First abstention text was factually wrong. |
| OpenClaw CLI on this laptop | Not required for what we shipped. The hosted BioNeMo agent **is** the OpenClaw-on-Nebius path. |
| Local ClawBio Python on this laptop | This is the official fallback. Four skills ran with `--demo` on **bundled toy data**, not on the 68-row family table: `rare-high-impact-variants`, `vcf-annotator`, `clinical-variant-reporter`, `cnv-acmg-classifier`. |
| One-off scripts in this folder | Parent-of-origin count and gnomAD v2 lookup. These are not ClawBio skills. |

To run a skill yourself, from a ClawBio clone:

```powershell
python skills\rare-high-impact-variants\rare_high_impact_variants.py --demo --output output\track1-demo\rhiv
```

Do **not** feed the family TSV to `rare-high-impact-variants` (it does not parse `EFF`). Do **not** run `vcf-annotator` on this GRCh37 pack with GRCh38 defaults.

Federated skills we designed for the two misses (`gwas-lookup` on `rs60459764`, PubMed / omics mapper on BDKRB1) were **not** completed: this Python install was missing `opentelemetry` when we tried.

After the talk, stop the Nebius endpoint so it stops billing.

---

## The idea: a state machine, not a chat dump

Do not paste the 68-row table into a model. For each variant, keep a small record:

- query tried
- outcome (`found` / `not_found` / `ambiguous` / `error`)
- failure class (`missing_in_build`, `indel_shift`, `no_rsid`, `rate_limit`)
- next tool
- evidence copied from API JSON only
- stop rule

The model only **chooses the next tool** and **writes the abstention**. Allele frequencies, ClinVar labels, and gene names stay in tool output. If a tool returns empty, the cell is `not_found`. **Never treat `not_found` as rare.**

---

## Layer 1 — identity (every site, cheap, no phenotype needed)

Already started. Automate fully.

- Count `PARENT_OF_ORIGIN_UNPHASED` (30 paternal, 38 maternal)
- gnomAD by `chrom-pos-ref-alt` on the **same build** as the file (here: version 2.1, GRCh37, prefer exome)
- Ensembl VEP / overlap: gene, consequence, existing rs list
- dbSNP by rs, then by position if rs is missing
- LiftOver when the catalogue is GRCh38 and the pack is GRCh37
- Left-normalise indels (BAGE case)
- myvariant.info as a merge of dbSNP, ClinVar, CADD, COSMIC — with **source tags**

Output: one row per site, separate columns for family `AF` and world AF. Do not mix them.

## Layer 2 — only misses, or AF under a stated threshold

Do **not** run this on the 52 sites that are already common in gnomAD (≥ 1%). That dump is how teams waste the hour.

- Other gnomAD releases (r3, r4) after lift
- ExAC if r2 is empty
- 1000 Genomes / TOPMed for stubborn indels
- ClinVar by rs **and** by gene + protein HGVS when there is no rs
- Skip HGMD unless we have a licence

Failure classes we already hit:

1. **SNV, no rs** (BDKRB1) → VEP → lift → other gnomAD → ClinVar gene+HGVS → myvariant. Tag COSMIC as somatic.
2. **Indel / nearby rs** (`rs138714104`) → left-normalise → Ensembl synonyms → retry gnomAD as `rs60459764` or `21-11029597-CC-C`.
3. **HTTP / timeout** → retry with backoff, then record `error`, still not rare.

If every catalogue in the class is empty, write `follow_up`: catalogues tried, none hit, **not rare-by-missingness**.

## Layer 3 — gene evidence on a shortlist only

Use this on the **open set**: the two misses, plus the sites with world AF under 0.01 (about ten rows). Still not a diagnosis.

| Search | ClawBio skill | When to fire |
|---|---|---|
| Federated rs lookup (GWAS Catalog, Open Targets, PheWAS, GTEx, eQTL) | `gwas-lookup` | Stable rs exists |
| Region GWAS betas | `gwas-catalog-region-fetch` | Window around a rare site, GRCh38 |
| Gene–disease evidence, UniProt, Open Targets, papers | `omics-target-evidence-mapper` | Shortlisted gene symbol |
| Recent papers | `pubmed-summariser` | Same shortlist; prefer `GENE AND (loss of function OR stop gained)` or the rs, not the gene alone |
| Trials | `clinical-trial-finder` | Only if a phenotype or named condition exists |
| Gene / transcript confirm | `ncbi-datasets` | Confirm symbol |
| Pharmacogenomics | `clinpgx` | Only known drug genes (CYP, VKORC1, …). Not BDKRB1 in this pack. |

## Layer 4 — extra searches that change a follow-up cell

1. Transcript and HGVS from VEP (`BDKRB1:p.Trp98Ter`) when there is no rs.
2. Canonical indel (`bcftools norm` / Ensembl mapped alleles), then retry frequency.
3. gnomAD gene constraint (pLI / loeuf) for the shortlist. Still not a diagnosis.
4. Population, not family: gnomAD popmax AF (AFR, SAS, EAS, …). Rare in one ancestry and common in another is a known trap.
5. Nearby ClinVar in the same codon. Record “different variant.” Never copy another variant’s star onto ours.
6. COSMIC vs germline: if only a somatic catalogue hits, do not fill `gnomad_af`.
7. PubMed for the **exact** variant (`rs60459764` or `"BDKRB1" "W98*"`).

## What not to put on the queue (wrong default on this pack)

- `rare-high-impact-variants` on the family TSV
- `vcf-annotator` / GRCh38 VEP on this GRCh37 pack
- ACMG / `clinical-variant-reporter` without phenotype
- OpenFold / structure on a stop-gain or a common HIGH site
- EGFR or other BioNeMo NVIDIA demos
- Expression / eQTL with no trait
- CNV skills on these 68 SNVs/indels

The orchestrator’s job is to **refuse** those, the same way the Slack demo bullet refused them.

---

## Suggested wiring

Give the agent tools, not web paste:

1. `lookup_frequency(chrom, pos, ref, alt, build)` → gnomAD JSON or `not_found`
2. `resolve_variant(...)` → VEP, rs list, synonyms, lifted coords
3. `lookup_clinvar(rsid or gene_hgvs)` → significance + review status or empty
4. `lookup_gene_evidence(symbol)` → Open Targets + UniProt
5. `search_pubmed(query)` → PMIDs only
6. `write_follow_up(row_id, tried, result)` → the spreadsheet column

Prompt rule: **every number in a report must appear in a tool result.**

Batch layer 1 in Python (we already did 68 gnomAD lookups). Use an LLM only on the **open set** (2 misses, maybe ~10 rare-in-world sites). That is cheap and will not crash a hosted chat.

Smallest shippable version: input the 68-row TSV, output `challenge1-results-export.tsv` plus `open_questions.json`, and call `gwas-lookup` / VEP / ClinVar only for `not_found` and `af < 0.01`.

---

## What “done” looks like for BDKRB1

1. gnomAD r2 `14-96730313-G-A` → not found
2. VEP → BDKRB1 stop-gain W98*, no rs
3. lift → `14-96263976-G-A`
4. gnomAD r4 on the lifted id → found or still missing
5. ClinVar gene+HGVS → record the hit count (including zero)
6. myvariant → if COSMIC only, tag somatic, do not fill AF
7. `follow_up`: not in gnomAD r2 as queried; stop-gain confirmed by VEP; germline catalogues empty or filled; **not rare-by-missingness**

That last sentence is the agent’s product. A ranked gene list without it is the failure this challenge is about.

---

## Files already in this repo

| File | What it is |
|---|---|
| `CHALLENGE1-REPORT.md` | Full write-up of what we actually ran |
| `challenge1-results-export.tsv` | 68 rows, gnomAD column, follow-up on the two misses |
| `GNOMAD-LAYER-NOTE.md` | World frequency vs family `AF` |
| `rhiv/report.md` | Local toy demo: missing frequency is not rarity |
| `DEMO-SCRIPT-PLAIN-ENGLISH.md` | Spoken two-minute script |

Source data: Corpasome, DOI 10.6084/m9.figshare.693052.v3, Creative Commons Attribution 4.0.
