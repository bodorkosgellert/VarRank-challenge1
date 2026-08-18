"""Look up gnomAD v2.1.1 (GRCh37) allele frequencies for Challenge 1 sites.

This is a SEPARATE evidence layer from the family VCF INFO AF field.
"""
from __future__ import annotations

import csv
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://gnomad.broadinstitute.org/api"
QUERY = """
query Variant($variantId: String!) {
  variant(variantId: $variantId, dataset: gnomad_r2_1) {
    variantId
    rsid
    exome { ac an af }
    genome { ac an af }
  }
}
"""

HERE = Path(__file__).resolve().parent
SRC = HERE / "challenge1-b37-segregation.tsv"
OUT = HERE / "challenge1-gnomad-v2-grch37.tsv"


def gnomad_af(exome, genome) -> tuple[str, str]:
    """Prefer exome AF for this WES pack; fall back to genome. Return (af, source)."""
    for src, block in (("exome", exome), ("genome", genome)):
        if not block:
            continue
        af = block.get("af")
        an = block.get("an") or 0
        if af is not None and an:
            return f"{af:.6g}", src
    return "", "not_in_gnomad_v2"


def lookup(variant_id: str) -> dict:
    payload = json.dumps({"query": QUERY, "variables": {"variantId": variant_id}}).encode()
    req = urllib.request.Request(
        API,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "ClawBio-hackathon-berlin-track1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        return {"error": f"HTTP {exc.code}"}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}
    if body.get("errors") and not (body.get("data") or {}).get("variant"):
        return {"error": body["errors"][0].get("message", "graphql error")}
    var = (body.get("data") or {}).get("variant")
    if not var:
        return {"gnomad_af": "", "gnomad_source": "not_in_gnomad_v2", "gnomad_variant_id": ""}
    af, src = gnomad_af(var.get("exome"), var.get("genome"))
    return {
        "gnomad_af": af,
        "gnomad_source": src,
        "gnomad_rsid": var.get("rsid") or "",
        "gnomad_variant_id": var.get("variantId") or variant_id,
    }


def main() -> None:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8"), delimiter="\t"))
    fieldnames = list(rows[0].keys()) + [
        "gnomad_variant_id",
        "gnomad_rsid",
        "gnomad_v2_af",
        "gnomad_v2_source",
        "lookup_note",
    ]
    out_rows = []
    found = missing = errors = 0
    for i, row in enumerate(rows, 1):
        vid = f"{row['CHROM']}-{row['POS']}-{row['REF']}-{row['ALT']}"
        note = "rsid=" + (row["ID"] if row["ID"] != "." else "none")
        result = lookup(vid)
        time.sleep(0.15)
        if "error" in result:
            errors += 1
            extra = {
                "gnomad_variant_id": vid,
                "gnomad_rsid": "",
                "gnomad_v2_af": "",
                "gnomad_v2_source": "error",
                "lookup_note": note + "; " + result["error"],
            }
        else:
            if result["gnomad_af"]:
                found += 1
            else:
                missing += 1
            extra = {
                "gnomad_variant_id": result.get("gnomad_variant_id", vid),
                "gnomad_rsid": result.get("gnomad_rsid", ""),
                "gnomad_v2_af": result["gnomad_af"],
                "gnomad_v2_source": result["gnomad_source"],
                "lookup_note": note,
            }
        merged = {**row, **extra}
        # drop bulky EFF for the frequency table
        merged.pop("EFF", None)
        out_rows.append(merged)
        print(f"{i:02d}/{len(rows)} {vid} af={extra['gnomad_v2_af'] or 'NA'} ({extra['gnomad_v2_source']})")

    freq_fields = [f for f in fieldnames if f != "EFF"]
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=freq_fields, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(out_rows)

    print(f"\nWrote {OUT}")
    print(f"found={found} missing={missing} errors={errors} total={len(rows)}")
    print("Do not mix gnomad_v2_af with the family VCF INFO AF.")


if __name__ == "__main__":
    main()
