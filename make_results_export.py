import csv
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILY = HERE / "challenge1-b37-segregation.tsv"
GNOMAD = HERE / "challenge1-gnomad-v2-grch37.tsv"
OUT_TSV = HERE / "challenge1-results-export.tsv"


def genes(eff: str) -> str:
    found = re.findall(
        r"\|([A-Z][A-Z0-9-]{1,20})\|\|(?:CODING|NON_CODING)\|",
        eff,
    )
    out, seen = [], set()
    for g in found:
        if g not in seen:
            seen.add(g)
            out.append(g)
    return ",".join(out[:4])


FOLLOW_UP = {
    ("14", "96730313"): (
        "Not in gnomAD v2 as 14-96730313-G-A. Stop-gain in BDKRB1 (W98*). "
        "Next: gnomAD and dbSNP by gene plus position; Ensembl GRCh37; ClinVar BDKRB1. "
        "Not found here is not proof of rarity."
    ),
    ("21", "11029596"): (
        "Not in gnomAD v2 as 21-11029596-AC-A because of indel shifting. "
        "Ensembl GRCh37 maps rs138714104 to rs60459764 at 21:11029597-11029598, alleles CC/C, "
        "with 1000 Genomes frequency evidence. Also synonyms rs796536508, rs376100218, rs144469422. "
        "Next: gnomAD v2 as rs60459764 or 21-11029597-CC-C; dbSNP; 1000 Genomes. BAGE duplicated region."
    ),
}

fam = {
    (r["CHROM"], r["POS"], r["REF"], r["ALT"]): r
    for r in csv.DictReader(FAMILY.open(encoding="utf-8"), delimiter="\t")
}
gno = list(csv.DictReader(GNOMAD.open(encoding="utf-8"), delimiter="\t"))

fields = [
    "chrom",
    "pos",
    "id",
    "ref",
    "alt",
    "genes",
    "parent_of_origin_unphased",
    "son_gt",
    "father_gt",
    "mother_gt",
    "sister_gt",
    "gnomad_v2_variant_id",
    "gnomad_v2_rsid",
    "gnomad_v2_af",
    "gnomad_v2_source",
    "world_freq_bin",
    "follow_up",
]


def bin_af(af: str, source: str) -> str:
    if source == "error" or af == "":
        return "not_in_this_gnomad_v2_query"
    f = float(af)
    if f >= 0.01:
        return "at_least_1_percent"
    if f >= 0.001:
        return "under_1_percent"
    if f >= 0.0001:
        return "under_0.1_percent"
    return "under_0.01_percent"


out = []
for r in gno:
    key = (r["CHROM"], r["POS"], r["REF"], r["ALT"])
    frow = fam[key]
    af = r["gnomad_v2_af"]
    src = r["gnomad_v2_source"]
    out.append(
        {
            "chrom": r["CHROM"],
            "pos": r["POS"],
            "id": r["ID"],
            "ref": r["REF"],
            "alt": r["ALT"],
            "genes": genes(frow["EFF"]),
            "parent_of_origin_unphased": r["PARENT_OF_ORIGIN_UNPHASED"],
            "son_gt": r["SON_GT_DP_GQ"].split(":")[0],
            "father_gt": r["FATHER_GT_DP_GQ"].split(":")[0],
            "mother_gt": r["MOTHER_GT_DP_GQ"].split(":")[0],
            "sister_gt": r["SISTER_GT_DP_GQ"].split(":")[0],
            "gnomad_v2_variant_id": r["gnomad_variant_id"],
            "gnomad_v2_rsid": r["gnomad_rsid"],
            "gnomad_v2_af": af,
            "gnomad_v2_source": src,
            "world_freq_bin": bin_af(af, src),
            "follow_up": FOLLOW_UP.get((r["CHROM"], r["POS"]), ""),
        }
    )

with OUT_TSV.open("w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t")
    w.writeheader()
    w.writerows(out)

print("wrote", OUT_TSV, "rows", len(out))
print("bins", {b: sum(1 for r in out if r["world_freq_bin"] == b) for b in sorted({r["world_freq_bin"] for r in out})})
