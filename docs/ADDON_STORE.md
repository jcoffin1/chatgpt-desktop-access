# NVDA Add-on Store preparation

ChatGPT Desktop Access uses NV Access's official Add-on Store process. All
interaction with the Store repository must be completed personally by the
publisher in a web browser. Do not use an API client, script, bot, coding
assistant, or other automation to create, edit, comment on, close, or reopen a
Store issue or pull request.

Never create a second submission while one for the same release is pending. If
the Store reports a validation failure, correct the release and use the official
form again as directed. If a reviewer asks a question, the publisher should read
it and type a reply personally.

## Before submission

1. Merge the fully tested release commit into the repository's `main` branch.
2. Create and push only the matching version tag. Do not manually create the
   GitHub Release or upload an add-on package. The tag-triggered GitHub Actions
   workflow builds, audits, publishes, downloads, and verifies the single
   correctly named `.nvda-addon` asset.
3. Wait for both the validation and release workflows to pass before using the
   release download.
4. Confirm the manifest version, minimum NVDA version, and last-tested NVDA
   version are valid entries in the Add-on Store API-version list.
5. If the last-tested NVDA API is marked experimental, use the beta or dev
   channel or wait until the Store marks it stable.
6. Download the release asset again and verify its SHA-256 checksum.
7. Generate local metadata for review only. This command does not submit it:

```powershell
python .\tools\addon_store_metadata.py `
  .\outputs\chatGPTDesktopAccess-2026.2.5.nvda-addon `
  https://github.com/jcoffin1/chatgpt-desktop-access/releases/download/v2026.2.5/chatGPTDesktopAccess-2026.2.5.nvda-addon `
  --output .\outputs\addonStore-2026.2.5.json
```

8. Review the generated JSON and the packaged manifest.
9. The publisher must personally open the **Add-on registration** issue form in
   the `nvaccess/addon-datastore` repository and enter the reviewed values.

New add-ons require manual submitter approval from NV Access. Automated checks,
SHA-256 validation, and VirusTotal scanning run after submission. Store
submission should happen only after the same package has passed local CI and
hands-on NVDA speech and Braille testing. Local tooling must stop at validation;
it must never perform Store repository actions.
