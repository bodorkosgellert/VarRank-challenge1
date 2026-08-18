import csv
import json
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = list(
    csv.DictReader(
        (HERE / "challenge1-b37-segregation.tsv").open(encoding="utf-8"),
        delimiter="\t",
    )
)
for r in rows:
    key = f"{r['CHROM']}:{r['POS']}"
    if key in ("14:96730313", "21:11029596"):
        print("ROW", key, r["ID"], r["REF"], r["ALT"], r["PARENT_OF_ORIGIN_UNPHASED"])
        print("EFF", r["EFF"][:240])
        print("---")


def fetch(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "ClawBio-hackathon"})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return resp.status, resp.read()[:4000]
    except Exception as exc:  # noqa: BLE001
        return "ERR", str(exc)[:400]


urls = [
    "https://grch37.rest.ensembl.org/overlap/region/human/14:96730313-96730313?feature=variation;content-type=application/json",
    "https://grch37.rest.ensembl.org/overlap/region/human/21:11029596-11029596?feature=variation;content-type=application/json",
    "https://grch37.rest.ensembl.org/variation/human/rs138714104?content-type=application/json",
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&term=rs138714104&retmode=json",
    "https://clinicaltables.nlm.nih.gov/api/variants/v4/search?terms=rs138714104",
]
for url in urls:
    print("\nGET", url)
    status, body = fetch(url)
    print("status", status)
    if isinstance(body, bytes):
        text = body.decode("utf-8", errors="replace")
        print(text[:1200])
    else:
        print(body)
