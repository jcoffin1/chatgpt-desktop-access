# Changelog

All notable changes to ChatGPT Desktop Access for NVDA, formerly Codex Access
Toolkit and Codex Status Announcer, are recorded here. The active release line
follows stable NVDA.

## 2026.2.3

### What to test

- Upgrade from 2026.2.2 and confirm NVDA Add-on Manager displays **ChatGPT
  Desktop Access for NVDA** while preserving all settings and Input Gestures
  assignments.
- Confirm NVDA Settings, Input Gestures, current release notes, diagnostics,
  settings import/export, and support-report dialogs use the new public name.
- Confirm documentation, package names, and release links point to the renamed
  `chatgpt-desktop-access` repository.
- In ChatGPT and Codex modes, smoke-test speech, Braille, sounds, prompt
  submission, recent-message review, chat history/actions, dialogs, voice
  controls, and completion in both focus and browse modes.
- Build the package twice and confirm identical SHA-256 checksums, a valid
  archive layout, current translations, and complete Add-on Store metadata.

### Changed

- Renamed the public product from **Codex Access Toolkit for NVDA** to
  **ChatGPT Desktop Access for NVDA** to reflect its support for both ChatGPT
  and Codex experiences.
- Moved public project and release links to the renamed
  `jcoffin1/chatgpt-desktop-access` GitHub repository.
- Renamed release packages, settings exports, support reports, CI artifacts,
  and the translation template to use the new product name.
- Added the required empty translations collection to generated NVDA Add-on
  Store metadata.

### Compatibility

- The internal add-on ID, Python module names, and configuration section remain
  `codexStatusAnnouncer`, so upgrades retain settings, gesture assignments, and
  compatibility with existing installations.
- This patch changes branding and release packaging only. Runtime accessibility
  behavior is unchanged from 2026.2.2.

## 2026.2.2

### What to test

- In Codex mode, submit a prompt and confirm prompt submission, Thinking, commentary,
  commands, file work, continuous Working feedback, completion, Braille, and sounds
  behave as configured in both NVDA focus mode and browse mode.
- Submit a non-empty prompt with physical Enter, numpad Enter, and Braille dot-8.
  Confirm each message is sent exactly once, the prompt clears, prompt-submission
  feedback starts, and NVDA does not play its log-error sound. Confirm Shift+Enter
  still inserts a new line without submitting.
- In both focus mode and browse mode, press NVDA+Alt+V with voice mode stopped and
  active. Confirm it starts and ends voice mode respectively. Press NVDA+Alt+M while
  voice mode is active and confirm it mutes and unmutes only the microphone, never
  the nearby speaker control. Confirm each action first reports the requested change
  and then reports success only after the native button state changes. Reassign or
  remove the actions in Input Gestures and confirm the custom assignments are honored.
- Reassign a recent-message or voice command to a gesture used by another NVDA add-on.
  Confirm it activates the Toolkit command in ChatGPT, then move outside ChatGPT and
  confirm the other add-on receives the same gesture without Toolkit interference.
- Upgrade over a build where a recent-message or voice command was customized or its
  default was removed. Confirm that assignment or removal is retained after restart.
- Switch to ChatGPT mode and repeat the same test. Confirm immediate activity events
  are announced without waiting for the fallback buffer poll.
- Open the usage page, allow usage to reset if applicable, and return to either mode.
  Confirm monitoring automatically reattaches without restarting NVDA.
- Open an embedded browser page from either mode. Confirm its page content is not
  misclassified as task commentary and the separate browser announcements still work.
- Open permission and other pop-up dialogs in both modes. Confirm focus enters each
  dialog and urgent information remains available in speech and Braille.
- Restart NVDA while ChatGPT is already open. Without first entering the prompt,
  invoke chat history from an older message, the top of the browse-mode document,
  and a sidebar chat. Confirm the Recent and Archived lists open each time.
- In a large active conversation, read several paragraphs with browse-mode keys and
  Braille scrolling commands while new response text arrives. Confirm the browse
  cursor and Braille viewport remain at the selected passage.
- Pause navigation and let the task finish. Confirm monitoring resumes, completion is
  spoken or sounded normally, and **Response complete** does not replace the Braille
  passage being read. Confirm permission dialogs still move focus and remain available.
- Let a task finish while ChatGPT is in the background. Confirm Working feedback stops
  within about five seconds after the final response. Then start another task, close the
  ChatGPT window, and confirm all retained activity stops without waiting for its helper
  processes to exit. Alt+Tab away without closing it and confirm monitoring continues.
