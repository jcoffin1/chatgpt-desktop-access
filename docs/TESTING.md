# Manual NVDA integration test checklist

Complete this checklist with the packaged add-on before publishing a release.

## Installation and startup

- Install the package and restart NVDA when prompted.
- Confirm the installed version and ensure the NVDA log has no add-on traceback.
- Confirm the one-time What's New document opens at the top and contains only
  the concise current-version summary. Confirm complete history remains available
  from the Settings panel.

## Settings organization

- Open ChatGPT Desktop Access Settings and confirm General, Speech and Braille,
  Sounds, Activity Output, Wording and Preview, Browser Access, Advanced, and
  Support are exposed as eight notebook pages.
- Use Control+Tab and Shift+Control+Tab to move through every page. Confirm Tab
  and Shift+Tab reach every control without leaving content clipped or hidden.
- Use the displayed Alt access keys on each page. Confirm each access key reaches a
  different control on that page and none activates a control from a hidden page.
- Confirm General contains the primary output choices, background timing is under
  Activity Output, technical compatibility controls are under Advanced, and
  account, documentation, report, import, and export actions are under Support.
- On Activity Output, change multiple categories, switch between them, Apply,
  reopen Settings, and confirm enabled state and routing remain independent. As
  each value changes, confirm the category selector immediately includes both its
  enabled state and route without requiring extra tabbing.
- Import a settings file while a non-first activity category is selected and
  confirm every page and the selected category refresh without stale values.
- Export settings and confirm the Save dialog suggests
  `chatgpt-desktop-access-settings.json` without forcing that name or location.

## Focus and browse modes

- Assign the Open searchable and arrow-navigable ChatGPT or Codex chat history
  action in Input Gestures. Invoke it from focus mode and browse mode, search by title,
  Tab from Recent chats to Archived chats, browse both lists with arrows, open
  with Enter, and verify Shift+F10 closes the history dialog and moves focus to
  the selected recent chat's Pin, Unpin, or Archive button.
- Populate Codex history, switch to ChatGPT mode, and open history again. Confirm
  the title and both lists identify ChatGPT and contain no Codex titles. Switch
  back to Codex and confirm its own cached lists return. Confirm a history dialog
  open during a mode change closes without performing its selected action.
- Confirm Codex archived titles load from the local session index without first
  visiting Settings. In ChatGPT mode, confirm archived titles remain separate
  and appear only after ChatGPT exposes its accessible Archived chats view.
- In ChatGPT focus and browse modes, confirm Control+1 reads the newest real
  conversation message and Control+2 through Control+0 read progressively older
  turns. Confirm timestamps, response controls, progress labels, hidden response
  copies, and the prompt are omitted. Confirm the keys pass through elsewhere.
- In Input Gestures, confirm all ten message positions are separately named.
  Reassign one to Alt+1, remove a different default, restart NVDA, and confirm
  the custom assignments persist without changing the remaining positions.
- Reach Add files and more, the model control, and Change permissions using ordinary
  Tab or browse-mode navigation. Confirm each recognized control has a concise,
  useful description and retains its native name, role, collapsed or expanded state,
  and action. Open with Enter or Space, navigate with arrows, choose with Enter, and
  close with Escape. Confirm no actions for these controls appear in Input Gestures.
- Move focus into ChatGPT and confirm one active click; move to another app and
  confirm one inactive click. Moving inside ChatGPT must not repeat either cue.
- Close ChatGPT while it is focused and confirm the inactive click plays.
- In focus mode at the Codex prompt, run a task containing commentary, a shell
  command, a file edit, and tests. Confirm each update is announced once.
- Switch to browse mode during a second task and confirm announcements continue.
- Switch repeatedly between modes and confirm monitoring does not detach.
- In a large conversation, read an older response in browse mode with Say All, arrow
  navigation, and Braille panning while a new response streams. With **Keep conversation
  reading stable** enabled, confirm streamed `Response:` updates do not interrupt speech,
  replace the Braille line, or relocate the browse cursor. Disable the option and confirm
  native live-region behavior returns. Focus the prompt in focus mode and confirm new
  response output still works normally.
