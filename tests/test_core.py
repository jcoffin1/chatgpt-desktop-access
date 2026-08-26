import importlib.util
import ast
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
CLICK_GENERATOR_PATH = PROJECT_ROOT / "tools" / "generate_click_sounds.py"
SPEC = importlib.util.spec_from_file_location("codex_status_core", CORE_PATH)
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)
AnnouncementHistory = core.AnnouncementHistory
firstStatusLabel = core.firstStatusLabel
statusMessage = core.statusMessage
brailleStatusMessage = core.brailleStatusMessage
statusDetails = core.statusDetails
redactSensitive = core.redactSensitive
elapsedSeconds = core.elapsedSeconds
formatElapsedDuration = core.formatElapsedDuration
completedTextDelta = core.completedTextDelta
outputActions = core.outputActions
tonePattern = core.tonePattern
nextBusyState = core.nextBusyState
pollDelay = core.pollDelay
coalescedPollDelay = core.coalescedPollDelay
shouldReplaceScheduledPoll = core.shouldReplaceScheduledPoll
shouldPlayContinuousWorkingClick = core.shouldPlayContinuousWorkingClick
shouldSuppressRoutineBraille = core.shouldSuppressRoutineBraille
focusStateTransition = core.focusStateTransition
promptSubmissionTransition = core.promptSubmissionTransition
isCodexPromptLabel = core.isCodexPromptLabel
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
uniqueThreadLabels = core.uniqueThreadLabels
semanticStatusKey = core.semanticStatusKey
shouldSuppressSemanticDuplicate = core.shouldSuppressSemanticDuplicate
duplicateChannelActions = core.duplicateChannelActions
formatCommandSpeech = core.formatCommandSpeech
promptControlKind = core.promptControlKind
repairConfigurationValues = core.repairConfigurationValues
chatTitleMatches = core.chatTitleMatches
chatActionMatches = core.chatActionMatches
chatMessageShortcutIndex = core.chatMessageShortcutIndex
chatMessagesFromTokens = core.chatMessagesFromTokens
isChatMessageTrailingUiText = core.isChatMessageTrailingUiText
codexThreadUrl = core.codexThreadUrl
isChatOptionsLabel = core.isChatOptionsLabel
isPermissionDecisionLabel = core.isPermissionDecisionLabel
isPermissionPromptText = core.isPermissionPromptText
pluginInstallProgress = core.pluginInstallProgress
currentActivitySummary = core.currentActivitySummary
backgroundActivityName = core.backgroundActivityName
looksLikeCodexConversation = core.looksLikeCodexConversation
looksLikeBlankCodexConversation = core.looksLikeBlankCodexConversation
pendingChatTitle = core.pendingChatTitle
pluginProgressBusyTransition = core.pluginProgressBusyTransition
supersedesResponseCompletionCandidate = core.supersedesResponseCompletionCandidate


