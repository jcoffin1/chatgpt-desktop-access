# Codex Access Toolkit for NVDA

Codex Access Toolkit supports both ChatGPT mode and Codex mode in the Windows app.
It automatically reattaches after switching modes or returning from the usage page;
no NVDA restart is required.

[![Validate NVDA add-on](https://github.com/jcoffin1/codex-access-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/jcoffin1/codex-access-toolkit/actions/workflows/ci.yml)

Codex Access Toolkit for NVDA provides live Codex activity announcements,
Braille, progress sounds, chat navigation and actions, and accessible dialog
focus in both browse mode and focus mode. It was formerly named Codex Status
Announcer; the internal add-on identifier remains unchanged so existing settings
and Input Gestures assignments continue working.

## Download

Download tested packages from the
[GitHub Releases page](https://github.com/jcoffin1/codex-access-toolkit/releases).
The project is being prepared for the official NVDA Add-on Store, but it is not
listed there yet.

## Settings

Open **NVDA Settings > Codex Access Toolkit**. The panel is divided into eight
keyboard-accessible pages: **General**, **Speech and Braille**, **Sounds**,
**Activity Output**, **Wording and Preview**, **Browser Access**, **Advanced**,
and **Support**.
Press Control+Tab or Shift+Control+Tab to move between pages. Every actionable
control has a distinct Alt access key within its page. General contains the main
output choices, Activity Output contains background timing and category routing,
Advanced contains technical compatibility controls, and Support contains account,
documentation, troubleshooting, and settings-file actions. Settings include:

- Minimal or Full progress labels (Full is the default).
- Essential, Balanced, or Informative Minimal-speech profiles. Balanced is the
  default; Essential limits speech to critical states, while Informative adds
  safe filenames, counts, and useful timing without exposing full commands.
- Standard, Developer, or Raw Full-speech profiles. Standard announces an
  action with concise targets, counts, and useful timing; Developer preserves
  complete normalized commands and progress; Raw preserves the exact exposed
  wording. Full braille remains complete independently of the speech profile.
- Speech and braille independently.
- Concise, Informative, or Full Braille detail independently of speech verbosity.
- Optional conversation reading protection keeps routine Toolkit progress and ordinary
  streamed-response live updates from interrupting speech, replacing the current Braille
  line, or relocating browse-mode reading in ChatGPT. Focus-mode response output,
  important results, permission dialogs, and urgent alerts continue normally.
- Optional interruption of current NVDA speech for urgent permissions and failures.
- Optional redaction of likely secrets and personal data.
- The interval for elapsed working-time updates.
- A recurring “Still working in background” pulse in Minimal and Full modes,
  with gentle alternating two-note earcons.
- Individual progress categories. Every category item states whether it is enabled
  and its current output route, such as “Commands: enabled; speech only.”
- Plain-language Codex commentary updates in both Minimal and Full modes.
- Completion sounds and sanitized diagnostic logging.
- Immediate, optional Prompt submitted sounds with a configurable delay before
  continuous Working sounds begin.
- Prompt submission detection for Enter and the Send button, prompt cancellation
  detection, duplicate-event suppression, and isolated state across Codex tasks.
- Immediate submission detection observes unmodified keyboard Enter and a Braille
  display's standalone dot-8 Enter before ChatGPT replaces its content-editable
  prompt. The observer never claims or re-sends the gesture; Shift+Enter and all
  other input retain their native behavior.
- Prompt-typing protection suspends full Chromium compatibility scans while text is
  being entered. Prompt-local state checks are debounced until typing pauses, leaving
  NVDA's main thread available for Braille translation, editor feedback, and ordinary
  key processing.
- A cancellable completion-settling window prevents commentary from being
  mistaken for the end of a task when delayed tool work follows.
- A choice of original soft click earcons or musical tones for every
  announcement, including while speech is enabled. Clicks are the default.
- Seventeen distinct percussive click signatures. Commands, code edits, searches,
  tests, tools, commentary, attention, completion, failure, submission, background
  work, and focus changes use different rhythms, pitch direction, and textures.
- Idle polling frequency.
- Soft, Normal, or Loud click levels, with an action selector and separate
  sound-only and speech-only preview buttons.
- Editable announcement wording for every action, with a restore button and
  `{message}`, `{activity}`, `{seconds}`, and `{duration}` placeholders for live details.
- Per-category routing to all enabled channels, speech, sound, braille, or off.
- Configuration repair, compatibility self-test, sanitized support diagnostics,
  a user-chosen-file sanitized support report, settings import/export, and focused
  speech-profile reset.
- Command punctuation and maximum spoken-length controls. Long complete commands
  remain available to braille and an assignable clipboard action.
- Search result counts and refresh for the Recent and Archived task lists.
- A maximum background-activity timeout.
- High-priority permission and user-input alerts.
- Configurable application process names for future Codex hosts.
- An optional continuous Working sound while Codex is busy. Its interval is
  configurable, begins after a configurable start delay, and is postponed by
  other progress sounds to prevent overlap. It follows the selected Clicks or
  Musical tones style. A separate optional submission cue
  plays immediately when a populated prompt is submitted with Enter or Send.
- Optional rising and falling clicks when ChatGPT/Codex gains or loses focus,
  including an inactive cue when the app closes.
- Optional embedded-browser enhancements that preserve native roles, states,
  actions, and focus while adding concise navigation descriptions to recognized
  Back, Forward, Reload, Stop, address, external-browser, Close, and document
  controls.
- Optional announcements when focus enters or leaves the embedded browser, when
  its page title changes, and when recognized loading progress crosses a
  ten-percent step. Loading updates obey the existing speech, Braille, sound,
  activity-routing, duplicate-suppression, and Braille-protection settings.
- Browser recognition classifies the local role and name before inspecting Chromium
  ancestors. The primary prompt, prompt toolbar, ordinary status controls, and cached
  negative matches bypass that ancestry work so browser enhancements do not delay
  queued keyboard or Braille input.
- An accessible embedded-browser help document, available from Browser Access
  settings or as an assignable Input Gesture, which opens with focus at the top.
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
example, `Still busy with {activity} after {duration}` retains live
background-progress details. Use `{message}` wherever the original Full-mode
command or progress text should appear in custom wording.

Settings export proposes `codex-access-toolkit-settings.json` as the filename;
the user can choose a different name or location. Support reports continue to use
a timestamped text filename. Neither file is created until the user approves its
Save dialog.

After each newly installed version starts for the first time, NVDA opens a
concise current-version summary and places focus at the top. **View current
release notes…** and **View complete release history…** are also available in
the add-on's Settings panel.

## Input gestures

Control+1 through Control+0 are assigned for direct chat-message review. Control+1
reads the most recent user or ChatGPT message, Control+2 reads the
second-most-recent, and so on through Control+0 for the tenth-most-recent. Each
position is a separately named action under **NVDA > Preferences > Input
Gestures > Codex Access Toolkit**, so every default can be replaced or removed.
The shortcuts work in focus and browse modes and pass through unchanged outside
ChatGPT. No other keyboard gestures are assigned by default. Assign only the
additional commands you want. Available actions
include repeat latest, previous/next history, show or clear history, pause or
resume, toggle Minimal/Full, toggle privacy redaction, show or copy diagnostics,
and save a sanitized support report.
Unbound actions are also available for opening usage statistics and usage
credits in the official Codex dashboard. **Open searchable and arrow-navigable
Codex chat history** opens a responsive dialog from focus or browse mode. Type
to search both collections, Tab from Recent chats directly to Archived chats,
use Up and Down Arrow to browse, and press Enter to open the selected chat. On a
Recent chat, Shift+F10 closes the history dialog and places focus on ChatGPT's
Pin, Unpin, or Archive button without activating it. Recent titles are cached from the sidebar.
Archived titles are read from Codex's local JSONL session metadata, so opening
Settings first is not required and no archive state is changed.

The add-on improves the native **Add files and more**, **model**, and **Change
permissions** controls without adding commands or gestures. Reach them using normal
Tab or browse-mode navigation. NVDA provides a concise description of each recognized
control and its popup navigation while preserving its native name, state, and action.
Use Enter or Space to open, arrow keys to navigate, Enter to choose, and Escape to
close.

## Embedded browser access

When ChatGPT exposes a browser or web-preview container through Chromium
accessibility, the Toolkit recognizes objects beneath that explicitly named
container. It also recognizes a genuine web document nested inside ChatGPT's outer
document, which is how some browser tabs are exposed. The native Browser submenu
and its commands are deliberately excluded. The Toolkit does not click, submit,
move focus, replace native commands, or read the page on the user's behalf. Native
browse mode and focus mode therefore remain in control: use Tab and Shift+Tab for
controls, NVDA+Space to switch modes, and the usual H, K, F, and D browse-mode
navigation commands inside page content.

The Toolkit keeps its original Codex conversation virtual buffer while focus is
inside the embedded page. This allows Codex activity monitoring to continue
without treating the page as a new task or detaching from the conversation. All
browser enhancements can be turned off independently on the Browser Access page.

Announcement history contains at most 20 entries, stays in memory, and is
cleared when the monitored Codex document changes or NVDA exits.

## Testing and building

Run `build.ps1` to execute the automated tests, validate the translation
template and Python syntax, audit version consistency, dependencies, gesture
policy, archive layout, CRCs, and sound inventory, and create a reproducible
package under `outputs`. GitHub Actions runs the same release checks on pushes
and pull requests. If Python is not available as
`python`, pass its executable with `-PythonPath`. Identical source files produce
an identical package checksum, including across LF and CRLF Git checkouts. See
`docs/TESTING.md` for the manual NVDA test
checklist used before publishing a release. Translation contributors should see
`docs/TRANSLATING.md`; Add-on Store maintainers should see
`docs/ADDON_STORE.md`.

## Release versioning

Add-on versions follow the current stable NVDA release. With NVDA 2026.2 stable,
the base line is `2026.2.0` and add-on patches are `2026.2.1`, `2026.2.2`, and so
on. A newer stable NVDA release starts a new matching line. Preview NVDA releases
do not change the add-on version line. See `docs/VERSIONING.md` for full details.

## Privacy

Full mode may speak commands, commentary, paths, file names, URLs, and search terms. NVDA's
debug log records spoken output, regardless of the add-on's sanitized internal
logging. Enable redaction or Minimal mode before sharing an NVDA log, and review
logs for private data before sending them to anyone.

The privacy-redaction action can be assigned in Input Gestures for temporary
privacy changes. Redaction also applies to complete commentary retained for Braille,
history, and Copy latest full Codex progress. Sanitized diagnostics report configuration
and monitoring state without including command text.

## Braille timing

Progress uses NVDA's standard braille flash-message mechanism. Its duration is
controlled by NVDA's global braille message-timeout setting. Routine Toolkit Braille
messages are suppressed while focus is in ChatGPT when Keep conversation reading stable
is enabled. While the user reads in browse mode, ordinary streamed `Response:` and
`ChatGPT said:` live-region updates are also withheld from NVDA's native output handler,
preventing them from temporarily replacing speech and the Braille line. Focus-mode
response output, permission prompts, dialogs, and urgent alerts are never suppressed.
Full conversation-buffer inspection is also paused while the prompt is being
edited; direct status and permission events remain available without waiting for a scan.
While contracted Braille is entered in the focused ChatGPT prompt, the Toolkit also
protects an active new-word composition from the delayed caret event Chromium can emit
for the preceding word. This does not change translation tables, consume Braille
gestures, replace NVDA's input handler, or run outside the ChatGPT prompt.

## Installation and removal

Install the `.nvda-addon` package through NVDA's Add-on Store manager. Restart
NVDA when requested. Remove or disable it from the same manager. Upgrades retain
saved settings; new features use safe defaults.

## Support and compatibility

The add-on supports NVDA 2023.1 and later and declares compatibility through the
NVDA alpha-57626,71bae80b (2026.3.0.57626) API and later. Preview NVDA releases are tested separately and
do not raise the stable manifest compatibility value.
If a Codex interface update stops announcements, enable sanitized diagnostics
and provide an NVDA log after removing remote keys and other personal data.
