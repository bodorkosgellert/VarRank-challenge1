"""Deterministic routing for a catalogue-lookup agent.

The LLM does not choose rarity. This module maps a lookup outcome to the next
tools, and refuses to call a missing catalogue hit rare.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Status = Literal["found", "not_found", "ambiguous", "error"]
FailureClass = Literal[
    "none",
    "missing_in_build",
    "indel_shift",
    "no_rsid",
    "rate_limit",
]
RarityCall = Literal["common", "uncommon_in_catalogue", "unknown"]


@dataclass(frozen=True)
class LookupOutcome:
    chrom: str
    pos: int
    ref: str
    alt: str
    status: Status
    af: float | None = None
    rsid: str | None = None
    is_indel: bool = False
    failure_class: FailureClass = "none"
    catalogues_tried: tuple[str, ...] = ()


@dataclass(frozen=True)
class Route:
    tools: tuple[str, ...]
    stop: bool
    reason: str
    rarity: RarityCall
    allow_gene_evidence: bool = False


COMMON_AF = 0.01


def rarity_call(outcome: LookupOutcome) -> RarityCall:
    """Missing or failed lookups are unknown, never rare."""
    if outcome.status in ("not_found", "error", "ambiguous"):
        return "unknown"
    if outcome.af is None:
        return "unknown"
    if outcome.af >= COMMON_AF:
        return "common"
    return "uncommon_in_catalogue"


def next_route(outcome: LookupOutcome) -> Route:
    rarity = rarity_call(outcome)

    if outcome.status == "error":
        return Route(
            tools=("retry_backoff",),
            stop=False,
            reason="http_or_timeout",
            rarity=rarity,
        )

    if outcome.status == "found" and rarity == "common":
        return Route(
            tools=(),
            stop=True,
            reason="common_in_catalogue_stop",
            rarity=rarity,
            allow_gene_evidence=False,
        )

    if outcome.status == "found" and rarity == "uncommon_in_catalogue":
        return Route(
            tools=("clinvar",),
            stop=False,
            reason="uncommon_shortlist",
            rarity=rarity,
            allow_gene_evidence=True,
        )

    if outcome.failure_class == "indel_shift" or (
        outcome.status == "not_found" and outcome.is_indel
    ):
        return Route(
            tools=("left_normalise", "ensembl_synonyms", "gnomad_retry"),
            stop=False,
            reason="indel_respelled",
            rarity=rarity,
        )

    if outcome.failure_class == "no_rsid" or (
        outcome.status == "not_found" and not outcome.rsid
    ):
        return Route(
            tools=("vep", "liftover", "gnomad_other_release", "clinvar_gene_hgvs"),
            stop=False,
            reason="snv_without_rs",
            rarity=rarity,
        )

    if outcome.status == "not_found":
        return Route(
            tools=("vep", "liftover", "gnomad_other_release"),
            stop=False,
            reason="generic_miss",
            rarity=rarity,
        )

    return Route(tools=(), stop=True, reason="no_further_action", rarity=rarity)


def layer_for(route: Route) -> int:
    """1 = identity done; 2 = retry miss; 3 = gene evidence allowed."""
    if route.stop and route.rarity == "common":
        return 1
    if route.allow_gene_evidence:
        return 3
    return 2
