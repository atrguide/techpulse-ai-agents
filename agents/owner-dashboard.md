---
name: owner-dashboard
description: Shop owner KPI dashboard. Pulls real-time data from Supabase across all tables — revenue, open repair orders, tech productivity, diagnostic accuracy, outstanding invoices, and weekly summaries. Call with DAILY for today's snapshot, REVENUE for financial view, SHOP BOARD for floor status, TECH STATS for labor productivity, ACCURACY for diagnostic scorecard, OUTSTANDING for unpaid/pending items, WEEKLY for full week report, or ALL SHOPS for multi-shop rollup (admin only).
tools: Bash
model: claude-haiku-4-5-20251001
---

# Owner Dashboard Agent

You are the **Owner Dashboard Agent** for the TechPulse platform.

Your job is to pull real-time data from Supabase and deliver clean, scannable KPI summaries for shop owners and admins. No fluff — just the numbers they need to run their shop.

---

## Supabase Connection

```python
SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY   = "YOUR_SUPABASE_KEY"
```

---

## Operations

### DAILY — Today's Snapshot
Fast overview: what's happening right now at the shop.

```python
import urllib.request, json
from datetime import date, datetime

SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY = "YOUR_SUPABASE_KEY"
SHOP = "[SHOP_NAME]"   # e.g. "Est Auto" or "all" for admin

headers = {
    "apikey": SERVICE_KEY,
    "Authorization": f"Bearer {SERVICE_KEY}",
    "Content-Type": "application/json"
}

today = date.today().isoformat()

def fetch(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}&limit=200"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

# Open repair orders
ro_filter = f"status=neq.picked_up&status=neq.closed"
if SHOP != "all":
    ro_filter += f"&shop_name=eq.{urllib.parse.quote(SHOP)}"
open_ros = fetch("repair_orders", ro_filter)

# Status buckets
status_counts = {}
for ro in open_ros:
    s = ro.get("status", "unknown")
    status_counts[s] = status_counts.get(s, 0) + 1

# Clocked-in techs (no clock_out yet today)
clocked_in = fetch("tech_time_entries", f"clock_out=is.null&clock_in=gte.{today}T00:00:00")

# Revenue today (paid invoices)
paid_today = fetch("repair_orders", f"status=eq.paid&updated_at=gte.{today}T00:00:00")
revenue_today = sum(float(ro.get("total_amount", 0) or 0) for ro in paid_today)

# Invoiced but not yet paid
awaiting_payment = [ro for ro in open_ros if ro.get("status") == "invoiced"]
outstanding_amount = sum(float(ro.get("total_amount", 0) or 0) for ro in awaiting_payment)

# Active diagnoses
diagnosing = [ro for ro in open_ros if ro.get("status") in ["diagnosing", "received"]]

print("=" * 55)
print(f"  DAILY SNAPSHOT — {SHOP.upper()}")
print(f"  {today}")
print("=" * 55)
print(f"\n  SHOP FLOOR")
print(f"  {'Open ROs:':<28} {len(open_ros)}")
for status, count in sorted(status_counts.items()):
    label = status.replace("_", " ").title()
    print(f"    {label + ':':<26} {count}")
print(f"\n  {'Techs Clocked In:':<28} {len(clocked_in)}")
for t in clocked_in:
    name = t.get("technician_name", "Unknown")
    clock_in = t.get("clock_in", "")[:16].replace("T", " ")
    print(f"    {name} (in since {clock_in})")

print(f"\n  MONEY")
print(f"  {'Revenue Today:':<28} ${revenue_today:,.2f}")
print(f"  {'Awaiting Payment:':<28} ${outstanding_amount:,.2f}  ({len(awaiting_payment)} invoices)")

print(f"\n  ACTIVE DIAGNOSES: {len(diagnosing)}")
for ro in diagnosing[:5]:
    v = f"{ro.get('year','')} {ro.get('make','')} {ro.get('model','')}".strip()
    tech = ro.get("assigned_tech", "unassigned")
    print(f"    {ro.get('ro_number','?')}  {v}  [{tech}]")
if len(diagnosing) > 5:
    print(f"    ... and {len(diagnosing)-5} more")

print("\n" + "=" * 55)
print("  --- DASHBOARD READY ---")
```

---

### REVENUE — Financial Report
Revenue by period with breakdowns.

