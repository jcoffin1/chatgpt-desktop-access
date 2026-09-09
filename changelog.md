# Changelog

All notable changes to ChatGPT Desktop Access for NVDA, formerly Codex Access
Toolkit and Codex Status Announcer, are recorded here. The active release line
follows stable NVDA.

## 2026.2.5

### What to test

- Start a task when the account has exhausted its allowance. Confirm the usage-limit
  pop-over stops the continuous Working sound immediately and announces **Usage
  limit reached** through speech and Braille. When exposed, confirm the message
  includes the reset time and the choices to upgrade or purchase more credits.
  Repeat with ChatGPT's percentage banner showing **0% usage remaining** and
  confirm it is detected even if Chromium does not announce the banner as an alert.
  Leave the pop-over open and confirm repeated accessibility events do not repeat
  the alert or restart Working feedback. Submit again and confirm a new rejection
  can be announced as a new event.
- Open a ChatGPT embedded-browser page and confirm NVDA says **Loading page** and
  **Loading complete** once for each navigation. Test a fast page, a slow page,
  Reload, Back, and Forward. Turn the Browser Access checkbox off and confirm
  those two add-on messages stop.
- In browse mode, use normal NVDA web commands for headings, links, form fields,
  landmarks, tables, and elements lists. Press Enter on a link and confirm its
  native action runs exactly once. In focus mode, confirm Tab, Shift+Tab, Enter,
  Space, arrow keys, and NVDA+Space behave exactly as they do in Microsoft Edge.
- Confirm the add-on adds no embedded-browser entries to NVDA's Input Gestures
  dialog and does not add descriptions to native page controls.
- Start a slow page load, move around its content with speech and Braille, and
  confirm loading feedback does not move focus, change browse/focus mode, scan the
  page, or relocate the Braille reading position. Close the browser during the
  load and confirm no delayed **Loading complete** message follows.
- Open chat history in Codex, note its Recent and Archived lists, switch to
  ChatGPT mode, and open history again. Confirm the dialog title says ChatGPT and
  no Codex title appears. Switch back and confirm the Codex list is restored.
- During that test, confirm the NVDA log records `conversation mode changed from
  chatgpt to codex` and then the reverse transition. Each subsequent history log
  entry must end with the same mode shown by ChatGPT's mode-switch control.
- After each switch, wait for the delayed history-classification and settled-cache
  log entries before opening history. ChatGPT's native Recents region deliberately
  combines ChatGPT chats and Codex tasks; confirm the add-on keeps only the correct
  type in each mode. The add-on must observe two matching post-switch snapshots.
  If history is opened too early, confirm NVDA says it is refreshing.
- Collapse Recents or leave older chats unloaded, then open add-on history. Confirm
  NVDA says it is loading recent chats, repeatedly uses only the native Recents
  **Show more** control, and opens the searchable dialog after the currently
  offered pages load. Alt+Tab away during loading and confirm expansion stops
  immediately.
- Load ChatGPT's accessible Archived chats view and confirm those titles appear
  only in ChatGPT history. Confirm Codex archived titles continue to come from
  the local Codex session index without first opening Settings.
- Let a long conversation expose its message controls below the recent-chat
  region, then open chat history. Confirm Share, Copy, Copy message, Read aloud,
  response-rating, regeneration, More actions, Sources, source results, and
  Outputs controls never appear as recent or archived chat titles in either
  ChatGPT or Codex mode.
- While a usage alert, account menu, or application-update notice is visible,
  open history and confirm Add credits, Upgrade, Update, reset details, plan
  controls, Settings, Help, and sign-out actions do not appear as chat titles.
- Start NVDA while Codex mode is already selected, then open chat history. Confirm
  the dialog is labeled Codex and contains Codex tasks rather than the much
  smaller ChatGPT list. Switch to ChatGPT without focusing the mode button (for
  example, activate it with a mouse or touch), open history again, and confirm the
  dialog follows the selector after one refresh without requiring an NVDA restart.

### Added

- Added terminal usage-limit detection for ChatGPT and Codex pop-overs. The alert
  reports an exposed reset time plus upgrade or credit options without speaking
  embedded URLs, and remains available in announcement history.
- Added automatic **Loading page** and **Loading complete** feedback for
  ChatGPT's embedded browser. Native document busy-state changes and exposed
  progress events are preferred; a bounded settle fallback handles pages that do
  not expose a final loading event.

### Changed

- Simplified Browser Access to native Chromium and NVDA behavior. Enter, Space,
  Tab, Shift+Tab, NVDA+Space, browse-mode quick navigation, and element lists are
  neither replaced nor simulated by the add-on.
- Reduced Browser Access settings to one loading-announcement checkbox. Removed
  the separate navigator, browser-help command, page actions, control-description
  overlay, and all browser-specific Input Gesture actions.
- Unchanged Codex session metadata is cached between history scans. The local
  session index is reread only after its source size or modification metadata
  changes, and unchanged classification summaries are no longer logged every
  polling interval.

### Fixed

