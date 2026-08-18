# Catalogue-miss agent: design, code, and tests

VarRank, Challenge 1, ClawBio + Nebius Hackathon Berlin, 18 August 2026.

A lookup agent that classifies *why* a database miss happened, picks the next catalogue, and **never treats a miss as rarity**. Layer 1 (68-site gnomAD v2 on GRCh37, 30/38 parent labels) is done. The router below is implemented and tested. The HTTP tools around it are not fully wired.

ClawBio is a research and educational tool. It is not a medical device and does not provide clinical diagnoses. Consult a healthcare professional before making any medical decisions.

Runnable core:

```text
python -m unittest agent_design.tests.test_router -v
```

---

## Layer 1 — identity (every site, cheap, no phenotype)

- Count `PARENT_OF_ORIGIN_UNPHASED` (30 paternal, 38 maternal)
- gnomAD `chrom-pos-ref-alt` on the **same build** as the file (v2.1, GRCh37, prefer exome)
- Ensembl VEP: gene, consequence, rs list
- dbSNP by rs, then by position
- LiftOver when the catalogue is GRCh38
- Left-normalise indels
- myvariant.info with **source tags** (germline vs COSMIC)

Output: one row per site. Family `AF` and world AF stay in separate columns.

## Layer 2 — only misses, or AF under a stated threshold

Do not run this on the 52 sites already ≥ 1% in gnomAD.

- Other gnomAD releases after lift; ExAC; 1000 Genomes / TOPMed for stubborn indels
- ClinVar by rs **or** gene + protein HGVS if there is no rs

Failure classes from this pack:

| Class | Example | Next tools |
|---|---|---|
| SNV, no rs | BDKRB1 `14:96730313 G>A` | VEP, lift, other gnomAD, ClinVar gene+HGVS |
| Indel shift | `rs138714104` → `rs60459764` | left-normalise, Ensembl synonyms, retry gnomAD |
| HTTP / timeout | any | backoff retry; still `unknown`, not rare |

## Layer 3 — gene evidence on a shortlist only

Open set: the two misses plus world AF < 0.01 (~10 rows). Still not a diagnosis.

`gwas-lookup` only if a **stable rs** exists. PubMed / Open Targets / trials only on that shortlist. `clinpgx` only for known pharmacogenes (not BDKRB1).

## Layer 4 — follow-up cells

HGVS from VEP, popmax AF, nearby ClinVar in the same codon (record “different variant”), COSMIC tagged somatic, PubMed for the **exact** allele not the gene alone.

**Do not queue:** `rare-high-impact-variants` on this TSV; GRCh38 VEP on GRCh37; ACMG without phenotype; OpenFold; CNV skills on these SNVs.

---

## How this differs from a standard lab pipeline

A typical clinical or research WES pipeline is **linear and complete**:

1. Align and call variants  
2. Annotate **every** variant with VEP or SnpEff  
3. Join gnomAD, ClinVar, often CADD, for the whole callset  
4. Filter by quality, consequence, AF, gene panel  
5. A human analyst reviews the remainder against **phenotype / HPO**

Those systems (seqr, InterVar, many hospital LIMS wrappers) are built for a **diagnosed-or-undiagnosed patient with a clinical question**. They apply the same tools to thousands of variants and rely on a person at the end.

This agent is different in four ways:

1. **Gated, not linear.** Common catalogue hits stop. We do not dump 52 common HIGH sites into PubMed.
2. **Failure-class routing.** A miss is classified (`no_rsid` vs `indel_shift` vs `error`) before the next API. Lab pipelines often leave “not in gnomAD” as an empty cell.
3. **Abstention is an output.** The product includes claims the file cannot support. Challenge 1 scores that. A lab report also has limitations, but the pipeline software rarely writes them as first-class fields.
4. **The LLM is not the annotator.** Frequencies and ClinVar labels come from APIs. The model may choose a tool only after the router has constrained the set. Numbers in the report must appear in tool JSON.

What is *not* different: the catalogues (Ensembl, gnomAD, ClinVar) are the same public ones labs use. We are not inventing a new genetics database. We are automating **which query to try next** and **when to stop**, which is the part analysts do by hand when a site is missing or an indel is spelled two ways.

In real research this is the “variant reconciliation” problem: the same DNA change has multiple rs synonyms, builds (GRCh37 vs GRCh38), and left-aligned indels. Papers and GWAS Catalog rows fail to merge unless someone normalises alleles. The BAGE indel in this pack is a teaching example of that.

---

## Code and tests (portfolio core)

The router is ordinary Python. Tests lock the rules so a later LLM wrapper cannot call a miss rare.

```python
# agent_design/router.py (excerpt)
def rarity_call(outcome: LookupOutcome) -> RarityCall:
    if outcome.status in ("not_found", "error", "ambiguous"):
        return "unknown"          # never "rare"
    if outcome.af is None:
        return "unknown"
    if outcome.af >= 0.01:
        return "common"
    return "uncommon_in_catalogue"
```

