# Clinical Variant Report — ACMG/AMP Classification

**Generated**: 2026-08-18 13:39:37 UTC
**Input**: C:\Users\galla\OneDrive\Documents\ClawBio\skills\clinical-variant-reporter\example_data\giab_acmg_panel.vcf
**Assembly**: GRCh38
**Total variants classified**: 20
**Mode**: Demo (pre-cached evidence)

## Classification Summary

| Classification | Count |
|----------------|-------|
| Pathogenic | 4 |
| Likely Pathogenic | 3 |
| Uncertain Significance | 4 |
| Likely Benign | 6 |
| Benign | 3 |

## Actionable Variants (Pathogenic / Likely Pathogenic)

### BRCA1 — BRCA1:p.Gln1756ProfsTer74 **[SF]**

- **Classification**: Pathogenic
- **Position**: chr17:43045684
- **rsID**: rs80357906
- **Transcript**: ENST00000357654.9
- **Consequence**: frameshift_variant
- **ClinVar**: Pathogenic (stars: 3)
- **gnomAD AF**: 2e-05
- **Evidence codes**: PM2(M), PVS1(V), PP5(S)

| Criterion | Triggered | Strength | Direction | Source |
|-----------|-----------|----------|-----------|--------|
| BA1 | No | stand_alone | benign | gnomAD AF=0.0000 |
| BS1 | No | strong | benign | gnomAD AF=0.0000 |
| PM2 | Yes | moderate | pathogenic | gnomAD AF=0.000020 |
| PVS1 | Yes | very_strong | pathogenic | consequence=frameshift_variant |
| PS1 | No | strong | pathogenic | ClinVar=Pathogenic, stars=3 |
| PM1 | No | moderate | pathogenic | impact=HIGH, consequence=frameshift_variant |
| PM4 | No | moderate | pathogenic | consequence=frameshift_variant |
| PP3 | No | supporting | pathogenic | CADD=35.0≥25.3 |
| PP5 | Yes | supporting | pathogenic | ClinVar=Pathogenic, stars=3 |
| BP4 | No | supporting | benign | No in silico data available |
| BP6 | No | supporting | benign | ClinVar=Pathogenic, stars=3 |
| BP7 | No | supporting | benign | consequence=frameshift_variant, SpliceAI=N/A |

### TP53 — TP53:p.Arg175His **[SF]**

- **Classification**: Pathogenic
- **Position**: chr17:7674220
- **rsID**: rs28934578
- **Transcript**: ENST00000269305.9
- **Consequence**: missense_variant
- **ClinVar**: Pathogenic (stars: 3)
- **gnomAD AF**: 8e-06
- **Evidence codes**: PM2(M), PS1(S), PM1(M), PP3(S), PP5(S)

| Criterion | Triggered | Strength | Direction | Source |
|-----------|-----------|----------|-----------|--------|
| BA1 | No | stand_alone | benign | gnomAD AF=0.0000 |
| BS1 | No | strong | benign | gnomAD AF=0.0000 |
| PM2 | Yes | moderate | pathogenic | gnomAD AF=0.000008 |
| PVS1 | No | very_strong | pathogenic | consequence=missense_variant |
| PS1 | Yes | strong | pathogenic | ClinVar=Pathogenic, stars=3 |
| PM1 | Yes | moderate | pathogenic | impact=HIGH, consequence=missense_variant |
| PM4 | No | moderate | pathogenic | consequence=missense_variant |
| PP3 | Yes | supporting | pathogenic | CADD=29.9≥25.3; SIFT=deleterious; PolyPhen=probably_damaging |
| PP5 | Yes | supporting | pathogenic | ClinVar=Pathogenic, stars=3 |
| BP4 | No | supporting | benign | No in silico data available |
| BP6 | No | supporting | benign | ClinVar=Pathogenic, stars=3 |
| BP7 | No | supporting | benign | consequence=missense_variant, SpliceAI=N/A |

### MSH2 — MSH2:c.942+3A>G **[SF]**

- **Classification**: Pathogenic
- **Position**: chr2:47429830
- **rsID**: rs267607899
- **Transcript**: ENST00000233146.7
- **Consequence**: splice_donor_variant
- **ClinVar**: Pathogenic (stars: 2)
- **gnomAD AF**: N/A
- **Evidence codes**: PM2(M), PVS1(V), PP5(S)

