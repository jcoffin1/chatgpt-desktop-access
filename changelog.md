# Changelog

All notable changes to Codex Access Toolkit for NVDA, formerly Codex Status Announcer, are recorded here.

## 2026.1.43

### What to test

- Open **NVDA Settings > Codex Access Toolkit** and confirm the panel contains eight
  clearly named pages: General, Speech and Braille, Sounds, Activity Output,
  Wording and Preview, Browser Access, Advanced, and Support. Use Control+Tab and
  Shift+Control+Tab to move through every page, and confirm every setting remains
  reachable with Tab and Shift+Tab.
- Open ChatGPT's embedded browser or web preview. Confirm entry and exit are
  announced once, useful page-title changes are announced once, and exposed
  loading progress is announced at most once per ten-percent step. Confirm an
  unrelated download is never described as browser loading.
- Open ChatGPT's native **Browser** submenu and move through Open Browser Tab,
  Focus Browser Address Bar, and Reload Browser Page. Confirm this menu does not
  announce “Embedded browser active” or a false return to ChatGPT. Then open a
  browser tab and confirm the announcement occurs only after focus reaches the
  nested web document.
- Navigate the embedded page in focus mode and browse mode. Confirm native names,
  roles, states, actions, Tab behavior, NVDA+Space, and browse-mode quick navigation
  are preserved; the Toolkit must not move focus or activate any control by itself.
- Start a Codex task and move into the embedded browser while it runs. Confirm
  speech, sounds, and urgent Braille continue, returning to the conversation keeps
  the original virtual buffer, and no false new-chat or monitoring-inactive event
  occurs. Test each Browser Access option independently and open its help document.
- On every page, use its displayed Alt access keys and confirm each one reaches a
  different control. Confirm General contains only the main output choices,
  background timing is under Activity Output, technical compatibility controls are
  under Advanced, and documentation, account, report, and settings-file actions are
  under Support.
- On Activity Output, select several activity categories, change both the enabled
  checkbox and output destination, and confirm each category's selector text
  immediately states its current enabled status and route. Move between categories,
  select Apply, reopen Settings, and confirm every category retained its independent
  values.
- Export settings and confirm the save dialog proposes
  `codex-access-toolkit-settings.json` while still allowing another name or location.
- In **NVDA > Preferences > Input Gestures**, expand Codex Access Toolkit and
  confirm ten separately named recent-message actions are available. Reassign one
  action, remove another default assignment, and confirm both changes persist.
- Confirm Control+1 through Control+0 still read the expected messages in ChatGPT
  focus and browse modes. Confirm these keys pass through normally outside ChatGPT.
- Save a sanitized support report from Support and from an assigned
  Input Gesture. Confirm it contains the Toolkit and NVDA versions, settings, and
  monitoring state, but no chat text, commands, file paths, or secrets.
- Exercise chat search, Recent and Archived lists, Shift+F10 chat actions, progress
  clicks and tones, prompt submission, permission dialogs, and Braille protection
  after the module split. Confirm behavior matches 2026.1.42.
- Type a long prompt in ChatGPT from a Braille display at normal speed. Confirm the
  Braille line follows the editor without pauses, stale intermediate words, missing
  characters, or unwanted Toolkit flash messages. Press Enter and confirm ChatGPT
  clears the editor, Prompt submitted is detected, and NVDA remains responsive.
- Leave ChatGPT idle and move to Outlook. Confirm the NVDA debug log no longer records
  a ChatGPT URL-property lookup about once per second. Start a Codex task, move away,
  and confirm direct progress events, background sounds, and completion still arrive.
- Leave the empty ChatGPT prompt focused for at least one minute without typing. Confirm
  the Toolkit performs no periodic idle compatibility scan; idle monitoring is event-only.
- During a long task, confirm direct Thinking, commentary, command, file, permission,
  and completion events remain immediate. Confirm the compatibility fallback performs
  at most one full-buffer inspection every five seconds when no event is available.
- With focus in the prompt, enter contracted Braille continuously without committing
  every chord with Space. Confirm raw dot and Space gestures activate typing protection
  immediately and no compatibility scan occurs inside the Braille composition.
- With contracted Braille enabled, type `we need using Braille from the Sense` several
  times at normal speed without pausing between words. Confirm the first cell of every
  word is retained: `need` must not become `eed`, and `using` must not become `sing`.
  Repeat in Outlook and confirm its existing Braille input behavior is unchanged.
- Type `The developers need to see the error` at normal Braille Sense speed. Confirm
  each uncommitted cell appears promptly and the result is not scrambled into text such
  as `The developers need se the every`. Compare the NVDA I/O log: prompt composition
  updates should no longer queue roughly 160–180 milliseconds behind every raw chord.
- Run `build.ps1` and confirm unit tests, translation-template validation, syntax,
  archive, sound, gesture, and reproducible-build checks all pass.

### Added

- Added eight keyboard-accessible notebook pages to organize the formerly long,
  cluttered Settings panel, separating Advanced configuration from Support actions.
- Added a dedicated Browser Access page with independently configurable recognized
  control descriptions, focus transitions, page titles, and loading progress.
