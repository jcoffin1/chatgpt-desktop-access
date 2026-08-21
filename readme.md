# Codex Status Announcer

Codex Status Announcer exposes live Codex desktop progress through NVDA speech
and braille in both browse mode and focus mode.

## Settings

Open **NVDA Settings > Codex Status Announcer** to configure:

- Minimal or Full progress labels (Full is the default).
- Speech and braille independently.
- Optional redaction of likely secrets and personal data.
- The interval for elapsed working-time updates.
- A recurring “Still working in background” pulse in Minimal and Full modes,
  with gentle alternating two-note earcons.
- Individual progress categories.
- Plain-language Codex commentary updates in both Minimal and Full modes.
- Completion sounds and sanitized diagnostic logging.
- A choice of original soft click earcons or musical tones for every
  announcement, including while speech is enabled. Clicks are the default.
- Idle polling frequency.
- Soft, Normal, or Loud click levels, with an action selector and separate
  sound-only and speech-only preview buttons.
- Editable announcement wording for every action, with a restore button and
  `{message}`, `{activity}`, and `{seconds}` placeholders for live details.
- Per-category routing to all enabled channels, speech, sound, braille, or off.
- A maximum background-activity timeout.
- High-priority permission and user-input alerts.
- Configurable application process names for future Codex hosts.
- Direct buttons for checking Codex usage statistics and opening the official
  credit-purchase area. The add-on never makes a purchase automatically.

The **Test current announcement outputs** button verifies the selected speech
and braille channels, including progress sounds. The **Test command progress sound** button plays the selected command sound
directly, regardless of the current speech settings.
Choose an action under **Preview action**, then use **Preview selected sound**
or **Preview selected speech** to hear only that one output. Previews never run
the full sound collection automatically.
To customize an announcement, select its action, enter the desired wording in
**Announcement text**, and save Settings. Leave the field blank—or choose
**Restore built-in announcement**—to use the add-on's standard wording. For
example, `Still busy with {activity} after {seconds} seconds` retains live
background-progress details. Use `{message}` wherever the original Full-mode
command or progress text should appear in custom wording.

After each newly installed version starts for the first time, NVDA opens a
concise **What's new?** dialog. **View current release notes…** and **View
complete release history…** are also available in the add-on's Settings panel.

## Input gestures

No keyboard gestures are assigned by default, preventing conflicts with NVDA or
other add-ons. Open **NVDA > Preferences > Input Gestures**, expand **Codex
Status Announcer**, and assign only the commands you want. Available actions
include repeat latest, previous/next history, show or clear history, pause or
resume, toggle Minimal/Full, toggle privacy redaction, and show diagnostics.
Unbound actions are also available for opening usage statistics and usage
credits in the official Codex dashboard.

Announcement history contains at most 20 entries, stays in memory, and is
cleared when the monitored Codex document changes or NVDA exits.

## Privacy

Full mode may speak commands, paths, file names, URLs, and search terms. NVDA's
debug log records spoken output, regardless of the add-on's sanitized internal
logging. Enable redaction or Minimal mode before sharing an NVDA log, and review
logs for private data before sending them to anyone.

The privacy-redaction action can be assigned in Input Gestures for temporary
privacy changes. Sanitized diagnostics report configuration and monitoring
state without including command text.

## Braille timing

Progress uses NVDA's standard braille flash-message mechanism. Its duration is
controlled by NVDA's global braille message-timeout setting.

## Installation and removal

Install the `.nvda-addon` package through NVDA's Add-on Store manager. Restart
NVDA when requested. Remove or disable it from the same manager. Upgrades retain
saved settings; new features use safe defaults.

## Support and compatibility

The add-on supports NVDA 2023.1 and later and has been tested with NVDA 2026.2.
If a Codex interface update stops announcements, enable sanitized diagnostics
and provide an NVDA log after removing remote keys and other personal data.