| Test | Rule |
|---|---|
| `test_not_found_is_never_rare` | BDKRB1-style miss → `unknown` |
| `test_missing_af_on_found_row_is_unknown_not_rare` | same rule as the ClawBio GENE2 demo |
| `test_common_site_stops_and_skips_gene_evidence` | AF 0.14 → stop, no PubMed |
| `test_uncommon_site_opens_shortlist` | AF 4e-6 → ClinVar + gene evidence allowed |
| `test_bdkrb1_no_rs_routes_to_vep_lift_clinvar_hgvs` | no `gwas_lookup` without rs |
| `test_indel_miss_routes_to_normalise_and_synonyms` | BAGE path |
| `test_http_error_retries_and_stays_unknown` | error is not rarity |

Still to build (not in this repo yet): HTTP adapters with recorded fixtures (no live network in CI), left-normalise, lift, and a writer for `follow_up`. The tests above are the contract those adapters must obey.

Prompt rule if an LLM is added: **every number in `report.md` must appear in a tool result.**

---

## Generalising to other inquiries

The pack-specific bit is “68 HIGH sites, unphased parent tags, GRCh37, no HPO.” The reusable bit is:

**identity → classify miss → retry on the right spelling → evidence only on a shortlist → abstain.**

| Inquiry | Layer 1 identity | Miss class | Shortlist evidence | Abstain when |
|---|---|---|---|---|
| This challenge | chrom-pos-ref-alt + parent label | no rs / indel shift | ClinVar, optional papers | no phenotype |
| Rare-disease WES with HPO | VEP + gnomAD + panel genes | build mismatch, homopolymer indel | OMIM, ClinVar, phenotype match | candidate ≠ HPO |
| GWAS hit follow-up | rs → GWAS Catalog | merged/split rs | credible sets, eQTL | p-value from wrong build |
| Pharmacogene | star alleles, CPIC | hybrid CYP2D6 | `clinpgx` | no prescription context |
| Literature gap / NTD | gene symbol | outdated alias | PubMed, Open Targets | citing papers the API did not return |

Same tests still apply: `not_found` is not evidence; common hits do not get a literature dump; tools are chosen by failure class.

That is also how this connects to AI engineering: it is a **tool-using agent with a deterministic policy**, not a chatbot that pastes a TSV. Eval is the unit tests plus “did the follow_up column stay honest.”

---

## Commentary

### Result of `gwas-lookup` on `rs60459764`

This is the Ensembl synonym of the chromosome 21 indel miss. Full report: [`gwas-rs60459764/report.md`](gwas-rs60459764/report.md).

- Ensembl resolved it as an indel at GRCh38 `chr21:10482859`, alleles GG/G, splice-donor consequence in BAGE2, **MAF 0.32** (common).
- **0** GWAS associations, **0** PheWAS, **0** eQTLs.
- Several APIs returned HTTP errors (Open Targets 400, GWAS Catalog 404, FinnGen 404, eQTL Catalogue 500). Those are failed queries, not “the variant has no disease.”
- **GTEx was OK but empty:** the GTEx HTTP call succeeded (`OK`). The body had **no eQTL rows** for this variant. The pipe worked; there was nothing to list. That is different from a 404.

So: the indel is a **common** splice-region change in a duplicated BAGE region, once you use the canonical rs. It is not a genome-wide association hit in the sources that answered. It still is not a diagnosis.

**Query Ensembl** means: call Ensembl’s REST API (the public genome database behind the Ensembl browser). The variation endpoint maps an rs id to coordinates and alleles. The VEP endpoint predicts consequence. `gwas-lookup` does that first, then fans out to other APIs.

### Why PubMed, omics mapper, trials, and ClinPGx were not run

They need a **gene or disease question**, not a 68-row identity pass. We had no HPO. Running them on all HIGH genes would be the dump the router now forbids. `gwas-lookup` needs an rs; BDKRB1 has none. `clinpgx` is for pharmacogenes (CYP2D6, VKORC1, …), not BDKRB1. OpenTelemetry blocked ClawBio imports until late; once it was installed we ran `gwas-lookup` only, on the one rs that Layer 2 actually needed.

What we would **expect** if we ran them on the shortlist anyway (research triage, not a diagnosis):

| Skill | Likely output here |
|---|---|
| `pubmed-summariser --query BDKRB1` | Papers on the bradykinin B1 receptor (inflammation, pain). Unlikely a paper about this family’s teaching pack. |
| `omics-target-evidence-mapper --gene BDKRB1` | UniProt + Open Targets associations, no disease filter. A gene card, not a patient result. |
| `clinical-trial-finder --gene BDKRB1` | Trials mentioning the gene or a mapped disease, or few hits. Unusable as eligibility without a condition. |
| `clinpgx --gene BDKRB1` | Empty or irrelevant. Not a CPIC gene. |

Empty or off-topic output would still be correct. It would not fill the rarity cell.

### Files

| Path | What it is |
|---|---|
| `agent_design/router.py` | Deterministic next-tool policy |
| `agent_design/tests/test_router.py` | Seven tests for that policy |
| `gwas-rs60459764/report.md` | Live `gwas-lookup` on `rs60459764` |
| `challenge1-results-export.tsv` | 68 rows, gnomAD layer, follow-up on two misses |
| `CHALLENGE1-REPORT.md` | What we actually ran |

Source data: Corpasome, DOI 10.6084/m9.figshare.693052.v3, Creative Commons Attribution 4.0.
