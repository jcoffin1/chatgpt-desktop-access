# NVDA Add-on Store preparation

Codex Access Toolkit is prepared for submission through NV Access's official
Add-on Store process. Submission is intentionally not automated because the
maintainer must be approved for this add-on and must review the final metadata.

## Before submission

1. Publish a fully tested GitHub release with one immutable `.nvda-addon`
   package.
2. Confirm the manifest version, minimum NVDA version, and last-tested NVDA
   version are valid entries in the Add-on Store API-version list.
3. If the last-tested NVDA API is marked experimental, use the beta or dev
   channel or wait until the Store marks it stable.
4. Download the release asset again and verify its SHA-256 checksum.
5. Generate submission metadata:

```powershell
python .\tools\addon_store_metadata.py `
  .\outputs\codexAccessToolkit-2026.1.43.nvda-addon `
  https://github.com/jcoffin1/codex-access-toolkit/releases/download/v2026.1.43/codexAccessToolkit-2026.1.43.nvda-addon `
  --output .\outputs\addonStore-2026.1.43.json
```

6. Review the generated JSON and the packaged manifest.
7. Open the **Add-on registration** issue form in the
   `nvaccess/addon-datastore` repository and enter the reviewed values.

New add-ons require manual submitter approval from NV Access. Automated checks,
SHA-256 validation, and VirusTotal scanning run after submission. Store
submission should happen only after the same package has passed local CI and
hands-on NVDA speech and Braille testing.
