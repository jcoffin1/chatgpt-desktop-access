# Changelog

All notable changes to Codex Status Announcer are recorded here.

## 2.2.4

- Added **Check Codex usage statistics** and **Buy Codex usage credits** buttons
  to NVDA Settings.
- Added matching unbound actions to NVDA's Input Gestures dialog.
- Both actions open the signed-in official Codex Usage Dashboard, where account
  limits, recent usage, credit balance, and eligible purchase options are shown.
- The add-on does not access billing credentials or make purchases automatically.

## 2.2.3

- Added editable announcement wording for every progress action.
- Added `{message}`, `{activity}`, and `{seconds}` placeholders for retaining
  live command text and background-progress details in custom announcements.
- Added a button that restores the selected action to its built-in wording.
- Custom wording applies consistently to speech, braille, history, repeats,
  and individual speech previews.

## 2.2.2

- Replaced the automatic sound gallery with a selector for one progress action.
- Added separate sound-only and speech-only preview buttons.
- Sound previews no longer speak a label, and speech previews do not play a sound.
- Added individual previews for thinking, working, commands, searches, files,
  builds, tools, commentary, both background pulses, completion, failure, and
  permission alerts.

## 2.2.1

- Fixed focus remaining at a previous location when opening current release
  notes or complete release history from NVDA Settings.
- After confirming the expected viewer is in the foreground, the add-on moves
  NVDA's virtual cursor to the top of the newly opened document.
- The foreground-title check prevents the navigation gesture from reaching the
  Settings dialog if the browseable viewer does not open.

## 2.2.0

- Removed all preassigned keyboard gestures. Every command is now available as
  an unbound action in NVDA's Input Gestures dialog.
- Added a 20-entry, memory-only announcement history with previous, next, show,
  and clear actions.
- Added an assignable pause/resume action.
- Added urgent permission and user-input alerts that interrupt stale speech.
- Added per-category output routing: all enabled channels, speech, sound,
  braille, or off.
- Added Soft, Normal, and Loud click levels plus a complete sound gallery.
- Added smarter background updates with activity type and elapsed seconds.
- Added assignable privacy-redaction and sanitized-diagnostics actions.
- Added a first-run guide explaining privacy, Settings, and Input Gestures.
- Added a maximum busy-state timeout and task-state isolation when the Codex
  document changes.
- Added configurable supported application process names, defaulting to
  `chatgpt`, for future Codex hosts.
- Strengthened redaction for bearer credentials and remote-access keys.
- Changed the manifest author from a product name to the project contributors.
- Added licensing, installation, removal, compatibility, privacy, and support
  documentation.
- Added the same release-notes system used by Outlook Empty Message List: a
  one-time concise What's New dialog for each version, Settings buttons for the
  current notes and complete history, accessible plain-text history display,
  and versioned README and CHANGELOG files beside the package.

## 2.1.13

- Slowed multi-click rhythms slightly for clearer separation between clicks.
- Gave commands, searches, files, builds, and tools distinct rhythmic patterns.
- Made search a quick three-click pattern and tool use a compact double click.
- Increased separation in completion and failure patterns so their rising and
  descending shapes are easier to recognize.
- Made the two alternating background-progress pulses more distinct.
- Preserved the louder 2.1.12 click level and the optional musical tones.

## 2.1.12

- Increased all click-earcon levels by approximately 4 to 5 dB.
- Preserved the short envelopes and conservative peak ceiling to avoid harshness
  or clipping.
- Left the optional musical tone style unchanged.

## 2.1.11

- Added 13 original, license-free soft click earcons for progress categories.
- Made **Clicks** the default sound style for new and upgraded installations.
- Retained the existing musical **Tones** as an alternative in Settings.
- Added distinct click patterns for activity, commands, searches, file work,
  builds, tools, commentary, background progress, completion, and failure.
- The test-sound button now plays the currently selected style before saving.
- Click playback uses NVDA's audio system and falls back to tones if a WAV file
  cannot be played.