- Added conservative embedded-browser recognition beneath explicitly named Browser,
  WebView, Web view, or web-preview containers and for web documents nested inside
  ChatGPT's outer Chromium document. Recognized Back, Forward, Reload, Stop,
  address, external-browser, Close, and document controls gain descriptions without
  changing their native roles, states, actions, focus, or gestures.
- Added an embedded-browser help document that opens at the top from Settings or an
  assignable Input Gesture. No browser gesture is assigned by default.
- Added distinct access keys for every actionable control within each Settings page.
- Added enabled-state and output-route summaries directly to every Activity category
  selector item.
- Added ten independently configurable Input Gestures actions for reading the ten
  most recent ChatGPT messages. Control+1 through Control+0 remain the defaults;
  users can replace or remove them through NVDA's Input Gestures dialog.
- Added a user-chosen-file workflow for saving a sanitized support report. The
  report contains versions, settings, attachment and task state, cache counts, and
  the latest internal inspection error without including conversation or command
  text.
- Added anonymized ChatGPT accessibility fixtures covering focus- and browse-mode
  messages, prompt names, task controls, chat actions, permissions, and plug-in
  installation progress.
- Added deterministic gettext-template generation, translator instructions, and
  automatic packaging of compiled translation catalogs.
- Added Windows GitHub Actions validation, issue forms, contribution instructions,
  a security policy, and Add-on Store preparation guidance.

### Changed

- Replaced the long pairs of activity checkboxes and output selectors with one
  activity-category selector, one enabled checkbox, and one output selector. Every
  category retains its own independent configuration.
- Moved background timing to Activity Output, kept General focused on primary output
  choices, and gave settings export a descriptive default filename.
- Normalized packaged text line endings so local and GitHub builds from the same
  commit produce the same byte-for-byte add-on archive.
- Preserved the Codex conversation virtual buffer while focus is within a recognized
  embedded browser so background monitoring continues in focus and browse modes.
- Routed browser loading updates through existing activity-output, duplicate,
  privacy, speech, sound, Braille, and Braille-reading-protection behavior.

### Fixed

- Imported the failure-safe completion beep from the isolated sound module. Enabling
  the additional task-completion sound no longer risks an undefined-name exception.
- Replaced unconditional whole-document polling with event-marked inspections and a
  lightweight housekeeping timer. The captured NVDA log contained 24,448 repeated
  ChatGPT URL-property reads and showed those background scans continuing while focus
  was in Outlook; idle ChatGPT is now event-only whether focused or in the background.
- Suspended compatibility fallback scans while the user is typing in the ChatGPT
  prompt. Braille input and editor feedback no longer compete with a complete Chromium
  virtual-buffer traversal every half second.
- Observes raw Braille dot and Space gestures while the ChatGPT prompt has focus. This
  closes the gap where Chromium emits no text-change event for an uncommitted contracted
  Braille chord; the observer never assigns or consumes the user's gesture.
- Preserved the first cell of a new contracted-Braille word when ChatGPT reports the
  previous word's caret movement late. The NVDA log showed the initial `n` in `need`
  and `u` in `using` reaching NVDA and the Braille display before that delayed event
  cleared them. The Toolkit now marks only this short, active-composition caret event
  as self-generated and lets NVDA's own Braille input protection process it. The guard
  runs only in the focused ChatGPT prompt and does not replace NVDA's Braille handler.
- Stopped Browser Access classification from walking up to eighteen Chromium ancestors
  for ordinary prompt edits, prompt-toolbar controls, status buttons, and other objects
  that cannot be embedded-browser controls. The enabled-add-on log showed Braille
  composition updates trailing raw Braille Sense chords by roughly 160–180 milliseconds,
  compared with approximately 9–23 milliseconds while the Toolkit was disabled. Browser
  controls are now classified locally first, prompt objects use a fast exclusion path,
  and negative browser results are cached on the NVDA object.
- Debounced prompt-local text inspection until typing pauses instead of reading the
  content-editable field once per character. An already-known empty value after Enter
  is trusted without a second IA2 TextInfo request against an editor object Chromium
  is replacing.
- Restricted scan requests to events belonging to the saved conversation buffer, so
  loading pages in ChatGPT's embedded browser cannot repeatedly rescan the chat.
- A transient Chromium buffer-read failure now preserves the task, working sounds, and
  attached buffer and retries at fallback cadence. It no longer falsely ends activity
  or detaches monitoring after one stale COM object.
- Restored the missing completion-sound classifier import. Completion events no
  longer raise `NameError`, detach the Chromium virtual buffer, stop active-state
  monitoring, or flood the NVDA log with repeated inspection failures.
- Prevented unrelated words such as “downloading” from being mistaken for embedded
  browser loading progress, and bounded numeric progress to ten-percent steps.
- Limited browser ancestry inspection to relevant controls and genuinely competing
  virtual buffers, and cached positive detections to protect NVDA main-thread,
  speech, and Braille responsiveness.
- Stopped ChatGPT's native Browser menu and its Open Browser Tab, Focus Browser
  Address Bar, and Reload Browser Page items from falsely announcing that an
  embedded page was active. Actual nested web documents are now recognized even
  when ChatGPT does not expose an ancestor named Browser or WebView.