```python
import urllib.request, json, urllib.parse
from datetime import date, timedelta

SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY = "YOUR_SUPABASE_KEY"
SHOP = "[SHOP_NAME]"
PERIOD = "[today|week|month]"   # default: month

headers = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}

today = date.today()
if PERIOD == "today":
    start_date = today.isoformat()
elif PERIOD == "week":
    start_date = (today - timedelta(days=today.weekday())).isoformat()
else:  # month
    start_date = today.replace(day=1).isoformat()

def fetch(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}&limit=500"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

shop_filter = f"&shop_name=eq.{urllib.parse.quote(SHOP)}" if SHOP != "all" else ""

# Paid in period
paid = fetch("repair_orders", f"status=eq.paid&updated_at=gte.{start_date}T00:00:00{shop_filter}")
# Invoiced (not yet paid)
invoiced = fetch("repair_orders", f"status=eq.invoiced{shop_filter}")
# All closed this period
closed = fetch("repair_orders", f"status=in.(paid,picked_up)&updated_at=gte.{start_date}T00:00:00{shop_filter}")

total_collected = sum(float(ro.get("total_amount", 0) or 0) for ro in paid)
total_outstanding = sum(float(ro.get("total_amount", 0) or 0) for ro in invoiced)

# Revenue by tech
by_tech = {}
for ro in paid:
    tech = ro.get("assigned_tech", "Unassigned")
    by_tech[tech] = by_tech.get(tech, 0) + float(ro.get("total_amount", 0) or 0)

# Labor hours in period
hours_data = fetch("tech_time_entries", f"clock_in=gte.{start_date}T00:00:00{shop_filter}")
total_hours = sum(float(e.get("hours_worked", 0) or 0) for e in hours_data)

print("=" * 55)
print(f"  REVENUE REPORT — {SHOP.upper()}")
print(f"  Period: {PERIOD.upper()} (from {start_date})")
print("=" * 55)
print(f"\n  COLLECTED")
print(f"  {'Total Revenue:':<30} ${total_collected:>10,.2f}")
print(f"  {'Jobs Invoiced & Paid:':<30} {len(paid):>10}")
print(f"  {'Avg Per Job:':<30} ${(total_collected/len(paid) if paid else 0):>10,.2f}")

print(f"\n  OUTSTANDING")
print(f"  {'Invoiced / Awaiting Payment:':<30} ${total_outstanding:>10,.2f}")
print(f"  {'# Open Invoices:':<30} {len(invoiced):>10}")

print(f"\n  LABOR")
print(f"  {'Total Hours Billed:':<30} {total_hours:>10.1f} hrs")
print(f"  {'Revenue Per Hour:':<30} ${(total_collected/total_hours if total_hours else 0):>10,.2f}")

if by_tech:
    print(f"\n  BY TECHNICIAN")
    for tech, rev in sorted(by_tech.items(), key=lambda x: -x[1]):
        tech_hrs = sum(float(e.get("hours_worked",0) or 0) for e in hours_data if e.get("technician_name") == tech)
        rph = rev/tech_hrs if tech_hrs else 0
        print(f"  {tech:<22} ${rev:>8,.2f}  ({tech_hrs:.1f} hrs @ ${rph:.0f}/hr)")

print("\n" + "=" * 55)
print("  --- REVENUE REPORT READY ---")
```

---

### SHOP BOARD — Floor Status
All open jobs, where they are in the pipeline.

