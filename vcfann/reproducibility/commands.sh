#!/usr/bin/env bash
# ClawBio VCF Annotator — portable reproducibility bundle
# Generated: 2026-08-18 13:40 UTC
# Input: demo_variants.vcf
#
# How to replay:
#   bash reproducibility/commands.sh
# from anywhere inside the repository clone.

set -euo pipefail

# ── Locate repo root ──────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$SCRIPT_DIR"
while [[ ! -d "$REPO_ROOT/skills" && "$REPO_ROOT" != "/" ]]; do
  REPO_ROOT="$(dirname "$REPO_ROOT")"
done
if [[ ! -d "$REPO_ROOT/skills" ]]; then
  echo "ERROR: Could not locate repo root (no skills/ directory found)" >&2
  exit 1
fi

# ── Replay command ────────────────────────────────────────────────────────────
python "$REPO_ROOT/skills/vcf-annotator/vcf_annotator.py" \
    --input "demo_variants.vcf" \
    --output "./vcf_report"