| Criterion | Triggered | Strength | Direction | Source |
|-----------|-----------|----------|-----------|--------|
| BA1 | No | stand_alone | benign | gnomAD AF=N/A |
| BS1 | No | strong | benign | gnomAD AF=N/A |
| PM2 | Yes | moderate | pathogenic | gnomAD AF=absent |
| PVS1 | Yes | very_strong | pathogenic | consequence=splice_donor_variant |
| PS1 | No | strong | pathogenic | ClinVar=Pathogenic, stars=2 |
| PM1 | No | moderate | pathogenic | impact=HIGH, consequence=splice_donor_variant |
| PM4 | No | moderate | pathogenic | consequence=splice_donor_variant |
| PP3 | No | supporting | pathogenic | CADD=33.0≥25.3 |
| PP5 | Yes | supporting | pathogenic | ClinVar=Pathogenic, stars=2 |
| BP4 | No | supporting | benign | No in silico data available |
| BP6 | No | supporting | benign | ClinVar=Pathogenic, stars=2 |
| BP7 | No | supporting | benign | consequence=splice_donor_variant, SpliceAI=0.85 |

### PTEN — PTEN:p.Arg130Ter **[SF]**

- **Classification**: Pathogenic
- **Position**: chr10:87933147
- **rsID**: rs121913296
- **Transcript**: ENST00000371953.8
- **Consequence**: stop_gained
- **ClinVar**: Pathogenic (stars: 3)
- **gnomAD AF**: N/A
- **Evidence codes**: PM2(M), PVS1(V), PP5(S)

| Criterion | Triggered | Strength | Direction | Source |
|-----------|-----------|----------|-----------|--------|
| BA1 | No | stand_alone | benign | gnomAD AF=N/A |
| BS1 | No | strong | benign | gnomAD AF=N/A |
| PM2 | Yes | moderate | pathogenic | gnomAD AF=absent |
| PVS1 | Yes | very_strong | pathogenic | consequence=stop_gained |
| PS1 | No | strong | pathogenic | ClinVar=Pathogenic, stars=3 |
| PM1 | No | moderate | pathogenic | impact=HIGH, consequence=stop_gained |
| PM4 | No | moderate | pathogenic | consequence=stop_gained |
| PP3 | No | supporting | pathogenic | CADD=40.0≥25.3 |
| PP5 | Yes | supporting | pathogenic | ClinVar=Pathogenic, stars=3 |
| BP4 | No | supporting | benign | No in silico data available |
| BP6 | No | supporting | benign | ClinVar=Pathogenic, stars=3 |
| BP7 | No | supporting | benign | consequence=stop_gained, SpliceAI=N/A |

### BRCA2 — BRCA2:p.Tyr3308Ter **[SF]**

- **Classification**: Likely Pathogenic
- **Position**: chr13:32394897
- **rsID**: rs80359065
- **Transcript**: ENST00000380152.8
- **Consequence**: stop_gained
- **ClinVar**: N/A (stars: 0)
- **gnomAD AF**: N/A
- **Evidence codes**: PM2(M), PVS1(V)

| Criterion | Triggered | Strength | Direction | Source |
|-----------|-----------|----------|-----------|--------|
| BA1 | No | stand_alone | benign | gnomAD AF=N/A |
| BS1 | No | strong | benign | gnomAD AF=N/A |
| PM2 | Yes | moderate | pathogenic | gnomAD AF=absent |
| PVS1 | Yes | very_strong | pathogenic | consequence=stop_gained |
| PS1 | No | strong | pathogenic | ClinVar=, stars=0 |
| PM1 | No | moderate | pathogenic | impact=HIGH, consequence=stop_gained |
| PM4 | No | moderate | pathogenic | consequence=stop_gained |
| PP3 | No | supporting | pathogenic | CADD=38.0≥25.3 |
| PP5 | No | supporting | pathogenic | ClinVar=, stars=0 |
| BP4 | No | supporting | benign | No in silico data available |
| BP6 | No | supporting | benign | ClinVar=, stars=0 |
| BP7 | No | supporting | benign | consequence=stop_gained, SpliceAI=N/A |

### LDLR — LDLR:p.Arg3527Gln **[SF]**

- **Classification**: Likely Pathogenic
- **Position**: chr19:11113280
- **rsID**: rs137929303
- **Transcript**: ENST00000252444.11
- **Consequence**: missense_variant
- **ClinVar**: Pathogenic (stars: 2)
- **gnomAD AF**: 6e-05
- **Evidence codes**: PM2(M), PS1(S), PP3(S), PP5(S)

