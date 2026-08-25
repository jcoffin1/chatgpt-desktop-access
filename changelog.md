# Changelog

All notable changes to Codex Status Announcer are recorded here.

## 2026.1.17

### What to test

- Import a settings file containing invalid output modes, timing values, booleans,
  and application names. Restart NVDA and confirm the panel opens with safe defaults
  and diagnostics list the repaired fields.
- Finish one task and immediately submit another with similar progress wording.
  Confirm the first Thinking or Working announcement is not suppressed and Copy
  latest full progress never returns text from the previous task.
- Switch Codex documents and confirm announcement history, duplicate suppression,
  active category, pulse sequence, and latest full progress all start cleanly.
- Open chat history and select a title that also appears elsewhere in the task.
  Confirm only an exact accessible sidebar button can be activated.
- Reload the add-on while chat history is open and after choosing a chat. Confirm
  NVDA remains responsive and no delayed action occurs after reload.
- Keep a long task open with many commentary updates and confirm NVDA memory and
  responsiveness remain stable.
- Retest speech, braille, clicks, focus and browse modes, native prompt controls,
  settings previews, release documents, and Recent and Archived chat lists.

- Expanded configuration repair to cover every category output mode, both previously
  omitted timing limits, all boolean settings, and supported application names.
- Fixed malformed imported application settings being able to break focus events and
  virtual-buffer monitoring.
- Fixed pressing OK after an import overwriting imported settings with stale panel
  values; every control now refreshes immediately from the repaired import.
- Rejects settings files larger than 1 MB to avoid blocking NVDA on an accidental
  oversized JSON import.
- Clears stale latest-progress, duplicate-suppression, active-category, and pulse data
  when changing documents or beginning a new prompt.
- Requires an exact normalized accessible chat-button name before activating a selected
  history entry, preventing conversation text or a different button from being used.
- Tracks and cancels delayed chat-history actions during add-on reload and balances
  NVDA's popup lifecycle when an open history dialog is destroyed.
- Bounds streamed-commentary bookkeeping to prevent unbounded growth in long tasks.
- Reduced archived-history memory use by retaining metadata only for the bounded set
  of archive files displayed.
- Ignores valid JSON records with the wrong shape instead of losing all archived
  history, and preserves the newest matching title metadata.
- Correctly classifies Running tests, Running build, and Running tool labels instead
  of reporting each as a generic shell command.
- Redacts quoted secrets and Windows user names containing spaces completely.
- Prevents malformed custom placeholders and unrelated window titles from interrupting
  announcements or receiving the release-viewer focus command.
- Stops sanitized diagnostic logging from recording arbitrary button labels and private
  task titles; only counts and label lengths are now written.
- Preserved the 2026.1.16 native prompt-control accessibility improvements without
  adding configurable or default gestures.

## 2026.1.16

### What to test

- From the Codex prompt, use ordinary Tab or browse-mode navigation to reach Add
  files and more, the model control, and Change permissions.
- Confirm NVDA announces a concise purpose and opening instruction for each control.
- Confirm native collapsed, expanded, and submenu states are still announced.
- Open each control with Enter or Space, navigate its popup with arrow keys, choose
  an item with Enter, and close it with Escape.
- Repeat in focus mode and browse mode and confirm NVDA remains responsive.
- Confirm these three controls did not add entries to NVDA's Input Gestures dialog.

- Replaced the temporary prompt-control actions with native object accessibility.
- Added contextual descriptions to recognized Add files and more, model, and Change
  permissions controls in the Codex desktop app.
- Preserves the controls' native names, roles, states, actions, and keyboard behavior.
- Preserves any description supplied by the Codex app and appends the add-on's
  keyboard guidance instead of replacing it.
- Performs no toolbar traversal and adds no scripts or keyboard gestures for these
  controls.
- Avoids traceback logging from the high-frequency NVDA object-overlay hook.

## 2026.1.15

### What to test

