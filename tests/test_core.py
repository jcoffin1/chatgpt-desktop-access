import importlib.util
from pathlib import Path
import unittest


CORE_PATH = Path(__file__).parents[1] / "globalPlugins" / "codexStatusAnnouncer" / "core.py"
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
shouldClearBusyAfterStatusGap = core.shouldClearBusyAfterStatusGap
soundKey = core.soundKey
categoryOutputActions = core.categoryOutputActions
announcementPriority = core.announcementPriority
changelogForDisplay = core.changelogForDisplay
viewerTitleMatches = core.viewerTitleMatches
previewSelection = core.previewSelection
formatCustomAnnouncement = core.formatCustomAnnouncement
unknownAnnouncementPlaceholders = core.unknownAnnouncementPlaceholders


class StatusMessageTests(unittest.TestCase):
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
		self.assertEqual((), unknownAnnouncementPlaceholders("{activity}: {message} for {seconds}"))
		self.assertEqual(("unknown",), unknownAnnouncementPlaceholders("Keep {unknown}"))
		self.assertEqual(("invalid format",), unknownAnnouncementPlaceholders("Broken {"))

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
		markdown = "# Changelog\n\nAll notable changes.\n\n## 2.2.0\n\n- Added **history**.\n- Uses `clicks`."
		self.assertEqual(
			"Complete release history\n\nAll notable changes.\n\nVersion 2.2.0\n\nAdded history.\nUses clicks.",
			changelogForDisplay(markdown),
		)

	def test_release_notes_viewer_title_guard(self):
		self.assertTrue(viewerTitleMatches("Codex — current release notes", "Codex — current release notes"))
		self.assertTrue(viewerTitleMatches("Codex — current release notes", "Codex — CURRENT RELEASE NOTES dialog"))
		self.assertFalse(viewerTitleMatches("Codex — current release notes", "NVDA Settings"))
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

	def test_missing_status_clears_busy_state_after_grace_period(self):
		self.assertFalse(shouldClearBusyAfterStatusGap(True, 1.99))
		self.assertTrue(shouldClearBusyAfterStatusGap(True, 2.0))
		self.assertFalse(shouldClearBusyAfterStatusGap(False, 30.0))

	def test_activity_messages(self):
		cases = {
			"Planning next step": "Thinking",
			"Thinking": "Thinking",
			"Working": "Working",
			"Analyzing files": "Analyzing",
			"Reading package metadata": "Reading",
			"Writing tests": "Writing",
			"Editing source": "Editing",
			"Applying patch": "Applying changes",
			"Generating output": "Generating",
			"Waiting for process": "Waiting",
			"Using tool": "Using tool",
			"Searching the web": "Searching the web",
			"Running command Get-ChildItem": "Running command",
			"Running web search": "Searching the web",
			"Searched the web": "Web search finished",
			"Ran command": "Command finished",
			"Ran command and web search": "Command and web search finished",
			"Completed task": "Finished",
			"Reviewed files": "Reading finished",
			"Updated source": "Changes finished",
		}
		for label, expected in cases.items():
			with self.subTest(label=label):
				self.assertEqual(expected, statusMessage(label))

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
		self.assertEqual("Editing file", statusMessage("File edit source.py"))
		self.assertEqual("File edit finished", statusMessage("File edit complete source.py"))

	def test_full_mode_returns_complete_normalized_label(self):
		self.assertEqual(
			"Running shell command: python -m unittest",
			statusMessage("  Running   shell command: python -m unittest  ", verbosity="full"),
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