- Moved sound playback and the chat-history dialog into focused modules so failures
  and future interface changes are easier to isolate and test.
- Updated manifest metadata for Add-on Store compatibility. Stable packages now
  declare the current stable NVDA 2026.1 API instead of the 2026.2 release candidate.

## 2026.1.42

### What to test

- In both browse mode and focus mode inside ChatGPT, press Control+1 and confirm the most
  recent user or ChatGPT message is read. Confirm Control+2 through Control+9 read progressively
  older messages and Control+0 reads the tenth-most-recent message.
- Test a task containing fewer than ten messages and confirm unavailable positions report
  the number of messages that can be read without raising an error.
- While a response is streaming, press the shortcuts repeatedly and confirm controls,
  “Response complete,” duplicated live-buffer nodes, and prompt text are not included.
- Move to another application and confirm Control+1 through Control+0 pass through normally.
- Confirm the shortcuts work without switching NVDA between focus and browse modes and do
  not leave Working sounds active or change the current task state.
- In searchable chat history, press Shift+F10 on a Recent chat whose Pin or Archive
  control is temporarily unavailable. Confirm Toolkit reports failure after a short,
  bounded retry window and NVDA remains responsive afterward.
- Navigate rapidly while ChatGPT is replacing accessibility objects and confirm the NVDA
  log contains no uncaught Toolkit event-handler traceback.
- Type a prompt and press Enter. Confirm the distinct Prompt submitted sound plays as the
  editor clears even though ChatGPT briefly moves focus to an intermediate section.

### Added

- Control+1 now reads the most recent message in the current ChatGPT conversation. Control+2
  through Control+0 directly read progressively older messages, up to ten turns.
- The explicitly requested shortcuts are active only while focus is within ChatGPT; in
  every other application the original keystrokes are passed through unchanged.

### Reliability

- Conversation turns are derived from ChatGPT's accessible “You said” and “ChatGPT said”
  markers. Interactive controls, the prompt editor, completion labels, and consecutive
  duplicate Chromium nodes are excluded.
- Extraction is bounded to ten turns and runs only on demand, avoiding additional polling
  or background work on NVDA's main thread.
- Fixed an overflow during the first ChatGPT foreground and focus events after NVDA
  startup. The poll coalescer now safely handles the deliberate infinite “no previous
  poll” sentinel as well as invalid, non-finite, and negative timing inputs, so Toolkit
  scheduling cannot abort NVDA's event chain.
- Removed the add-on-owned `appModules/chatgpt.py` override. Control-number shortcuts are
  now bound dynamically by the global plug-in only while ChatGPT has focus, preventing
  the Toolkit from shadowing another ChatGPT app module or changing native prompt
  handling. Enter remains entirely unbound and is passed directly to ChatGPT; the
  Toolkit only observes whether the prompt clears or a submitted message appears.
- Recent-message review now removes Chromium's hidden flattened response copy, trailing
  timestamps, progress metadata, step counters, and response controls. It also rejoins
  words split across inline accessibility nodes instead of inserting an unwanted space.
- A selected chat whose Pin or Archive control never appears now stops retrying after the
  bounded retry window. It no longer leaves a repeating main-thread timer running.
- Toolkit work in every NVDA event hook is now exception-isolated. A transient, stale
  Chromium accessibility object can be logged for diagnosis but cannot escape the add-on
  and interrupt NVDA's event chain.
- Fixed the missing Prompt submitted sound after Enter. ChatGPT temporarily focuses a
  section between the populated and empty prompt states; Toolkit now preserves submission
  tracking across that transient focus change while real task switches still reset it.

## 2026.1.41

### What to test

- Enable Braille announcements and leave Protect Braille reading enabled. While focus is
  inside ChatGPT, read a long response on the Braille display while Codex continues to
  think, run commands, edit files, and produce commentary. Confirm Toolkit routine
  progress does not replace the line being read.
- During the same task, confirm speech and progress sounds continue normally.
- Trigger completion, failure, or a permission request and confirm that important message
  still appears in Braille.
- Move focus outside ChatGPT while Codex is working and confirm enabled routine progress
  is again available through Braille.
- Disable Protect Braille reading and confirm routine progress can flash in Braille while
  ChatGPT is focused, preserving the previous fully verbose behavior.
- Use Repeat latest status or announcement-history commands and confirm their explicitly
  requested Braille messages always appear.

### Added

- Added Protect Braille reading from routine progress while focused in ChatGPT, enabled
  by default. It applies only to Toolkit-generated routine activity and commentary.
- Completion, failure, permission, navigation, monitoring, and user-requested messages
  remain eligible for Braille output while protection is active.
- Routine Braille progress remains available whenever focus is outside ChatGPT, and the
  setting can be disabled for users who prefer every flash while reading in the app.

### Diagnostics

- The reported reading reset was reproduced in the NVDA log while Toolkit Braille output
  was disabled. ChatGPT repeatedly rebuilt NVDA's live virtual-buffer Braille region as
  the response changed. This setting prevents Toolkit output from adding interruptions;
  it cannot stop Chromium itself from refreshing a response that is still streaming.

