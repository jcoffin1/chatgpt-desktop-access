# Changelog

All notable changes to Codex Access Toolkit for NVDA, formerly Codex Status
Announcer, are recorded here. The active release line follows stable NVDA.

## 2026.2.1

### What to test

- In browse mode, place the browse cursor on ChatGPT's empty **Do anything** prompt
  and press Braille dot-8 once. Confirm NVDA enters focus mode without a Prompt
  submitted sound, Working sound, or elapsed-time announcement.
- With the empty prompt already in focus mode, press physical Enter or Braille dot-8.
  Confirm the Toolkit remains idle because no prompt was submitted.
- Type a prompt rapidly with the physical keyboard and submit it. Repeat with a
  Braille display, including contracted Braille. Confirm the Prompt submitted sound
  occurs immediately and the first elapsed announcement starts from the real submit.
- Submit a second prompt after the first task completes. Confirm task feedback starts
  once, elapsed time resets to zero, and no keystroke or Braille chord is consumed.
- Run `build.ps1` and confirm all automated, translation, syntax, archive, sound,
  gesture, and reproducibility checks pass.

### Fixed

- Stopped Braille dot-8 from falsely starting task feedback when it is used only to
  activate ChatGPT's empty prompt from NVDA browse mode. Prompt-submission feedback
  now requires focus mode plus evidence of existing or just-entered prompt text.
- Stopped browse-mode Braille quick-navigation chords from being recorded as prompt
  typing. This prevents a later empty Enter from inheriting false typing evidence.
- Added regression coverage for browse-mode activation, empty focus-mode Enter, rapid
  Braille typing, and immediate real submission without claiming the user's gesture.

## 2026.2.0

### What to test

- Install the package manually and restart NVDA. Confirm Add-on Store manager,
  Settings, diagnostics, and release notes all report version 2026.2.0.
- Open **NVDA Settings > Codex Access Toolkit** and confirm the panel contains
  eight clearly named pages: General, Speech and Braille, Sounds, Activity
  Output, Wording and Preview, Browser Access, Advanced, and Support. Use
  Control+Tab and Shift+Control+Tab to move through every page.
- Test ChatGPT in both focus mode and browse mode. Confirm Thinking, commentary,
  commands, searches, file operations, builds, tools, permissions, and completion
  use the selected speech, Braille, and sound routes without duplicate output.
- Start a long task, leave ChatGPT, and return. Confirm background status remains
  available, the Working sound begins only after a prompt is submitted, continues
  only while the task is active, and stops promptly on completion or cancellation.
- Type long prompts with a physical keyboard and a Braille display. Confirm input
  is responsive, contracted Braille retains the first cell of each new word, Enter
  submits without leaving stale text, and Shift+Enter still inserts a new line.
- In a large streaming conversation, read an older response with speech or Braille.
  Confirm ordinary response updates do not displace the browse cursor, speech, or
  Braille line. Permission dialogs and urgent alerts must still interrupt normally.
- Press Control+1 through Control+0 in ChatGPT and confirm the ten most recent
  messages are read in order. Confirm these keys pass through outside ChatGPT and
  remain independently configurable in NVDA's Input Gestures dialog.
- Open searchable chat history. Confirm Recent and Archived chats are separate,
  chats open correctly, and Shift+F10 places focus on an available Pin, Archive,
  Unarchive, or Open action without freezing NVDA.
- Trigger permission, plug-in installation, and other ChatGPT pop-up dialogs.
  Confirm focus moves to each dialog, its essential text is announced, and exposed
  installation progress is reported without taking focus from an unrelated app.
- Open ChatGPT's embedded browser or web preview. Confirm entry, exit, useful page
  titles, and exposed ten-percent loading steps are announced once. Confirm native
  roles, states, actions, Tab behavior, NVDA+Space, and quick navigation remain intact.
- Export settings, preview each speech or sound action independently, edit custom
  announcement wording, and save a sanitized support report. Reopen Settings and
  confirm values persist without exposing chat text, commands, paths, or secrets.
- Run `build.ps1` and confirm unit tests, translation-template validation, Python
  syntax, archive layout, sound assets, gestures, and reproducible-build checks pass.

### Added

- Added structured Full and Minimal speech profiles. Full remains the default and
  can include exact commentary, commands, file changes, builds, and tool activity;
  Minimal gives concise but meaningful activity and completion summaries.
- Added independent speech, sound, Braille, and disabled output routing for every
  activity category, with editable announcement wording and individual previews.
- Added click earcons and musical tones for prompt submission, thinking, commands,
  searches, file work, builds, tools, permissions, completion, attachment, and
  working state, including Soft, Normal, and Loud click levels.
- Added a continuous, non-interfering Working sound that starts when a prompt is
  submitted, continues during active background work, and stops when work ends.
- Added active, inactive, and ChatGPT-closed feedback while preventing navigation
  and task switching from falsely starting the Working sound.
- Added searchable Recent and Archived chat lists with keyboard navigation, bounded
  loading, open and unarchive actions, and native chat actions through Shift+F10.
- Added ten independently configurable recent-message actions. Control+1 through
  Control+0 are the defaults and can be changed in NVDA's Input Gestures dialog.
