# Codex Status Announcer

Codex Status Announcer exposes live Codex desktop progress through NVDA speech
and braille in both browse mode and focus mode.

## Settings

Open **NVDA Settings > Codex Status Announcer** to configure:

- Minimal or Full progress labels (Full is the default).
- Essential, Balanced, or Informative Minimal-speech profiles. Balanced is the
  default; Essential limits speech to critical states, while Informative adds
  safe filenames, counts, and useful timing without exposing full commands.
- Standard, Developer, or Raw Full-speech profiles. Standard announces an
  action with concise targets, counts, and useful timing; Developer preserves
  complete normalized commands and progress; Raw preserves the exact exposed
  wording. Full braille remains complete independently of the speech profile.
- Speech and braille independently.
- Optional redaction of likely secrets and personal data.
- The interval for elapsed working-time updates.
- A recurring “Still working in background” pulse in Minimal and Full modes,
  with gentle alternating two-note earcons.
- Individual progress categories.
- Plain-language Codex commentary updates in both Minimal and Full modes.
- Completion sounds and sanitized diagnostic logging.
- Immediate, optional Prompt submitted clicks with a configurable delay before
  continuous Working clicks begin.
- Prompt submission detection for Enter and the Send button, prompt cancellation
  detection, duplicate-event suppression, and isolated state across Codex tasks.
- A cancellable completion-settling window prevents commentary from being
  mistaken for the end of a task when delayed tool work follows.
- A choice of original soft click earcons or musical tones for every
  announcement, including while speech is enabled. Clicks are the default.
- Idle polling frequency.
- Soft, Normal, or Loud click levels, with an action selector and separate
  sound-only and speech-only preview buttons.
- Editable announcement wording for every action, with a restore button and
  `{message}`, `{activity}`, and `{seconds}` placeholders for live details.
- Per-category routing to all enabled channels, speech, sound, braille, or off.
- Configuration repair, compatibility self-test, sanitized support diagnostics,
  settings import/export, and focused speech-profile reset.
- Command punctuation and maximum spoken-length controls. Long complete commands
  remain available to braille and an assignable clipboard action.
- Search result counts and refresh for the Recent and Archived task lists.
- A maximum background-activity timeout.
- High-priority permission and user-input alerts.
- Configurable application process names for future Codex hosts.
- An optional continuous Working click while Codex is busy. Its interval is
  configurable, begins after a configurable start delay, and is postponed by
  other progress sounds to prevent overlap. A separate optional submission cue
  plays immediately when a populated prompt is submitted with Enter or Send.
- Optional rising and falling clicks when ChatGPT/Codex gains or loses focus,
  including an inactive cue when the app closes.
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
concise current-version summary and places focus at the top. **View current
release notes…** and **View complete release history…** are also available in
the add-on's Settings panel.

## Input gestures

No keyboard gestures are assigned by default, preventing conflicts with NVDA or
other add-ons. Open **NVDA > Preferences > Input Gestures**, expand **Codex
Status Announcer**, and assign only the commands you want. Available actions
include repeat latest, previous/next history, show or clear history, pause or
resume, toggle Minimal/Full, toggle privacy redaction, and show diagnostics.
Unbound actions are also available for opening usage statistics and usage
credits in the official Codex dashboard. **Open searchable and arrow-navigable
Codex chat history** opens a responsive dialog from focus or browse mode. Type
to search both collections, Tab from Recent chats directly to Archived chats,
use Up and Down Arrow to browse, press Enter to open the selected chat, or press
Shift+F10 for its context menu. Recent titles are cached from the sidebar.
Archived titles are read from Codex's local JSONL session metadata, so opening
Settings first is not required and no archive state is changed.

The add-on improves the native **Add files and more**, **model**, and **Change
permissions** controls without adding commands or gestures. Reach them using normal
Tab or browse-mode navigation. NVDA provides a concise description of each recognized
control and its popup navigation while preserving its native name, state, and action.
Use Enter or Space to open, arrow keys to navigate, Enter to choose, and Escape to
close.

Announcement history contains at most 20 entries, stays in memory, and is
cleared when the monitored Codex document changes or NVDA exits.

## Testing and building

Run `build.ps1` to execute the automated tests, validate Python syntax, audit
version consistency, dependencies, gesture policy, archive layout, CRCs, and
sound inventory, and create a reproducible package under `outputs`. If Python is not available as
`python`, pass its executable with `-PythonPath`. Identical source files produce
an identical package checksum. See `docs/TESTING.md` for the manual NVDA test
checklist used before publishing a release.

## Release versioning

Beginning with the next release, add-on versions follow the current stable NVDA
release. With NVDA 2026.1 stable, the base line is `2026.1` and add-on patches
are `2026.1.1`, `2026.1.2`, and so on. A newer stable NVDA release starts a new
matching line. Preview NVDA releases do not change the add-on version line.
Existing historical versions are not renamed. Version `2026.1.1` is the first
patch release under this policy. See `docs/VERSIONING.md` for full details.

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
