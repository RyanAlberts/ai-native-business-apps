#!/usr/bin/env bash
# Copyright 2026 Ryan Alberts
# Licensed under the Apache License, Version 2.0
#
# Deterministic gates for the agent-native Founding Journey (playbooks/).
#
#   bash verify/journey_gate.sh 00      # check one phase
#   bash verify/journey_gate.sh all     # check every phase, in order
#
# Exit 0 = the phase's artifacts exist and look structurally right.
# These gates check structure, not legal correctness — a licensed
# professional reviewing the packet is still the real final gate.
#
# Needs only bash + grep + wc (macOS, Linux, Git Bash on Windows).
set -u
cd "$(dirname "$0")/.."

COMPANY="company.json"
PACKET_DIR="formation-packet"
MARKER="<!-- keel-disclaimer -->"

fail() { echo "FAIL $PHASE: $1"; exit 1; }
pass() { echo "PASS $PHASE: $1"; exit 0; }

# json_field <name> — succeeds if company.json has a non-empty string value.
json_field() {
  grep -Eq "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]" "$COMPANY"
}

# artifact <file> <min-bytes> — the phase's output exists, is substantial,
# and carries the disclaimer footer.
artifact() {
  local f="$PACKET_DIR/$1" min="$2"
  [ -f "$f" ] || fail "$f is missing — run this phase's playbook first"
  [ "$(wc -c < "$f")" -ge "$min" ] || fail "$f looks like a stub (under $min bytes)"
  grep -q "$MARKER" "$f" || fail "$f is missing the disclaimer footer (see the contract: How to work a playbook)"
}

check_phase() {
  PHASE="phase $1"
  case "$1" in
    00)
      [ -f "$COMPANY" ] || fail "$COMPANY not found at the repo root — run playbooks/00-intake.md"
      json_field legal_name || fail "legal_name is empty in $COMPANY (a working name is fine)"
      json_field home_state || fail "home_state is empty in $COMPANY"
      json_field one_liner  || fail "one_liner is empty in $COMPANY (what the business does, one sentence)"
      pass "$COMPANY has the required profile fields"
      ;;
    01)
      artifact "01-incorporation.md" 2000
      grep -qi "entity type" "$PACKET_DIR/01-incorporation.md" || fail "no entity-type section in the incorporation plan"
      grep -qi "filing checklist" "$PACKET_DIR/01-incorporation.md" || fail "no filing checklist in the incorporation plan"
      json_field entity_type        || fail "entity_type not recorded in $COMPANY — get the founder's yes, then write it"
      json_field state_of_formation || fail "state_of_formation not recorded in $COMPANY"
      pass "incorporation plan written and the decision is recorded in $COMPANY"
      ;;
    02)
      artifact "02-election_83b.md" 1500
      grep -qi "postmark" "$PACKET_DIR/02-election_83b.md" || fail "the 83(b) output never addresses the postmark deadline"
      pass "83(b) artifact written with deadline framing"
      ;;
    03)
      artifact "03-legal_doc.md" 3000
      grep -qi "signature" "$PACKET_DIR/03-legal_doc.md" || fail "no signature block found — these should be usable drafts, not summaries"
      pass "founding legal documents drafted"
      ;;
    04)
      artifact "04-bank_insurance.md" 2000
      grep -qi "bank" "$PACKET_DIR/04-bank_insurance.md" || fail "banking half is missing"
      grep -qi "insurance" "$PACKET_DIR/04-bank_insurance.md" || fail "insurance half is missing"
      pass "banking & insurance plan written"
      ;;
    05)
      artifact "05-compliance_tax.md" 2000
      grep -Eqi "annual report|franchise tax" "$PACKET_DIR/05-compliance_tax.md" || fail "no annual-obligation analysis found"
      grep -q "BEGIN:VCALENDAR" "$PACKET_DIR/05-compliance_tax.md" || fail "no embedded compliance calendar (.ics block) — the playbook's generate_compliance_ics substitution"
      pass "compliance & tax plan written with embedded calendar"
      ;;
    06)
      artifact "00-formation-packet.md" 2000
      grep -qi "master day-0 checklist" "$PACKET_DIR/00-formation-packet.md" || fail "packet is missing the Master Day-0 Checklist section"
      grep -qi "key deadlines" "$PACKET_DIR/00-formation-packet.md" || fail "packet is missing the Key Deadlines section"
      local html="$PACKET_DIR/00-formation-packet.html"
      [ -f "$html" ] || fail "$html is missing (the printable Save-as-PDF page)"
      grep -qi "<!doctype html>" "$html" || fail "$html is not a self-contained HTML page"
      [ -f "$PACKET_DIR/company.json" ] || fail "final company.json was not copied into $PACKET_DIR/"
      if json_field formation_date; then
        local ics="$PACKET_DIR/compliance-deadlines.ics"
        [ -f "$ics" ] || fail "formation_date is set, so $ics must exist (83(b) postmark is computable)"
        grep -q "BEGIN:VCALENDAR" "$ics" || fail "$ics is not a valid calendar file"
        grep -q "BEGIN:VEVENT" "$ics" || fail "$ics has no events"
      fi
      pass "Day-0 Formation Packet complete in $PACKET_DIR/"
      ;;
    *)
      echo "usage: bash verify/journey_gate.sh {00|01|02|03|04|05|06|all}"; exit 2
      ;;
  esac
}

if [ "${1:-}" = "all" ]; then
  overall=0
  for p in 00 01 02 03 04 05 06; do
    out="$(bash "$0" "$p")" || overall=1
    echo "$out"
  done
  exit "$overall"
fi

check_phase "${1:-}"