```python
import urllib.request, json, urllib.parse
from datetime import datetime

SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY = "YOUR_SUPABASE_KEY"
SHOP = "[SHOP_NAME]"

headers = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}

def fetch(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}&limit=200"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

shop_filter = f"&shop_name=eq.{urllib.parse.quote(SHOP)}" if SHOP != "all" else ""
open_ros = fetch("repair_orders", f"status=neq.picked_up&status=neq.closed&order=created_at{shop_filter}")

# Order the pipeline display
PIPELINE_ORDER = [
    "received", "diagnosing", "estimate_ready", "awaiting_approval",
    "approved", "in_repair", "repair_complete", "invoiced", "paid"
]

PIPELINE_LABELS = {
    "received": "RECEIVED — Waiting for tech",
    "diagnosing": "DIAGNOSING — In bay",
    "estimate_ready": "ESTIMATE READY — Waiting for approval",
    "awaiting_approval": "AWAITING APPROVAL — Customer notified",
    "approved": "APPROVED — Ready to start repair",
    "in_repair": "IN REPAIR — Wrench time",
    "repair_complete": "REPAIR COMPLETE — Awaiting invoice",
    "invoiced": "INVOICED — Awaiting payment",
    "paid": "PAID — Awaiting pickup"
}

by_status = {}
for ro in open_ros:
    s = ro.get("status", "unknown")
    by_status.setdefault(s, []).append(ro)

print("=" * 65)
print(f"  SHOP BOARD — {SHOP.upper()}")
print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  {len(open_ros)} open jobs")
print("=" * 65)

for status in PIPELINE_ORDER:
    jobs = by_status.get(status, [])
    if not jobs:
        continue
    print(f"\n  [{len(jobs)}] {PIPELINE_LABELS.get(status, status.upper())}")
    print(f"  {'RO Number':<20} {'Vehicle':<25} {'Tech':<15} {'Est $':<10}")
    print(f"  {'-'*68}")
    for ro in jobs:
        ro_num = ro.get("ro_number", "?")
        vehicle = f"{ro.get('year','')} {ro.get('make','')} {ro.get('model','')}".strip()[:24]
        tech = (ro.get("assigned_tech") or "Unassigned")[:14]
        est = f"${float(ro.get('estimate_amount',0) or 0):,.0f}"
        print(f"  {ro_num:<20} {vehicle:<25} {tech:<15} {est:<10}")

# Alerts
alerts = []
for ro in open_ros:
    status = ro.get("status", "")
    created = ro.get("created_at", "")[:10]
    if created and (datetime.now() - datetime.strptime(created, "%Y-%m-%d")).days > 3:
        vehicle = f"{ro.get('year','')} {ro.get('make','')} {ro.get('model','')}".strip()
        alerts.append(f"  [AGE] {ro.get('ro_number','?')} — {vehicle} — {created} ({status})")

if alerts:
    print(f"\n  ATTENTION — Jobs Over 3 Days Old:")
    for a in alerts:
        print(a)

print("\n" + "=" * 65)
print("  --- BOARD READY ---")
```

---

### TECH STATS — Technician Productivity
Hours worked, jobs completed, revenue generated per tech.

```python
import urllib.request, json, urllib.parse
from datetime import date, timedelta

SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY = "YOUR_SUPABASE_KEY"
SHOP = "[SHOP_NAME]"
PERIOD = "week"   # today | week | month

headers = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}

today = date.today()
if PERIOD == "today":
    start_date = today.isoformat()
elif PERIOD == "week":
    start_date = (today - timedelta(days=today.weekday())).isoformat()
else:
    start_date = today.replace(day=1).isoformat()

def fetch(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}&limit=500"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

shop_filter = f"&shop_name=eq.{urllib.parse.quote(SHOP)}" if SHOP != "all" else ""

time_entries = fetch("tech_time_entries", f"clock_in=gte.{start_date}T00:00:00{shop_filter}")
paid_ros = fetch("repair_orders", f"status=eq.paid&updated_at=gte.{start_date}T00:00:00{shop_filter}")
clocked_in = fetch("tech_time_entries", f"clock_out=is.null{shop_filter}")

# Build tech stats
techs = {}
for entry in time_entries:
    name = entry.get("technician_name", "Unknown")
    if name not in techs:
        techs[name] = {"hours": 0, "jobs": 0, "revenue": 0, "entries": 0}
    techs[name]["hours"] += float(entry.get("hours_worked", 0) or 0)
    techs[name]["entries"] += 1

for ro in paid_ros:
    tech = ro.get("assigned_tech", "Unassigned")
    if tech in techs:
        techs[tech]["jobs"] += 1
        techs[tech]["revenue"] += float(ro.get("total_amount", 0) or 0)

# Currently clocked in
currently_in = {e.get("technician_name"): e.get("clock_in","")[:16].replace("T"," ") for e in clocked_in}

print("=" * 65)
print(f"  TECH PRODUCTIVITY — {SHOP.upper()}")
print(f"  Period: {PERIOD.upper()} (from {start_date})")
print("=" * 65)

print(f"\n  {'TECHNICIAN':<20} {'HRS':>6} {'JOBS':>6} {'REVENUE':>10} {'$/HR':>7} {'STATUS'}")
print(f"  {'-'*63}")

for name, stats in sorted(techs.items(), key=lambda x: -x[1]["revenue"]):
    hrs = stats["hours"]
    jobs = stats["jobs"]
    rev = stats["revenue"]
    rph = rev / hrs if hrs > 0 else 0
    status = "CLOCKED IN" if name in currently_in else ""
    print(f"  {name:<20} {hrs:>6.1f} {jobs:>6} ${rev:>9,.2f} ${rph:>6.0f} {status}")

total_hrs = sum(s["hours"] for s in techs.values())
total_rev = sum(s["revenue"] for s in techs.values())
total_jobs = sum(s["jobs"] for s in techs.values())
print(f"  {'-'*63}")
print(f"  {'TOTAL':<20} {total_hrs:>6.1f} {total_jobs:>6} ${total_rev:>9,.2f} ${(total_rev/total_hrs if total_hrs else 0):>6.0f}")

if currently_in:
    print(f"\n  CURRENTLY CLOCKED IN:")
    for name, clock_in in currently_in.items():
        print(f"    {name} — in since {clock_in}")

print("\n" + "=" * 65)
print("  --- TECH STATS READY ---")
```