- Install on stable NVDA 2026.2 and confirm the package is accepted as compatible.
- Run `build.ps1` and confirm all automated, translation, syntax, archive, sound,
  gesture, and reproducibility checks pass.

### Added

- Added configurable voice-mode controls with NVDA+Alt+V as the default for starting
  or ending voice mode and NVDA+Alt+M as the default for muting or unmuting the
  microphone. The actions locate and activate ChatGPT's exact native buttons in both
  focus and browse modes, report the requested transition in speech and Braille, and
  never match the separate speaker-mute control. Voice and recent-message commands
  now live on ChatGPT's application module, so default and reassigned bindings are
  claimed only in ChatGPT and cannot block another add-on elsewhere.

### Fixed

- Preserved existing Input Gestures customizations and default-command removals when
  migrating recent-message and voice commands from the global plug-in to ChatGPT's
  application module. Unrelated global mappings are never moved.
- Changed the packaged update channel from development to the stable default so the
  manifest agrees with the stable Add-on Store metadata and NVDA 2026.2 release target.
- Removed global key emulation from the twelve application-specific commands. NVDA's
  user gesture map can now scope customized bindings by the ChatGPT/Codex app-module
  class instead of bypassing a global plug-in focus check.
- Voice controls now announce an in-progress transition first and report success only
  after the corresponding native Start, Stop, Mute, or Unmute state is found. A failed
  or delayed interface action no longer produces a false success announcement.
- Added first-class support for both ChatGPT and Codex conversation document names.
  Immediate status and commentary events in ChatGPT mode no longer depend on slower
  whole-buffer polling.
- Mode changes now clear the previous task's busy state, preventing a continuous
  Working sound from carrying across a usage page or ChatGPT/Codex mode transition.
- Current-activity reports name ChatGPT while ChatGPT mode is active and retain Codex
  wording in Codex mode. Shared monitoring and new-chat messages are mode neutral.
- Required both `chatgpt` and `codex` NVDA app-module hosts in migrated, imported,
  and newly saved settings so a host-process change cannot silently disable support.
- Expanded conversation recognition to the **Message ChatGPT** and **Send a message**
  prompt variants used outside Codex mode.
- Kept nested embedded-browser documents excluded from conversation activity handling.
- Restored chat-history access when focus is on a top-level or browse-mode ChatGPT
  object. Buffer validation now happens while walking NVDA's focus ancestors instead
  of rejecting the request before the conversation document is reached.
- Embedded-browser recovery skips its nested web buffer and can retain or locate the
  outer ChatGPT/Codex conversation buffer safely.
- Preserved browse-mode reading when Chromium rebuilds the live region with a new
  tree-interceptor object. Reading protection now follows the retained conversation
  buffer instead of trusting a transient event object's identity.
- Suppressed the exact **Response complete** live-region variant, which previously
  bypassed the colon-based check and displaced the Braille line at task completion.
- Deferred whole-conversation status scans for three seconds after keyboard or Braille
  navigation. Direct activity and permission events continue immediately while large
  virtual-buffer reads wait until the user pauses.
- Replaced the full-transcript read performed during a Chromium buffer refresh with a
  bounded 8,192-character tail read, preventing large chats from blocking NVDA's main
  thread merely to determine whether a new blank chat opened.
- Suppressed non-urgent completion flash messages in Braille while browse-mode reading
  protection is active; speech and sounds continue, and urgent prompts are never hidden.
- Restored the minimum NVDA compatibility declaration to NVDA 2023.1 instead of
  incorrectly requiring a newer NVDA release, while keeping stable NVDA 2026.2 as
  the tested ceiling for this release line.
- Reduced the tentative final-response settling period from 30 seconds to five seconds.
  A missing Stop control and quiet activity scan are still required, and later work
  cancels the candidate. Working pulses and continuous sounds pause immediately during
  that confirmation, so completed tasks no longer produce false progress feedback.
- Tracked the outer ChatGPT window independently of its background helper processes.
  Closing or hiding that window for two seconds now discards its stale virtual buffer and
  clears speech, Braille, pulses, and continuous Working sounds; Alt+Tab does not.
- Preferred NVDA's current `braille.input` API and retained the legacy `brailleInput`
  import only as a fallback, removing the deprecation warning found in the NVDA log.
- Stopped NVDA's generic multiline-edit Enter handler from inspecting ChatGPT's
  already-replaced prompt object after submission. Physical Enter, numpad Enter, and
  Braille dot-8 now remain native while avoiding the misleading log-error sound and
  IA2 `COMError`; Shift+Enter continues to create a line break.

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

- Added development-channel compatibility for NVDA alpha-57626,71bae80b
  (2026.3.0.57626) and later.
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
