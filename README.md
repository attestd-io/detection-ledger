# Attestd Detection Ledger

Public, GPG-signed record of supply chain compromise incidents registered by Attestd.

Each incident is one commit. GitHub timestamps commits at push time. For historical
incidents registered before this repository existed, the `attestd_detected_at` field
inside each JSON file reflects internal database records. The git commit date reflects
when the ledger entry was created, not when Attestd first detected the incident.

Future incidents will be committed in real time, and the commit timestamp will match
detection time.

## Verification

Add your GPG key fingerprint to this README after configuring commit signing.

Verify a commit signature:

```bash
git log --show-signature -1
```

## Files

- `incidents/{id}.json` — one file per incident
- `ledger.json` — machine-readable index

Repository: https://github.com/attestd/detection-ledger