---

### ACCURACY — Diagnostic Scorecard
Synth's diagnostic accuracy across all cases.

```python
import urllib.request, json, urllib.parse
from datetime import date, timedelta

SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY = "YOUR_SUPABASE_KEY"
SHOP = "[SHOP_NAME]"   # "all" for full platform view

headers = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}

def fetch(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}&limit=1000"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

shop_filter = f"&shop_name=eq.{urllib.parse.quote(SHOP)}" if SHOP != "all" else ""

all_cases = fetch("diagnostic_case_studies", f"select=diagnosis_outcome,shop_name,year,make,model,dtc_codes,confirmed_date{shop_filter}")

correct = [c for c in all_cases if c.get("diagnosis_outcome") == "confirmed_correct"]
incorrect = [c for c in all_cases if c.get("diagnosis_outcome") == "confirmed_incorrect"]
pending = [c for c in all_cases if c.get("diagnosis_outcome") in ["pending", None, ""]]

total = len(all_cases)
confirmed_total = len(correct) + len(incorrect)
accuracy = (len(correct) / confirmed_total * 100) if confirmed_total > 0 else 0

# Recent month
month_start = date.today().replace(day=1).isoformat()
recent_correct = [c for c in correct if (c.get("confirmed_date") or "") >= month_start]
recent_incorrect = [c for c in incorrect if (c.get("confirmed_date") or "") >= month_start]
recent_pending = [c for c in pending]

# By shop breakdown (if all shops)
by_shop = {}
for c in all_cases:
    shop = c.get("shop_name", "Unknown")
    if shop not in by_shop:
        by_shop[shop] = {"correct": 0, "incorrect": 0, "pending": 0}
    outcome = c.get("diagnosis_outcome", "pending")
    if outcome == "confirmed_correct":
        by_shop[shop]["correct"] += 1
    elif outcome == "confirmed_incorrect":
        by_shop[shop]["incorrect"] += 1
    else:
        by_shop[shop]["pending"] += 1

print("=" * 55)
print(f"  DIAGNOSTIC ACCURACY SCORECARD")
print(f"  Scope: {SHOP.upper()}")
print("=" * 55)
print(f"\n  ALL TIME")
print(f"  {'Total Cases:':<30} {total:>6}")
print(f"  {'Confirmed Correct:':<30} {len(correct):>6}")
print(f"  {'Confirmed Incorrect:':<30} {len(incorrect):>6}")
print(f"  {'Pending Confirmation:':<30} {len(pending):>6}")
print(f"  {'Accuracy (confirmed):':<30} {accuracy:>5.1f}%")

print(f"\n  THIS MONTH")
print(f"  {'Confirmed Correct:':<30} {len(recent_correct):>6}")
print(f"  {'Confirmed Incorrect:':<30} {len(recent_incorrect):>6}")

if incorrect:
    print(f"\n  INCORRECT DIAGNOSES (Review):")
    for c in incorrect[:10]:
        v = f"{c.get('year','')} {c.get('make','')} {c.get('model','')}".strip()
        shop = c.get("shop_name","?")
        dtcs = str(c.get("dtc_codes",""))[:30]
        print(f"    {v} | {shop} | {dtcs}")

if pending:
    print(f"\n  PENDING CONFIRMATION ({len(pending)} cases):")
    for c in pending[:10]:
        v = f"{c.get('year','')} {c.get('make','')} {c.get('model','')}".strip()
        shop = c.get("shop_name","?")
        dtcs = str(c.get("dtc_codes",""))[:30]
        print(f"    {v} | {shop} | {dtcs}")

if SHOP == "all" and len(by_shop) > 1:
    print(f"\n  BY SHOP")
    print(f"  {'Shop':<20} {'Correct':>8} {'Wrong':>7} {'Pending':>8} {'Accuracy':>9}")
    print(f"  {'-'*55}")
    for shop_name, stats in sorted(by_shop.items()):
        conf = stats['correct'] + stats['incorrect']
        acc = (stats['correct'] / conf * 100) if conf > 0 else 0
        print(f"  {shop_name:<20} {stats['correct']:>8} {stats['incorrect']:>7} {stats['pending']:>8} {acc:>8.1f}%")

print("\n" + "=" * 55)
print("  --- SCORECARD READY ---")
```

