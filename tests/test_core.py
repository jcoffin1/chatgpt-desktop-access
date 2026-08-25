import importlib.util
import json
import math
import os
from pathlib import Path
import struct
import tempfile
import unittest
import wave


CORE_PATH = Path(__file__).parents[1] / "globalPlugins" / "codexStatusAnnouncer" / "core.py"
PROJECT_ROOT = Path(__file__).parents[1]
PLUGIN_PATH = CORE_PATH.parent / "__init__.py"
SPEC = importlib.util.spec_from_file_location("codex_status_core", CORE_PATH)
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)
AnnouncementHistory = core.AnnouncementHistory
firstStatusLabel = core.firstStatusLabel
statusMessage = core.statusMessage
statusDetails = core.statusDetails
redactSensitive = core.redactSensitive
elapsedSeconds = core.elapsedSeconds
completedTextDelta = core.completedTextDelta
outputActions = core.outputActions
tonePattern = core.tonePattern
nextBusyState = core.nextBusyState
pollDelay = core.pollDelay
shouldPlayContinuousWorkingClick = core.shouldPlayContinuousWorkingClick
focusStateTransition = core.focusStateTransition
promptSubmissionTransition = core.promptSubmissionTransition
userMessageNumber = core.userMessageNumber
userMessageSubmissionTransition = core.userMessageSubmissionTransition
confirmedUserMessageSubmission = core.confirmedUserMessageSubmission
isStopControlLabel = core.isStopControlLabel
stopControlTransition = core.stopControlTransition
shouldSuppressDuplicate = core.shouldSuppressDuplicate
shouldLogDiagnosticSnapshot = core.shouldLogDiagnosticSnapshot
responseCompletionTransition = core.responseCompletionTransition
shouldFinalizeResponseCompletion = core.shouldFinalizeResponseCompletion
isTaskCompletionLabel = core.isTaskCompletionLabel
intermediateCompletionCategory = core.intermediateCompletionCategory
isKnownNonStatusButton = core.isKnownNonStatusButton
soundKey = core.soundKey
categoryOutputActions = core.categoryOutputActions
announcementPriority = core.announcementPriority
changelogForDisplay = core.changelogForDisplay
viewerTitleMatches = core.viewerTitleMatches
previewSelection = core.previewSelection
formatCustomAnnouncement = core.formatCustomAnnouncement
loadArchivedThreads = core.loadArchivedThreads
semanticStatusKey = core.semanticStatusKey
shouldSuppressSemanticDuplicate = core.shouldSuppressSemanticDuplicate
formatCommandSpeech = core.formatCommandSpeech
promptControlKind = core.promptControlKind
repairConfigurationValues = core.repairConfigurationValues
chatTitleMatches = core.chatTitleMatches