- In NVDA Input Gestures under Codex Status Announcer, assign temporary gestures to
  Open Codex Add files and more, Open Codex model selector, and Open Codex Change
  permissions menu. Confirm no gestures were assigned automatically.
- From the Codex prompt in focus mode, invoke each action and confirm its native popup
  opens with NVDA focus ready for arrow navigation.
- Repeat all three actions from browse mode and from another control in the Codex task.
- Invoke each action outside ChatGPT and confirm the add-on asks you to move to Codex.
- Type the control names into a conversation and confirm the actions still target the
  actual prompt controls rather than matching the conversation text.
- Test in a long task and confirm the actions return quickly without slowing NVDA.

- Added three unbound Input Gestures actions for Add files and more, model selection,
  and Change permissions.
- Uses bounded NVDA-object navigation around the prompt toolbar instead of searching
  the complete Chromium virtual-buffer text.
- Recognizes the stable accessible labels confirmed in the live NVDA log and dynamic
  model names such as GPT and o-series labels.
- Uses an unclassified popup-button fallback only when the toolbar exposes exactly one
  safe candidate for the dynamic model selector.
- Focuses and activates the native Codex control, leaving its native popup available
  for normal arrows, Enter, and Escape.

## 2026.1.14

### What to test

- Start with an older configuration and confirm invalid profile, sound, interval, and
  command-length values are repaired without preventing the add-on from loading.
- Assign and run the compatibility self-test in Input Gestures. Verify monitoring,
  speech, braille, sounds, chat caches, and the last inspection error are reported.
- Copy sanitized diagnostics and confirm profile names, cached chat counts, repairs,
  and the last error are included without commands or secrets.
- Trigger cosmetically different versions of the same activity and confirm they are
  spoken once while genuinely different activity is still announced.
- In Full Developer mode, test Normal, Enhanced, and Literal command punctuation.
- Set a short maximum command length, confirm long speech is shortened, then assign
  Copy latest full Codex progress and verify the complete text reaches the clipboard.
- Open chat history, search, review the result-count text, and activate Refresh chat
  lists. Confirm NVDA remains responsive.
- Export settings, change several values, import the file, reopen Settings, and confirm
  values return. Test Reset speech profile settings followed by Cancel and by OK.
- Perform manual compatibility checks with focus and browse modes, NVDA speech off,
  a built-in synthesizer, a third-party synthesizer, braille, multiple Codex windows,
  sleep mode, and ChatGPT closing while monitored.

- Added bounded migration and repair for profile, sound, timing, and command-length
  configuration values.
- Expanded sanitized diagnostics and added an unbound compatibility self-test.
- Added semantic duplicate suppression for equivalent activity wording.
- Added Normal, Enhanced, and Literal command punctuation plus a maximum spoken
  command length. Complete text remains available in braille and through a new
  unbound clipboard action.
- Added searchable-history result counts and a safe refresh button that uses caches
  and read-only JSONL metadata without a synchronous Chromium scan.
- Added JSON settings export/import and a focused speech-profile reset.
- Added restricted-runtime regression checks for optional modules absent from NVDA.
- Expanded the manual checklist for synthesizers, braille, speech-off behavior,
  multiple windows, sleep mode, focus mode, and browse mode.

### Deferred platform limitations

- Per-message synthesizer rate changes are not applied because NVDA does not offer a
  safe universal API that avoids altering the user's global synthesizer settings.
- Opening an archived task directly remains dependent on Codex exposing a supported
  navigation action; the add-on does not modify archive state or private application
  databases to simulate it.
- Secure-screen testing remains manual because add-ons and user configuration are
  intentionally isolated on NVDA secure screens.

## 2026.1.13

### What to test

- Set Announcement detail to Minimal and preview Essential, Balanced, and Informative.
- Essential should speak thinking, attention, failures, and whole-task completion while
  ordinary commands and edits continue using their configured sounds and braille.