---

### OUTSTANDING — What Needs Attention
Unpaid invoices, pending cases, stalled ROs.

```python
import urllib.request, json, urllib.parse
from datetime import datetime, timedelta

SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY = "YOUR_SUPABASE_KEY"
SHOP = "[SHOP_NAME]"

headers = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}

def fetch(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}&limit=200"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

shop_filter = f"&shop_name=eq.{urllib.parse.quote(SHOP)}" if SHOP != "all" else ""
now = datetime.now()

# Unpaid invoices
invoiced = fetch("repair_orders", f"status=eq.invoiced{shop_filter}")
# Awaiting customer approval (estimate sent, no response)
awaiting = fetch("repair_orders", f"status=eq.awaiting_approval{shop_filter}")
# Pending diagnostic confirmations
pending_cases = fetch("diagnostic_case_studies", f"diagnosis_outcome=eq.pending{shop_filter}")
# Jobs not updated in 24+ hours (potentially stuck)
cutoff = (now - timedelta(hours=24)).isoformat()
active_statuses = "status=in.(received,diagnosing,in_repair)"
all_active = fetch("repair_orders", f"{active_statuses}&updated_at=lt.{cutoff}{shop_filter}")

unpaid_total = sum(float(r.get("total_amount",0) or 0) for r in invoiced)

print("=" * 60)
print(f"  OUTSTANDING ITEMS — {SHOP.upper()}")
print(f"  {now.strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# Unpaid invoices
print(f"\n  UNPAID INVOICES ({len(invoiced)}) — Total: ${unpaid_total:,.2f}")
if invoiced:
    for ro in sorted(invoiced, key=lambda x: float(x.get("total_amount",0) or 0), reverse=True):
        v = f"{ro.get('year','')} {ro.get('make','')} {ro.get('model','')}".strip()
        amt = float(ro.get("total_amount",0) or 0)
        customer = ro.get("customer_name","?")
        inv_date = (ro.get("updated_at") or "")[:10]
        print(f"    {ro.get('ro_number','?'):<18} {customer:<18} {v:<22} ${amt:>7,.2f}  (sent {inv_date})")
else:
    print("    None — all clear")

# Awaiting approval
print(f"\n  AWAITING CUSTOMER APPROVAL ({len(awaiting)})")
if awaiting:
    for ro in awaiting:
        v = f"{ro.get('year','')} {ro.get('make','')} {ro.get('model','')}".strip()
        est = float(ro.get("estimate_amount",0) or 0)
        customer = ro.get("customer_name","?")
        sent_date = (ro.get("updated_at") or "")[:10]
        days_waiting = (now - datetime.strptime(sent_date, "%Y-%m-%d")).days if sent_date else "?"
        print(f"    {ro.get('ro_number','?'):<18} {customer:<18} ${est:>7,.0f}  ({days_waiting} days waiting)")
else:
    print("    None")

# Pending diagnostic confirmations
print(f"\n  PENDING DIAGNOSTIC CONFIRMATIONS ({len(pending_cases)})")
if pending_cases:
    for c in pending_cases:
        v = f"{c.get('year','')} {c.get('make','')} {c.get('model','')}".strip()
        shop = c.get("shop_name","?")
        dtcs = str(c.get("dtc_codes",""))[:25]
        print(f"    {v} | {shop} | {dtcs}")
else:
    print("    None — all diagnosed cases confirmed")

# Stalled jobs (no update in 24hrs)
print(f"\n  STALLED JOBS — No Update in 24+ Hours ({len(all_active)})")
if all_active:
    for ro in all_active:
        v = f"{ro.get('year','')} {ro.get('make','')} {ro.get('model','')}".strip()
        status = ro.get("status","?")
        last = (ro.get("updated_at") or "")[:16].replace("T"," ")
        print(f"    {ro.get('ro_number','?'):<18} {v:<25} [{status}]  last: {last}")
else:
    print("    None — all active jobs updated recently")

print("\n" + "=" * 60)
print("  --- OUTSTANDING REVIEW COMPLETE ---")
```

