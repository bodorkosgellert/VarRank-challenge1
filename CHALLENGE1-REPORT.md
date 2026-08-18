# Challenge 1 report: End the diagnostic odyssey

ClawBio and Nebius hackathon, Berlin, 18 August 2026.

Public teaching pack from the Corpas family genome (Corpasome, DOI 10.6084/m9.figshare.693052.v3, Creative Commons Attribution 4.0). Four people: son, father, mother, sister. Genome build GRCh37. This is research teaching data, not a clinical diagnosis.

## What we asked

Show which variants the son inherited from one parent, make every filter visible, then say what the file cannot support. There is no phenotype and no Human Phenotype Ontology list, so a defensible analysis must refuse to turn segregation into a diagnosis.

## Data

Official files:

- https://docs.clawbio.ai/hackathon/berlin/data/challenge1-b37-segregation.tsv
- matching compressed VCF and tabix index on the same page

The readable table has 69 lines (one header and 68 variant rows) and 11 columns: chromosome, position, identifier, reference, alternate, genotypes for son, father, sister, and mother, the unphased parent-of-origin teaching label, and the historical SnpEff effect string.

Each of the 68 rows is a high-impact annotated change that the son carries together with exactly one parent.

Local copies live under `output/track1-demo/`.

## Hour one: parent of origin

We counted the column `PARENT_OF_ORIGIN_UNPHASED`.

| Label | Count |
|---|---|
| Paternal (from the father) | 30 |
| Maternal (from the mother) | 38 |
| Total variant rows | 68 |

The same numbers were obtained twice:

1. On this laptop, from the downloaded table, with a Python `Counter`.
2. In the hosted BioNeMo Research Agent, after downloading the table to disk with `curl` and running the same count. Pasting the whole table into the chat crashed the agent. Counting on disk worked.

These labels are teaching tags. They are not molecular phase. They do not define a disease inheritance pattern. Thirty sites are labelled from the father. Thirty eight are labelled from the mother. Not every site came from the same parent.

We have genotypes for all four people in every row. The other parent is usually reference at that site. We do not lack parental genotypes.

## Family allele frequency is not world frequency

The compressed VCF contains an `AF` field. Teammates were right that variant files often carry a frequency. In this file that field is the frequency **inside this family of four**. Example from the first site: `AC=2;AF=0.25;AN=8` means two of eight gene copies in these four people. That is not gnomAD and must not be used to call a variant rare or common in the world.

## Extra layer: gnomAD version 2 on GRCh37

We did not run `vcf-annotator` on the family file. That skill expects GRCh38, can mis-annotate GRCh37 coordinates, drops family genotypes, and is forbidden on the full Corpas VCF. Instead we looked up each of the 68 sites in **gnomAD version 2.1, exome, GRCh37**, using chromosome-position-reference-alternate. That matches the pack build.

Result table: `output/track1-demo/challenge1-gnomad-v2-grch37.tsv`  
Script: `output/track1-demo/lookup_gnomad_v2.py`

| Outcome | Count |
|---|---|
| Family sites | 68 |
| Found in gnomAD version 2 | 66 |
| Not found | 2 (`14:96730313` and `21:11029596`) |
| World frequency at least 1 percent | 52 of 66 |
| World frequency under 1 percent | 14 of 66 |
| World frequency under 0.1 percent | 12 of 66 |
| World frequency under 0.01 percent | 10 of 66 |

Most of these “high impact” teaching sites are common in the world. A pipeline that treated family `AF`, or absence from a catalogue, as rarity would be wrong. A few sites are uncommon in gnomAD (examples: `7:44610376`, `19:23844937`, `6:132203615`, `4:165878621`). We still do not call those diagnostic: there is still no phenotype. The two sites not found in this lookup are also not proof of rarity.

Keep `gnomad_v2_af` as its own column. Do not mix it with the family VCF `AF`.

## Method check on bundled demo data (not the family)

The hosted BioNeMo image could not run `rare-high-impact-variants` (`demo is not qualified in this image`). We ran it locally:

```
python skills/rare-high-impact-variants/rare_high_impact_variants.py --demo --output output/track1-demo/rhiv
```

Toy genome, not the Corpas table. Threshold: population frequency below 0.01.

- 3 high-impact variants with a documented low frequency (GENE1, GENE7, GENE5)
- 1 high-impact variant that is common
- 1 high-impact variant with **no** frequency (GENE2), reported separately and **not** called rare

That is the method the brief asked for: absence of a frequency is not evidence of rarity.

We also ran, on bundled demo inputs only, `vcf-annotator`, `clinical-variant-reporter`, and `cnv-acmg-classifier`. Those reports are under `output/track1-demo/vcfann`, `acmg`, and `cnv`. They show how ClinVar and gnomAD look when the skill is qualified. They are not a ranking of the 68 family sites.

## What we will not claim

1. **Rare in the population**, from the family file alone. Family `AF` is not world frequency. Two gnomAD misses are not rarity. Most of the 66 looked-up sites are common in gnomAD version 2.
2. **Pathogenic or diagnostic.** The effect string is historical SnpEff, not a current ACMG classification. There is no phenotype.
3. **De novo.** A parent carries the allele at every one of the 68 sites. This is a four-person family, not a missing-parent design.
4. **Compound heterozygous.** Parent-of-origin tags are unphased teaching labels.
5. **Autosomal dominant or recessive disease.** No affection status, no phenotype terms.
6. **A clinical diagnosis.**

## What we will claim

Sixty eight high-impact teaching records in a public four-person exome. Thirty labelled from the father, thirty eight from the mother. The same count on the laptop and in BioNeMo. A gnomAD version 2 layer on GRCh37 showing that most of these sites are common in the world. A local ClawBio demo that refuses to call a no-frequency variant rare. An explicit list of claims this pack cannot support.

## How we used the hosted agent

BioNeMo Research Agent on Nebius endpoint `yellow-boa-endpoint-9`. It listed tools, fetched the data page, crashed when the table was loaded into the chat, then succeeded when the table was counted on disk. It could not run the rare-high-impact demo. Its first abstention text wrongly said parental genotypes were missing. We corrected that. We did not use OpenFold or the EGFR drug demo for this challenge.

## Files

| File | Role |
|---|---|
| `challenge1-b37-segregation.tsv` | Official family table |
| `challenge1-gnomad-v2-grch37.tsv` | Family rows plus gnomAD version 2 frequencies |
| `rhiv/report.md` | Local rare-high-impact demo (toy data) |
| `GNOMAD-LAYER-NOTE.md` | Short gnomAD note |
| `DEMO-SCRIPT-PLAIN-ENGLISH.md` | Spoken two-minute script |
| `HOW-WE-GOT-THIS.md` | Early provenance of the first demo run |

## One line for the demo channel

Challenge 1: 30 paternal and 38 maternal labels on the 68-row Corpas table; gnomAD version 2 on GRCh37 shows most sites are common in the world; we refuse rarity from family AF and we refuse a diagnosis without phenotype.