- Balanced should say Checking files, Editing code, Running tests, File updated,
  Tests passed or failed, and context-aware waiting messages.
- Informative should add safe filenames, counts, and elapsed times of ten seconds or more.
- Confirm Balanced background pulses omit elapsed time before 30 seconds and identify
  the current activity, such as Tests still running.
- Confirm Minimal commentary is omitted in Essential, shortened in Balanced, and
  slightly longer in Informative while complete commentary remains available in braille.

- Added Essential, Balanced, and Informative Minimal-speech profiles.
- Made Balanced the default for concise but meaningful progress.
- Added contextual file, test, waiting, success, and failure wording.
- Informative retains safe filenames, result counts, and useful longer timing without
  exposing full commands or paths.
- Minimal speech filtering no longer disables independently configured sounds or braille.
- Background pulses and commentary now follow the selected Minimal profile.

## 2026.1.12

### What to test

- Install the update and restart NVDA. Confirm the one-time startup document contains
  only the concise current-version summary rather than the complete release history.
- Confirm focus still lands at the top of the startup document.
- Open NVDA Settings > Codex Status Announcer and confirm View complete release history
  still provides every version back through 1.0.0.
- Confirm the Standard, Developer, and Raw Full-speech profiles remain available.

- Restored the earlier concise startup behavior at the user's request.
- The startup document now summarizes only the current patch and its relevant features.
- Kept the complete changelog in the packaged add-on and the dedicated Settings button.
- Preserved the top-of-document focus correction for both viewers.

## 2026.1.11

### What to test

- In NVDA Settings, set Announcement detail to Full and test each Full speech profile.
- Standard should announce the action plus a concise target, count, or useful elapsed
  time without reading the complete shell command.
- Developer should preserve the existing normalized complete command and progress text.
- Raw should preserve the exact exposed wording and repeated internal spacing.
- Use Test current announcement outputs after selecting each profile and confirm the
  preview changes before saving.
- With braille connected, confirm Full mode continues to show the complete normalized
  progress text even when Standard speech is selected.
- Confirm privacy redaction continues to remove secrets and personal usernames in all
  three profiles.

- Added Standard, Developer, and Raw profiles under Full speech verbosity.
- Kept Developer as the default so existing users retain the current detailed behavior.
- Standard produces action-first messages and retains useful filenames, command names,
  counts, and elapsed times of at least five seconds.
- Raw returns the progress label as exposed by Codex instead of normalizing whitespace.
- Speech and braille can now receive different text for the same event: speech follows
  the selected profile while braille retains the complete normalized Full label.
- The Settings test button now previews the selected Full profile using a realistic
  shell-command example.

## 2026.1.10

### What to test

- Install the update and restart NVDA. Confirm Codex Status Announcer appears in
  Settings and Input Gestures and the log reports version 2026.1.10 loaded.
- Confirm there is no `ModuleNotFoundError: No module named 'sqlite3'` traceback.
- Invoke chat history, Tab to Archived chats, and confirm the archived task names load.
- Confirm the complete startup changelog still opens at the top and includes this fix.
- Test ordinary progress speech, braille, and Working clicks to confirm the global
  plugin is fully active again.

- Fixed a startup-blocking import failure found in the live NVDA log. NVDA's embedded
  Python does not provide the optional `sqlite3` standard-library extension.
- Removed the SQLite import and all database access from the add-on.
- Archived task IDs now come from filenames in Codex's `archived_sessions` directory,
  while accessible task names come from the read-only `session_index.jsonl` file.
- Added a regression assertion that the shipped core never imports SQLite.
- Preserved the complete startup history introduced in 2026.1.9.

## 2026.1.9

### What to test

- Install the update and restart NVDA. Confirm the startup document includes this
  version, today's archived-history work, the calendar-version transition, and every
  earlier release back through version 1.0.0.
- Confirm focus lands at the top of the startup document.
- Close the document, restart NVDA again, and confirm it does not reopen repeatedly
  after the version has been recorded.