---

### WEEKLY — Full Weekly Report
Complete week-in-review across all KPIs.

```python
import urllib.request, json, urllib.parse
from datetime import date, timedelta, datetime

SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY = "YOUR_SUPABASE_KEY"
SHOP = "[SHOP_NAME]"

headers = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}
today = date.today()
week_start = (today - timedelta(days=today.weekday())).isoformat()
prev_week_start = (today - timedelta(days=today.weekday()+7)).isoformat()

def fetch(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}&limit=500"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

shop_filter = f"&shop_name=eq.{urllib.parse.quote(SHOP)}" if SHOP != "all" else ""

# This week
paid_this = fetch("repair_orders", f"status=eq.paid&updated_at=gte.{week_start}T00:00:00{shop_filter}")
new_ros_this = fetch("repair_orders", f"created_at=gte.{week_start}T00:00:00{shop_filter}")
hours_this = fetch("tech_time_entries", f"clock_in=gte.{week_start}T00:00:00{shop_filter}")
cases_this = fetch("diagnostic_case_studies", f"confirmed_date=gte.{week_start}{shop_filter}")

# Last week (for comparison)
paid_last = fetch("repair_orders", f"status=eq.paid&updated_at=gte.{prev_week_start}T00:00:00&updated_at=lt.{week_start}T00:00:00{shop_filter}")

rev_this = sum(float(r.get("total_amount",0) or 0) for r in paid_this)
rev_last = sum(float(r.get("total_amount",0) or 0) for r in paid_last)
rev_change = ((rev_this - rev_last) / rev_last * 100) if rev_last > 0 else 0
rev_arrow = "+" if rev_change >= 0 else ""

hrs_this = sum(float(e.get("hours_worked",0) or 0) for e in hours_this)
jobs_closed = len(paid_this)
new_jobs = len(new_ros_this)
cases_confirmed = len(cases_this)

# Tech breakdown
by_tech_rev = {}
by_tech_hrs = {}
for ro in paid_this:
    t = ro.get("assigned_tech","Unassigned")
    by_tech_rev[t] = by_tech_rev.get(t,0) + float(ro.get("total_amount",0) or 0)
for e in hours_this:
    t = e.get("technician_name","Unknown")
    by_tech_hrs[t] = by_tech_hrs.get(t,0) + float(e.get("hours_worked",0) or 0)

# Current open
open_ros = fetch("repair_orders", f"status=neq.picked_up&status=neq.closed{shop_filter}")

print("=" * 60)
print(f"  WEEKLY REPORT — {SHOP.upper()}")
print(f"  Week of {week_start}")
print("=" * 60)

print(f"\n  BUSINESS SUMMARY")
print(f"  {'Revenue Collected:':<30} ${rev_this:>10,.2f}  ({rev_arrow}{rev_change:.1f}% vs last week)")
print(f"  {'Jobs Closed (Paid):':<30} {jobs_closed:>10}")
print(f"  {'New Jobs Opened:':<30} {new_jobs:>10}")
print(f"  {'Labor Hours Billed:':<30} {hrs_this:>10.1f} hrs")
print(f"  {'Cases Confirmed:':<30} {cases_confirmed:>10}")
print(f"  {'Avg Revenue Per Job:':<30} ${(rev_this/jobs_closed if jobs_closed else 0):>10,.2f}")

print(f"\n  TECH PERFORMANCE THIS WEEK")
print(f"  {'Name':<22} {'Revenue':>10} {'Hours':>7} {'$/Hr':>7}")
print(f"  {'-'*48}")
all_techs = set(list(by_tech_rev.keys()) + list(by_tech_hrs.keys()))
for t in sorted(all_techs, key=lambda x: -by_tech_rev.get(x,0)):
    rev = by_tech_rev.get(t,0)
    hrs = by_tech_hrs.get(t,0)
    rph = rev/hrs if hrs > 0 else 0
    print(f"  {t:<22} ${rev:>9,.2f} {hrs:>7.1f} ${rph:>6.0f}")

print(f"\n  CURRENT PIPELINE ({len(open_ros)} open jobs)")
from collections import Counter
status_counts = Counter(ro.get("status","?") for ro in open_ros)
for status, count in sorted(status_counts.items()):
    label = status.replace("_"," ").title()
    bar = "#" * count
    print(f"  {label:<28} {count:>3}  {bar}")

if rev_change > 10:
    print(f"\n  HIGHLIGHT: Revenue up {rev_arrow}{rev_change:.1f}% vs last week")
elif rev_change < -10:
    print(f"\n  ATTENTION: Revenue down {rev_change:.1f}% vs last week — review pipeline")

print("\n" + "=" * 60)
print("  --- WEEKLY REPORT COMPLETE ---")
```

