import json
import urllib.request

UA = {"User-Agent": "ClawBio-hackathon-berlin", "Content-Type": "application/json"}
QUERY = """
query V($variantId: String!, $dataset: DatasetId!) {
  variant(variantId: $variantId, dataset: $dataset) {
    variantId
    rsids
    rsid
    exome { ac an af }
    genome { ac an af }
  }
}
"""


def gnomad(vid, ds):
    data = json.dumps({"query": QUERY, "variables": {"variantId": vid, "dataset": ds}}).encode()
    req = urllib.request.Request("https://gnomad.broadinstitute.org/api", data=data, headers=UA, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return json.loads(resp.read().decode())
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ClawBio-hackathon-berlin"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()[:2500].decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001
        return "ERR", str(exc)[:400]


print("gnomAD GRCh38 14-96263976-G-A")
for ds in ("gnomad_r3", "gnomad_r4"):
    print(ds, gnomad("14-96263976-G-A", ds))

print("\nClinVar COSV53706532")
print(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=COSV53706532+OR+COSM3499561+OR+BDKRB1+Trp98Ter&retmode=json"))

print("\nCOSMIC-style Ensembl GRCh38 VEP")
print(get("https://rest.ensembl.org/vep/human/region/14:96263976-96263976:1/A?content-type=application/json"))
