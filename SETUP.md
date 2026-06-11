# Detection Ledger Setup

## Repository

Public ledger: https://github.com/attestd-io/detection-ledger

## Sync after new incidents

When you add an entry to `Attestd-App/data/supply_chain_ledger.yaml`:

```bash
cd ../Attestd-App
python scripts/sync_ledger.py --ledger-repo ../detection-ledger
git -C ../detection-ledger push
```

The script updates incident JSON files, `ledger.json`, and `Attestd-website/lib/detection-ledger.ts`.

## GPG commit signing (optional)

```bash
gpg --list-secret-keys --keyid-format=long
git config user.signingkey YOUR_KEY_ID
git config commit.gpgsign true
```

Add the public key to your GitHub account. Re-run sync with:

```bash
python scripts/sync_ledger.py --ledger-repo ../detection-ledger --gpg-fingerprint YOUR_FINGERPRINT
```

Verify signatures:

```bash
git log --show-signature -1
```