- In NVDA Settings, compare View complete release history with the startup document
  and confirm their release contents match.

- Replaced the short hard-coded startup summary with the complete packaged changelog.
- The accessible startup document now covers the entire add-on development history,
  including versions 1.0.0 through 2.2.5, the move to NVDA-aligned 2026.1 patch
  versions, and all changes completed today.
- Reused the established top-of-document focus helper for the startup viewer.
- Retained a safe current-release fallback if the packaged changelog cannot be read.

## 2026.1.8

### What to test

- Restart NVDA and invoke the assigned history gesture without opening Settings.
- Tab from Recent chats to Archived chats and confirm the archived titles load.
- Confirm archived tasks are ordered from most recently archived to oldest.
- Search for an archived title and confirm filtering remains immediate.
- Confirm the NVDA log reports the number of archived tasks loaded and contains no
  traceback or SQLite locking error.
- Repeat from focus mode and browse mode and verify NVDA remains responsive.

- Replaced the Settings accessibility-buffer dependency with a direct read-only query
  of Codex's local `state_*.sqlite` thread index.
- The loader reads only ID, title, and archive ordering; it never changes Codex data.
- Added bounded loading of at most 200 archived tasks and a short database timeout.
- Added automated coverage for filtering out recent tasks, archive ordering, title
  normalization, and preferred user-assigned names.

## 2026.1.7

### What to test

- Open the assigned chat-history gesture and confirm focus starts in Search chats.
- Press Tab once to reach Recent chats, then Tab again to reach Archived chats.
- Search for text and confirm both lists are filtered without slowing or freezing NVDA.
- Before visiting ChatGPT Settings > Archived chats, confirm the archived list gives a
  clear loading instruction and cannot be accidentally opened.
- Visit ChatGPT Settings > Archived chats, allow monitoring to inspect the view, then
  reopen history and confirm exposed archived titles appear in the second list.
- From the Archived chats settings view, test Enter and Shift+F10 on an archived title.
- Repeat from both NVDA focus mode and browse mode.

- Added separate Recent chats and Archived chats list boxes to the modeless history
  dialog. Their creation order makes Archived chats the direct Tab stop after Recents.
- Search now filters both title collections independently.
- Added a non-actionable, spoken instruction when ChatGPT has not yet exposed archived
  titles through its Settings > Archived chats accessibility view.
- Archived titles are cached during the existing background buffer inspection; opening
  the dialog still performs no synchronous full-document scan.
- Archived actions fail safely with a specific instruction when the archived Settings
  view is no longer available.

## 2026.1.6

### What to test

- Restart NVDA, invoke the assigned chat-history gesture, and confirm NVDA stays
  responsive while the Codex chat history dialog is open.
- Type in Search chats, arrow through the result list, cancel with Escape, and
  immediately verify normal NVDA navigation and speech still work.
- Reopen the dialog, press Enter on a chat, and test Shift+F10 on another chat.
- Invoke the gesture immediately after entering Codex. If the first background
  inspection has not populated the cache, confirm the add-on reports that no
  recent chats are available instead of freezing.

- Replaced blocking `ShowModal()` execution inside the NVDA gesture with a
  modeless dialog and callback-based selection handling.
- The NVDA watchdog log showed the modal call freezing the core for more than
  75 seconds; the gesture now returns immediately after showing the dialog.
- Chat titles are cached during the existing background virtual-buffer scan.
  Pressing the gesture performs no Chromium document read or history scan.
- Added safe dialog reuse, cancellation, popup cleanup, and delayed execution of
  the chosen open or context-menu action after focus returns to ChatGPT.

## 2026.1.5

### What to test

- Invoke the assigned history gesture from a long Codex conversation. Confirm a
  “Codex chat history” dialog opens with only titles from the Recents sidebar.
- Type in the Search chats field, use Down Arrow to enter the filtered list, and
  press Enter to open a selected chat.
