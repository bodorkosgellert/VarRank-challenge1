# Rare High-Impact Variants Report

**Input**: C:\Users\galla\OneDrive\Documents\ClawBio\skills\rare-high-impact-variants\demo_input.txt
**Rarity threshold**: population AF < 0.01

## 3 rare high-impact variants carried

Of 6 carried, annotated variants, 5 are high-impact (loss-of-function). Of those:

- **3 rare** with documented population frequency below 0.01 (ultra-rare AF < 0.001: 1; rare: 2)
- 1 common (documented AF at or above the threshold)
- 1 with no population-frequency data, so they cannot be confirmed rare (absence of a frequency is not evidence of rarity; many are common LoF polymorphisms)

## Variants

| Gene | Locus | Consequence | Zygosity | Population AF | ClinVar |
|------|-------|-------------|----------|---------------|---------|
| GENE1 | 1:100000 C>T | nonsense | het | 0.0002 | Pathogenic |
| GENE7 | 7:700000 C>T | splice_acceptor | het | 0.002 | - |
| GENE5 | 5:500000 C>G | nonsense | het | 0.004 | - |

## Scope

Counts high-impact (loss-of-function) variants annotated with molecular consequence and population frequency in the input VCF. 'Rare' requires a documented frequency below the threshold; variants with no frequency are reported separately and not called rare. Genome-wide novel LoF calling (VEP / SnpEff / bcftools csq) and a complete frequency reference (gnomAD) are out of scope for v0.1.0.

*ClawBio is a research and educational tool. It is not a medical device and does not provide clinical diagnoses. Consult a healthcare professional before making any medical decisions.*
