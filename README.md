# Attestd Detection Ledger

Public record of supply chain compromise incidents registered by Attestd.

See the live dashboard at [attestd.io/docs/detection-ledger](https://attestd.io/docs/detection-ledger).

## Schema

Each incident is one JSON object in `incidents/{id}.json` and one row in `ledger.json`. The index entry and incident file use the same shape.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Slug with date suffix (e.g. `litellm-2026-03-24`) |
| `display_name` | string | Human-readable package or campaign label |
| `campaign` | string \| null | Linked campaign name when part of a coordinated publish wave |
| `detection_source` | string | `registry`, `osv`, `news_monitor`, or other ingestion source |
| `packages` | array | Affected packages (see below) |
| `malware_type` | string | e.g. `malware`, `backdoor` |
| `attestd_detected_at` | ISO UTC \| null | When Attestd first registered the detection |
| `flagged_at` | ISO UTC \| null | When flagged before full confirmation (worker-written entries) |
| `confirmed_at` | ISO UTC \| null | When corroborated or human-approved |
| `osv_earliest_published_at` | ISO UTC \| null | Earliest OSV publish timestamp for this incident |
| `hours_ahead_of_osv` | float \| null | Lead time vs earliest OSV publish |
| `hours_ahead_of_press` | float \| null | Lead time vs first press or advisory coverage |
| `press_coverage_at` | ISO UTC \| null | First public press or advisory timestamp |
| `press_urls` | string[] | URLs contributing to press coverage |
| `advisory_url` | string | Primary advisory link when available |
| `ledger_commit_at` | ISO UTC \| null | Git commit timestamp when this entry was last pushed |

Each element of `packages[]`:

| Field | Type | Description |
|-------|------|-------------|
| `package` | string | Exact package name on PyPI or npm |
| `ecosystem` | string | `pypi` or `npm` |
| `versions` | string[] | Compromised version strings |
| `osv_entries` | array | `[{ "osv_id", "osv_published_at" }]` |

`flagged_at` and `confirmed_at` are populated on entries written by the live ingestion worker. Backfilled launch entries (March to May 2026) may omit them or leave them null.

## Historical entries

The six launch entries (March to May 2026) were backfilled in a single commit from internal Attestd records. `attestd_detected_at` is populated where defensible from database `first_seen_at` timestamps. Entries where detection postdates press coverage omit that field.

From June 2026 onward, each new incident is committed individually. Commits are GPG-signed when signing is configured on the ingestion bot account.

## Verification

Verify the latest commit signature:

```bash
git log --show-signature -1
```

## Files

- `incidents/{id}.json` — one file per incident
- `ledger.json` — machine-readable index

Repository: https://github.com/attestd-io/detection-ledger

Licensed under CC BY 4.0.