## 2.1.10

- Added an independent idle safeguard: if no recognized active status remains
  for two seconds, background pulses stop automatically.
- Brief Chromium accessibility flicker is tolerated without immediately ending
  a task.
- Added sanitized active/idle transition logging with the transition reason.
- Prevents a missed or reordered completion event from causing endless pulses.

## 2.1.9

- Fixed recurring background progress pulses continuing after a task finishes.
- Final-response commentary can no longer restart the busy state after a
  completion or failure event.
- Commentary still resets the pulse interval while a task is genuinely active.

## 2.1.8

- Fixed background progress updates stopping when Codex temporarily removes its
  visible status button while work continues.
- Tracks the work lifecycle from a recognized start event until completion.
- Replaced the heartbeat-like double tick with gentle alternating two-note
  background pulses.
- Renamed the Settings control to **recurring background progress pulse**.
- Real progress resets the pulse timer, preventing unnecessary repetition.

## 2.1.7

- Added a recurring **Still working in background** announcement while Codex
  remains active without changing its visible status.
- The heartbeat works in both Minimal and Full modes.
- Added a subtle double-tick heartbeat earcon alongside speech and braille.
- Reused the configurable background-progress interval, which defaults to five
  seconds.
- Heartbeat timing resets whenever real progress is announced and stops as soon
  as Codex becomes idle.
- Added a Settings checkbox to disable the heartbeat independently.

## 2.1.6

- Replaced flat single progress beeps with brief, gentler category earcons.
- Added distinct patterns for thinking, commands, searches, files, builds,
  tools, commentary, and other activity.
- Added a clear rising three-note completion pattern.
- Added a distinct descending three-note failure or cancellation pattern.
- Kept every pattern short to minimize interference with speech.
- Added automated tests for category distinction, duration, and failure shape.

## 2.1.5

- Progress tones now play alongside speech for every recognized announcement.
- Renamed the Settings option to **Play progress sounds for all announcements**.
- The sound option remains enabled by default and can still be turned off.
- Speech, braille, and tones remain independently controllable.
- Added automated coverage for tones with speech both enabled and disabled.

## 2.1.4

- Added a dedicated **Test command progress sound** button that works regardless
  of the current speech settings.
- Extracted the output-routing decision into an NVDA-independent helper.
- Added automated coverage for normal speech, add-on speech disabled, NVDA
  Speech Mode Off, braille continuity, disabled fallback, and missing tone
  categories.
- Excluded generated Python cache files from the release package.

## 2.1.3

- Added distinct category-based progress tones when the add-on's speech output
  is disabled or NVDA Speech Mode is Off.
- Sound fallback is enabled by default and can be changed in NVDA Settings.
- Braille flash messages continue normally while sound fallback is active.
- Avoids playing the completion fallback and optional completion sound twice.

## 2.1.2

- Assigned a unique Alt mnemonic to every control in the NVDA Settings panel.
- Added the active Minimal or Full mode to the add-on's sanitized startup log,
  making configuration problems immediately visible during diagnostics.

## 2.1.1

- Recognizes every completed shell-command label beginning with `Ran`, even
  when the accessible label does not contain the literal word `command`.
- Full/default mode speaks the complete `Ran …` label.
- Minimal mode announces the same event as “Command finished.”

## 2.1.0

- Announces Codex's plain-language commentary updates, such as explanations of
  what it is inspecting, replacing, testing, or preparing.
- Commentary is enabled by default and spoken in both Full and Minimal modes.
- Buffers streaming text until complete sentences are available, preventing
  repeated partial-word announcements.
- Added a separate Commentary checkbox in NVDA Settings.

## 2.0.0

- Added independent speech and braille output controls.
- Added per-category controls for thinking, working, commands, searches, file
  activity, builds/tests, tools, completions/failures, and other progress.
- Added a configurable interval for elapsed working-time announcements.
- Added optional Full-mode redaction for likely secrets, email addresses,
  personal path components, and URL query strings.
