# Attestd Detection Ledger

Public record of supply chain compromise incidents registered by Attestd.

See the live dashboard at [attestd.io/docs/detection-ledger](https://attestd.io/docs/detection-ledger).

This repository is an **archive** of what Attestd registered (packages, versions, source, citations). It is not a claim that Attestd beat OSV or press coverage.

## Schema

Each incident is one JSON object in `incidents/{id}.json` and one row in `ledger.json`. The index entry and incident file use the same shape.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Slug with date suffix (e.g. `litellm-2026-03-24`) |
| `display_name` | string | Human-readable package or campaign label |
| `campaign` | string \| null | Linked campaign name when part of a coordinated publish wave |
| `detection_source` | string | `osv`, `registry`, `npm_deprecation`, `pypi_yank`, `npm_registry`, `news_monitor`, `agent`, … |
| `packages` | array | Affected packages (see below) |
| `malware_type` | string | e.g. `malware`, `backdoor` |
| `attestd_detected_at` | ISO UTC \| null | When Attestd first registered the detection (alias of `observed_at`) |
| `flagged_at` | ISO UTC \| null | When flagged before full confirmation (worker-written entries) |
| `confirmed_at` | ISO UTC \| null | When corroborated or human-approved |
| `osv_earliest_published_at` | ISO UTC \| null | Earliest OSV publish timestamp (citation context) |
| `source_published_at` | ISO UTC \| null | When the originating source first published the signal/advisory |
| `observed_at` | ISO UTC \| null | When Attestd's pipeline first observed the signal |
| `ingested_at` | ISO UTC \| null | When the signal entered Attestd's production database |
| `first_served_at` | ISO UTC \| null | When the production API first returned `compromised: true` for an affected version |
| `hours_ahead_of_osv` | float \| null | **Deprecated.** Always null on new writes. Kept for schema compatibility. |
| `hours_ahead_of_press` | float \| null | **Deprecated.** Always null on new writes. Kept for schema compatibility. |
| `press_coverage_at` | ISO UTC \| null | First public press or advisory timestamp when recorded |
| `press_urls` | string[] | Citation URLs (press or advisory) |
| `advisory_url` | string | Primary advisory link when available |
| `ledger_commit_at` | ISO UTC \| null | Git commit timestamp when this entry was last pushed |
| `ledger_committed_at` | ISO UTC \| null | Alias of `ledger_commit_at` (canonical name for lead-time reporting) |

These timestamp fields are intentionally separate. Do not treat `source_published_at` as artifact publish time when the source is an OSV advisory that reused an older ID. Lead-time reporting should use `source_published_at`, `observed_at` / `first_served_at`, and `press_coverage_at` as distinct clocks.

Each element of `packages[]`:

| Field | Type | Description |
|-------|------|-------------|
| `package` | string | Exact package name on PyPI or npm |
| `ecosystem` | string | `pypi` or `npm` |
| `versions` | string[] | Compromised version strings |
| `osv_entries` | array | `[{ "osv_id", "osv_published_at" }]` |

`flagged_at` and `confirmed_at` are populated on entries written by the live ingestion worker. Backfilled launch entries (March to May 2026) may omit them or leave them null.

## Historical entries

The six launch entries (March to May 2026) were backfilled in a single commit from internal Attestd records. `attestd_detected_at` is populated where defensible from database `first_seen_at` timestamps.

From June 2026 onward, each new incident is committed individually. Live auto-push uses the GitHub contents API. Manual historical sync may create GPG-signed commits when signing is configured on the operator machine.

## Verification

Inspect commit history in this repository:

```bash
git log --oneline -20
git log --show-signature -1
```

GPG signatures apply when the committer configured signing (manual sync). Contents-API auto-push commits are public GitHub commits and may be unsigned.

## Files

- `incidents/{id}.json` — one file per incident
- `ledger.json` — machine-readable index

Repository: https://github.com/attestd-io/detection-ledger

Licensed under CC BY 4.0.
