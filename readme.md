# ChatGPT Desktop Access for NVDA

ChatGPT Desktop Access supports both ChatGPT mode and Codex mode in the Windows app.
It automatically reattaches after switching modes or returning from the usage page;
no NVDA restart is required.

[![Validate NVDA add-on](https://github.com/jcoffin1/chatgpt-desktop-access/actions/workflows/ci.yml/badge.svg)](https://github.com/jcoffin1/chatgpt-desktop-access/actions/workflows/ci.yml)

ChatGPT Desktop Access for NVDA provides live activity announcements,
Braille, progress sounds, chat navigation and actions, and accessible dialog
focus in both browse mode and focus mode. It was formerly named Codex Access
Toolkit and Codex Status Announcer; the internal add-on identifier remains
unchanged so existing settings and Input Gestures assignments continue working.

## Download

Download tested packages from the
[GitHub Releases page](https://github.com/jcoffin1/chatgpt-desktop-access/releases).
The project is being prepared for the official NVDA Add-on Store, but it is not
listed there yet.

## Settings

Open **NVDA Settings > ChatGPT Desktop Access**. The panel is divided into eight
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
- Optional conversation reading protection keeps routine add-on progress and ordinary
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
- A searchable Embedded Browser Navigator with category filters for browser
  controls, headings, landmarks, links, buttons, form fields, and tables. It can
  move to an item without activating it and exposes native activation separately.
- Explicit page actions for a structural summary, an in-memory accessible text
  snapshot, copying the exposed address, opening the current HTTP or HTTPS page in
  the default browser, restoring a remembered navigator location, refreshing the
  page list, and returning directly to the ChatGPT prompt.
- Browser scans run only after a user command and are divided into bounded slices.
  They never poll the page continuously, log page content, or move focus automatically.
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

Settings export proposes `chatgpt-desktop-access-settings.json` as the filename;
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
Gestures > ChatGPT Desktop Access**, so every default can be replaced or removed.
The shortcuts work in focus and browse modes. NVDA+Alt+V starts or ends ChatGPT
voice mode, and NVDA+Alt+M mutes or unmutes the voice-mode microphone. These two
actions can also be changed or removed in Input Gestures. All twelve commands are
implemented by ChatGPT's application module rather than a global plug-in binding,
so both default and reassigned gestures are claimed only while ChatGPT has focus.
Outside ChatGPT, NVDA and other add-ons remain free to use the same keystrokes.
Assign only the additional commands you want. Available actions
include repeat latest, previous/next history, show or clear history, pause or
resume, toggle Minimal/Full, toggle privacy redaction, show or copy diagnostics,
and save a sanitized support report. Additional application-scoped, unassigned
actions open Embedded Browser Navigator, read a page summary, show an accessible
page snapshot, open the current page externally, and return to the ChatGPT prompt.
Unbound actions are also available for opening usage statistics and usage
credits in the official Codex dashboard. **Open searchable and arrow-navigable
ChatGPT or Codex chat history** opens a responsive, mode-specific dialog from
focus or browse mode. ChatGPT's native Recents region intentionally combines
ChatGPT chats and Codex tasks. The add-on separates that unified region using
the active local Codex session index, so ChatGPT history excludes Codex task
titles and Codex history retains only Codex task titles. Type to search both
collections, Tab from Recent chats directly to Archived chats, use Up and Down
Arrow to browse, and press Enter to open the selected chat. On a Recent chat,
Shift+F10 closes the history dialog and places focus on ChatGPT's Pin, Unpin, or
Archive button without activating it. The add-on reads ChatGPT's exposed
current-mode control because
the application document itself remains named ChatGPT in both modes. Codex
archived titles are read from its local JSONL session
metadata. ChatGPT archived titles come only from ChatGPT's accessible Archived
chats view; if that view has not been exposed yet, the dialog explains how to
load it. Message controls and source panels such as Share, Copy, Read aloud,
response ratings, Sources, Outputs, and More actions are excluded from both
lists. After changing modes, the add-on waits for the unified sidebar to settle,
confirms two matching snapshots, and then partitions its entries. An early
history command reports that the list is refreshing instead of showing an
unclassified list. When the native Recents list offers **Show more**, opening
history activates that exact Recents control one page at a time, waits for the
accessible item count to grow, and then displays the settled searchable list.
Each request is limited to 20 ten-item pages so a very large account cannot trap
NVDA in an unlimited loading loop; reopening history continues if more pages
remain. This expands every page currently offered through ChatGPT's native
**Show more** control; it does not simulate scrolling when the app chooses its
infinite-scroll layout. The expansion stops if focus leaves ChatGPT. No archive
state is changed merely by opening history.

The add-on improves the native **Add files and more**, **model**, and **Change
permissions** controls without adding commands or gestures. Reach them using normal
Tab or browse-mode navigation. NVDA provides a concise description of each recognized
control and its popup navigation while preserving its native name, state, and action.
Use Enter or Space to open, arrow keys to navigate, Enter to choose, and Escape to
close.

## Embedded browser access

When ChatGPT exposes a browser or web-preview container through Chromium
accessibility, the add-on recognizes objects beneath that explicitly named
container. It also recognizes a genuine web document nested inside ChatGPT's outer
document, which is how some browser tabs are exposed. The native Browser submenu
and its commands are deliberately excluded. The add-on does not click, submit,
move focus, replace native commands, or read the page on the user's behalf. Native
browse mode and focus mode therefore remain in control: use Tab and Shift+Tab for
controls, NVDA+Space to switch modes, and the usual H, K, F, and D browse-mode
navigation commands inside page content.

The add-on keeps its original Codex conversation virtual buffer while focus is
inside the embedded page. This allows Codex activity monitoring to continue
without treating the page as a new task or detaching from the conversation. All
browser enhancements can be turned off independently on the Browser Access page.

To use Browser Navigator, assign **Open the searchable Embedded Browser Navigator**
under **NVDA > Preferences > Input Gestures > ChatGPT Desktop Access**. The command
is available only while ChatGPT or Codex has focus. Search by typing, select a
category, and use the result list with the arrow keys. Enter or **Move to item**
moves to the native object without activating it. Use **Activate item** or
Shift+F10 only when you intend to invoke a link, button, or browser action.

Page summaries expose only the page title, domain, loading state, and structural
counts. Accessible snapshots contain text already exposed to NVDA, remain in
memory, and are not written to logs or files. When privacy redaction is enabled,
likely secrets and personal paths are redacted from navigator presentation and
snapshots. Scans inspect no more than 900 accessibility objects and yield at least
every 20 objects or 8 milliseconds, with a 15-millisecond pause between slices,
so speech, Braille, and keyboard input remain responsive. Remembered locations
cover at most sixteen pages and are restored only after an explicit user action.

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
the base line is `2026.2.0` and add-on patches are `2026.2.1`, `2026.2.2`,
`2026.2.3`, `2026.2.4`, `2026.2.5`, and so on. A newer stable NVDA release starts a new matching line. Preview NVDA releases
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
controlled by NVDA's global braille message-timeout setting. Routine add-on Braille
messages are suppressed while focus is in ChatGPT when Keep conversation reading stable
is enabled. While the user reads in browse mode, ordinary streamed `Response:`,
`ChatGPT said:`, and `Response complete` live-region updates are also withheld from
NVDA's native output handler, preventing them from replacing speech, the browse cursor,
or the Braille viewport. Non-urgent add-on completion flashes are withheld from Braille
at the same time, while their selected speech and sound output continues. Focus-mode
response output, permission prompts, dialogs, and urgent alerts are never suppressed.
Full conversation-buffer inspection is paused while the prompt is being edited and for
three seconds after keyboard or Braille navigation in a conversation. Direct status and
permission events remain available without waiting for a scan. When Chromium replaces
its buffer, the add-on inspects only a bounded tail instead of copying the full chat.
After a final response, Working pulses and continuous sounds pause while the add-on
waits five seconds for another operation and requires the Stop control to be absent; it
then confirms the task is idle. Closing or hiding the ChatGPT window for two seconds
clears retained activity even if Electron helper processes remain. Simply moving to
another application keeps monitoring active.
While contracted Braille is entered in the focused ChatGPT prompt, the add-on also
protects an active new-word composition from the delayed caret event Chromium can emit
for the preceding word. This does not change translation tables, consume Braille
gestures, replace NVDA's input handler, or run outside the ChatGPT prompt.

## Installation and removal

Install the `.nvda-addon` package through NVDA's Add-on Store manager. Restart
NVDA when requested. Remove or disable it from the same manager. Upgrades retain
saved settings; new features use safe defaults.

## Support and compatibility

The add-on supports NVDA 2023.1 and later and has been tested with stable NVDA
2026.2.
If a Codex interface update stops announcements, enable sanitized diagnostics
and provide an NVDA log after removing remote keys and other personal data.
