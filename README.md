# Attestd Detection Ledger

Public record of supply chain compromise incidents registered by Attestd.

See the live dashboard at [attestd.io/docs/detection-ledger](https://attestd.io/docs/detection-ledger).

## Schema

Each incident JSON file contains:

- `id` — slug with date suffix (e.g. `litellm-2026-03-24`)
- `package`, `ecosystem`, `version` — affected package coordinates
- `press_coverage_at` — first public press or advisory timestamp (UTC)
- `attestd_detected_at` — when Attestd first registered the detection (null when unavailable)
- `hours_ahead_of_osv` — lead time vs earliest OSV publish (null when unavailable)
- `ledger_commit_at` — git commit timestamp for this entry (null until committed)

`ledger.json` is the machine-readable index. `incidents/{id}.json` holds full detail per incident.

## Historical entries

The six launch entries (March–May 2026) were backfilled in a single commit from internal
Attestd records. `attestd_detected_at` is populated where defensible from database
`first_seen_at` timestamps. Entries where detection postdates press coverage omit that field.

From June 2026 onward, each new incident is committed individually. Commits are GPG-signed
when signing is configured on the ingestion bot account.

## Verification

Verify the latest commit signature:

```bash
git log --show-signature -1
```

## Files

- `incidents/{id}.json` — one file per incident
- `ledger.json` — machine-readable index

Repository: https://github.com/attestd-io/detection-ledger

Licensed under [CC BY 4.0](LICENSE).