- Leave search blank and arrow through the complete recent-chat list.
- Press Shift+F10 on a selected title and confirm its ChatGPT context menu opens.
- Type rapidly in a long Codex prompt and confirm NVDA speech, braille, and input
  remain responsive without repeated full-document processing.
- Submit the prompt and confirm status detection and Working clicks still start.

- Removed the unreliable search for the words `Open chat` across the complete
  conversation. The live log proved it matched earlier message text, moved the
  virtual cursor into the conversation, and forced NVDA to process a huge range.
- Added a dedicated searchable and arrowable NVDA dialog populated only from the
  bounded Recents sidebar section.
- Opening a selection resolves the actual sidebar button and invokes its action.
- Shift+F10 focuses the actual selected chat button before requesting ChatGPT's
  native context menu.
- Ordinary editable-text changes no longer schedule a full virtual-buffer scan
  for every character; confirmed prompt submission still schedules immediately.
- Raised the minimum idle fallback scan interval to one second while preserving
  event-driven 10-millisecond scans and 250-millisecond active fallback scans.

## 2026.1.4

### What to test

- Place focus in the Codex prompt while NVDA is in focus mode and invoke the
  assigned chat-history gesture. Confirm it opens instead of saying to move to
  Codex.
- Repeat from browse mode and from several controls within the Codex interface.
- Confirm invoking the gesture from another application still reports that the
  user must move to ChatGPT Codex first.
- Search, arrow through results, open a chat, and test Shift+F10 on a selection.

- Fixed an overly strict history-command guard that required every focused
  Chromium object to expose a directly discoverable Codex document ancestor.
- The command now accepts any configured ChatGPT host object and then uses the
  remembered Codex virtual buffer, matching the add-on's established focus-mode
  monitoring strategy.

## 2026.1.3

### What to test

- Assign “Open searchable and arrow-navigable Codex chat history” in NVDA's
  Input Gestures dialog and invoke it from focus mode and browse mode.
- Type part of a chat title and confirm the native result list is filtered.
- Open history without typing and use Up and Down Arrow to review chats.
- Press Enter and confirm the selected chat opens.
- Select a chat, press Shift+F10, and confirm ChatGPT's native context menu opens.
- Arrow through the context actions, press Escape, and confirm focus returns to
  the selected chat without opening or modifying it.

- Clarified the assignable history action as both searchable and arrow navigable.
- Documented the complete native keyboard workflow: type to filter, arrows to
  browse, Enter to open, and Shift+F10 to access the selected chat's actions.
- Leaves Shift+F10 under Windows and ChatGPT control instead of intercepting it,
  preserving standard context-menu behavior and future ChatGPT actions.

## 2026.1.2

### What to test

- In NVDA's Input Gestures dialog, assign a preferred gesture to “Open
  searchable Codex chat history” under Codex Status Announcer.
- Invoke it while the Codex prompt is in focus mode and confirm ChatGPT's native
  chat-history picker opens with focus ready for searching or navigation.
- Repeat in browse mode and from elsewhere inside the Codex document.
- Type part of a chat title, choose a result, press Enter, and confirm that task
  opens without submission or Working clicks.
- Confirm the action reports a clear message when used outside Codex or if the
  ChatGPT interface does not expose its Open chat control.

- Switch among existing Codex tasks with different conversation lengths and
  confirm no Prompt submitted or repeating Working clicks play.
- Navigate ChatGPT controls, Settings, and task history before typing a prompt
  and confirm no work sounds begin.
- Type and submit a prompt with Enter and confirm the Prompt submitted click
  plays immediately, followed by Working clicks while Codex is processing.
- Submit a prompt with the Send button and confirm the same behavior.
- Confirm completion or cancellation stops the repeating Working clicks.
- Repeat these checks in both NVDA focus mode and browse mode.

- Fixed task navigation being misidentified as a prompt submission when the
  newly loaded conversation had a higher historical user-message number.