## 2026.1.40

### What to test

- Start a busy task while Chromium is producing frequent accessibility events. Confirm
  activity announcements remain prompt and the fallback scan is not delayed indefinitely.
- Install a ChatGPT plug-in whose last progress event says “installation complete” without
  exposing 100 percent. Confirm completion is announced and Working sounds stop.
- Enable privacy redaction and expose commentary or a command containing `--token value`
  or `--password value`. Confirm the secret is absent from speech, Braille, history, and
  Copy latest full Codex progress.
- Disable progress sounds, then move focus into and out of ChatGPT. Confirm monitoring
  focus sounds remain silent. Repeat while announcements are paused.
- With a speech synthesizer or Braille display temporarily unavailable, confirm failure
  of that channel does not prevent the other channel or the selected progress sound.
- In Standard Full speech, run an `rg`, PowerShell, or Python command and confirm its
  executable name is retained when the completed `Ran …` status is announced.

### Fixed

- Repeated Chromium events could continually replace an earlier scheduled scan with a
  later one, starving the virtual-buffer fallback during an event storm. An already
  scheduled earlier scan is now preserved.
- Plug-in installation completion without an explicit 100-percent value was not treated
  as complete and could leave background activity active indefinitely. Installation
  identities are now stable across in-progress and completion wording.
- Privacy redaction now covers plain-language commentary and common command-line secret
  options such as `--token value` and `--password value`.
- Monitoring focus sounds now respect both the global progress-sound switch and the
  announcement Pause state.
- Speech, Braille, urgent speech cancellation, click playback, and musical-tone delivery
  are isolated, so failure in one output path no longer prevents the remaining enabled
  channels or escapes into NVDA's accessibility event handler.
- Malformed archived-session filenames are excluded instead of appearing as tasks that
  can never be opened.
- Archived tasks with duplicate titles now receive distinct numbered display labels, so
  every native task ID remains independently selectable and openable.

### Improved

- Standard Full speech retains the executable name in completed `Ran …` command labels.

## 2026.1.39

### What to test

- Run a task for more than one minute and confirm recurring progress says, for example,
  “File operations still running, 1 minute 25 seconds,” rather than “85 seconds.”
- Let a task pass 200 seconds and confirm the duration is “3 minutes 20 seconds.”
- Run commands followed by file reading, code editing, tests, tool use, and web search.
  Confirm each heartbeat follows the newest detailed activity instead of retaining an
  older command category.
- Use the current-activity command during a long quiet operation and confirm its elapsed
  time uses the same hours, minutes, and seconds formatting.

### Improved

- Long elapsed times now use speech-friendly hours, minutes, and seconds in speech and
  Braille rather than an increasingly large raw seconds count.
- Background activity names are noun phrases that read naturally before “still running.”
- The newest detailed status can correct a stale broad activity category, improving the
  distinction among commands, file operations, tests, tools, and web searches.
- Custom announcement templates can use `{duration}` for the same natural elapsed time;
  the existing `{seconds}` placeholder remains available for backward compatibility.

## 2026.1.38

### What to test

- Submit a prompt that includes several commands and file-reading operations. Confirm
  continuous Working clicks play while Codex is active.
- Wait for the final response and confirm the Working clicks stop without restarting
  NVDA, including when the log reports a trailing `Reading finished` event.
- Start another task within 30 seconds of a completion candidate and confirm genuine
  Reading, Working, Thinking, or command activity keeps the clicks running.

### Fixed

- A trailing `Reading finished` accessibility event could be classified as new file
  activity and erase an already queued whole-response completion signal. The busy state
  then remained active indefinitely, so Working clicks continued until NVDA restarted.
- Gerund-form reading completion labels are now classified as intermediate completion,
  and intermediate completions preserve the pending whole-response completion signal.
- A persistent intermediate-completion label is now treated as quiet during the guarded
  completion settle period, so it cannot keep Working clicks active indefinitely.

## 2026.1.37

### What to test

- Run a long task in a large conversation while typing, navigating with Braille, and
  switching between focus and browse modes. Confirm NVDA remains responsive.
- Confirm Thinking, commands, file work, commentary, permissions, and completion still
  speak and appear in Braille immediately when Chromium raises their live events.
- Leave a task active during a quiet period and confirm fallback progress and continuous
  Working sounds continue without noticeable main-thread pauses.
- Open Add files and more, the model selector, and Change permissions. Confirm their
  accessible descriptions remain available without slowing ordinary focus movement.
- Review the NVDA log after several minutes and confirm no toolkit frame appears in a
  watchdog freeze stack and no virtual-buffer inspection failure is logged.

### Fixed

- Rapid Chromium accessibility events could repeatedly request a complete virtual-buffer
  scan after only 10 milliseconds. Large conversations could therefore add avoidable work
  to NVDA's main thread during already busy UI Automation activity.
- Event-triggered scans are now coalesced to a minimum 150-millisecond interval. Direct
  live-event speech, Braille, and sounds remain immediate.
- The active compatibility fallback now scans twice per second instead of four times per
  second. Event-driven announcements remain the primary path.