- Added a clear warning that NVDA debug logging records spoken Full-mode text.
- Added optional completion/failure sounds and a test-announcement button.
- Added `NVDA+Shift+P` to repeat the latest Codex progress message.
- Added `NVDA+Shift+V` to toggle Minimal and Full announcements immediately.
- Added adaptive polling: fast during activity and configurable while idle.
- Added sanitized diagnostics for unknown buttons to help support new Codex
  progress labels without exposing obvious secrets.
- Expanded detection for tests and command success, failure, and cancellation.
- Expanded automated parser, category, privacy, and timing tests.

## 1.8.1

- Changed the factory-default announcement detail from **Minimal** to **Full**.
- New installations now speak the complete Codex progress labels, including
  command text, paths, file operations, compilation details, and search terms.
- Preserves an existing user's saved Minimal or Full selection during upgrades.

## 1.8.0

- Added a Codex Status Announcer category to the NVDA Settings dialog.
- Added **Minimal** mode for brief, privacy-preserving activity summaries.
- Added **Full** mode to speak the complete progress label, including shell
  command text, file names, paths, and web-search terms when Codex exposes them.
- Added explicit detection for executing shell commands, compiling or
  transpiling, editing files, file-edit completion, and compilation completion.
- Added a settings warning that Full mode may announce sensitive information.

## 1.7.0

- Expanded recognized progress messages beyond commands and web searches.
- Announces thinking, working, analyzing, reading, writing, editing, applying
  changes, generating, searching, waiting, tool use, and completion states.
- Continues to omit potentially sensitive command text and search terms from
  speech, braille, and diagnostic logs.

## 1.6.0

- Reduced the fallback polling interval from 250 ms to 100 ms.
- Added event-triggered scans after Chromium text, name, value, live-region,
  show, focus, and foreground changes.
- Resets activity state after an idle gap so consecutive events with identical
  labels are both announced.
- Reduced duplicate suppression to half a second, enough to merge simultaneous
  object and polling reports without hiding a later repeated event.
- Stops writing full activity labels to the log because they can contain
  command text or web-search terms.

## 1.5.1

- Fixed the first activity after an idle scan being consumed as a baseline and
  therefore not announced.
- Confirmed in a live focus-mode test that command activity is detected and
  sent to both NVDA speech and braille.

## 1.5.0

- Added a focus-ancestor-cache fallback when Chromium parent traversal does not
  expose the document's virtual buffer.
- Detects activity from a button's accessible name as well as its nested text.
- Added explicit load, attachment, baseline, scan, and detection log entries to
  make live-test failures diagnosable.

## 1.4.0

- Added support for monitoring while NVDA remains in focus mode.
- The watcher now walks from the focused Codex edit field to its Chromium
  document ancestor instead of requiring the focused object itself to expose
  the virtual buffer.
- Browse mode continues to work normally.

## 1.3.0

- Removed the exact virtual-buffer title check that prevented attachment in
  the current Codex desktop build.
- Announces “Codex status monitoring active” once after successfully attaching
  to the Chromium document.
- Added diagnostic log entries for attachment, detected activity, and buffer
  inspection failures.

## 1.2.0

- Fixed virtual-buffer acquisition using the active `ChatGPT.exe` object and
  the buffer's Codex document root.
- Status detection now examines actual accessible button fields rather than
  searching all conversation text.
- Prevents ordinary messages containing phrases such as “Running command”
  from being mistaken for live activity.

## 1.1.0

- Added a lightweight watcher for Codex's Chromium virtual document.
- Fixed intermediate activity labels not being announced because Chromium does
  not send NVDA object events when those buttons change.
- Remembers the Codex document so activity can continue to be announced when
  focus moves elsewhere.

## 1.0.0

- Announces Codex planning as “Thinking.”
- Announces command execution without reading potentially sensitive commands.
- Announces web searches and completed command activity.
- Sends each status through both speech and braille.
- Suppresses repeated accessibility events and runs only in Codex documents.