class StatusMessageTests(unittest.TestCase):
	def test_every_nvda_event_hook_is_exception_isolated_after_next_handler(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		eventMethods = [
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name.startswith("event_")
		]
		self.assertGreaterEqual(len(eventMethods), 7)
		for method in eventMethods:
			self.assertIsInstance(method.body[0], ast.Expr, method.name)
			self.assertIsInstance(method.body[0].value, ast.Call, method.name)
			self.assertEqual("nextHandler", getattr(method.body[0].value.func, "id", ""), method.name)
			self.assertTrue(any(isinstance(node, ast.Try) for node in method.body[1:]), method.name)

	def test_transient_focus_after_enter_preserves_prompt_submission_state(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "event_gainFocus"
		)
		class Roles:
			EDITABLETEXT = "edit"
			SECTION = "section"
		class Object:
			def __init__(self, role, isPrompt=False, hasText=False):
				self.role = role
				self.isPrompt = isPrompt
				self.hasText = hasText
		class Subject:
			def __init__(self):
				self._promptHadText = True
				self._pendingUserMessageIncrease = True
				self.submissions = 0
				self.polls = 0
			def _updateAppFocusState(self, obj): pass
			def _rememberBuffer(self, obj): pass
			def _schedulePoll(self): self.polls += 1
			def _trackPromptSubmission(self, obj):
				self._promptHadText, submitted = promptSubmissionTransition(
					self._promptHadText, obj.hasText,
				)
				self.submissions += int(submitted)
		namespace = {
			"Role": Roles,
			"_isCodexPromptObject": lambda obj: obj.isPrompt,
			"_isChatGPTObject": lambda obj: True,
			"log": type("Log", (), {"debugWarning": staticmethod(lambda *args, **kwargs: None)})(),
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		subject = Subject()
		namespace["event_gainFocus"](subject, Object(Roles.SECTION), lambda: None)
		self.assertTrue(subject._promptHadText)
		self.assertTrue(subject._pendingUserMessageIncrease)
		namespace["event_gainFocus"](subject, Object(Roles.EDITABLETEXT, True, False), lambda: None)
		self.assertFalse(subject._promptHadText)
		self.assertEqual(1, subject.submissions)
		self.assertEqual(2, subject.polls)

	def test_release_metadata_and_requested_chat_message_gestures_are_consistent(self):
		manifest = (PROJECT_ROOT / "manifest.ini").read_text(encoding="utf-8")
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		self.assertIn("version = 2026.1.42", manifest)
		self.assertIn('summary = "Codex Access Toolkit for NVDA"', manifest)
		self.assertIn('ADDON_VERSION = "2026.1.42"', plugin)
		self.assertIn('"protectBrailleReading": "boolean(default=True)"', plugin)
		self.assertIn('conf["protectBrailleReading"], self._appFocusState', plugin)
		self.assertIn("actualDelay = coalescedPollDelay(", plugin)
		self.assertIn("shouldReplaceScheduledPoll(self._nextPollAt, requestedDeadline)", plugin)
		self.assertIn('log.debugWarning("Codex Access Toolkit speech output failed"', plugin)
		self.assertIn('log.debugWarning("Codex Access Toolkit Braille output failed"', plugin)
		self.assertIn('log.debugWarning("Codex Access Toolkit tone output failed"', plugin)
		self.assertIn('log.debugWarning("Codex Access Toolkit could not cancel speech for an urgent message"', plugin)
		self.assertIn('redactSensitive(message) if conf["redactSensitive"] else message', plugin)
		self.assertIn("or not _isChatGPTObject(obj):", plugin)
		self.assertIn("previousValues = {", plugin)
		self.assertIn("backgroundActivityName(self._activeCategory, self._latestFullMessage)", plugin)
		self.assertIn("self._schedulePopupDialogFocus(obj)", plugin)
		self.assertIn("self._focusPopupDialog", plugin)
		self.assertIn("if not _isChatGPTObject(obj):", plugin)
		self.assertIn("self._pluginProgressOwnedBusy.discard(expiredIdentity)", plugin)
		self.assertIn('Role.PROGRESSBAR or not _isChatGPTObject(obj)', plugin)
		self.assertIn('self._setBusy(False, "prompt superseded plugin installation")', plugin)
		self.assertNotIn("Codex Status Announcer 2026.1.18 loaded", plugin)
		self.assertNotIn("Adds assignable focus- and browse-mode actions", manifest)
		self.assertIn('default=\'full\'', plugin)
		self.assertIn("fullSpeechProfile", plugin)
		self.assertIn("default='developer'", plugin)
		self.assertIn("minimalSpeechProfile", plugin)
		self.assertIn("default='balanced'", plugin)
		self.assertIn("brailleDetail", plugin)
		self.assertIn("interruptUrgentSpeech", plugin)
		self.assertNotIn("__gestures", plugin)
		self.assertIn('CHAT_MESSAGE_GESTURES = tuple(', plugin)
		self.assertIn('for digit in "1234567890"', plugin)
		self.assertIn("gesture.send()", plugin)
		self.assertIn("self.bindGesture(gestureIdentifier, \"readPreviousChatMessage\")", plugin)
		self.assertIn("self.removeGestureBinding(gestureIdentifier)", plugin)
		self.assertIn("self._setChatMessageShortcutBindings(appFocused)", plugin)
		self.assertNotIn('"kb:enter"', plugin)
		self.assertNotIn("script_enter", plugin.casefold())
		self.assertFalse((PROJECT_ROOT / "appModules" / "chatgpt.py").exists())
		self.assertNotIn("gesture=", plugin)
		self.assertNotIn("self._chatHistoryDialog.ShowModal", plugin)
		self.assertIn('label=_("Recent chats:")', plugin)
		self.assertIn('label=_("Archived chats:")', plugin)
		self.assertIn("self.recentList", plugin)
		self.assertIn("self.archivedList", plugin)
		self.assertIn("self.recentList.Bind(wx.EVT_CONTEXT_MENU, self._onContextMenu)", plugin)
		self.assertIn("self.archivedList.Bind(wx.EVT_CONTEXT_MENU, self._onContextMenu)", plugin)
		self.assertIn("self._showChatActionMenu(selection)", plugin)
		self.assertIn("self._retryDirectChatAction", plugin)
		self.assertIn('self._performSelectedAction(selection, "focusActions")', plugin)
		self.assertIn('actionButton.setFocus()', plugin)
		self.assertIn("self._scheduleUnarchiveButtonFocus()", plugin)
		self.assertIn('position.find("Unarchive and open"', plugin)
		self.assertIn("message = _completeChangelogMessage()", plugin)
		self.assertIn("_showBrowseableMessageAtTop(", plugin)
		self.assertIn('CURRENT_RELEASE_NOTES, _("Codex Access Toolkit — what\'s new")', plugin)
		self.assertIn('scriptCategory = _("Codex Access Toolkit")', plugin)
		self.assertIn('self._lastSpeechMessage', plugin)
		self.assertIn('self._lastBrailleMessage', plugin)
		self.assertIn('version=ADDON_VERSION', plugin)
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

	def test_braille_detail_is_independent_of_speech_verbosity(self):
		label = "Running shell command: rg -n status globalPlugins"
		self.assertEqual("Running command", brailleStatusMessage(label, detail="concise"))
		self.assertEqual("Running command", brailleStatusMessage(label, detail="informative"))
		self.assertEqual(label, brailleStatusMessage(label, detail="full"))
		self.assertEqual(label, brailleStatusMessage(label, detail="invalid"))

	def test_speech_duplicate_does_not_hide_distinct_braille_detail(self):
		result = duplicateChannelActions(
			"Running command", "Running shell command: rg one", "Running command",
			"Running shell command: rg two", 0.2, 0.2,
		)
		self.assertEqual({"speech": True, "braille": False}, result)

	def test_send_calls_real_braille_message_path_when_speech_is_disabled(self):
		pluginSource = PLUGIN_PATH.read_text(encoding="utf-8")
		function = next(
			node for node in ast.parse(pluginSource).body
			if isinstance(node, ast.FunctionDef) and node.name == "_send"
		)
		calls = []
		class Speech:
			def speakMessage(self, message):
				calls.append(("speech", message))
			def cancelSpeech(self):
				calls.append(("cancel", None))
		class Handler:
			def message(self, message):
				calls.append(("braille", message))
		namespace = {
			"outputActions": lambda speak, speechOff, showBraille, sounds, tone: {
				"speech": bool(speak), "braille": bool(showBraille), "tone": False,
			},
			"_speechIsOff": lambda: False,
			"_settings": lambda: {"interruptUrgentSpeech": True},
			"speech": Speech(),
			"braille": type("Braille", (), {"handler": Handler()})(),
			"_playProgressSound": lambda *args: None,
		}
		exec(compile(ast.Module(body=[function], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		namespace["_send"]("short speech", False, True, brailleMessage="complete braille command")
		self.assertEqual([("braille", "complete braille command")], calls)
		calls.clear()
		namespace["_send"]("Permission required", True, False, priority="urgent", interruptUrgent=False)
		self.assertEqual([("speech", "Permission required")], calls)
		calls.clear()
		namespace["_send"]("Permission required", True, False, priority="urgent", interruptUrgent=True)
		self.assertEqual([("cancel", None), ("speech", "Permission required")], calls)

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

	def test_failed_settings_save_rolls_back_the_complete_import(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		panel = next(
			node for node in pluginTree.body
			if isinstance(node, ast.ClassDef) and node.name == "CodexStatusAnnouncerSettingsPanel"
		)
		method = next(
			node for node in panel.body
			if isinstance(node, ast.FunctionDef) and node.name == "_onImportSettings"
		)
		with tempfile.TemporaryDirectory() as directory:
			settingsPath = Path(directory) / "settings.json"
			settingsPath.write_text(json.dumps({"speech": False, "verbosity": "minimal"}), encoding="utf-8")
			class Dialog:
				def __enter__(self): return self
				def __exit__(self, *args): return False
				def ShowModal(self): return 1
				def GetPath(self): return str(settingsPath)
			class Wx:
				ID_OK = 1
				FD_OPEN = 2
				FD_FILE_MUST_EXIST = 4
				FileDialog = lambda *args, **kwargs: Dialog()
			class ConfManager:
				spec = {"codexStatusAnnouncer": {"speech": "", "verbosity": ""}}
				def __init__(self): self.saveCalls = 0
				def save(self):
					self.saveCalls += 1
					if self.saveCalls == 1:
						raise OSError("simulated save failure")
			confManager = ConfManager()
			values = {"speech": True, "verbosity": "full"}
			loaded = []
			messages = []
			namespace = {
				"wx": Wx, "Path": Path, "json": json, "CONFIG_SECTION": "codexStatusAnnouncer",
				"config": type("Config", (), {"conf": confManager})(), "_settings": lambda: values,
				"_repairConfiguration": lambda: (), "_": lambda text: text,
				"log": type("Log", (), {"error": lambda *args, **kwargs: None, "debugWarning": lambda *args, **kwargs: None})(),
				"ui": type("Ui", (), {"message": lambda self, message: messages.append(message)})(),
			}
			exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
			instance = type("Panel", (), {"_loadControlsFromConfiguration": lambda self: loaded.append(True)})()
			namespace["_onImportSettings"](instance, None)
			self.assertEqual({"speech": True, "verbosity": "full"}, values)
			self.assertEqual(2, confManager.saveCalls)
			self.assertEqual([True], loaded)
			self.assertEqual(["Settings could not be imported"], messages)

	def test_chat_action_requires_exact_normalized_accessible_title(self):
		self.assertTrue(chatTitleMatches(" My   task ", "my task"))
		self.assertTrue(chatTitleMatches("My task", "", titleFoundInsideButton=True))
		self.assertFalse(chatTitleMatches("My task", ""))
		self.assertFalse(chatTitleMatches("My task", "Open My task menu"))
		self.assertFalse(chatTitleMatches("", ""))

	def test_chat_options_button_labels_are_specific(self):
		self.assertTrue(isChatOptionsLabel("Open conversation options"))
		self.assertTrue(isChatOptionsLabel("Project chat options"))
		self.assertTrue(isChatOptionsLabel("More"))
		self.assertFalse(isChatOptionsLabel("Add files and more"))
		self.assertFalse(isChatOptionsLabel("Change permissions"))

	def test_direct_chat_actions_match_only_pin_and_archive_controls(self):
		self.assertTrue(chatActionMatches("pin", "Pin chat"))
		self.assertTrue(chatActionMatches("pin", "Unpin chat"))
		self.assertTrue(chatActionMatches("archive", "Archive chat"))
		self.assertFalse(chatActionMatches("archive", "Archive project"))
		self.assertFalse(chatActionMatches("pin", "Pin message"))

	def test_missing_direct_chat_action_stops_after_bounded_retries(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_retryDirectChatAction"
		)
		class Button:
			name = "Selected chat"
			def setFocus(self): pass
		class Subject:
			def __init__(self):
				self._pendingDirectChatAction = ("Selected chat", "focusActions", 0)
				self._chatHistoryActionTimer = object()
			def _chatButtonObject(self, title): return Button()
			def _namedChatActionButton(self, button, action): return None
		timers = []
		messages = []
		namespace = {
			"wx": type("Wx", (), {"CallLater": staticmethod(lambda *args: timers.append(args) or object())}),
			"ui": type("Ui", (), {"message": staticmethod(messages.append)}),
			"log": type("Log", (), {
				"debugWarning": staticmethod(lambda *args, **kwargs: None),
				"info": staticmethod(lambda *args, **kwargs: None),
			})(),
			"_": lambda text: text,
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		Subject._retryDirectChatAction = namespace["_retryDirectChatAction"]
		subject = Subject()
		for _ in range(12):
			namespace["_retryDirectChatAction"](subject)
		self.assertIsNone(subject._pendingDirectChatAction)
		self.assertEqual(11, len(timers))
		self.assertEqual(["The selected chat's Pin or Archive button could not be focused"], messages)

	def test_starting_direct_chat_action_cancels_an_old_retry_timer(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_startDirectChatAction"
		)
		class Timer:
			def __init__(self): self.stopped = False
			def Stop(self): self.stopped = True
		class Subject:
			def __init__(self):
				self.oldTimer = Timer()
				self._chatActionRetryTimer = self.oldTimer
				self._pendingDirectChatAction = None
				self.retryCount = 0
			def _retryDirectChatAction(self): self.retryCount += 1
		namespace = {}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		subject = Subject()
		namespace["_startDirectChatAction"](subject, "Selected chat", "archive")
		self.assertTrue(subject.oldTimer.stopped)
		self.assertIsNone(subject._chatActionRetryTimer)
		self.assertEqual(("Selected chat", "archive", 0), subject._pendingDirectChatAction)
		self.assertEqual(1, subject.retryCount)

	def test_permission_prompt_and_decision_labels_are_narrow(self):
		self.assertTrue(isPermissionPromptText("Permission required. Allow this command? Deny"))
		self.assertTrue(isPermissionPromptText("This action requires your approval"))
		self.assertFalse(isPermissionPromptText("Change permissions"))
		self.assertTrue(isPermissionDecisionLabel("Allow once"))
		self.assertTrue(isPermissionDecisionLabel("Deny and tell Codex what to do"))
		self.assertFalse(isPermissionDecisionLabel("Change permissions"))

	def test_plugin_install_progress_is_scoped_parsed_and_bucketed(self):
		self.assertEqual(
			("plugin", 37, 30),
			pluginInstallProgress("Installing plugin 37%"),
		)
		self.assertEqual(
			("connector", 100, 100),
			pluginInstallProgress("Connector installation 100 percent"),
		)
		self.assertEqual(
			("plugin", None, None),
			pluginInstallProgress("Plugin installation in progress"),
		)
		self.assertEqual(
			("plugin", 100, 100),
			pluginInstallProgress("Plugin installation complete"),
		)
		self.assertIsNone(pluginInstallProgress("Downloading model 50%"))

	def test_current_activity_summary_covers_silent_background_periods(self):
		self.assertEqual("Running Outlook test", currentActivitySummary(True, "tool", "Running Outlook test", 45))
		self.assertEqual("Codex is still using tools, 45 seconds", currentActivitySummary(True, "tool", "", 45))
		self.assertEqual("Codex is still running commands", currentActivitySummary(True, "command", "", 0))
		self.assertEqual("Codex is idle", currentActivitySummary(False, "other", "", 0))
		self.assertEqual("Codex is still working, 3 minutes 20 seconds", currentActivitySummary(True, "working", "", 200))

	def test_elapsed_duration_uses_speech_friendly_units(self):
		self.assertEqual("0 seconds", formatElapsedDuration(0))
		self.assertEqual("59 seconds", formatElapsedDuration(59))
		self.assertEqual("1 minute", formatElapsedDuration(60))
		self.assertEqual("1 minute 25 seconds", formatElapsedDuration(85))
		self.assertEqual("3 minutes 20 seconds", formatElapsedDuration(200))
		self.assertEqual("1 hour 1 minute 1 second", formatElapsedDuration(3661))

	def test_background_activity_names_preserve_file_work_without_claiming_finished_work_continues(self):
		self.assertEqual("Editing code", backgroundActivityName("file", "Editing code: core.py"))
		self.assertEqual("Checking files", backgroundActivityName("file", "Checking files"))
		self.assertEqual("Processing", backgroundActivityName("file", "Reading finished"))
		self.assertEqual("Command", backgroundActivityName("command", "Running command"))
		self.assertEqual("Checking files", backgroundActivityName("command", "Reading file core.py"))
		self.assertEqual("File operations", backgroundActivityName("file", ""))

	def test_conversation_detection_excludes_settings_documents(self):
		self.assertTrue(looksLikeCodexConversation("Main landmark Do anything multiline edit"))
		self.assertTrue(looksLikeCodexConversation("Message Codex"))
		self.assertFalse(looksLikeCodexConversation("Settings Account Archived chats"))

	def test_blank_chat_detection_ignores_existing_conversation_buffer_refreshes(self):
		self.assertTrue(looksLikeBlankCodexConversation("Main landmark Do anything New chat"))
		self.assertFalse(looksLikeBlankCodexConversation("Do anything User message 3 Response complete: done"))
		self.assertFalse(looksLikeBlankCodexConversation("Do anything ChatGPT said: existing answer"))
		self.assertFalse(looksLikeBlankCodexConversation("Settings General Archived chats"))

	def test_buffer_backend_refresh_preserves_task_state_but_blank_chat_resets_it(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_rememberBuffer"
		)
		class TextInfo:
			def __init__(self, text): self.text = text
		class Buffer:
			def __init__(self, text): self.text = text
			def makeTextInfo(self, position): return TextInfo(self.text)
		class Subject:
			def __init__(self, oldBuffer):
				self._buffer = oldBuffer
				self._pendingOpenedChatTitle = ""
				self._pendingOpenedChatAt = 0.0
				self._documentSwitchCount = 2
				self._monitoringAnnounced = True
				self._latestMessage = self._latestFullMessage = "Running command"
				self.resets = []
				self.spoken = []
			def _bufferCandidates(self, obj): return (obj,)
			def _resetTaskState(self, reason): self.resets.append(reason)
			def _speakOnce(self, message, *args, **kwargs): self.spoken.append(message)
		namespace = {
			"_isChatGPTObject": lambda obj: True, "pendingChatTitle": pendingChatTitle,
			"looksLikeBlankCodexConversation": looksLikeBlankCodexConversation,
			"time": type("Time", (), {"monotonic": staticmethod(lambda: 100.0)}),
			"textInfos": type("TextInfos", (), {"POSITION_ALL": object()}),
			"_": lambda text: text,
			"log": type("Log", (), {"info": lambda *args, **kwargs: None, "debug": lambda *args, **kwargs: None})(),
			"_settings": lambda: {"speech": True, "braille": True}, "_send": lambda *args, **kwargs: None,
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		oldBuffer = Buffer("Do anything ChatGPT said: existing answer")
		refreshedBuffer = Buffer("Do anything User message 2 ChatGPT said: existing answer")
		subject = Subject(oldBuffer)
		namespace["_rememberBuffer"](subject, type("Object", (), {"treeInterceptor": refreshedBuffer})())
		self.assertIs(refreshedBuffer, subject._buffer)
		self.assertEqual([], subject.resets)
		self.assertEqual([], subject.spoken)
		self.assertEqual(2, subject._documentSwitchCount)
		blankBuffer = Buffer("Main landmark Do anything New chat")
		namespace["_rememberBuffer"](subject, type("Object", (), {"treeInterceptor": blankBuffer})())
		self.assertEqual(["document changed"], subject.resets)
		self.assertEqual(["New Codex chat opened"], subject.spoken)
		self.assertEqual(3, subject._documentSwitchCount)

	def test_plugin_progress_only_releases_busy_state_it_started(self):
		self.assertEqual((True, True), pluginProgressBusyTransition(False, False, False))
		self.assertEqual((False, False), pluginProgressBusyTransition(True, True, True))
		self.assertEqual((True, False), pluginProgressBusyTransition(True, False, True))

	def test_stale_pending_chat_titles_are_discarded(self):
		self.assertEqual("My chat", pendingChatTitle(" My  chat ", 2.0))
		self.assertEqual("", pendingChatTitle("My chat", 11.0))
		self.assertEqual("", pendingChatTitle("", 1.0))

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
			invalidPath = archiveDirectory / "not-a-thread.jsonl"
			olderPath.write_text("{}\n", encoding="utf-8")
			newerPath.write_text("{}\n", encoding="utf-8")
			invalidPath.write_text("{}\n", encoding="utf-8")
			os.utime(olderPath, (10, 10))
			os.utime(newerPath, (20, 20))
			os.utime(invalidPath, (30, 30))
			self.assertEqual(
				((newerId, "Named archived"), (olderId, "Older archived")),
				loadArchivedThreads(codexRoot),
			)

	def test_native_codex_thread_url_requires_a_uuid(self):
		self.assertEqual(
			"codex://threads/00000000-0000-0000-0000-000000000002",
			codexThreadUrl("00000000-0000-0000-0000-000000000002"),
		)
		self.assertEqual("", codexThreadUrl("../settings"))
		self.assertEqual("", codexThreadUrl(""))

	def test_duplicate_archived_titles_keep_every_native_thread_id(self):
		self.assertEqual(
			(
				("00000000-0000-0000-0000-000000000001", "Repeated title"),
				("00000000-0000-0000-0000-000000000002", "Repeated title (2)"),
				("00000000-0000-0000-0000-000000000003", "Repeated title (3)"),
			),
			uniqueThreadLabels((
				("00000000-0000-0000-0000-000000000001", "Repeated title"),
				("00000000-0000-0000-0000-000000000002", "Repeated title"),
				("00000000-0000-0000-0000-000000000003", "Repeated title"),
			)),
		)
		labels = [label for threadId, label in uniqueThreadLabels((
			("1", "Repeated title"), ("2", "Repeated title"), ("3", "Repeated title (2)"),
		))]
		self.assertEqual(len(labels), len(set(labels)))

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

	def test_click_designs_use_distinct_patterns_and_percussive_characters(self):
		tree = ast.parse(CLICK_GENERATOR_PATH.read_text(encoding="utf-8"))
		patterns = ast.literal_eval(next(
			node.value for node in tree.body
			if isinstance(node, ast.Assign) and any(
				isinstance(target, ast.Name) and target.id == "PATTERNS" for target in node.targets
			)
		))
		self.assertEqual(17, len(patterns))
		self.assertEqual(17, len({tuple(pattern) for pattern in patterns.values()}))
		characters = {character for pattern in patterns.values() for offset, frequency, character in pattern}
		self.assertGreaterEqual(len(characters), 6)
		self.assertNotEqual(patterns["command"], patterns["file"])
		self.assertNotEqual(patterns["completion"], patterns["failure"])

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
		self.assertEqual(
			"File operations still running for 1 minute 25 seconds",
			formatCustomAnnouncement("{activity} still running for {duration}", "Working", "File operations", 85),
		)

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

	def test_chat_message_shortcuts_and_accessibility_token_extraction(self):
		self.assertEqual(tuple(range(1, 11)), tuple(
			chatMessageShortcutIndex(key) for key in "1234567890"
		))
		self.assertIsNone(chatMessageShortcutIndex("numpad1"))
		self.assertIsNone(chatMessageShortcutIndex(""))
		tokens = [
			("text", "sidebar title"),
			("speaker", "user"), ("speaker", "user"), ("text", " First question "),
			("text", "with a second line"),
			("speaker", "assistant"), ("text", "Response complete"), ("text", "First answer"),
			("speaker", "assistant"), ("text", "First answer"),
			("speaker", "user"), ("text", "Second question"), ("end", "prompt"),
			("text", "Do anything"),
		]
		self.assertEqual(
			(("user", "First question with a second line"), ("assistant", "First answer"), ("user", "Second question")),
			chatMessagesFromTokens(tokens),
		)

	def test_chat_message_extraction_is_bounded_and_tolerates_bad_tokens(self):
		tokens = []
		for index in range(12):
			tokens.extend((
				("speaker", "user" if index % 2 == 0 else "assistant"),
				("text", f"message {index}"),
			))
		tokens.extend((None, ("bad",), ("speaker", "unknown")))
		messages = chatMessagesFromTokens(tokens, 10)
		self.assertEqual(10, len(messages))
		self.assertEqual(("user", "message 2"), messages[0])
		self.assertEqual(("assistant", "message 11"), messages[-1])

	def test_chat_message_extraction_removes_trailing_chatgpt_interface_text(self):
		for text in (
			"3:07 PM", "Today 3:19 PM", "13:45", "Working for 17s", "Working for 4m 4s",
			"Edited 7 files", "Good response", "Bad response", "Change permissions",
			"Review changed files", "Copy message", "Thinking", "Step 1 / 5",
			"Add files and more", "Full access",
		):
			self.assertTrue(isChatMessageTrailingUiText(text), text)
		for text in ("Meet at 3:07 PM tomorrow", "I edited 7 files", "This is a good response"):
			self.assertFalse(isChatMessageTrailingUiText(text), text)
		tokens = (
			("speaker", "assistant"), ("text", "Actual answer"), ("text", "Edited 7 files"),
			("text", "+21 -20"), ("text", "Good response"), ("text", "3:02 PM"),
			("speaker", "user"), ("text", "Actual question"), ("text", "3:07 PM"),
			("text", "Working for 17s"),
			("speaker", "assistant"), ("text", "Latest answer"), ("text", "Change permissions"),
		)
		self.assertEqual(
			(("assistant", "Actual answer"), ("user", "Actual question"), ("assistant", "Latest answer")),
			chatMessagesFromTokens(tokens),
		)

	def test_chat_message_extraction_skips_hidden_response_copy_and_preserves_split_words(self):
		tokens = (
			("speaker", "user"), ("text", "L"), ("text", "ooks like this works. "),
			("speaker", "assistant"),
			("text", "Response complete: Real answer. Real answer. Thinking Step 1 / 5"),
			("text", "Real answer. "), ("text", "Second paragraph."),
			("text", "Thinking"), ("text", "Step 1 / 5"),
		)
		self.assertEqual(
			(("user", "Looks like this works."), ("assistant", "Real answer. Second paragraph.")),
			chatMessagesFromTokens(tokens),
		)

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
		self.assertEqual(500, pollDelay(True, 500))
		self.assertEqual(1000, pollDelay(False, 750))
		self.assertEqual(2000, pollDelay(False, 2000))

	def test_event_triggered_scans_are_coalesced_away_from_the_last_poll(self):
		self.assertEqual(150, coalescedPollDelay(10, 0.0))
		self.assertEqual(100, coalescedPollDelay(10, 0.05))
		self.assertEqual(10, coalescedPollDelay(10, 0.20))
		self.assertEqual(250, coalescedPollDelay(250, 0.0))
		self.assertEqual(10, coalescedPollDelay(10, float("inf")))
		self.assertEqual(150, coalescedPollDelay(10, float("-inf")))
		self.assertEqual(150, coalescedPollDelay(10, float("nan")))
		self.assertEqual(150, coalescedPollDelay(10, -1.0))
		self.assertEqual(150, coalescedPollDelay("bad", None))
		self.assertEqual(10, coalescedPollDelay(10, 0.20, float("inf")))
		self.assertFalse(shouldReplaceScheduledPoll(10.1, 10.2))
		self.assertTrue(shouldReplaceScheduledPoll(10.2, 10.1))
		self.assertTrue(shouldReplaceScheduledPoll(0.0, 10.1))

	def test_continuous_working_sound_uses_quiet_gaps_for_clicks_and_tones(self):
		self.assertTrue(shouldPlayContinuousWorkingClick(True, True, "clicks", True, 1.4, 1.4))
		self.assertTrue(shouldPlayContinuousWorkingClick(True, True, "tones", True, 1.4, 1.4))
		self.assertFalse(shouldPlayContinuousWorkingClick(False, True, "clicks", True, 10, 1.4))
		self.assertFalse(shouldPlayContinuousWorkingClick(True, False, "clicks", True, 10, 1.4))
		self.assertFalse(shouldPlayContinuousWorkingClick(True, True, "invalid", True, 10, 1.4))
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

	def test_prompt_labels_are_narrow_and_do_not_require_a_document_name(self):
		for label in ("Do anything", "Ask anything", "Message Codex", "Message ChatGPT", "Send a message"):
			self.assertTrue(isCodexPromptLabel(label), label)
		for label in ("Search chats", "Announcement text", "Change permissions", ""):
			self.assertFalse(isCodexPromptLabel(label), label)

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
		self.assertTrue(shouldFinalizeResponseCompletion(True, 30, 30, True, False, "Reading finished"))
		self.assertTrue(shouldFinalizeResponseCompletion(True, 30, 30, True, False, "Command finished"))
		self.assertFalse(shouldFinalizeResponseCompletion(True, 30, 30, True, True, ""))
		self.assertFalse(shouldFinalizeResponseCompletion(True, 30, 30, True, False, "Running command"))
		self.assertFalse(shouldFinalizeResponseCompletion(True, 30, 30, False, False, ""))
		self.assertFalse(shouldFinalizeResponseCompletion(True, 29.9, 30, True, False, ""))

	def test_trailing_intermediate_completion_preserves_response_completion_candidate(self):
		self.assertEqual(("completion", "Reading finished"), statusDetails("Reading finished"))
		for label in ("Reading finished", "Command finished", "File edit complete"):
			self.assertFalse(supersedesResponseCompletionCandidate(label), label)
		for label in ("Reading", "Working", "Thinking", "Running command"):
			self.assertTrue(supersedesResponseCompletionCandidate(label), label)

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
		self.assertEqual(
			"Command finished: rg",
			statusMessage("Ran rg -n pattern source", verbosity="full", fullProfile="standard"),
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
		commandLine = redactSensitive("Running command: tool --token abc123 --password 'two words'")
		self.assertNotIn("abc123", commandLine)
		self.assertNotIn("two words", commandLine)

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

	def test_braille_reading_protection_only_suppresses_focused_routine_progress(self):
		for category in (
			"thinking", "working", "command", "search", "file", "build", "tool", "commentary",
			"backgroundPulse1", "backgroundPulse2",
		):
			self.assertTrue(shouldSuppressRoutineBraille(True, True, category, "normal"), category)
		self.assertFalse(shouldSuppressRoutineBraille(True, False, "command", "normal"))
		self.assertFalse(shouldSuppressRoutineBraille(False, True, "command", "normal"))
		self.assertFalse(shouldSuppressRoutineBraille(True, True, "completion", "high"))
		self.assertFalse(shouldSuppressRoutineBraille(True, True, "attention", "urgent"))
		self.assertFalse(shouldSuppressRoutineBraille(True, True, "other", "normal"))
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