| Criterion | Triggered | Strength | Direction | Source |
|-----------|-----------|----------|-----------|--------|
| BA1 | No | stand_alone | benign | gnomAD AF=0.0001 |
| BS1 | No | strong | benign | gnomAD AF=0.0001 |
| PM2 | Yes | moderate | pathogenic | gnomAD AF=0.000060 |
| PVS1 | No | very_strong | pathogenic | consequence=missense_variant |
| PS1 | Yes | strong | pathogenic | ClinVar=Pathogenic, stars=2 |
| PM1 | No | moderate | pathogenic | impact=MODERATE, consequence=missense_variant |
| PM4 | No | moderate | pathogenic | consequence=missense_variant |
| PP3 | Yes | supporting | pathogenic | CADD=26.5≥25.3; SIFT=deleterious; PolyPhen=probably_damaging |
| PP5 | Yes | supporting | pathogenic | ClinVar=Pathogenic, stars=2 |
| BP4 | No | supporting | benign | No in silico data available |
| BP6 | No | supporting | benign | ClinVar=Pathogenic, stars=2 |
| BP7 | No | supporting | benign | consequence=missense_variant, SpliceAI=N/A |

### DPYD — DPYD:c.1905+1G>A

- **Classification**: Likely Pathogenic
- **Position**: chr1:97515839
- **rsID**: rs3918290
- **Transcript**: ENST00000370192.8
- **Consequence**: splice_donor_variant
- **ClinVar**: N/A (stars: 0)
- **gnomAD AF**: 8e-05
- **Evidence codes**: PM2(M), PVS1(V)

| Criterion | Triggered | Strength | Direction | Source |
|-----------|-----------|----------|-----------|--------|
| BA1 | No | stand_alone | benign | gnomAD AF=0.0001 |
| BS1 | No | strong | benign | gnomAD AF=0.0001 |
| PM2 | Yes | moderate | pathogenic | gnomAD AF=0.000080 |
| PVS1 | Yes | very_strong | pathogenic | consequence=splice_donor_variant |
| PS1 | No | strong | pathogenic | ClinVar=, stars=0 |
| PM1 | No | moderate | pathogenic | impact=HIGH, consequence=splice_donor_variant |
| PM4 | No | moderate | pathogenic | consequence=splice_donor_variant |
| PP3 | No | supporting | pathogenic | CADD=34.0≥25.3 |
| PP5 | No | supporting | pathogenic | ClinVar=, stars=0 |
| BP4 | No | supporting | benign | No in silico data available |
| BP6 | No | supporting | benign | ClinVar=, stars=0 |
| BP7 | No | supporting | benign | consequence=splice_donor_variant, SpliceAI=0.98 |

## Variants of Uncertain Significance (VUS)

| Gene | Variant | Transcript | Position | gnomAD AF | Evidence Codes | SF Gene |
|------|---------|------------|----------|-----------|----------------|---------|
| SCN5A | SCN5A:p.Ala1656Asp | ENST00000333535.10 | chr3:38603170 | 0.000030 | PM2(M), PP3(S) | Yes |
| MLH1 | MLH1:p.Lys618Ala | ENST00000231790.8 | chr3:37038110 | 0.000050 | PM2(M), BP4(S) | Yes |
| RYR2 | RYR2:p.Arg420Gln | ENST00000366574.7 | chr1:237287200 | 0.000040 | PM2(M), PP3(S) | Yes |
| CDH1 | CDH1:p.Ala634Val | ENST00000261769.10 | chr16:68812350 | 0.000020 | PM2(M), BP4(S) | Yes |

## Benign / Likely Benign Variants

| Gene | Variant | Classification | gnomAD AF | Evidence Codes |
|------|---------|----------------|-----------|----------------|
| TP53 | TP53:p.Pro72Arg | Benign | 0.2503 | BA1(S), BS1(S), BP4(S), BP6(S) |
| BRCA2 | BRCA2:p.Asn372His | Benign | 0.2348 | BA1(S), BS1(S), BP4(S), BP6(S) |
| HFE | HFE:p.His63Asp | Benign | 0.1425 | BA1(S), BS1(S), BP4(S), BP6(S) |
| APC | APC:p.Ile1307Lys | Likely Benign | 0.0215 | BS1(S), BP4(S) |
| MLH1 | MLH1:p.Val384Asp | Likely Benign | 0.0008 | BP4(S), BP6(S) |
| BRCA1 | BRCA1:p.Ser1613Gly | Likely Benign | 0.0052 | BP4(S), BP6(S) |
| BRCA1 | BRCA1:c.4308T>C | Likely Benign | 0.0321 | BS1(S), BP4(S), BP6(S), BP7(S) |
| TP53 | TP53:c.672G>A | Likely Benign | 0.0189 | BS1(S), BP4(S), BP6(S), BP7(S) |
| NF2 | NF2:c.585G>A | Likely Benign | 0.0245 | BS1(S), BP4(S), BP6(S), BP7(S) |

