"""
check_tsb_cache.py

Fast TSB cache lookup — called by synth-diagnostic-conductor before live search.
Returns cached TSBs for a vehicle + DTCs/symptoms.
Zero token cost. Instant. Runs before any LLM call.

Usage (CLI):
  py -3.12 check_tsb_cache.py "Chevrolet" "Equinox" 2019
  py -3.12 check_tsb_cache.py "Ford" "F-150" 2018 "P0171,P0174"
  py -3.12 check_tsb_cache.py "Toyota" "Camry" 2022 "" "rough idle"

Usage (import):
  from check_tsb_cache import check_tsb
  results = check_tsb(make="Chevrolet", model="Equinox", year=2019, dtc_codes=["P0171"])
  # Returns list of TSB dicts, empty list if none found
"""

import os
import sys
import json
import requests

# Load API keys from ~/.env.techpulse (auto-runs on import)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env_loader  # noqa: F401

URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
KEY = os.environ.get("SUPABASE_KEY", "")
HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json"
}


def check_tsb(make, model=None, year=None, dtc_codes=None, symptom_keywords=None):
    """
    Look up TSBs in local cache.

    Priority order:
      1. make + model + year + DTC match (most specific)
      2. make + model + year (vehicle match only)
      3. make + DTC match (make-wide)

    Returns list of matching TSB dicts, sorted by specificity.
    Empty list if nothing in cache for this vehicle.
    """
    results = []
    seen_ids = set()

    def add_results(rows):
        for row in rows:
            if row["id"] not in seen_ids:
                seen_ids.add(row["id"])
                results.append(row)

    # Pass 1 — make + model + year range match
    if make and model and year:
        r = requests.get(
            f"{URL}/rest/v1/tsb_cache",
            headers=HEADERS,
            params={
                "make":       f"eq.{make}",
                "model":      f"eq.{model}",
                "year_start": f"lte.{year}",
                "year_end":   f"gte.{year}",
                "select":     "id,tsb_number,title,summary,dtc_codes,symptoms,fix_procedure,source",
                "order":      "tsb_number.asc",
                "limit":      "50"
            }
        )
        if r.status_code == 200:
            add_results(r.json())

    # Pass 2 — make + year only (catches model name variations)
    if make and year and not results:
        r = requests.get(
            f"{URL}/rest/v1/tsb_cache",
            headers=HEADERS,
            params={
                "make":       f"eq.{make}",
                "year_start": f"lte.{year}",
                "year_end":   f"gte.{year}",
                "select":     "id,tsb_number,title,summary,dtc_codes,symptoms,fix_procedure,source",
                "order":      "tsb_number.asc",
                "limit":      "100"
            }
        )
        if r.status_code == 200:
            add_results(r.json())

    # Filter by DTC if provided
    if dtc_codes and results:
        dtc_upper = [d.upper() for d in dtc_codes]
        dtc_matches = []
        no_dtc = []
        for row in results:
            row_dtcs = [d.upper() for d in (row.get("dtc_codes") or [])]
            if any(d in row_dtcs for d in dtc_upper):
                dtc_matches.append(row)
            else:
                no_dtc.append(row)
        # DTC matches first, then general vehicle matches
        results = dtc_matches + no_dtc

    # Filter by symptoms if provided
    if symptom_keywords and results:
        kw_lower = [k.lower() for k in symptom_keywords]
        sym_matches = []
        other = []
        for row in results:
            row_syms = [s.lower() for s in (row.get("symptoms") or [])]
            row_title = (row.get("title") or "").lower()
            if any(kw in row_syms or kw in row_title for kw in kw_lower):
                sym_matches.append(row)
            else:
                other.append(row)
        results = sym_matches + other

    return results


def format_results(results, make, model, year):
    """Format TSB results for display."""
    if not results:
        print(f"\n[CACHE] No TSBs cached for {make} {model or ''} {year or ''}.")
        print("        Run: py -3.12 build_tsb_cache.py to populate cache.")
        return

    print(f"\n[CACHE] {len(results)} TSB(s) found for {make} {model or ''} {year or ''}")
    print("=" * 60)

    for i, tsb in enumerate(results[:10], 1):  # Show top 10
        dtcs = ", ".join(tsb.get("dtc_codes") or []) or "none"
        print(f"\n{i}. {tsb['tsb_number']} — {tsb['title']}")
        print(f"   DTCs: {dtcs}")
        if tsb.get("summary"):
            print(f"   Summary: {tsb['summary'][:200]}...")
        if tsb.get("fix_procedure"):
            print(f"   Fix: {tsb['fix_procedure'][:150]}...")
        print(f"   Source: {tsb.get('source', 'NHTSA')}")

    if len(results) > 10:
        print(f"\n   ... and {len(results) - 10} more TSBs in cache.")


def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print(__doc__)
        return

    make   = args[0] if len(args) >= 1 else None
    model  = args[1] if len(args) >= 2 else None
    year   = int(args[2]) if len(args) >= 3 else None
    dtcs   = [d.strip() for d in args[3].split(",")] if len(args) >= 4 and args[3] else None
    syms   = [args[4]] if len(args) >= 5 else None

    results = check_tsb(make=make, model=model, year=year, dtc_codes=dtcs, symptom_keywords=syms)
    format_results(results, make, model, year)


if __name__ == "__main__":
    main()