- The user-message fallback now requires ChatGPT's active Stop or Cancel
  control before it can start the working state.
- Retained a newly observed message-count increase until Chromium exposes the
  Stop control, preventing legitimate submissions from being missed when those
  accessibility updates arrive in separate scans.
- Cleared stale prompt-text state whenever focus moves from the prompt to other
  ChatGPT controls, preventing draft state from leaking across task switches.
- Filtered current task-history, review, undo, download, and elapsed-work
  controls from sanitized unknown-button diagnostics.
- Prevented a tentative `Response complete` marker from stopping Working clicks
  while a Stop or Cancel control, another activity label, or an already-idle
  state contradicts completion.
- Increased the fallback completion settling window to 30 seconds after the
  live log showed a later command arriving beyond the former 15-second window.
- Explicit progress and completion events now cancel tentative completion state,
  preventing delayed duplicate Finished announcements.
- Added regression coverage for message-count changes without active work.
- Added an unbound “Open searchable Codex chat history” action to NVDA's Input
  Gestures dialog. It activates ChatGPT's native Open chat control from the
  remembered virtual buffer in both focus and browse modes.
- No keyboard shortcut is assigned by default, avoiding conflicts with NVDA,
  other add-ons, and user-defined commands.

## 2026.1.1

### What to test

- Switch among existing Codex tasks with different conversation lengths and
  confirm no Prompt submitted or repeating Working clicks play.
- Submit a real prompt with Enter and with the Send button, confirming prompt
  submission and Working clicks still begin normally.
- Repeat in NVDA focus mode and browse mode.

- Fixed task navigation being misidentified as a prompt submission when a
  loaded conversation had a higher historical user-message number.
- Required ChatGPT's active Stop or Cancel control before the historical
  message-count fallback can start Working clicks.
- Cleared stale prompt-text state during task and sidebar navigation.
- Added regression coverage for navigation without active work.

## 2.2.5

### What to test

- Submit a populated prompt with Enter and confirm the Prompt submitted click
  plays once immediately.
- Submit another prompt with the Send button and confirm the same behavior.
- Confirm repeating Working clicks continue through commentary, commands,
  intermediate command/file/build/search completions, and quiet processing gaps.
- Confirm commentary followed by a tool that takes at least 11 seconds to appear
  does not produce a premature Finished announcement or stop Working clicks.
- Complete and cancel separate tasks, confirming Working clicks stop and do not
  continue after the task is idle.
- Switch between focus mode and browse mode during an active task and confirm
  announcements and Working clicks continue without duplicates.
- Turn NVDA speech off and confirm configured clicks continue; restore speech and
  confirm speech and sound routing follow each category's setting.
- With a braille display connected, confirm progress flash messages appear in
  both focus and browse modes independently of speech.
- Switch between two Codex tasks and confirm history, prompt state, and Working
  clicks do not leak from one task into the other.
- Move into and away from ChatGPT, then close it, confirming the monitoring-active
  and monitoring-inactive clicks play once per transition.
- Preview every sound and speech action individually, including Prompt submitted,
  monitoring active, and monitoring inactive, at Soft, Normal, and Loud levels.
- Enable sanitized diagnostic logging and confirm ordinary ChatGPT navigation,
  voice, attachment, message, and file-diff controls are not reported as unknown.
- Review the NVDA log after testing and confirm there is no Codex Status Announcer
  traceback, sound failure, or repeated duplicate announcement.

- Fixed the sound-generation utility writing WAV files beneath an incorrect
  nested directory after the project was reorganized for GitHub.
- Replaced timestamp-dependent ZIP creation with a deterministic package
  builder, producing identical SHA-256 checksums from unchanged source.
- Reduced full virtual-buffer fallback scans during active work from ten times
  per second to four times per second.
- Preserved fast 10-millisecond polling triggered by Chromium accessibility
  events, so normal live announcements remain event driven.