---

### TECH ACCURACY — Technician Diagnostic Scorecard
Per-tech accuracy, Synth-guided vs independent cases, hours, and jobs via tech_scorecard view.

```python
import urllib.request, json, urllib.parse

SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY = "YOUR_SUPABASE_KEY"
SHOP = "[SHOP_NAME]"   # "all" for all shops

headers = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}

def fetch(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}&limit=200"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

shop_filter = f"shop_name=eq.{urllib.parse.quote(SHOP)}" if SHOP != "all" else ""
rows = fetch("tech_scorecard", shop_filter)

if not rows:
    print("No scorecard data found")
else:
    print("=" * 80)
    print(f"  TECH DIAGNOSTIC SCORECARD")
    print(f"  Scope: {SHOP.upper()}")
    print("=" * 80)
    print(f"  {'TECH':<20} {'SHOP':<16} {'CASES':>6} {'CORRECT':>8} {'WRONG':>6} {'ACC%':>6} {'SYNTH':>6} {'INDEP':>6} {'HRS':>6} {'JOBS':>5}")
    print(f"  {'-'*78}")
    for r in rows:
        print(f"  {(r.get('tech_name') or ''):<20} "
              f"{(r.get('shop_name') or ''):<16} "
              f"{r.get('total_cases',0):>6} "
              f"{r.get('correct',0):>8} "
              f"{r.get('incorrect',0):>6} "
              f"{float(r.get('accuracy_pct') or 0):>5.1f}% "
              f"{r.get('synth_guided',0):>6} "
              f"{r.get('independent',0):>6} "
              f"{float(r.get('total_hours') or 0):>6.1f} "
              f"{r.get('jobs_completed',0):>5}")
    print("=" * 80)
    print("  --- TECH SCORECARD READY ---")
```

**Output format**:
```
TECH DIAGNOSTIC SCORECARD
Scope: EST AUTO
================================================================================
TECH                 SHOP             CASES  CORRECT  WRONG   ACC%  SYNTH  INDEP   HRS  JOBS
--------------------------------------------------------------------------------
Mike M.              Est Auto             8        8      0  100.0%      5      3   22.5     8
Sarah K.             Est Auto             3        2      1   66.7%      1      2   11.0     3
================================================================================
```

---

### ALL SHOPS — Multi-Shop Rollup
Admin only. Compare all shops side by side.

