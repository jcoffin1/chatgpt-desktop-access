# Contributing

Thank you for helping improve ChatGPT Desktop Access for NVDA.

## Before opening an issue

- Confirm the problem occurs with the newest published add-on.
- Restart NVDA once and reproduce the problem in both focus mode and browse
  mode when relevant.
- Run the add-on's sanitized support-report command or button.
- Remove chat text, commands, paths, account information, tokens, and other
  private data before attaching an NVDA log.

## Code changes

1. Keep NVDA event handlers fast and exception-isolated.
2. Do not add default keyboard gestures unless the project explicitly approves
   them. New commands should normally appear unassigned in NVDA's Input
   Gestures dialog.
3. Preserve behavior outside supported ChatGPT processes.
4. Add or update tests, including anonymized accessibility fixtures when the
   ChatGPT interface changes.
5. Update `changelog.md`, including a **What to test** section.
6. Update the translation template with
   `python tools/extract_messages.py`.
7. Run `build.ps1` and verify that a second build has the same SHA-256 hash.

Pull requests are automatically tested on Windows. A passing workflow does not
replace hands-on testing with NVDA speech and Braille.