- Added focused handling for permission requests, ChatGPT pop-ups, new chats, and
  plug-in installation progress.
- Added optional background commentary and autonomous-activity feedback plus an
  assignable action to hear the latest complete Codex progress without switching apps.
- Added accessible access to Add files and more, model selection, and permission
  controls while preserving their native behavior.
- Added eight keyboard-accessible Settings pages, per-page access keys, accessible
  help and release-note documents, settings import/export, and sanitized diagnostics.
- Added conservative embedded-browser descriptions, focus transitions, page-title
  announcements, loading progress, and a dedicated help document.
- Added deterministic translation-template generation, compiled-catalog packaging,
  automated accessibility fixtures, GitHub validation, issue forms, contribution
  guidance, security guidance, and Add-on Store metadata tooling.

### Changed

- Aligned the add-on version, package name, runtime constant, release notes, build
  tooling, tests, documentation, issue forms, translation metadata, and declared
  stable NVDA compatibility with NVDA 2026.2. Future add-on-only patches use
  2026.2.1, 2026.2.2, and so on until a newer stable NVDA release.
- Renamed the add-on to Codex Access Toolkit for NVDA to reflect its broader speech,
  Braille, sound, chat navigation, dialog, browser, and control-access features.
- Organized Settings into General, Speech and Braille, Sounds, Activity Output,
  Wording and Preview, Browser Access, Advanced, and Support pages.
- Replaced a single verbosity switch with configurable Full and Minimal profiles
  while retaining verbose developer-oriented output as the default.
- Replaced the combined preview with separate preview actions so speech and every
  sound can be evaluated independently.
- Moved all keyboard assignments into NVDA's Input Gestures dialog; no new fixed
  shortcuts are introduced when a configurable action is sufficient.
- Routed progress, duplicates, privacy redaction, speech, sounds, and Braille through
  shared category and priority rules for consistent foreground and background output.
- Preserved the Codex conversation virtual buffer while focus is inside a recognized
  embedded browser, allowing task monitoring to continue in focus and browse modes.
- Normalized packaged text line endings so identical source produces a reproducible
  add-on archive across LF and CRLF checkouts.

### Fixed

- Stabilized speech, Braille, and the browse cursor in large conversations. Ordinary
  streamed response updates no longer replace an older passage being read in browse
  mode when reading protection is enabled. Focus-mode output, permissions, dialogs,
  urgent alerts, and completion state continue normally.
- Replaced unconditional whole-document polling with event-marked inspections and a
  lightweight housekeeping timer. Idle ChatGPT monitoring is event-driven, and the
  compatibility fallback is bounded to protect NVDA's main thread.
- Suspended fallback scans and prompt-local text inspection during active typing so
  Braille input does not compete with Chromium virtual-buffer traversal.
- Protected contracted-Braille composition from Chromium's delayed caret event for
  the preceding word, preventing missing first cells and scrambled input without
  consuming or replacing NVDA's Braille gestures.
- Removed expensive browser-ancestry walks from ordinary prompt edits, toolbar
  controls, status buttons, and other objects that cannot be embedded-browser controls.
- Restored immediate Prompt submitted sounds for physical Enter and standalone
  Braille dot-8 Enter without claiming or replacing the input gesture.
- Corrected click-volume scaling so Soft, Normal, and Loud produce distinct levels,
  and made Working clicks slower, clearer, and non-overlapping with event earcons.
- Corrected musical-tone mode so active work has an audible continuing indicator.
- Stopped stale Working and file-operation states after completion, cancellation,
  navigation, a closed ChatGPT window, or a transient Chromium object replacement.
- Replaced vague elapsed output with category-aware durations such as file operations
  still running for one minute and twenty-five seconds.
- Fixed chat-history opening, archived-chat loading, unarchive focus, and Shift+F10
  chat actions while keeping retries bounded and off blocking NVDA paths.
- Prevented chat switches, empty conversations, browser pages, and unrelated busy
  controls from being mistaken for newly submitted tasks.
- Kept focus on permission dialogs and other ChatGPT pop-ups and placed focus on the
  appropriate action after unarchiving a chat.
- Prevented routine Toolkit Braille flash messages from taking the reading position;
  urgent messages remain available and respect NVDA's Braille message timeout.
- Isolated every NVDA event hook, speech call, Braille call, tone, click, dialog,
  history load, and completion classifier so one failure cannot break monitoring or
  stop the rest of NVDA's event chain.
- Restored the completion-sound classifier and failure-safe completion beep, preventing
  completion events from detaching monitoring or flooding the NVDA log.
- Prevented false embedded-browser entry from ChatGPT's native Browser menu and
  prevented unrelated downloads from being reported as browser loading progress.

### Earlier development history

Earlier development established focus- and browse-mode virtual-buffer discovery,
speech and Braille status output, configurable verbosity, activity sounds, editable
announcements, chat history and actions, recent-message reading, dialog focus,
background monitoring, privacy redaction, diagnostics, and extensive NVDA main-thread
and Braille-input safeguards. Exact legacy version labels remain available in Git
history; the active source and packaged documentation now use the current release line.
