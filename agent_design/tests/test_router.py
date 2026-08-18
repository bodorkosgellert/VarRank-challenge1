"""Tests for the lookup-agent router. These define behaviour before any LLM is involved."""

import unittest

from agent_design.router import LookupOutcome, layer_for, next_route, rarity_call


class RouterTests(unittest.TestCase):
    def test_not_found_is_never_rare(self):
        miss = LookupOutcome(
            chrom="14", pos=96730313, ref="G", alt="A", status="not_found", rsid=None
        )
        self.assertEqual(rarity_call(miss), "unknown")
        self.assertNotEqual(rarity_call(miss), "uncommon_in_catalogue")

    def test_missing_af_on_found_row_is_unknown_not_rare(self):
        found = LookupOutcome(
            chrom="1", pos=1, ref="C", alt="T", status="found", af=None, rsid="rs1"
        )
        self.assertEqual(rarity_call(found), "unknown")

    def test_common_site_stops_and_skips_gene_evidence(self):
        common = LookupOutcome(
            chrom="1",
            pos=11906068,
            ref="A",
            alt="G",
            status="found",
            af=0.137,
            rsid="rs5065",
        )
        route = next_route(common)
        self.assertTrue(route.stop)
        self.assertFalse(route.allow_gene_evidence)
        self.assertEqual(route.tools, ())
        self.assertEqual(layer_for(route), 1)

    def test_uncommon_site_opens_shortlist(self):
        rareish = LookupOutcome(
            chrom="7",
            pos=44610376,
            ref="G",
            alt="A",
            status="found",
            af=3.99e-6,
            rsid="rs774566321",
        )
        route = next_route(rareish)
        self.assertEqual(route.rarity, "uncommon_in_catalogue")
        self.assertIn("clinvar", route.tools)
        self.assertTrue(route.allow_gene_evidence)
        self.assertEqual(layer_for(route), 3)

    def test_bdkrb1_no_rs_routes_to_vep_lift_clinvar_hgvs(self):
        miss = LookupOutcome(
            chrom="14",
            pos=96730313,
            ref="G",
            alt="A",
            status="not_found",
            rsid=None,
            is_indel=False,
            failure_class="no_rsid",
        )
        route = next_route(miss)
        self.assertEqual(route.rarity, "unknown")
        self.assertEqual(
            route.tools,
            ("vep", "liftover", "gnomad_other_release", "clinvar_gene_hgvs"),
        )
        self.assertNotIn("gwas_lookup", route.tools)

    def test_indel_miss_routes_to_normalise_and_synonyms(self):
        miss = LookupOutcome(
            chrom="21",
            pos=11029596,
            ref="AC",
            alt="A",
            status="not_found",
            rsid="rs138714104",
            is_indel=True,
            failure_class="indel_shift",
        )
        route = next_route(miss)
        self.assertEqual(
            route.tools, ("left_normalise", "ensembl_synonyms", "gnomad_retry")
        )

    def test_http_error_retries_and_stays_unknown(self):
        err = LookupOutcome(
            chrom="1", pos=1, ref="A", alt="G", status="error", failure_class="rate_limit"
        )
        route = next_route(err)
        self.assertEqual(route.tools, ("retry_backoff",))
        self.assertEqual(route.rarity, "unknown")
        self.assertFalse(route.stop)


if __name__ == "__main__":
    unittest.main()
