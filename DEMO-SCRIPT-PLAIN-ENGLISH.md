# Challenge 1 demo script in plain English

Speak this in about two minutes. Do not diagnose anyone. Do not show protein folding.

## One sentence for the Slack demo channel

We counted sixty eight high impact variants in a public four person family genome. Thirty were labelled as coming from the father and thirty eight from the mother. We then listed what this data is not allowed to claim, including rarity and a clinical diagnosis.

## What to show

First, the family table. Second, the count of thirty and thirty eight. Third, the toy report where one variant has no population frequency and is therefore not called rare.

## Spoken script

Hello. We took Challenge 1, End the diagnostic odyssey.

The data is a public teaching pack from the Corpas family genome, used with a Creative Commons licence. It is four people: a son, a father, a mother, and a sister. The genome build is GRCh37. There are sixty eight variant rows. Each row is a high impact change that the son carries together with exactly one parent. The table has eleven columns, including a teaching label for which parent the allele came from. That label is not molecular phase. It is a teaching tag.

We did not guess the thirty and thirty eight. We downloaded the official table and counted the parent of origin column. We got thirty labelled paternal and thirty eight labelled maternal. We got the same numbers on this laptop and later in the hosted BioNeMo agent, after we stopped pasting the whole table into the chat and counted it with a short Python script instead.

Those numbers do not tell us a disease inheritance pattern. There is no clinical description of the family. There are no phenotype terms. So we cannot say autosomal dominant or autosomal recessive. We also cannot say every site came from the same parent. Thirty came from the father. Thirty eight came from the mother.

The hosted agent could not run the ClawBio rare high impact demo skill. We ran that skill locally on bundled toy data, not on the family table. The toy report is the method check the brief asked for. It found three variants with a documented low frequency, one common high impact variant, and one high impact variant with no frequency at all. That last one, labelled GENE2, is the point. Missing frequency is not evidence that a variant is rare. We refused to call it rare.

Here is what we will not claim about the sixty eight family rows.

We will not call them rare, because this pack has no trustworthy population frequency layer.

We will not call them pathogenic or diagnostic, because the effect field is old software annotation, not a current clinical classification, and because there is no phenotype.

We will not call them new in the child, meaning de novo, because a parent carries the same allele at every one of these sixty eight sites. We have genotypes for the son, the father, the mother, and the sister. The second parent is usually reference at that site. The design of the pack is inherited from one parent, not missing parents.

We will not call compound heterozygosity, because the parent of origin tags are unphased teaching labels.

We will not give a clinical diagnosis.

What we can say is narrow and honest. Sixty eight high impact teaching records. Thirty from the father, thirty eight from the mother, as labelled. A method check that refuses rarity when frequency is absent. An explicit list of claims this file cannot support.

That refusal is the work. A ranked gene list without it would be the failure this challenge is about.

Thank you.

## What not to say or show

Do not show the EGFR drug demo or OpenFold. Do not say the data is synthetic. Do not say we lack parental genotypes. Do not dump the table on screen. After the talk, stop the Nebius endpoint so it stops billing.