## ACMG SF v3.2 Secondary Findings Screening

**19** variant(s) found in ACMG SF v3.2 genes (81 genes screened).

| Gene | Variant | Classification | Evidence Codes |
|------|---------|----------------|----------------|
| BRCA1 | BRCA1:p.Gln1756ProfsTer74 | Pathogenic | PM2(M), PVS1(V), PP5(S) |
| TP53 | TP53:p.Arg175His | Pathogenic | PM2(M), PS1(S), PM1(M), PP3(S), PP5(S) |
| MSH2 | MSH2:c.942+3A>G | Pathogenic | PM2(M), PVS1(V), PP5(S) |
| PTEN | PTEN:p.Arg130Ter | Pathogenic | PM2(M), PVS1(V), PP5(S) |
| BRCA2 | BRCA2:p.Tyr3308Ter | Likely Pathogenic | PM2(M), PVS1(V) |
| LDLR | LDLR:p.Arg3527Gln | Likely Pathogenic | PM2(M), PS1(S), PP3(S), PP5(S) |
| SCN5A | SCN5A:p.Ala1656Asp | Uncertain Significance | PM2(M), PP3(S) |
| MLH1 | MLH1:p.Lys618Ala | Uncertain Significance | PM2(M), BP4(S) |
| RYR2 | RYR2:p.Arg420Gln | Uncertain Significance | PM2(M), PP3(S) |
| CDH1 | CDH1:p.Ala634Val | Uncertain Significance | PM2(M), BP4(S) |
| TP53 | TP53:p.Pro72Arg | Benign | BA1(S), BS1(S), BP4(S), BP6(S) |
| BRCA2 | BRCA2:p.Asn372His | Benign | BA1(S), BS1(S), BP4(S), BP6(S) |
| HFE | HFE:p.His63Asp | Benign | BA1(S), BS1(S), BP4(S), BP6(S) |
| APC | APC:p.Ile1307Lys | Likely Benign | BS1(S), BP4(S) |
| MLH1 | MLH1:p.Val384Asp | Likely Benign | BP4(S), BP6(S) |
| BRCA1 | BRCA1:p.Ser1613Gly | Likely Benign | BP4(S), BP6(S) |
| BRCA1 | BRCA1:c.4308T>C | Likely Benign | BS1(S), BP4(S), BP6(S), BP7(S) |
| TP53 | TP53:c.672G>A | Likely Benign | BS1(S), BP4(S), BP6(S), BP7(S) |
| NF2 | NF2:c.585G>A | Likely Benign | BS1(S), BP4(S), BP6(S), BP7(S) |

## Methodology

Variants were classified according to the ACMG/AMP 2015 standards and guidelines 
(Richards et al., *Genet Med* 2015; PMID 25741868). Evidence was collected from Ensembl VEP 
(consequence annotation, ClinVar, gnomAD colocated frequencies, SIFT, PolyPhen). 
The ACMG combining rules were applied to assign one of five classifications: 
Pathogenic, Likely Pathogenic, Uncertain Significance, Likely Benign, or Benign. 
Secondary findings were screened against ACMG SF v3.2 (Miller et al., 2023; 81 genes).

### Criteria Not Automatically Assessed

The following ACMG criteria require additional data (family studies, functional assays, etc.) 
and were not evaluated in this automated run:

- **PS2/PM6**: De novo status (requires parental samples)
- **PS3/BS3**: Functional studies (requires experimental data)
- **PS4**: Case-control prevalence (requires cohort data)
- **PM3**: In trans with pathogenic variant (requires phased data)
- **PP1/BS4**: Family segregation (requires pedigree)
- **PP2/BP1**: Gene-level missense constraint (planned)
- **PP4**: Phenotype specificity (requires HPO terms)
- **BP2/BP3/BP5/BS2**: Require additional contextual data

## Data Sources

| Source | Version / Release |
|--------|-------------------|
| ClinVar | 2025-03-01 release (demo cache) |
| gnomAD | v4.1 (demo cache) |
| Ensembl VEP | REST API, assembly GRCh38 |
| ACMG SF list | v3.2 (Miller et al., 2023; 81 genes) |

## Limitations

- Not all 28 ACMG/AMP criteria can be evaluated automatically; manual review is recommended for actionable variants
- In silico predictor scores may not be available for all variants
- ClinVar assertions reflect submitter interpretations and may change over time
- gnomAD does not include all populations equally; AF may underestimate prevalence in underrepresented groups

---

*ClawBio is a research and educational tool. It is not a medical device and does not provide clinical diagnoses. Consult a healthcare professional before making any medical decisions.*