class StatusMessageTests(unittest.TestCase):
	def test_release_metadata_and_default_gesture_policy_are_consistent(self):
		manifest = (PROJECT_ROOT / "manifest.ini").read_text(encoding="utf-8")
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		self.assertIn("version = 2026.1.17", manifest)
		self.assertIn('ADDON_VERSION = "2026.1.17"', plugin)
		self.assertNotIn("Adds assignable focus- and browse-mode actions", manifest)
		self.assertIn('default=\'full\'', plugin)
		self.assertIn("fullSpeechProfile", plugin)
		self.assertIn("default='developer'", plugin)
		self.assertIn("minimalSpeechProfile", plugin)
		self.assertIn("default='balanced'", plugin)
		self.assertNotIn("__gestures", plugin)
		self.assertNotIn("gesture=", plugin)
		self.assertNotIn("self._chatHistoryDialog.ShowModal", plugin)
		self.assertIn('label=_("Recent chats:")', plugin)
		self.assertIn('label=_("Archived chats:")', plugin)
		self.assertIn("self.recentList", plugin)
		self.assertIn("self.archivedList", plugin)
		self.assertIn("message = _completeChangelogMessage()", plugin)
		self.assertIn("_showBrowseableMessageAtTop(", plugin)
		self.assertIn('CURRENT_RELEASE_NOTES, _("Codex Status Announcer — what\'s new")', plugin)
		self.assertNotIn("Unable to load the complete startup changelog", plugin)
		self.assertNotIn("import sqlite3", CORE_PATH.read_text(encoding="utf-8"))
		self.assertIn("_repairConfiguration()", plugin)
		self.assertIn("script_runCompatibilitySelfTest", plugin)
		self.assertIn("script_copyLatestFullProgress", plugin)
		self.assertIn("_onExportSettings", plugin)
		self.assertIn("_onImportSettings", plugin)
		self.assertIn("_loadControlsFromConfiguration", plugin)
		self.assertIn("settings file exceeds 1 MB", plugin)
		self.assertIn("_onResetSpeechSettings", plugin)
		self.assertIn("_onRefresh", plugin)
		self.assertNotIn("script_openAddFilesAndMore", plugin)
		self.assertNotIn("script_openModelSelector", plugin)
		self.assertNotIn("script_openChangePermissions", plugin)
		self.assertNotIn("_boundedDescendants", plugin)
		self.assertIn("class CodexPromptControlOverlay", plugin)
		self.assertIn("chooseNVDAObjectOverlayClasses", plugin)
		self.assertIn("_codexNativeDescription", plugin)
		self.assertNotIn("could not enhance a prompt control", plugin)
		self.assertIn("_chatHistoryActionTimer", plugin)
		self.assertIn("chatTitleMatches(title", plugin)
		self.assertIn("unrecognized buttons: count=%d, lengths=%s", plugin)
		self.assertNotIn('unrecognized buttons: %s", list(snapshot)', plugin)

	def test_restricted_nvda_runtime_does_not_require_known_optional_modules(self):
		source = CORE_PATH.read_text(encoding="utf-8") + PLUGIN_PATH.read_text(encoding="utf-8")
		for forbiddenImport in ("import sqlite3", "import requests", "import numpy", "import yaml"):
			self.assertNotIn(forbiddenImport, source)

	def test_semantic_duplicate_suppression_ignores_cosmetic_wording_changes(self):
		self.assertEqual("editing code", semanticStatusKey("Editing file"))
		self.assertEqual("editing code", semanticStatusKey("Editing code"))
		self.assertTrue(shouldSuppressSemanticDuplicate("Editing file", "Editing code", 0.5))
		self.assertFalse(shouldSuppressSemanticDuplicate("Running tests", "Editing code", 0.5))
		self.assertFalse(shouldSuppressSemanticDuplicate("Editing file", "Editing code", 1.5))

	def test_command_speech_punctuation_and_length_controls(self):
		self.assertEqual(
			("rg files pipe sort redirect to output.txt", False),
			formatCommandSpeech("rg files | sort > output.txt", "enhanced", 240),
		)
		literal, shortened = formatCommandSpeech("one && two", "literal", 240)
		self.assertEqual("one ampersand ampersand two", literal)
		self.assertFalse(shortened)
		short, shortened = formatCommandSpeech("x" * 100, "normal", 40)
		self.assertTrue(shortened)
		self.assertLessEqual(len(short), 41)

	def test_prompt_toolbar_control_names_are_classified_without_conversation_search(self):
		self.assertEqual("files", promptControlKind("Add files and more"))
		self.assertEqual("files", promptControlKind("Attach files"))
		self.assertEqual("permissions", promptControlKind("Change permissions"))
		self.assertEqual("model", promptControlKind("Select model"))
		self.assertEqual("model", promptControlKind("GPT-5.6 Developer"))
		self.assertEqual("model", promptControlKind("o4-mini"))
		self.assertEqual("", promptControlKind("Send"))

	def test_configuration_repair_covers_choices_numbers_booleans_and_strings(self):
		values = {
			"outputCommands": "invalid", "workingClickStartDelayMs": -1,
			"maximumBusyMinutes": "bad", "speech": "false", "braille": "invalid",
			"supportedAppNames": 42,
		}
		repaired = repairConfigurationValues(
			values,
			{"outputCommands": (("all", "off"), "all")},
			{"workingClickStartDelayMs": (0, 10000, 750), "maximumBusyMinutes": (1, 240, 60)},
			(("speech", True), ("braille", True)),
			(("supportedAppNames", "chatgpt"),),
		)
		self.assertEqual("all", values["outputCommands"])
		self.assertEqual(750, values["workingClickStartDelayMs"])
		self.assertEqual(60, values["maximumBusyMinutes"])
		self.assertFalse(values["speech"])
		self.assertTrue(values["braille"])
		self.assertEqual("chatgpt", values["supportedAppNames"])
		self.assertEqual(len(repaired), len(set(repaired)))

	def test_chat_action_requires_exact_normalized_accessible_title(self):
		self.assertTrue(chatTitleMatches(" My   task ", "my task"))
		self.assertFalse(chatTitleMatches("My task", "Open My task menu"))
		self.assertFalse(chatTitleMatches("", ""))

	def test_archived_threads_load_from_jsonl_metadata_newest_first(self):
		with tempfile.TemporaryDirectory() as directory:
			codexRoot = Path(directory)
			archiveDirectory = codexRoot / "archived_sessions"
			archiveDirectory.mkdir()
			olderId = "00000000-0000-0000-0000-000000000001"
			newerId = "00000000-0000-0000-0000-000000000002"
			index = codexRoot / "session_index.jsonl"
			index.write_text(
				json.dumps(["valid JSON, wrong shape"]) + "\n" +
				json.dumps({"id": olderId, "thread_name": " Older   archived "}) + "\n" +
				json.dumps({"id": newerId, "thread_name": "Named archived"}) + "\n",
				encoding="utf-8",
			)
			olderPath = archiveDirectory / f"rollout-old-{olderId}.jsonl"
			newerPath = archiveDirectory / f"rollout-new-{newerId}.jsonl"
			olderPath.write_text("{}\n", encoding="utf-8")
			newerPath.write_text("{}\n", encoding="utf-8")
			os.utime(olderPath, (10, 10))
			os.utime(newerPath, (20, 20))
			self.assertEqual(
				((newerId, "Named archived"), (olderId, "Older archived")),
				loadArchivedThreads(codexRoot),
			)

	def test_every_click_tier_has_the_complete_valid_sound_inventory(self):
		sounds = CORE_PATH.parent / "sounds"
		expected = set(core.TONE_PATTERNS)
		for level in ("soft", "normal", "loud"):
			paths = sorted((sounds / level).glob("*.wav"))
			self.assertEqual(expected, {path.stem for path in paths}, level)
			for path in paths:
				with wave.open(str(path), "rb") as audio:
					self.assertEqual(1, audio.getnchannels(), path)
					self.assertEqual(2, audio.getsampwidth(), path)
					self.assertEqual(44100, audio.getframerate(), path)
					self.assertGreater(audio.getnframes(), 0, path)

	def test_click_volume_levels_are_clearly_separated(self):
		sounds = CORE_PATH.parent / "sounds"
		for soundPath in sorted((sounds / "normal").glob("*.wav")):
			levels = []
			for level in ("soft", "normal", "loud"):
				with wave.open(str(sounds / level / soundPath.name), "rb") as audio:
					raw = audio.readframes(audio.getnframes())
				samples = struct.unpack("<" + "h" * (len(raw) // 2), raw)
				levels.append(math.sqrt(sum(sample * sample for sample in samples) / len(samples)))
			with self.subTest(sound=soundPath.name):
				self.assertLess(levels[0], levels[1] * 0.45)
				self.assertLess(levels[1], levels[2] * 0.65)

	def test_preview_selection_returns_only_requested_item(self):
		items = (("thinking", "Thinking"), ("command", "Running command"))
		self.assertEqual(items[1], previewSelection(items, 1))
		self.assertEqual(items[0], previewSelection(items, -1))
		self.assertEqual(items[0], previewSelection(items, 99))
		self.assertIsNone(previewSelection((), 0))

	def test_custom_announcement_placeholders_and_safe_fallbacks(self):
		self.assertEqual(
			"Still running Build after 12 seconds: Running tests",
			formatCustomAnnouncement(
				"Still running {activity} after {seconds} seconds: {message}",
				"Running tests", "Build", 12,
			),
		)
		self.assertEqual("Running tests", formatCustomAnnouncement("", "Running tests"))
		self.assertEqual("Keep {unknown}", formatCustomAnnouncement("Keep {unknown}", "Running tests"))
		self.assertEqual("Keep {message.missing}", formatCustomAnnouncement("Keep {message.missing}", "Running tests"))

	def test_bounded_announcement_history_and_navigation(self):
		history = AnnouncementHistory(3)
		self.assertFalse(history.add(""))
		self.assertTrue(history.add("one"))
		self.assertFalse(history.add("one"))
		history.add("two")
		history.add("three")
		history.add("four")
		self.assertEqual(("two", "three", "four"), history.items())
		self.assertEqual("three", history.move(-1))
		self.assertEqual("two", history.move(-20))
		self.assertEqual("four", history.move(20))
		history.clear()
		self.assertEqual(0, len(history))
		self.assertEqual("", history.move(-1))

	def test_changelog_is_clean_for_accessible_display(self):
		markdown = "# Changelog\n\nAll notable changes.\n\n## 2.2.0\n\n### What to test\n\n- Added **history**.\n- Uses `clicks`."
		self.assertEqual(
			"Complete release history\n\nAll notable changes.\n\nVersion 2.2.0\n\nWhat to test\n\nAdded history.\nUses clicks.",
			changelogForDisplay(markdown),
		)

	def test_release_notes_viewer_title_guard(self):
		self.assertTrue(viewerTitleMatches("Codex — current release notes", "Codex — current release notes"))
		self.assertTrue(viewerTitleMatches("Codex — current release notes", "Codex — CURRENT RELEASE NOTES dialog"))
		self.assertFalse(viewerTitleMatches("Codex — current release notes", "NVDA Settings"))
		self.assertFalse(viewerTitleMatches("Codex — current release notes", "Unrelated Codex — current release notes"))
		self.assertFalse(viewerTitleMatches("", "NVDA Settings"))

	def test_output_actions_with_all_channels_available(self):
		self.assertEqual(
			{"speech": True, "braille": True, "tone": True},
			outputActions(True, False, True, True, "command"),
		)

	def test_output_actions_can_disable_tones_while_speech_is_available(self):
		self.assertEqual(
			{"speech": True, "braille": True, "tone": False},
			outputActions(True, False, True, False, "command"),
		)

	def test_output_actions_when_addon_speech_is_disabled(self):
		self.assertEqual(
			{"speech": False, "braille": True, "tone": True},
			outputActions(False, False, True, True, "command"),
		)

	def test_output_actions_when_nvda_speech_mode_is_off(self):
		self.assertEqual(
			{"speech": False, "braille": True, "tone": True},
			outputActions(True, True, True, True, "command"),
		)

	def test_output_actions_respect_disabled_fallback(self):
		self.assertEqual(
			{"speech": False, "braille": False, "tone": False},
			outputActions(True, True, False, False, "command"),
		)

	def test_output_actions_require_a_tone_category(self):
		self.assertFalse(outputActions(False, False, True, True, None)["tone"])

	def test_tone_patterns_are_short_and_category_specific(self):
		self.assertNotEqual(tonePattern("command"), tonePattern("search"))
		self.assertLessEqual(sum(duration for frequency, duration in tonePattern("completion")), 250)
		self.assertEqual(((392, 35), (523, 55)), tonePattern("backgroundPulse1"))
		self.assertNotEqual(tonePattern("backgroundPulse1"), tonePattern("backgroundPulse2"))

	def test_failure_uses_descending_tone_pattern(self):
		pattern = tonePattern("completion", "Command failed with exit code 1")
		frequencies = [frequency for frequency, duration in pattern]
		self.assertEqual(frequencies, sorted(frequencies, reverse=True))
		self.assertNotEqual(pattern, tonePattern("completion", "Command finished"))
		self.assertEqual("failure", soundKey("completion", "Command failed"))
		self.assertEqual("completion", soundKey("completion", "Command finished"))
		self.assertEqual("other", soundKey("unknown"))

	def test_final_commentary_cannot_restart_completed_task(self):
		self.assertTrue(nextBusyState(False, "command"))
		self.assertFalse(nextBusyState(True, "completion"))
		self.assertFalse(nextBusyState(False, commentary=True))
		self.assertTrue(nextBusyState(True, commentary=True))

	def test_active_polling_uses_lower_cost_fallback(self):
		self.assertEqual(250, pollDelay(True, 500))
		self.assertEqual(1000, pollDelay(False, 750))
		self.assertEqual(2000, pollDelay(False, 2000))

	def test_continuous_working_click_uses_quiet_gaps(self):
		self.assertTrue(shouldPlayContinuousWorkingClick(True, True, "clicks", True, 1.4, 1.4))
		self.assertFalse(shouldPlayContinuousWorkingClick(False, True, "clicks", True, 10, 1.4))
		self.assertFalse(shouldPlayContinuousWorkingClick(True, False, "clicks", True, 10, 1.4))
		self.assertFalse(shouldPlayContinuousWorkingClick(True, True, "tones", True, 10, 1.4))
		self.assertFalse(shouldPlayContinuousWorkingClick(True, True, "clicks", False, 10, 1.4))
		self.assertFalse(shouldPlayContinuousWorkingClick(True, True, "clicks", True, 1.39, 1.4))

	def test_focus_state_clicks_only_on_transitions(self):
		state, cue = focusStateTransition(None, False)
		self.assertEqual((False, ""), (state, cue))
		state, cue = focusStateTransition(state, True)
		self.assertEqual((True, "active"), (state, cue))
		state, cue = focusStateTransition(state, True)
		self.assertEqual((True, ""), (state, cue))
		state, cue = focusStateTransition(state, False)
		self.assertEqual((False, "inactive"), (state, cue))

	def test_prompt_submission_detects_populated_to_empty_transition(self):
		state, submitted = promptSubmissionTransition(None, False)
		self.assertEqual((False, False), (state, submitted))
		state, submitted = promptSubmissionTransition(state, True)
		self.assertEqual((True, False), (state, submitted))
		state, submitted = promptSubmissionTransition(state, True)
		self.assertEqual((True, False), (state, submitted))
		state, submitted = promptSubmissionTransition(state, False)
		self.assertEqual((False, True), (state, submitted))
		state, submitted = promptSubmissionTransition(state, False)
		self.assertEqual((False, False), (state, submitted))

	def test_user_message_number_and_submission_transition(self):
		self.assertEqual(80, userMessageNumber("Jump to user message 80"))
		self.assertIsNone(userMessageNumber("Jump to latest message"))
		state, submitted = userMessageSubmissionTransition(None, 79)
		self.assertEqual((79, False), (state, submitted))
		state, submitted = userMessageSubmissionTransition(state, 80)
		self.assertEqual((80, True), (state, submitted))
		state, submitted = userMessageSubmissionTransition(state, 80)
		self.assertEqual((80, False), (state, submitted))
		state, submitted = userMessageSubmissionTransition(state, None)
		self.assertEqual((80, False), (state, submitted))

	def test_user_message_increase_requires_active_stop_control(self):
		pending, confirmed = confirmedUserMessageSubmission(False, True, False)
		self.assertEqual((True, False), (pending, confirmed))
		pending, confirmed = confirmedUserMessageSubmission(pending, False, True)
		self.assertEqual((False, True), (pending, confirmed))
		self.assertEqual((False, False), confirmedUserMessageSubmission(False, False, True))

	def test_current_navigation_buttons_are_not_diagnostic_noise(self):
		for label in (
			"Review", "Review changed files", "Undo", "Open chat", "Edit message",
			"Worked for 2m 58s", "Worked for 27s",
			"Download Codex Status Announcer 2026.1.1",
		):
			self.assertTrue(isKnownNonStatusButton(label), label)

	def test_stop_control_and_duplicate_event_safeguards(self):
		self.assertTrue(isStopControlLabel("Stop generating"))
		self.assertTrue(isStopControlLabel("Cancel task"))
		self.assertFalse(isStopControlLabel("Send message"))
		state, stopped = stopControlTransition(False, True)
		self.assertEqual((True, False), (state, stopped))
		state, stopped = stopControlTransition(state, False)
		self.assertEqual((False, True), (state, stopped))
		self.assertTrue(shouldSuppressDuplicate("Working", "Working", 1.49))
		self.assertFalse(shouldSuppressDuplicate("Working", "Working", 1.5))
		self.assertFalse(shouldSuppressDuplicate("Thinking", "Working", 0.1))
		self.assertTrue(shouldLogDiagnosticSnapshot(("Copy",), (), 0))
		self.assertTrue(shouldLogDiagnosticSnapshot(("Retry",), ("Copy",), 1))
		self.assertFalse(shouldLogDiagnosticSnapshot(("Copy",), ("Copy",), 29.9))
		self.assertTrue(shouldLogDiagnosticSnapshot(("Copy",), ("Copy",), 30))
		self.assertFalse(shouldLogDiagnosticSnapshot((), ("Copy",), 30))

	def test_response_completion_marker_requires_baseline_and_busy_state(self):
		marker, initialized, completed = responseCompletionTransition(None, False, 100, False)
		self.assertEqual((100, True, False), (marker, initialized, completed))
		marker, initialized, completed = responseCompletionTransition(marker, initialized, 100, True)
		self.assertEqual((100, True, False), (marker, initialized, completed))
		marker, initialized, completed = responseCompletionTransition(marker, initialized, 200, True)
		self.assertEqual((200, True, True), (marker, initialized, completed))
		marker, initialized, completed = responseCompletionTransition(marker, initialized, None, True)
		self.assertEqual((200, True, False), (marker, initialized, completed))
		marker, initialized, completed = responseCompletionTransition(marker, initialized, 300, False)
		self.assertEqual((300, True, False), (marker, initialized, completed))

	def test_tentative_response_completion_requires_a_quiet_idle_scan(self):
		self.assertTrue(shouldFinalizeResponseCompletion(True, 30, 30, True, False, ""))
		self.assertFalse(shouldFinalizeResponseCompletion(True, 30, 30, True, True, ""))
		self.assertFalse(shouldFinalizeResponseCompletion(True, 30, 30, True, False, "Running command"))
		self.assertFalse(shouldFinalizeResponseCompletion(True, 30, 30, False, False, ""))
		self.assertFalse(shouldFinalizeResponseCompletion(True, 29.9, 30, True, False, ""))

	def test_only_whole_task_labels_end_continuous_activity(self):
		for label in ("Response complete", "Finished", "Completed task", "Cancelled"):
			self.assertTrue(isTaskCompletionLabel(label), label)
		for label in ("Ran command", "File edit complete", "Compiled project", "Search finished"):
			self.assertFalse(isTaskCompletionLabel(label), label)
		self.assertEqual("command", intermediateCompletionCategory("Ran rg --files"))
		self.assertEqual("file", intermediateCompletionCategory("File edit complete"))
		self.assertEqual("build", intermediateCompletionCategory("Compiled project"))
		self.assertEqual("search", intermediateCompletionCategory("Searched the web"))

	def test_known_codex_controls_are_not_diagnostic_noise(self):
		for label in (
			"Jump to user message 95", "Outputs", "Sources", "View all", "Copy", "Copy message",
			"Fork chat from here", "Scroll to bottom", "Add files and more", "Dictate",
			"Start voice chat", "Send", "Show 4 more files", "changelog.md+11-2",
		):
			self.assertTrue(isKnownNonStatusButton(label), label)
		self.assertFalse(isKnownNonStatusButton("Unexpected new control"))
		self.assertFalse(isKnownNonStatusButton("Running command"))

	def test_activity_messages(self):
		cases = {
			"Planning next step": "Thinking",
			"Thinking": "Thinking",
			"Working": "Working",
			"Analyzing files": "Analyzing",
			"Reading package metadata": "Checking files",
			"Writing tests": "Editing code",
			"Editing source": "Editing code",
			"Applying patch": "Applying changes",
			"Generating output": "Generating",
			"Waiting for process": "Waiting for command",
			"Using tool": "Using tool",
			"Searching the web": "Searching the web",
			"Running command Get-ChildItem": "Running command",
			"Running web search": "Searching the web",
			"Searched the web": "Web search finished",
			"Ran command": "Command finished",
			"Ran command and web search": "Command and web search finished",
			"Completed task": "Task finished",
			"Response complete: final answer": "Task finished",
			"Reviewed files": "Reading finished",
			"Updated source": "File updated",
		}
		for label, expected in cases.items():
			with self.subTest(label=label):
				self.assertEqual(expected, statusMessage(label))
		self.assertEqual(("build", "Running tests"), statusDetails("Running tests: 53 tests"))
		self.assertEqual(("build", "Generating"), statusDetails("Running build"))
		self.assertEqual(("tool", "Using tool"), statusDetails("Running tool: apply_patch"))

	def test_attention_messages(self):
		self.assertEqual(("attention", "Permission required"), statusDetails("Permission required to continue"))
		self.assertEqual(("attention", "User input required"), statusDetails("Waiting for your input"))
		self.assertFalse(nextBusyState(True, "attention"))
		self.assertEqual("urgent", announcementPriority("attention", "Permission required"))

	def test_first_status_label_falls_back_to_accessible_name(self):
		self.assertEqual("Planning", firstStatusLabel("", " Planning  "))

	def test_first_status_label_rejects_ordinary_button(self):
		self.assertEqual("", firstStatusLabel("Copy", "Retry"))

	def test_compilation_and_file_edit_messages(self):
		self.assertEqual("Compiling", statusMessage("Compiling project"))
		self.assertEqual("Compilation finished", statusMessage("Compiled project"))
		self.assertEqual("Editing code", statusMessage("File edit source.py"))
		self.assertEqual("File updated", statusMessage("File edit complete source.py"))

	def test_full_mode_returns_complete_normalized_label(self):
		self.assertEqual(
			"Running shell command: python -m unittest",
			statusMessage("  Running   shell command: python -m unittest  ", verbosity="full"),
		)

	def test_full_speech_profiles_offer_standard_developer_and_raw_detail(self):
		label = "  Running   shell command: python -m unittest discover -s tests  "
		self.assertEqual("Running command: python", statusMessage(label, verbosity="full", fullProfile="standard"))
		self.assertEqual(
			"Running shell command: python -m unittest discover -s tests",
			statusMessage(label, verbosity="full", fullProfile="developer"),
		)
		self.assertEqual(
			"Running   shell command: python -m unittest discover -s tests",
			statusMessage(label, verbosity="full", fullProfile="raw"),
		)

	def test_standard_full_profile_keeps_file_counts_and_useful_timing(self):
		self.assertEqual(
			"Running tests: 43 tests, 12 seconds",
			statusMessage("Testing project: 43 tests for 12 seconds", verbosity="full", fullProfile="standard"),
		)

	def test_minimal_speech_profiles_are_essential_balanced_and_informative(self):
		self.assertEqual("", statusMessage("Editing C:\\project\\core.py", minimalProfile="essential"))
		self.assertEqual("Thinking", statusMessage("Thinking", minimalProfile="essential"))
		self.assertEqual("Task finished", statusMessage("Response complete", minimalProfile="essential"))
		self.assertEqual("Checking files", statusMessage("Inspecting source", minimalProfile="balanced"))
		self.assertEqual("Editing code", statusMessage("Editing C:\\project\\core.py", minimalProfile="balanced"))
		self.assertEqual(
			"Editing code: core.py",
			statusMessage("Editing C:\\project\\core.py", minimalProfile="informative"),
		)
		self.assertEqual(
			"Running tests: 43 tests, 12 seconds",
			statusMessage("Testing project: 43 tests for 12 seconds", minimalProfile="informative"),
		)

	def test_minimal_results_distinguish_success_failure_and_file_updates(self):
		self.assertEqual("Tests passed", statusMessage("Tests passed: 43 tests", minimalProfile="balanced"))
		self.assertEqual("Tests failed", statusMessage("Tests failed: 1 failure", minimalProfile="balanced"))
		self.assertEqual("File updated", statusMessage("Updated core.py", minimalProfile="balanced"))
		self.assertEqual("Waiting for command", statusMessage("Waiting for command", minimalProfile="balanced"))
		self.assertEqual(
			"Editing: core.py",
			statusMessage("Editing C:\\project\\core.py", verbosity="full", fullProfile="standard"),
		)

	def test_categories(self):
		self.assertEqual(("command", "Running command"), statusDetails("Executing shell command: dir"))
		self.assertEqual(("build", "Running tests"), statusDetails("Testing project"))
		self.assertEqual(("completion", "Command failed"), statusDetails("Command failed with exit code 1"))
		self.assertEqual(("completion", "Command finished"), statusDetails("Ran rg -n pattern source"))

	def test_full_mode_speaks_complete_ran_label(self):
		label = "Ran rg -n pattern source -g '*.py'"
		self.assertEqual(label, statusMessage(label, verbosity="full"))
		self.assertEqual("Command finished", statusMessage(label))

	def test_sensitive_redaction(self):
		text = redactSensitive("Running token=abc123 remote key=mySecret C:\\Users\\alice\\project https://example.com/?key=value")
		self.assertNotIn("abc123", text)
		self.assertNotIn("alice", text)
		self.assertNotIn("key=value", text)
		self.assertNotIn("mySecret", text)
		quoted = redactSensitive('password="two word secret" C:\\Users\\Jane Doe\\project')
		self.assertNotIn("two word secret", quoted)
		self.assertNotIn("Jane Doe", quoted)

	def test_category_output_routing_respects_master_switches(self):
		self.assertEqual(
			{"speech": True, "braille": True, "sound": True},
			categoryOutputActions("all", True, True, True),
		)
		self.assertEqual(
			{"speech": False, "braille": False, "sound": True},
			categoryOutputActions("sound", True, True, True),
		)
		self.assertEqual(
			{"speech": False, "braille": False, "sound": False},
			categoryOutputActions("speech", False, True, True),
		)
		self.assertEqual(
			{"speech": False, "braille": False, "sound": False},
			categoryOutputActions("off", True, True, True),
		)

	def test_announcement_priorities(self):
		self.assertEqual("urgent", announcementPriority("completion", "Command failed"))
		self.assertEqual("high", announcementPriority("completion", "Command finished"))
		self.assertEqual("low", announcementPriority("commentary", "Inspecting files"))
		self.assertEqual("normal", announcementPriority("command", "Running command"))

	def test_elapsed_seconds(self):
		self.assertEqual(25, elapsedSeconds("Working for 25s"))
		self.assertIsNone(elapsedSeconds("Working"))

	def test_streamed_commentary_waits_for_complete_sentences(self):
		message, offset = completedTextDelta("I am inspecting the source")
		self.assertEqual("", message)
		message, offset = completedTextDelta("I am inspecting the source. Next step", offset)
		self.assertEqual("I am inspecting the source.", message)
		message, offset = completedTextDelta("I am inspecting the source. Next step is testing.", offset)
		self.assertEqual("Next step is testing.", message)


if __name__ == "__main__":
	unittest.main()