- Repeat while a permission dialog opens. Confirm the dialog receives focus and its
  urgent speech and Braille output are never suppressed by reading protection.

## Embedded browser access

- In **NVDA > Preferences > Input Gestures > ChatGPT Desktop Access**, assign
  **Open the searchable Embedded Browser Navigator**. Confirm the command has no
  default gesture and is unavailable outside ChatGPT.
- Open the Navigator from the embedded page in focus mode and browse mode. Search
  by name, change categories, and confirm the results list announces both its
  matching count and whether the safe scan limit was reached.
- From the results list, confirm Enter and double-click move to an item without
  activating it. Open Shift+F10 and confirm Activate performs exactly one native
  action only for a supported control.
- Test Page summary, Accessible snapshot, Copy address, Open in default browser,
  Refresh page items, Restore last location, and Return to ChatGPT prompt.
  Confirm each action happens only when explicitly requested.
- Test duplicate page items with the same name and confirm Restore last location
  returns to the same occurrence after a refresh. Remove or replace the page and
  confirm a stale or defunct item produces a safe error instead of moving focus.
- Enable privacy redaction and confirm the page title, Navigator item labels,
  summary, and snapshot are redacted. Confirm full addresses remain hidden in the
  dialog and are copied or opened only through their explicit actions.
- Run the Navigator on a large page while typing from a Braille display. Confirm
  scanning yields repeatedly, speech and Braille remain responsive, and no page
  update changes focus while the Navigator is open.

- Open ChatGPT's Browser submenu and arrow through Open Browser Tab, Focus Browser
  Address Bar, and Reload Browser Page. Confirm neither the menu nor its items
  trigger embedded-browser entry or exit announcements.
- Open ChatGPT's embedded browser or web preview and confirm NVDA announces entry
  only after focus reaches the nested web document. Move among its controls and
  confirm no repeated entry notice. Leave for another ChatGPT control and confirm
  the return notice occurs once.
- Verify recognized Back, Forward, Reload, Stop, address, external-browser, Close,
  and page-document controls retain their native names, roles, states, actions,
  and keyboard behavior while gaining a concise description.
- Use the page in both focus mode and browse mode. Confirm Tab and Shift+Tab move
  among controls, NVDA+Space switches modes, and H, K, F, and D retain their normal
  browse-mode behavior. Confirm the add-on never moves focus or activates a page
  control automatically.
- Navigate between two pages and confirm useful page titles are announced once.
  If the page exposes loading progress, confirm it is announced at most once per
  ten-percent step and that unrelated downloads elsewhere are not called browser
  loading.
- Start a Codex task, move into the embedded browser while it runs, and confirm
  activity speech, sounds, and urgent Braille continue without a task reset. Then
  return to the conversation and confirm the original virtual buffer is still
  monitored.
- Turn each Browser Access option off independently and confirm only that feature
  stops. Open **View embedded browser help** and confirm focus starts at the top.

## Output channels

- Test Essential, Balanced, and Informative Minimal speech. Then test Standard,
  Developer, and Raw Full speech. Confirm filtered speech does not disable
  independently configured braille or sounds.
- Turn NVDA speech mode off and confirm configured progress sounds still play.
- Re-enable speech and confirm speech and sounds follow their selected routes.
- With a braille display connected, confirm flash messages appear independently
  of speech and work in both focus and browse modes.

## Compatibility and support

- Run the assignable compatibility self-test and copy sanitized diagnostics.
- Save a sanitized support report from Support and through an
  assigned gesture. Confirm it includes add-on and NVDA versions, settings,
  monitoring state, and error status but excludes chat and command text.
- Test a built-in synthesizer and at least one third-party synthesizer.
- Test speech mode Off, a connected braille display, sleep mode, multiple Codex
  windows, and closing ChatGPT while monitoring is active.
- Export and import settings, then test speech-profile reset with Cancel and OK.
- Test command punctuation, truncation, and Copy latest full Codex progress.

## Sounds and custom announcements