- Added a repeatable manual NVDA integration-test checklist covering focus and
  browse modes, speech-off sounds, braille, long tasks, and permission prompts.
- Increased the separation between Soft, Normal, and Loud click amplitudes so
  selecting a lower level produces an obvious reduction instead of a subtle
  change that can be masked by NVDA's audio mix.
- Added automated audio-level checks for every click category.
- Added an enabled-by-default continuous Working click while Codex is busy,
  with an adjustable 500–5000 millisecond interval.
- The Working click uses the selected click volume and only plays with the
  Clicks sound style when the active category permits sounds.
- Every other progress sound resets its timer, ensuring the Working click uses
  a quiet gap rather than overlapping command, file, completion, or alert sounds.
- Added distinct rising and falling clicks when the ChatGPT/Codex window gains
  or loses focus. Closing the app also produces the losing-focus cue.
- Focus-state clicks occur only on transitions, not while moving between
  controls within ChatGPT, and can be disabled independently in Settings.
- Added both focus-state sounds to the individual sound and speech preview list.
- Prompt submission now produces an immediate cue when the Codex prompt changes
  from containing text to empty after Enter or the Send button is activated.
- Prompt submission detection stores only a boolean text-present state, never
  the prompt contents, and requires no assigned keyboard gesture.
- Fixed prompt submission detection when Chromium destroys the populated edit
  object and replaces it with a new blank object after Enter is pressed.
- Added the newly posted user-message number as a fallback submission signal
  when Chromium omits editable-text accessibility events.
- Added an optional, distinct three-click Prompt submitted cue and an individual
  preview for it in Settings.
- Added a configurable delay before repeating Working clicks begin; the prompt
  submission cue remains immediate.
- Added Send-button confirmation through the appearance of Codex's active-task
  stop control, without assigning or intercepting a keyboard gesture.
- Working clicks now stop immediately when a visible stop or cancel control
  disappears and no activity status remains.
- Strengthened task isolation when switching Codex documents by clearing prompt,
  stop-control, commentary, history, and click-timer state at each buffer change.
- Diagnostics now report the last state reason, submission signal, document
  switch count, and last buffer-inspection failure.
- Increased rapid duplicate-event suppression to 1.5 seconds and optionally log
  sanitized suppression records for troubleshooting noisy accessibility events.
- Removed status-gap inference from the busy state. Quiet processing can no
  longer stop Working clicks; only explicit completion, cancellation, document
  switching, pausing, or the configured maximum safety timeout can stop them.
- Identical diagnostic button snapshots are now logged at most once every 30
  seconds; changed snapshots remain available immediately.
- Fixed Chromium's non-button `Response complete` live region being discarded as
  commentary. It now queues a completion candidate without repeating the full
  response text in Full mode.
- Added a virtual-buffer completion fallback for Chromium builds that display
  `Response complete` to NVDA but omit the plug-in live-region event. The fallback
  retains only a temporary in-memory fingerprint and never stores response text.
- Corrected `Response complete` semantics: it is now a 15-second, cancellable
  completion candidate because the live NVDA trace showed ChatGPT delaying a
  subsequent command accessibility event by more than 10 seconds.
- Intermediate completions such as `Ran command`, file edits, compilation, and
  searches no longer end the overall busy state or interrupt Working clicks.
- Intermediate completion sounds now retain their related command, file, build,
  or search routing for subsequent Working clicks instead of inheriting the
  Completion channel configuration.
- Known Codex controls such as user-message navigation, Outputs, Sources, View
  all, and Copy are no longer reported as unknown diagnostic buttons.
- Extended diagnostic filtering to ordinary chat, voice, attachment, scrolling,
  message-copying, and file-diff controls observed during the final smoke test.
- Busy-state diagnostics now update their reason during activity transitions
  even when the task remains busy.
- Updated the manifest, built-in release notes, README, and build script for the
  complete 2.2.5 release candidate. The build script now accepts `-PythonPath`.

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