- Prompt-control overlay selection no longer walks up to 20 Chromium ancestors for every
  candidate button or combo box; the unique control names and ChatGPT process scope are
  sufficient.

### Diagnostics

- The reported watchdog freezes were captured inside NVDA's Chromium UI Automation
  property retrieval, not inside Codex Access Toolkit. Speech and HIMS Braille output
  continued in the log until NVDA received an explicit shutdown gesture.

## 2026.1.36

### What to test

- Open an existing Codex conversation, use Windows+Tab or Alt+Tab to move away, and
  return to ChatGPT. Confirm the add-on does not say “New Codex chat opened.”
- Repeat the focus switch while Codex is working and confirm continuous Working sounds
  and background progress continue without restarting their elapsed time.
- Open an actually blank new Codex chat and confirm “New Codex chat opened” is announced.
- Open a Recent or Archived chat through the add-on and confirm its selected title is
  still announced when the conversation opens.

### Fixed

- NVDA can replace Chromium's UIA tree interceptor with an IA2 virtual buffer when focus
  returns to ChatGPT. The add-on previously treated every interceptor replacement as a
  new conversation, announced a false new chat, and cleared active task state.
- Accessibility-backend refreshes now preserve the current task. A reset occurs only
  for an explicitly selected history entry or an unmistakably blank new conversation.

## 2026.1.35

### What to test

- Customize the File or Completion announcement so it does not contain the word
  “finished.” Finish a file step while the overall task continues and confirm the
  recurring pulse says “Processing still running,” not “File work still running.”
- Export settings, deliberately damage the JSON, and try to import it. Confirm the
  panel reports failure and every setting remains exactly as it was before the import.
- Import a valid settings file and confirm all controls refresh immediately and retain
  their values after restarting NVDA.
- Repeat normal activity in focus and browse modes and confirm speech, Braille, click
  earcons, musical tones, history, and chat actions behave as in 2026.1.34.

### Fixed

- Background activity classification now uses the original detailed status rather than
  user-customized speech, so customized wording cannot make a completed file operation
  sound as though it is still running.
- Settings import is now transactional. If reading, validation, application, or saving
  fails, the add-on restores the complete previous configuration and refreshes the panel.

### Validation

- Added release assertions for transactional import and original-status background
  classification.
- Re-ran the source, syntax, sound, archive, metadata, and live NVDA-log audits.

## 2026.1.34

### What to test

- Start a file edit and confirm the recurring pulse says “Editing code still running.”
- Trigger reading or inspection and confirm it says “Checking files still running.”
- Let a file-reading, editing, or command step finish while the overall task remains busy.
  Confirm subsequent pulses say “Processing still running” instead of claiming the
  completed operation is still running.
- Confirm command, tests, tools, search, and thinking pulses retain their useful names.
- Repeat with Minimal and Full speech and confirm Braille receives the matching detailed pulse.

### Fixed

- Replaced the generic “File operation still running” background wording with activity-aware
  Editing code, Checking files, or File work wording.
- Finished intermediate steps now fall back to Processing for recurring announcements,
  avoiding statements such as “File operation still running” after Reading finished.

## 2026.1.33

### What to test

- Select Musical tones, submit a prompt, and confirm the Prompt submitted rising tone
  plays immediately.
- Let Codex continue working and confirm the short Working tone repeats at the configured
  interval during quiet gaps between other progress tones.
- Confirm command, file, search, test, tool, commentary, background, completion, and
  failure tones still postpone the next Working tone so sounds do not overlap excessively.
- Move focus into and away from ChatGPT and confirm monitoring active and inactive use
  musical rising and falling tones instead of click files.
- Switch back to Clicks and confirm submission, continuous Working, and monitoring cues
  still use the redesigned click earcons from 2026.1.32.
- Confirm completion, cancellation, or the maximum activity timeout stops both repeating
  click and tone Working sounds.

### Fixed

- The continuous Working routine previously required `soundStyle == "clicks"` and then
  hard-coded the click player, making a Working cue impossible in Musical tones mode.
- Continuous Working now accepts both Clicks and Musical tones and plays the selected style.
- Prompt submitted and monitoring active or inactive cues now follow the selected sound
  style rather than remaining partially hard-coded to clicks.
- Updated settings labels from “click” to “sound” where the option controls both styles.

## 2026.1.32

### What to test

- In Settings, select each Preview action and use Preview selected sound. Confirm every
  action is recognizable without playing its speech preview.
- Compare Running command with File editing. Running command should be a sharp low-to-high
  double click; file activity should be a dry close pair followed by a lower save-like hit.
- Confirm Search is a fast bright rise, Build and test is a measured three-step rise,
  and Tool is a tight high double click.
- Confirm Completion rises, Failure falls heavily, and Permission required alternates
  urgently without being painfully loud.
- Submit a prompt and distinguish its four-step send pattern from the single muted
  continuous Working tick.
- Leave a task running long enough to hear both background-progress patterns and confirm
  they remain gentle and do not resemble completion or failure.
- Move focus into and away from ChatGPT and confirm active rises while inactive falls.
- Repeat the complete sound review at Soft, Normal, and Loud volume levels.

### Changed

