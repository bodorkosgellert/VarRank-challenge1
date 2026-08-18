# gnomAD version 2 layer (GRCh37)

This is a **second** evidence layer. It is not the family file's own `AF` field.

- Catalogue: gnomAD version 2.1, exome, same build as the pack (GRCh37)
- Method: each site looked up as chromosome-position-reference-alternate
- Table: `challenge1-gnomad-v2-grch37.tsv`
- Do not mix `gnomad_v2_af` with VCF `AF=0.25`. That 0.25 is two of eight copies in this family of four people.

## Counts

- 68 family sites
- 66 found in gnomAD version 2
- 2 not found (lookup failed): 14:96730313 and 21:11029596 (rs138714104)
- 52 of 66 have world frequency at least 1 percent (not rare by a 1 percent rule)
- 14 of 66 have world frequency under 1 percent
- 12 of 66 under 0.1 percent
- 10 of 66 under 0.01 percent

## What this means for the demo

Most of these sixty eight "high impact" teaching sites are **common in the world**. A pipeline that treated family `AF` or missing gnomAD as rarity would be wrong. A few sites are actually uncommon in gnomAD. We still do not call them diagnostic: there is still no phenotype.

Lowest world frequencies (examples): 7:44610376, 19:23844937, 6:132203615, 4:165878621.
