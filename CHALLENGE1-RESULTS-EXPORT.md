# Challenge 1 results export

Berlin hackathon, 18 August 2026. Corpas family teaching pack, GRCh37.

## Spreadsheet

Open this file in Excel or Google Sheets:

`output/track1-demo/challenge1-results-export.tsv`

68 variant rows. Columns:

- chrom, pos, id, ref, alt, genes
- parent_of_origin_unphased (30 paternal, 38 maternal)
- son, father, mother, sister genotypes (allele calls only)
- gnomad_v2_variant_id, gnomad_v2_rsid, gnomad_v2_af, gnomad_v2_source
- world_freq_bin
- follow_up (filled only for the two sites this gnomAD version 2 query missed)

Do not treat `gnomad_v2_af` as the family VCF `AF`. Family `AF` is how often the allele appears in these four people.

## Counts

| Item | Number |
|---|---|
| Variant rows | 68 |
| Labelled from the father | 30 |
| Labelled from the mother | 38 |
| Found in gnomAD version 2, GRCh37 exome | 66 |
| World frequency at least 1 percent | 52 |
| World frequency under 1 percent | 14 (10 of those under 0.01 percent) |
| Not found in this gnomAD version 2 query | 2 |

## The two sites that need another catalogue

**14:96730313 G to A**, no rs number, gene BDKRB1, stop-gain, maternal label.  
Not in gnomAD version 2 as `14-96730313-G-A`. Next: gnomAD and dbSNP by gene and position, Ensembl GRCh37, ClinVar for BDKRB1. Missing here is not rarity.

**21:11029596 AC to A**, `rs138714104`, BAGE genes, maternal label.  
Indel shifting. Ensembl GRCh37 maps this to **`rs60459764`** at **21:11029597–11029598**, alleles CC to C, with 1000 Genomes frequency evidence. Synonyms: rs796536508, rs376100218, rs144469422. Next: gnomAD as `rs60459764` or `21-11029597-CC-C`, dbSNP, 1000 Genomes.

## Other files in this folder

| File | What it is |
|---|---|
| `CHALLENGE1-REPORT.md` | Full write-up |
| `challenge1-b37-segregation.tsv` | Official family table |
| `challenge1-gnomad-v2-grch37.tsv` | Raw gnomAD lookup including genotypes |
| `challenge1-results-export.tsv` | Clean export for the team |
| `rhiv/report.md` | Local toy demo: missing frequency is not rarity |
| `DEMO-SCRIPT-PLAIN-ENGLISH.md` | Spoken demo script |

Source data: Corpasome, DOI 10.6084/m9.figshare.693052.v3, Creative Commons Attribution 4.0.