- Redesigned all 17 bundled click earcons. The previous set used essentially the same
  noise-heavy click with small brightness changes that could blur together in NVDA's
  normal audio mix.
- New earcons combine distinct muted, dry, sharp, bright, hollow, and heavy percussive
  textures with category-specific rhythm and pitch direction.
- Kept every signature short, monophonic, license-free, and available in clearly
  separated Soft, Normal, and Loud levels.

## 2026.1.31

### What to test

- Install over 2026.1.30 and confirm existing settings and Input Gestures assignments
  remain available under the new Codex Access Toolkit category.
- In Settings, test Concise, Informative, and Full Braille detail. Confirm Full preserves
  complete commands even when Minimal speech is selected.
- Run several different commands rapidly which share the same Minimal speech summary.
  Confirm every distinct command can still appear in Braille.
- Disable speech, enable Braille, and confirm Thinking, commands, file activity,
  commentary, background progress, permissions, failures, and completion flash in Braille.
- Disable “Allow urgent permission and failure announcements to interrupt current speech,”
  start reading text, and confirm an urgent alert does not cancel the current utterance.
  Re-enable it and confirm urgent alerts interrupt as expected.
- Review previous and next announcement history with speech and Braille configured at
  different detail levels. Confirm each channel presents its own stored text.
- Open diagnostics and confirm version 2026.1.31, Braille detail, urgent interruption,
  separate history counts, and all category output modes are reported.
- Open Recent chats, press Shift+F10, and confirm focus lands on Pin chat, Unpin chat,
  or Archive chat. Check the log and confirm the exact focused action type is named but
  the private chat title is not recorded.

### Renamed

- Codex Status Announcer is now **Codex Access Toolkit for NVDA**, reflecting its speech,
  Braille, sound, navigation, chat-management, and dialog-focus features.
- Preserved the internal `codexStatusAnnouncer` add-on and configuration identifiers so
  upgrades retain existing settings and assigned Input Gestures.

### Added

- Added independent Concise, Informative, and Full Braille detail profiles.
- Added an option controlling whether urgent permission and failure announcements cancel
  current NVDA speech before speaking.
- Added separate speech and Braille histories and channel-aware history review.
- Diagnostics now list every category's Speech, Sound, Braille, All, or Off routing mode.
- Added a direct test of the production `braille.handler.message` output path.

### Fixed

- Different detailed Braille updates are no longer suppressed merely because their
  Minimal speech summaries are identical.
- Diagnostics now derive their version from current release metadata instead of reporting
  the obsolete 2026.1.18 value.
- Shift+F10 failure feedback now distinguishes failure to focus a button from failure to
  activate an action, and successful logs identify Pin, Unpin, or Archive precisely.

## 2026.1.30

### What to test

- Open searchable chat history, focus a Recent chat, and press Shift+F10. Confirm the
  history window closes and focus lands directly on Pin chat or Unpin chat.
- Press Tab and confirm focus moves to Archive chat. Activate it and confirm the exact
  selected chat is archived.
- Test a chat for which Pin/Unpin is unavailable and confirm focus falls back to Archive chat.
- Focus an Archived chat and press Shift+F10. Confirm Open archived chat remains available.

### Changed

- Shift+F10 on a recent chat now bypasses the add-on-owned action menu and places focus
  directly on ChatGPT's Pin chat or Unpin chat button, falling back to Archive chat.
- Merely pressing Shift+F10 never activates Pin or Archive; the user remains in control
  and can inspect or activate the focused button normally.

## 2026.1.29

### What to test

- Open searchable chat history, focus a Recent chat, and press Shift+F10. Confirm an
  accessible Windows menu contains Pin or unpin chat and Archive chat.
- Choose Pin or unpin chat and confirm the selected chat's exposed Pin chat or Unpin chat
  control is activated.
- Repeat and choose Archive chat. Confirm that exact selected chat is archived and the
  add-on does not report that the chat could not be opened.
- Use the dedicated Context Menu key and confirm it opens the same action menu.
- Focus an Archived chat, press Shift+F10, and confirm the menu offers Open archived chat.

### Fixed

- Current ChatGPT builds do not expose the assumed per-sidebar-chat options button. Logs
  showed `selected chat options button not found`, even though focusing a chat exposed
  separate Pin chat and Archive chat buttons in the accessible tab order.
- Shift+F10 now opens an add-on-owned, accessible Windows menu with explicit Pin/Unpin and
  Archive choices instead of searching for the removed options button.
- After a choice, the add-on focuses the exact selected sidebar chat and retries briefly
  while Chromium exposes its action buttons, then activates only an exact Pin chat,
  Unpin chat, or Archive chat match.
- Searches only the selected chat's bounded accessible container, preventing transcript
  text that mentions “Pin chat” or “Archive chat” from being mistaken for an action.

## 2026.1.28

### What to test

- Install a plug-in from any ChatGPT marketplace, settings, or pop-up surface outside
  the Codex conversation document. Confirm its progress bar is announced.
- While installation progress is active, submit a Codex task. Confirm the task's working
  state continues after installation completes and stops only when the task completes.
- Rapidly navigate away immediately after choosing an archived chat. Confirm the correct
  title is retained when navigation succeeds and cleared when launching fails.