- Preview each selected sound and speech action separately.
- Test Clicks and Tones plus Soft, Normal, and Loud click levels.
- Confirm the continuous Working sound repeats while busy, pauses around other
  action sounds, uses the selected click volume in Clicks mode, and uses the
  dedicated Working pattern in Tones mode.
- Type a prompt and press Enter, then repeat using the Send button. Confirm the
  Prompt submitted click starts immediately in both cases without a keyboard
  gesture, followed by Working clicks after the configured start delay.
- Repeat submission with the physical Enter key and a Braille display's standalone
  dot-8 Enter chord. Confirm each produces exactly one immediate submission click,
  Shift+Enter still inserts a new line, and no gesture is consumed or sent twice.
- Disable the distinct submission click and confirm an immediate Working click is
  used instead. Test minimum and maximum repeating-click start delays.
- Customize one announcement with `{message}`, save, and confirm live output.
- Restore the customized announcement and confirm built-in wording returns.

## Task state and attention

- Run a task longer than two background intervals and confirm progress pulses
  occur only while the task is active.
- Include a quiet processing interval longer than 30 seconds and confirm Working
  clicks continue until an explicit completion or cancellation signal.
- Complete and cancel tasks, confirming pulses stop promptly.
- Confirm the continuous Working sound also stops immediately when each task ends.
- Confirm a completed response stops Working clicks even when the NVDA log shows
  `Response complete` only as braille output and no live-region plug-in event.
- Confirm commentary followed by a delayed tool start (at least 11 seconds) does
  not stop Working clicks during the `Response complete` settling window.
- Trigger a permission or user-input request and confirm its urgent announcement.
- Confirm a final commentary update does not restart background pulses.
- Start work in two different Codex tasks, switch between them, and confirm no
  history, prompt state, or continuous-click state leaks between documents.
- Switch among idle tasks with different conversation lengths before typing and
  confirm no Prompt submitted or Working clicks play.
- Confirm a tentative Response complete marker does not stop Working clicks if
  another command begins during the 30-second settling period.
- Generate repeated identical accessibility events and confirm each announcement
  is emitted once while later legitimate repeats remain available.

## Performance and shutdown

- Run a long task in a lengthy conversation and check that NVDA remains responsive.
- Type a multi-sentence prompt from a Braille display without pausing. Confirm character
  entry and Braille feedback remain responsive and no full-buffer diagnostic scan is
  logged until at least 1.25 seconds after typing stops.
- Repeat with contracted Braille and pause before pressing Space. Confirm no scan occurs
  while the display shows the uncommitted dot composition, even before Chromium emits a
  prompt text-change event. Confirm routing and scroll gestures still work normally.
- With contracted Braille enabled, repeatedly type `we need using Braille from the Sense`
  at normal speed without pausing between words. Confirm the first cell of the word after
  each Space is retained: `need` must not become `eed`, and `using` must not become `sing`.
  Open the add-on diagnostic report and confirm **Preserved Braille compositions**
  increases when ChatGPT delivers the delayed caret event. Repeat the phrase in Outlook
  and confirm the add-on does not change its Braille input or caret behavior there.
- Type `The developers need to see the error` at normal Braille Sense speed and confirm
  the result is exact. In an NVDA I/O log, compare each `Input: br(hims.BrailleSense)`
  timestamp with the following untranslated `Braille regions text` update. Confirm the
  enabled add-on no longer adds the repeated roughly 160–180 millisecond queue seen in
  the regression log and remains close to the disabled-add-on baseline.
- With ChatGPT idle, move to Outlook for at least one minute. Confirm no repeated
  ChatGPT URL-property lookups or full-buffer scans occur. Then run a task while focus
  remains in Outlook and confirm event-driven progress and completion still arrive.
- Repeat the idle test while the empty ChatGPT prompt remains focused. Confirm there is
  no periodic compatibility scan until a relevant accessibility event marks it dirty.
- Press Enter from a populated prompt and confirm the editor clears without an add-on
  traceback, Prompt submitted is detected, and continuous Working feedback begins.
- Review the NVDA log for repeated buffer-inspection errors or unexpected output.
- Restart NVDA while Codex is open and confirm the add-on attaches again cleanly.