- Exhausting the account allowance now clears pending completion and plug-in
  progress ownership, stops continuous Working clicks and background pulses, and
  prevents stale Thinking or Running labels beneath the pop-over from restarting
  them. Percentage banners showing zero remaining or 100 percent consumed are now
  terminal-limit evidence. A periodic virtual-buffer scan also detects the banner
  when Chromium omits its alert event. Repeated events from one visible notice are
  suppressed.
- Embedded-browser loading state now ends from a native busy-state change,
  100-percent progress, or a quiet settle timer and is canceled when focus leaves
  the browser or ChatGPT closes. Repeated events do not repeat the same start or
  completion message.
- ChatGPT and Codex chat history now use separate Recent and Archived caches.
  Changing modes closes an outdated history dialog and prevents delayed actions
  from opening a chat belonging to the previous mode.
- Active-mode detection now uses ChatGPT's exposed `Switch mode, current mode`
  control. The top-level document remains named ChatGPT while Codex is active;
  that host name can no longer overwrite the authoritative Codex mode during
  later focus events.
- ChatGPT's native Recents region is a unified list of ChatGPT chats and Codex
  tasks, regardless of which product mode is selected. The add-on now partitions
  that list with the active local Codex session index: ChatGPT history excludes
  active Codex task titles, and Codex history retains only those task titles.
- History mode verification now queries the live ChatGPT/Codex selector through
  Windows UI Automation when Chromium omits that control from NVDA's virtual
  buffer. The targeted query runs on NVDA's UI Automation worker instead of its
  main thread. Until verification completes, the add-on asks the user to retry
  history instead of opening a confidently wrong ChatGPT or Codex cache.
  Duplicate session-index records are resolved to their latest entry and archived
  task IDs are excluded. Logs report only aggregate kept and excluded counts.
- Opening add-on history now expands ChatGPT's native Recents list in ten-item
  pages before displaying the searchable dialog. It activates only the exact
  **Show more** button found inside the scanned Recents region, waits for the
  accessible item count to increase between actions, stops if ChatGPT loses focus,
  and caps one request at 20 pages to prevent an unbounded main-thread loop.
  **Show more**, **Show less**, and loading labels are excluded from chat titles.
- A newly selected mode's sidebar must now remain settled for 750 milliseconds
  and produce two matching snapshots at least 250 milliseconds apart before its
  titles can replace that mode's history cache. An early scan is discarded and
  automatically rescheduled. A candidate identical to the other mode's current
  cache is also rejected, and history refuses to open an unsettled cache.
  Privacy-safe log entries report classification, item, and overlap counts without
  recording any chat title.
- History dialog titles, empty-list notices, and errors now identify the active
  ChatGPT or Codex mode instead of always referring to Codex.
- Chat history now filters transcript and message-action controls even when
  Chromium does not expose a reliable boundary after the recent-chat region.
  The first conversation marker now ends history collection, the Recents region
  cannot restart inside message text, and alternate Main landmark metadata is
  recognized. Items such as Share, Copy, Read aloud, response ratings, Sources,
  source results, Outputs, and More actions can no longer become chat titles.
- Usage alerts and account or application controls interleaved with Chromium's
  Recents accessibility stream are no longer treated as chats. This includes
  Add credits, Upgrade, Update, reset information, plan controls, and account
  menu actions. A usage-alert marker also ends the active Recents region so later
  controls from the same pop-over cannot leak into history.

## 2026.2.4

### What to test

- Upgrade from 2026.2.3 and confirm existing settings and Input Gestures assignments
  remain unchanged.
- In Add-on Manager, open the add-on's Help document and confirm the README opens
  successfully at the top.
- Smoke-test speech, Braille, sounds, prompt submission, recent-message review,
  chat history, voice controls, and completion in both focus and browse modes;
  behavior should match 2026.2.3.
- Confirm the archive contains exactly 63 ordered entries and 51 tiered WAV files,
  including `readme.md`, `changelog.md`, and `LICENSE.txt`, with no root-level
  legacy sounds, translation template, cache files, or duplicate entries.
- Confirm GitHub publishes `chatGPTDesktopAccess-2026.2.4.nvda-addon` from the
  audited CI build and that the downloaded release asset has the same SHA-256
  checksum as the validated package.

### Fixed

- Corrected release packaging so the documentation, complete changelog, and GPL
  license are installed with the add-on.
- Excluded thirteen obsolete un-tiered sound files and the developer gettext
  template from release packages. Only the current Soft, Normal, and Loud sound
  sets are installed.
- Standardized the public release filename as
  `chatGPTDesktopAccess-2026.2.4.nvda-addon` while retaining the internal
  `codexStatusAnnouncer` identity for safe upgrades.
- Added a tag-triggered GitHub Actions release workflow that builds and audits
  the package, verifies reproducibility, publishes only that validated artifact,
  downloads it again, and confirms its checksum and archive layout.
- Kept source syntax audits scoped to project files so generated output folders
  and temporary validation dependencies cannot change release-audit results.

### Compatibility

- Runtime accessibility behavior is unchanged from 2026.2.3. This is a packaging
  and release-process correction only.

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
- Expanded the GitHub issue chooser with structured bug, feature,
  accessibility, compatibility, and documentation/support forms, plus direct
  links to security guidance, setup documentation, and published releases.

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