- Repeat the complete 2026.1.27 test list, including unrelated application dialogs.

### Additional audit fixes

- Expanded plug-in progress detection from Codex-document descendants to all supported
  ChatGPT process objects while retaining installation-specific wording checks.
- Hardened ChatGPT and Codex object classification against stale or failing app-module,
  role, name, and parent properties from Chromium accessibility objects.
- Transfers installation-owned busy state to a newly submitted prompt, explicit Codex
  activity, or new commentary so installation completion cannot terminate later work.
- Records an archived title before launching its native link, covering an unusually fast
  document switch, and clears it immediately if Windows rejects the link.
- Updated the packaged manifest's short changelog, which still described an older Recent
  chats fix despite the newer package contents.

## 2026.1.27

### What to test

- Trigger ChatGPT permission, confirmation, and error dialogs and confirm focus moves
  inside them. Open an NVDA or unrelated application dialog and confirm the add-on does
  not alter its focus.
- Begin a Codex task that remains active while a plug-in installation completes. Confirm
  the completion announcement does not stop Codex's working clicks or background speech.
- Open a history chat, cancel or interrupt navigation, wait more than ten seconds, and
  then change views. Confirm the old title is not announced for the unrelated view.
- Exercise plug-in progress, archived and recent chat opening, Shift+F10 chat actions,
  unarchive focus, silent background activity, and the current-activity command.

### Audit fixes

- Restricted automatic pop-up focus to accessible objects belonging to ChatGPT. The
  previous generalized handler could inspect unrelated application dialogs.
- Tracks whether plug-in installation initiated the add-on's busy state. Installation
  completion now clears that state only when it owns it, preserving concurrent Codex
  computer-use, commands, tests, and other autonomous work.
- Expires pending history titles after ten seconds so failed or cancelled navigation
  cannot mislabel a later document as the selected chat.
- Hardened progress-bar inspection against transient Chromium accessibility failures so
  a bad name, value, description, or parent object cannot escape the NVDA event handler.
- Keeps plug-in progress ownership metadata bounded with its percentage cache, including
  installations that disappear without exposing a completion event.
- Reviewed current NVDA tracebacks; observed process-access, speech-symbol, UI Automation,
  and Chromium COM warnings were outside this add-on, with no add-on traceback present.

## 2026.1.26

### What to test

- Create a new chat and switch among chats from the sidebar and searchable history.
  Confirm NVDA announces that the chat opened, including the selected history title
  when it is known.
- Start a computer-use or autonomous task, move focus to Outlook or another application,
  and leave Codex working through a period with no visible status label. Confirm the
  configured background-progress speech and sounds continue.
- Assign the existing “Report current Codex activity or repeat the latest message”
  command in NVDA's Input Gestures dialog. Invoke it outside ChatGPT during active work,
  after a commentary update, and while idle.
- Confirm newly exposed commentary continues to announce outside ChatGPT when the
  existing commentary setting is enabled, with no duplicate sentence announcements.

### Added

- Announces a newly attached Codex conversation document. Chats opened from searchable
  history include the selected title; other conversation switches use a concise generic
  announcement.
- The existing assignable latest-status command now reports a useful current activity
  and elapsed time when Codex is busy but has exposed no recent commentary. It remains
  unassigned by default to avoid gesture conflicts.

### Fixed

- Background-progress speech previously returned early whenever the transient status
  button disappeared, even though Codex remained busy. Spoken heartbeat updates now
  continue through those silent computer-use, automation, and tool-execution gaps.

## 2026.1.25

### What to test

- Install a ChatGPT plug-in or connector and confirm NVDA announces that installation
  has started, meaningful percentage changes, and completion.
- Repeat once in focus mode and once in browse mode.
- Confirm unchanged percentages are not repeated and NVDA remains responsive during a
  busy installation.
- With speech disabled, confirm the configured tool-progress sound still plays. With a
  braille display enabled in the add-on, confirm the progress message flashes in braille.
- Observe an unrelated progress bar and confirm it is not described as a plug-in install.

### Added

- Added dedicated handling for accessible progress bars whose surrounding ChatGPT text
  identifies a plug-in, connector, or extension installation.
- Announces indeterminate installation activity, percentage progress in ten-percent
  buckets, and completion through the existing speech, braille, and sound routing.
- Works from global show and value-change events, independent of focus or browse mode,
  and bounds its progress cache to protect long-running NVDA sessions.

## 2026.1.24

### What to test

- Trigger a permission request, an archive or deletion confirmation, and any available
  error or account notice. Confirm focus enters each dialog when it opens.
- If ChatGPT already focuses a control inside a dialog, confirm the add-on preserves
  that focus instead of moving it again.
- Tab through each dialog and confirm all controls remain reachable and no option is
  activated automatically.
- Open and close several dialogs consecutively and confirm NVDA remains responsive and
  each newly created dialog receives focus once.

### Fixed

- Generalized automatic focus handling from permission requests to every accessible
  ChatGPT pop-up with the dialog role, including confirmations, errors, account notices,
  file prompts, and future dialogs using the same accessible pattern.