```python
import urllib.request, json
from datetime import date, timedelta

SUPABASE_URL = "https://fcqejcrxtrqdxybgyueu.supabase.co"
SERVICE_KEY = "YOUR_SUPABASE_KEY"
# ADMIN ONLY — no shop filter

headers = {"apikey": SERVICE_KEY, "Authorization": f"Bearer {SERVICE_KEY}"}
today = date.today()
month_start = today.replace(day=1).isoformat()

def fetch(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?{params}&limit=1000"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

shops = fetch("shops", "is_active=eq.true&order=shop_name")
paid_month = fetch("repair_orders", f"status=eq.paid&updated_at=gte.{month_start}T00:00:00")
open_all = fetch("repair_orders", "status=neq.picked_up&status=neq.closed")
hours_month = fetch("tech_time_entries", f"clock_in=gte.{month_start}T00:00:00")
accuracy_data = fetch("diagnostic_case_studies", "select=shop_name,diagnosis_outcome")
invoiced_all = fetch("repair_orders", "status=eq.invoiced")

# Aggregate by shop
shop_data = {}
for s in shops:
    name = s.get("shop_name", s.get("name", "Unknown"))
    shop_data[name] = {
        "revenue": 0, "jobs_paid": 0, "open_jobs": 0, "hours": 0,
        "correct": 0, "incorrect": 0, "pending_cases": 0, "outstanding": 0
    }

for ro in paid_month:
    name = ro.get("shop_name","Unknown")
    if name in shop_data:
        shop_data[name]["revenue"] += float(ro.get("total_amount",0) or 0)
        shop_data[name]["jobs_paid"] += 1

for ro in open_all:
    name = ro.get("shop_name","Unknown")
    if name in shop_data:
        shop_data[name]["open_jobs"] += 1

for ro in invoiced_all:
    name = ro.get("shop_name","Unknown")
    if name in shop_data:
        shop_data[name]["outstanding"] += float(ro.get("total_amount",0) or 0)

for e in hours_month:
    name = e.get("shop_name","Unknown")
    if name in shop_data:
        shop_data[name]["hours"] += float(e.get("hours_worked",0) or 0)

for c in accuracy_data:
    name = c.get("shop_name","Unknown")
    if name in shop_data:
        outcome = c.get("diagnosis_outcome","pending")
        if outcome == "confirmed_correct": shop_data[name]["correct"] += 1
        elif outcome == "confirmed_incorrect": shop_data[name]["incorrect"] += 1
        else: shop_data[name]["pending_cases"] += 1

total_rev = sum(d["revenue"] for d in shop_data.values())
total_jobs = sum(d["jobs_paid"] for d in shop_data.values())
total_open = sum(d["open_jobs"] for d in shop_data.values())
total_outstanding = sum(d["outstanding"] for d in shop_data.values())

print("=" * 75)
print(f"  ALL SHOPS ROLLUP — ADMIN VIEW")
print(f"  Month of {month_start[:7]}  |  {len(shop_data)} shops")
print("=" * 75)
print(f"\n  {'SHOP':<20} {'REVENUE':>10} {'JOBS':>5} {'OPEN':>5} {'OWED':>9} {'HRS':>6} {'ACC%':>6}")
print(f"  {'-'*65}")
for name, d in sorted(shop_data.items(), key=lambda x: -x[1]["revenue"]):
    conf = d["correct"] + d["incorrect"]
    acc = (d["correct"]/conf*100) if conf > 0 else 0
    print(f"  {name:<20} ${d['revenue']:>9,.0f} {d['jobs_paid']:>5} {d['open_jobs']:>5} ${d['outstanding']:>8,.0f} {d['hours']:>6.0f} {acc:>5.1f}%")
print(f"  {'-'*65}")
print(f"  {'PLATFORM TOTAL':<20} ${total_rev:>9,.0f} {total_jobs:>5} {total_open:>5} ${total_outstanding:>8,.0f}")

# Platform highlights
if shop_data:
    top_shop = max(shop_data.items(), key=lambda x: x[1]["revenue"])
    print(f"\n  TOP SHOP THIS MONTH: {top_shop[0]} (${top_shop[1]['revenue']:,.2f})")
    if total_outstanding > 0:
        print(f"  OUTSTANDING ACROSS PLATFORM: ${total_outstanding:,.2f} — follow up needed")

print("\n" + "=" * 75)
print("  --- ALL SHOPS ROLLUP COMPLETE ---")
```

---

## Output Summary

All operations end with a clean block:

```
DAILY         — Floor status, techs in, revenue today, active diagnoses
REVENUE       — Collected vs outstanding, by tech, revenue per hour
SHOP BOARD    — All open ROs by pipeline stage, age alerts
TECH STATS    — Hours, jobs, revenue per tech, currently clocked in
ACCURACY      — Diagnostic scorecard, pending confirmations, by shop
TECH ACCURACY — Per-tech scorecard: accuracy%, synth-guided vs independent, hours
OUTSTANDING   — Unpaid invoices, stalled approvals, pending cases
WEEKLY        — Full week summary + comparison to last week
ALL SHOPS     — Admin cross-shop rollup with platform totals
```

---

## Execution

Write dashboard script to temp file and run:

```bash
py -3.12 C:/Users/User/dashboard_query.py
```

Then delete:
```bash
del C:/Users/User/dashboard_query.py
```

---

## Access Control

| Role | Operations Allowed |
|------|-------------------|
| admin (Mike) | All operations including ALL SHOPS |
| owner | DAILY, REVENUE, SHOP BOARD, TECH STATS, ACCURACY, OUTSTANDING, WEEKLY for their shop only |
| counter | SHOP BOARD, OUTSTANDING for their shop only |
| tech | Not applicable — no dashboard access |
