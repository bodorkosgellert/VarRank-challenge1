import json
import urllib.parse
import urllib.request

UA = {"User-Agent": "ClawBio-hackathon-berlin", "Accept": "application/json"}


def get(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            try:
                return resp.status, json.loads(raw.decode())
            except json.JSONDecodeError:
                return resp.status, raw.decode("utf-8", errors="replace")[:2000]
    except Exception as exc:  # noqa: BLE001
        return "ERR", str(exc)[:500]


def post_json(url: str, payload: dict, timeout: int = 30):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={**UA, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode())
    except Exception as exc:  # noqa: BLE001
        return "ERR", str(exc)[:500]


def gnomad(variant_id: str, dataset: str):
    query = """
    query V($variantId: String!, $dataset: DatasetId!) {
      variant(variantId: $variantId, dataset: $dataset) {
        variantId
        rsids
        rsid
        chrom
        pos
        ref
        alt
        exome { ac an af }
        genome { ac an af }
      }
    }
    """
    return post_json(
        "https://gnomad.broadinstitute.org/api",
        {"query": query, "variables": {"variantId": variant_id, "dataset": dataset}},
    )


print("=== Ensembl lift GRCh37 -> GRCh38 ===")
print(get("https://grch37.rest.ensembl.org/map/human/GRCh37/14:96730313..96730313/GRCh38?content-type=application/json"))

print("\n=== Ensembl GRCh37 region variations ===")
print(get("https://grch37.rest.ensembl.org/overlap/region/human/14:96730310-96730316?feature=variation;content-type=application/json"))

print("\n=== Ensembl GRCh37 lookup 14:96730313 ===")
print(get("https://grch37.rest.ensembl.org/vep/human/region/14:96730313-96730313:1/A?content-type=application/json"))

print("\n=== myvariant hg19 ===")
print(get("https://myvariant.info/v1/variant/chr14:g.96730313G>A?assembly=hg19"))

print("\n=== myvariant hg38 via query ===")
print(get("https://myvariant.info/v1/query?q=bdkrb1%20AND%20hg19.chrom:14%20AND%20hg19.hg19.end:96730313&fields=dbsnp,clinvar,gnomad_exome,gnomad_genome,exac,chrom,hg19,hg38,rsid"))

print("\n=== NCBI dbSNP position GRCh37 ===")
print(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&term=14[CHR]+AND+96730313[CHRPOS]+AND+GRCh37[Assembly]&retmode=json"))

print("\n=== ClinVar BDKRB1 W98 ===")
print(get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BDKRB1[gene]+AND+(W98*%20OR%20Trp98Ter%20OR%2014:96730313)&retmode=json"))

print("\n=== gnomAD datasets 14-96730313-G-A ===")
for ds in ("gnomad_r2_1", "exac", "gnomad_r3", "gnomad_r4"):
    status, body = gnomad("14-96730313-G-A", ds)
    print(ds, status)
    print(str(body)[:800])