- Preserves correct native focus when it is already inside the dialog. Otherwise it
  focuses the first useful interactive control, avoiding Close, Cancel, and Dismiss when
  another control is available; the dialog itself is the final fallback.
- Permission prompts retain decision-control targeting, but focus movement never
  activates or chooses any action.

## 2026.1.23

### What to test

- Start a task that causes Codex to request permission. Confirm focus automatically
  enters the approval dialog and lands on its first available decision button.
- Arrow or Tab through every approval choice and confirm NVDA speaks and brailles each
  option. Confirm the add-on never activates an option automatically.
- Deny or cancel one request, then trigger another and confirm focus moves into the new
  dialog again.
- Open the ordinary Change permissions control and confirm the add-on does not mistake
  that settings menu for an approval request.

### Fixed

- Newly displayed Codex permission and approval dialogs now receive focus automatically.
- Focus lands on the first accessible Allow, Approve, Deny, or Reject decision button;
  the add-on only moves focus and never makes the permission decision for the user.
- Detection is restricted to actual dialog ancestry and permission-request wording, with
  bounded traversal to protect NVDA responsiveness.

## 2026.1.22

### What to test

- Open chat history, Tab to Archived chats, select a task, and press Enter.
- Confirm focus lands on the Unarchive and open button when Codex displays its
  confirmation document. Press Enter and confirm the task opens.
- Repeat with a second archived task and confirm NVDA does not pause or freeze while
  waiting for the button.
- Cancel or navigate away during a confirmation and confirm the focus retry stops after
  a few seconds with a useful announcement.

### Fixed

- Added a bounded, non-blocking focus handoff to Codex's exact Unarchive and open button
  after launching an archived task. This accommodates the delay while Chromium replaces
  the current virtual buffer with the confirmation document.
- The retry stops as soon as focus is set and is cancelled when the add-on terminates.
- Corrected the loaded-version log entry so it reports the current add-on version rather
  than the obsolete 2026.1.18 value.

## 2026.1.21

### What to test

- Open chat history, focus a Recent chat, and press Shift+F10. Confirm ChatGPT's custom
  menu opens and contains Pin chat and Archive chat.
- Repeat with the dedicated Context Menu key, if present.
- Choose Pin chat, reopen history, and confirm Shift+F10 still opens the correct chat's
  menu. Repeat with Archive chat on a disposable task.
- Confirm Enter still opens the selected chat normally.

### Fixed

- Shift+F10 now activates ChatGPT's custom conversation-options button associated with
  the selected sidebar chat. Sending Shift+F10 to the title button itself was accepted
  by NVDA but ignored by ChatGPT, so Pin chat and Archive chat never appeared.
- Uses bounded accessible-object traversal and narrowly recognized options-button names
  to avoid activating an unrelated More or Options control elsewhere in the interface.
- Archived entries now explain that the task must be opened before its active-chat Pin
  or Archive menu can be used.

## 2026.1.20

### What to test

- Open chat history, focus a Recent chat, and press Shift+F10. Confirm its native
  context menu opens on the selected chat.
- Repeat with the dedicated Context Menu key if the keyboard has one.
- Focus an Archived chat and repeat both commands. Confirm the selected archived task
  is acted on and NVDA remains responsive.
- Press Enter on Recent and Archived tasks to confirm ordinary opening still works.

### Fixed

- The Recent and Archived list boxes now handle Windows' native context-menu event.
  Previously the dialog depended only on a character-hook fallback, so Shift+F10 and
  the dedicated Context Menu key could be swallowed by the list control.
- Centralized context-action submission and guards it against duplicate delivery while
  the history dialog is closing.

## 2026.1.19

### What to test

- Open chat history, Tab to Archived chats, select a task, and press Enter. Confirm
  Codex navigates to that exact task without an error announcement.
- Double-click an archived task and confirm the same behavior.
- Press Shift+F10 on an archived task and confirm the task opens without freezing NVDA.
- Return to Recent chats and confirm Enter and Shift+F10 still perform their existing
  open and context-menu actions.

### Fixed

- Fixed archived tasks not opening from the searchable chat-history list. Archived
  selections now open through Codex's registered `codex://threads/<thread ID>` link
  instead of looking for a sidebar button that cannot exist while a task is archived.
- Validates the locally indexed thread ID as a UUID before passing it to Windows.
- When archived tasks share the same title, consistently selects the newest entry
  rather than silently retaining the oldest one.

## 2026.1.18

### What to test

- Open the searchable chat-history dialog, select several Recent chats, and press
  Enter. Confirm each selected chat opens.
- Repeat using a double-click and Shift+F10. Confirm the selected chat opens or its
  native context menu appears.
- Confirm the Recents section heading is no longer listed as a chat.
- Confirm a conversation phrase matching a chat title cannot activate an unrelated
  named button.
- Retest the Archived list separately; this patch does not change archive behavior.

- Fixed the 2026.1.17 exact-name safety check rejecting valid Recent-chat buttons
  whose title is exposed as child text while Chromium leaves the button name empty.
- Accepts an unnamed button only when the exact selected title was found inside that
  button; named buttons still require an exact normalized title match.
- Filters the Recents section heading out of the Recent-chat results.

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
