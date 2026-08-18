import csv
import re
from pathlib import Path

path = Path(__file__).with_name("challenge1-b37-segregation.tsv")
rows = list(csv.DictReader(path.open(encoding="utf-8"), delimiter="\t"))


def genes(eff: str) -> str:
    found = re.findall(
        r"\|([A-Z][A-Z0-9-]{1,20})\|\|(?:CODING|NON_CODING)\|",
        eff,
    )
    out = []
    seen = set()
    for g in found:
        if g not in seen:
            seen.add(g)
            out.append(g)
    return ",".join(out[:4]) or "?"


print(f"n={len(rows)}")
for label in ("paternal", "maternal"):
    sub = [r for r in rows if r["PARENT_OF_ORIGIN_UNPHASED"] == label]
    print(f"\n## {label} ({len(sub)})")
    for r in sub:
        vid = r["ID"] if r["ID"] != "." else "."
        print(f"{r['CHROM']}:{r['POS']}\t{vid}\t{genes(r['EFF'])}")
