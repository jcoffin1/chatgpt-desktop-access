import importlib.util
import ast
import json
import math
import os
from pathlib import Path
import re
import struct
import sys
import tempfile
import unittest
import wave


CORE_PATH = Path(__file__).parents[1] / "globalPlugins" / "codexStatusAnnouncer" / "core.py"
PROJECT_ROOT = Path(__file__).parents[1]
PLUGIN_PATH = CORE_PATH.parent / "__init__.py"
CHAT_DIALOG_PATH = CORE_PATH.parent / "chatHistoryDialog.py"
SOUND_OUTPUT_PATH = CORE_PATH.parent / "soundOutput.py"
CLICK_GENERATOR_PATH = PROJECT_ROOT / "tools" / "generate_click_sounds.py"
ACCESSIBILITY_FIXTURE_PATH = PROJECT_ROOT / "tests" / "fixtures" / "chatgpt_accessibility_snapshots.json"
ADDON_STORE_METADATA_PATH = PROJECT_ROOT / "tools" / "addon_store_metadata.py"
AUDIT_PATH = PROJECT_ROOT / "tools" / "audit_addon.py"
BUILD_PATH = PROJECT_ROOT / "tools" / "build_addon.py"
RELEASE_WORKFLOW_PATH = PROJECT_ROOT / ".github" / "workflows" / "release.yml"
TRANSLATION_TEMPLATE_PATH = PROJECT_ROOT / "locale" / "chatGPTDesktopAccess.pot"
BROWSER_ACCESS_PATH = CORE_PATH.parent / "browserAccess.py"
BROWSER_NAVIGATOR_DIALOG_PATH = CORE_PATH.parent / "browserNavigatorDialog.py"
CHATGPT_APP_MODULE_PATH = PROJECT_ROOT / "appModules" / "chatgpt.py"
CODEX_APP_MODULE_PATH = PROJECT_ROOT / "appModules" / "codex.py"
SPEC = importlib.util.spec_from_file_location("codex_status_core", CORE_PATH)
core = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(core)
STORE_SPEC = importlib.util.spec_from_file_location("codex_store_metadata", ADDON_STORE_METADATA_PATH)
storeMetadata = importlib.util.module_from_spec(STORE_SPEC)
STORE_SPEC.loader.exec_module(storeMetadata)
BUILD_SPEC = importlib.util.spec_from_file_location("codex_package_builder", BUILD_PATH)
packageBuilder = importlib.util.module_from_spec(BUILD_SPEC)
BUILD_SPEC.loader.exec_module(packageBuilder)
BROWSER_ACCESS_SPEC = importlib.util.spec_from_file_location("codex_browser_access", BROWSER_ACCESS_PATH)
browserAccess = importlib.util.module_from_spec(BROWSER_ACCESS_SPEC)
BROWSER_ACCESS_SPEC.loader.exec_module(browserAccess)
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
bufferInspectionDue = core.bufferInspectionDue
conversationWindowShouldDetach = core.conversationWindowShouldDetach
brailleTypingGestureCommitsText = core.brailleTypingGestureCommitsText
isBrailleTypingGestureIdentifier = core.isBrailleTypingGestureIdentifier
isPromptSubmissionGestureIdentifier = core.isPromptSubmissionGestureIdentifier
promptSubmissionGestureShouldStart = core.promptSubmissionGestureShouldStart
shouldPreserveBrailleComposition = core.shouldPreserveBrailleComposition
coalescedPollDelay = core.coalescedPollDelay
shouldReplaceScheduledPoll = core.shouldReplaceScheduledPoll
shouldPlayContinuousWorkingClick = core.shouldPlayContinuousWorkingClick
shouldSuppressRoutineBraille = core.shouldSuppressRoutineBraille
shouldSuppressNativeConversationUpdate = core.shouldSuppressNativeConversationUpdate
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
isResponseCompletionMarkerText = core.isResponseCompletionMarkerText
responseCompletionScanMarker = core.responseCompletionScanMarker
shouldFinalizeResponseCompletion = core.shouldFinalizeResponseCompletion
isTaskCompletionLabel = core.isTaskCompletionLabel
intermediateCompletionCategory = core.intermediateCompletionCategory
isKnownNonStatusButton = core.isKnownNonStatusButton
isChatHistoryInterfaceText = core.isChatHistoryInterfaceText
isChatHistoryConversationBoundary = core.isChatHistoryConversationBoundary
soundKey = core.soundKey
categoryOutputActions = core.categoryOutputActions
announcementPriority = core.announcementPriority
changelogForDisplay = core.changelogForDisplay
viewerTitleMatches = core.viewerTitleMatches
previewSelection = core.previewSelection
formatCustomAnnouncement = core.formatCustomAnnouncement
loadArchivedThreads = core.loadArchivedThreads
loadActiveCodexThreadTitles = core.loadActiveCodexThreadTitles
uniqueThreadLabels = core.uniqueThreadLabels
semanticStatusKey = core.semanticStatusKey
shouldSuppressSemanticDuplicate = core.shouldSuppressSemanticDuplicate
duplicateChannelActions = core.duplicateChannelActions
formatCommandSpeech = core.formatCommandSpeech
promptControlKind = core.promptControlKind
repairConfigurationValues = core.repairConfigurationValues
mergeSupportedAppNames = core.mergeSupportedAppNames
conversationModeFromDocumentNames = core.conversationModeFromDocumentNames
conversationModeFromSwitchLabel = core.conversationModeFromSwitchLabel
chatHistorySnapshotDecision = core.chatHistorySnapshotDecision
modeSpecificRecentChatTitles = core.modeSpecificRecentChatTitles
chatTitleMatches = core.chatTitleMatches
chatActionMatches = core.chatActionMatches
voiceControlKind = core.voiceControlKind
chatMessageShortcutIndex = core.chatMessageShortcutIndex
chatMessagesFromTokens = core.chatMessagesFromTokens
isChatMessageTrailingUiText = core.isChatMessageTrailingUiText
codexThreadUrl = core.codexThreadUrl
codexHistorySourceSignature = core.codexHistorySourceSignature
isChatOptionsLabel = core.isChatOptionsLabel
isPermissionDecisionLabel = core.isPermissionDecisionLabel
isPermissionPromptText = core.isPermissionPromptText
usageLimitNotice = core.usageLimitNotice
pluginInstallProgress = core.pluginInstallProgress
currentActivitySummary = core.currentActivitySummary
backgroundActivityName = core.backgroundActivityName
looksLikeCodexConversation = core.looksLikeCodexConversation
looksLikeBlankCodexConversation = core.looksLikeBlankCodexConversation
pendingChatTitle = core.pendingChatTitle
pluginProgressBusyTransition = core.pluginProgressBusyTransition
supersedesResponseCompletionCandidate = core.supersedesResponseCompletionCandidate


class StatusMessageTests(unittest.TestCase):
	def test_codex_history_source_signature_and_runtime_cache_avoid_repeated_disk_reads(self):
		with tempfile.TemporaryDirectory() as temporaryDirectory:
			root = Path(temporaryDirectory)
			missingSignature = codexHistorySourceSignature(root)
			indexPath = root / "session_index.jsonl"
			indexPath.write_text("first\n", encoding="utf-8")
			firstSignature = codexHistorySourceSignature(root)
			self.assertNotEqual(missingSignature, firstSignature)
			with indexPath.open("a", encoding="utf-8") as indexFile:
				indexFile.write("second\n")
			secondSignature = codexHistorySourceSignature(root)
			self.assertNotEqual(firstSignature, secondSignature)
			(root / "archived_sessions").mkdir()
			self.assertNotEqual(secondSignature, codexHistorySourceSignature(root))

		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		methods = {
			node.name: node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name in {
				"_activeCodexThreadTitles", "_modeSpecificRecentChatTitles",
			}
		}
		sourceSignature = [1]
		diskReads = []
		infoLogs = []
		namespace = {
			"Path": Path, "os": os,
			"codexHistorySourceSignature": lambda root: sourceSignature[0],
			"loadActiveCodexThreadTitles": lambda root: diskReads.append(root) or ("Codex task",),
			"modeSpecificRecentChatTitles": modeSpecificRecentChatTitles,
			"log": type("Log", (), {
				"info": staticmethod(lambda *args, **kwargs: infoLogs.append(args)),
				"debugWarning": staticmethod(lambda *args, **kwargs: None),
			}),
		}
		exec(compile(ast.Module(body=list(methods.values()), type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class CacheSubject:
			_activeCodexTitlesCache = ()
			_activeCodexTitlesSourceSignature = None
		cacheSubject = CacheSubject()
		self.assertEqual(("Codex task",), namespace["_activeCodexThreadTitles"](cacheSubject))
		self.assertEqual(("Codex task",), namespace["_activeCodexThreadTitles"](cacheSubject))
		self.assertEqual(1, len(diskReads))
		sourceSignature[0] = 2
		namespace["_activeCodexThreadTitles"](cacheSubject)
		self.assertEqual(2, len(diskReads))

		class ClassificationSubject:
			def __init__(self): self._recentClassificationSummaries = {"chatgpt": None, "codex": None}
			def _activeCodexThreadTitles(self): return ("Codex task",)
		classificationSubject = ClassificationSubject()
		logCount = len(infoLogs)
		namespace["_modeSpecificRecentChatTitles"](
			classificationSubject, "chatgpt", ("ChatGPT chat", "Codex task"),
		)
		namespace["_modeSpecificRecentChatTitles"](
			classificationSubject, "chatgpt", ("ChatGPT chat", "Codex task"),
		)
		self.assertEqual(logCount + 1, len(infoLogs))

	def test_embedded_browser_accessibility_classification_is_conservative(self):
		self.assertTrue(browserAccess.isEmbeddedBrowserContainerText("Browser", ""))
		self.assertTrue(browserAccess.isEmbeddedBrowserContainerText("", "WebView preview"))
		self.assertFalse(browserAccess.isEmbeddedBrowserContainerText("Codex", "main conversation"))
		self.assertTrue(browserAccess.isEmbeddedBrowserContainerRole("pane"))
		self.assertFalse(browserAccess.isEmbeddedBrowserContainerRole("button"))
		self.assertFalse(browserAccess.isEmbeddedBrowserContainerRole("menu"))
		self.assertFalse(browserAccess.isEmbeddedBrowserDocumentStructure("menu", "document"))
		self.assertTrue(browserAccess.isEmbeddedBrowserDocumentStructure("heading", "document", "document"))
		self.assertEqual("back", browserAccess.embeddedBrowserControlKind("Go back", "button"))
		self.assertEqual("address", browserAccess.embeddedBrowserControlKind("Address and search bar", "edit"))
		self.assertEqual("content", browserAccess.embeddedBrowserControlKind("Example page", "document"))
		self.assertEqual("", browserAccess.embeddedBrowserControlKind("Approve permission", "button"))
		self.assertEqual("Example page", browserAccess.embeddedBrowserTitle("  Example   page  "))
		self.assertEqual("", browserAccess.embeddedBrowserTitle("Embedded browser"))
		self.assertEqual("", browserAccess.browserNavigatorCategory("document", "content"))

	def test_browser_navigator_safe_address_summary_and_snapshot_helpers(self):
		self.assertEqual(
			"https://example.com/account?secret=one#section",
			browserAccess.browserPageAddress(
				"Address: https://example.com/account?secret=one#section",
			),
		)
		self.assertEqual("http://localhost:3000/page", browserAccess.browserPageAddress(
			"http://localhost:3000/page",
		))
		self.assertEqual("", browserAccess.browserPageAddress(
			"javascript:alert(1)", "data:text/html,private",
		))
		self.assertEqual("example.com", browserAccess.browserAddressDomain(
			"https://user:password@example.com/account?secret=one#section",
		))
		self.assertEqual(
			"account|example.com/account",
			browserAccess.browserPageIdentity(
				"Account", "https://user:password@example.com/account?secret=one#section",
			),
		)
		self.assertEqual("account|localhost:3000/page", browserAccess.browserPageIdentity(
			"Account", "http://localhost:3000/page?secret=one",
		))
		self.assertEqual("", browserAccess.browserPageIdentity("", ""))
		items = (
			{"category": "headings"}, {"category": "links"},
			{"category": "links"}, {"category": "formFields"},
		)
		summary = browserAccess.browserPageSummary(
			"Account", "https://example.com/private?token=secret", items, 70, True,
		)
		self.assertIn("Domain: example.com", summary)
		self.assertIn("1 headings", summary)
		self.assertIn("2 links", summary)
		self.assertIn("loading, 70 percent", summary)
		self.assertIn("scan limit reached", summary)
		self.assertNotIn("token", summary)
		snapshot = browserAccess.browserSnapshotText(
			"Account", "https://example.com/private?token=secret",
			("Welcome", "Welcome", "Sign in, button"), True,
		)
		self.assertEqual(1, snapshot.count("Welcome"))
		self.assertIn("Domain: example.com", snapshot)
		self.assertNotIn("token", snapshot)
		self.assertIn("safe scan limit", snapshot)

	def test_browser_navigator_categories_labels_and_search(self):
		self.assertEqual("headings", browserAccess.browserNavigatorCategory("heading"))
		self.assertEqual("landmarks", browserAccess.browserNavigatorCategory("navigation"))
		self.assertEqual("links", browserAccess.browserNavigatorCategory("link"))
		self.assertEqual("buttons", browserAccess.browserNavigatorCategory("button"))
		self.assertEqual("formFields", browserAccess.browserNavigatorCategory("edit"))
		self.assertEqual("tables", browserAccess.browserNavigatorCategory("table"))
		self.assertEqual("controls", browserAccess.browserNavigatorCategory("button", "reload"))
		label = browserAccess.browserNavigatorItemLabel(
			"headings", "Account settings", "heading", level=2, states=("expanded",),
		)
		self.assertEqual("Account settings, heading level 2, expanded", label)
		item = {"category": "headings", "label": label}
		self.assertTrue(browserAccess.browserNavigatorMatches(item, "all", "ACCOUNT"))
		self.assertTrue(browserAccess.browserNavigatorMatches(item, "headings", "level 2"))
		self.assertFalse(browserAccess.browserNavigatorMatches(item, "links", "account"))
		self.assertNotEqual(
			browserAccess.browserNavigatorSignature("links", "link", "Learn more"),
			browserAccess.browserNavigatorSignature("links", "link", "Learn more", 2),
		)
		longName = "A" * 900
		secondLongSignature = browserAccess.browserNavigatorSignature("links", "link", longName, 2)
		self.assertLessEqual(len(secondLongSignature), 600)
		self.assertTrue(secondLongSignature.endswith("|2"))

	def test_embedded_browser_uses_native_navigation_without_a_command_layer(self):
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		appModule = CHATGPT_APP_MODULE_PATH.read_text(encoding="utf-8")
		for command in (
			"openEmbeddedBrowserNavigator", "readEmbeddedBrowserPageSummary",
			"showEmbeddedBrowserSnapshot", "openEmbeddedBrowserExternally",
			"returnToChatGPTPrompt", "showEmbeddedBrowserHelp",
		):
			self.assertNotIn(f"script_{command}", plugin + appModule)
		self.assertNotIn("class CodexEmbeddedBrowserOverlay", plugin)
		self.assertNotIn('"enhanceEmbeddedBrowser"', plugin)
		self.assertNotIn('"rememberEmbeddedBrowserLocations":', plugin)
		self.assertNotIn('"announceEmbeddedBrowserFocus"', plugin)
		self.assertNotIn('"announceEmbeddedBrowserTitles"', plugin)
		self.assertIn('"announceEmbeddedBrowserProgress": "boolean(default=True)"', plugin)
		self.assertIn("BROWSER_LOAD_SETTLE_MILLISECONDS = 1500", plugin)
		self.assertIn("BROWSER_BUSY_FALLBACK_MILLISECONDS = 30000", plugin)
		self.assertIn('self._embeddedBrowserNotice(_("Loading page"))', plugin)
		self.assertIn('self._embeddedBrowserNotice(_("Loading complete"))', plugin)
		eventHooks = plugin[plugin.index("\tdef event_gainFocus"):]
		self.assertNotIn("_startEmbeddedBrowserScan", eventHooks)
		self.assertNotIn("_rememberEmbeddedBrowserObject", eventHooks)

	def test_browser_scan_yields_and_reports_every_result_limit(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_continueEmbeddedBrowserScan"
		)
		class Timer:
			def Stop(self): pass
		class Wx:
			@staticmethod
			def CallLater(delay, callback): return Timer()
		class Time:
			@staticmethod
			def monotonic(): return 0.0
		class Object:
			def __init__(self, role, name):
				self.role = role
				self.name = name
				self.description = ""
				self.value = ""
				self.states = ()
				self.firstChild = None
				self.next = None
		root = Object("pane", "Browser")
		document = Object("document", "Example page")
		root.firstChild = document
		headings = [Object("heading", f"Heading {index}") for index in range(20)]
		headings[2].states = ("defunct",)
		headings[3].states = ("invisible",)
		document.firstChild = headings[0]
		for current, following in zip(headings, headings[1:]):
			current.next = following
		class Subject:
			def __init__(self):
				self._browserScanTimer = Timer()
				self._browserScanState = {
					"stack": [(root, False, 0, False)], "seen": set(), "retained": [],
					"found": False, "firstBrowserObject": None, "items": [],
					"signatureCounts": {},
					"snapshotLines": [], "title": "", "address": "", "objects": 0,
					"truncated": False,
				}
				self.completed = None
			def _browserObjectLevel(self, obj): return 2 if obj.role == "heading" else None
			def _browserObjectStateNames(self, obj): return obj.states
			def _completeEmbeddedBrowserScan(self):
				self.completed = self._browserScanState
				self._browserScanState = None
		namespace = {
			"wx": Wx, "time": Time, "BROWSER_SCAN_MAX_OBJECTS": 12,
			"BROWSER_SCAN_SLICE_OBJECTS": 3, "BROWSER_SCAN_SLICE_SECONDS": 1.0,
			"BROWSER_SCAN_YIELD_MILLISECONDS": 1,
			"BROWSER_SCAN_MAX_ITEMS": 4, "BROWSER_SNAPSHOT_MAX_LINES": 3,
			"_roleName": lambda obj: obj.role,
			"isEmbeddedBrowserContainerText": browserAccess.isEmbeddedBrowserContainerText,
			"isEmbeddedBrowserContainerRole": browserAccess.isEmbeddedBrowserContainerRole,
			"embeddedBrowserControlKind": browserAccess.embeddedBrowserControlKind,
			"embeddedBrowserTitle": browserAccess.embeddedBrowserTitle,
			"browserPageAddress": browserAccess.browserPageAddress,
			"browserNavigatorCategory": browserAccess.browserNavigatorCategory,
			"browserNavigatorItemLabel": browserAccess.browserNavigatorItemLabel,
			"browserNavigatorSignature": browserAccess.browserNavigatorSignature,
			"browserSnapshotLine": browserAccess.browserSnapshotLine,
			"_": lambda text: text,
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		subject = Subject()
		subject._continueEmbeddedBrowserScan = lambda: namespace["_continueEmbeddedBrowserScan"](subject)
		calls = 0
		while subject._browserScanState is not None:
			namespace["_continueEmbeddedBrowserScan"](subject)
			calls += 1
		self.assertGreater(calls, 1)
		self.assertEqual(12, subject.completed["objects"])
		self.assertTrue(subject.completed["found"])
		self.assertTrue(subject.completed["truncated"])
		self.assertEqual(4, len(subject.completed["items"]))
		self.assertEqual(3, len(subject.completed["snapshotLines"]))
		labels = tuple(item["label"] for item in subject.completed["items"])
		self.assertFalse(any("Heading 2" in label or "Heading 3" in label for label in labels))

	def test_completed_browser_scan_rejects_a_page_that_disappeared(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_completeEmbeddedBrowserScan"
		)
		class Subject:
			def __init__(self):
				self._browserScanState = {
					"firstBrowserObject": object(), "found": True, "title": "Example",
					"address": "https://example.com", "items": [{"category": "links"}],
					"snapshotLines": ["Example link"], "truncated": False, "objects": 4,
				}
				self._browserScanPurpose = "navigator"
				self._browserScanCount = 0
				self._lastBrowserScanObjects = 0
				self._browserScanLimitCount = 0
				self._lastEmbeddedBrowserObject = None
				self._embeddedBrowserPageTitle = ""
				self._embeddedBrowserAddress = ""
				self._embeddedBrowserLoadingPercent = None
				self._browserSavedLocations = {}
				self._browserNavigatorResult = None
				self.dispatched = None
			def _browserObjectStateNames(self, obj): return ("invisible",)
			def _dispatchEmbeddedBrowserScan(self, purpose, result): self.dispatched = (purpose, result)
		namespace = {
			"_isDefunctObject": lambda obj: False,
			"browserPageIdentity": browserAccess.browserPageIdentity,
			"browserPageSummary": browserAccess.browserPageSummary,
			"redactSensitive": lambda text: text,
			"_settings": lambda: {"redactSensitive": False},
			"_": lambda text: text,
			"log": type("Log", (), {"debugWarning": staticmethod(lambda *args, **kwargs: None)}),
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		subject = Subject()
		namespace["_completeEmbeddedBrowserScan"](subject)
		self.assertFalse(subject.dispatched[1]["found"])
		self.assertEqual((), subject.dispatched[1]["items"])
		self.assertEqual((), subject.dispatched[1]["snapshotLines"])

	def test_embedded_browser_loading_announces_once_and_completes(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		methods = {
			node.name: node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name in {
				"_scheduleEmbeddedBrowserLoadComplete", "_startEmbeddedBrowserLoading",
				"_completeEmbeddedBrowserLoading", "_resetEmbeddedBrowserProgress",
			}
		}
		class Timer:
			def __init__(self): self.stopped = False
			def Stop(self): self.stopped = True
		class Wx:
			calls = []
			@classmethod
			def CallLater(cls, delay, callback, *args):
				cls.calls.append((delay, callback, args))
				return Timer()
		namespace = {
			"wx": Wx,
			"BROWSER_LOAD_SETTLE_MILLISECONDS": 1500,
			"BROWSER_BUSY_FALLBACK_MILLISECONDS": 30000,
			"_settings": lambda: {"announceEmbeddedBrowserProgress": True},
			"_": lambda text: text,
			"log": type("Log", (), {"info": staticmethod(lambda *args, **kwargs: None)}),
		}
		exec(compile(ast.Module(body=list(methods.values()), type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class Subject:
			def __init__(self):
				self._embeddedBrowserLoadTimer = None
				self._embeddedBrowserLoadGeneration = 0
				self._embeddedBrowserLoadingPercent = None
				self._embeddedBrowserLoading = False
				self._embeddedBrowserBusySeen = False
				self._embeddedBrowserLoadIdentity = ""
				self._embeddedBrowserCompletedIdentity = ""
				self._embeddedBrowserPageTitle = ""
				self._embeddedBrowserProgressBuckets = {}
				self.notices = []
			def _embeddedBrowserNotice(self, message): self.notices.append(message)
			def _scheduleEmbeddedBrowserLoadComplete(self, busy=False):
				return namespace["_scheduleEmbeddedBrowserLoadComplete"](self, busy)
			def _completeEmbeddedBrowserLoading(self, generation=None):
				return namespace["_completeEmbeddedBrowserLoading"](self, generation)
		subject = Subject()
		namespace["_startEmbeddedBrowserLoading"](subject, "page:one", "Example", True, False)
		namespace["_startEmbeddedBrowserLoading"](subject, "page:one", "Example", True, False)
		self.assertEqual(["Loading page"], subject.notices)
		self.assertEqual(1500, Wx.calls[-1][0])
		namespace["_completeEmbeddedBrowserLoading"](subject)
		self.assertEqual(["Loading page", "Loading complete"], subject.notices)
		self.assertFalse(subject._embeddedBrowserLoading)
		namespace["_startEmbeddedBrowserLoading"](subject, "page:two", "Slow", True, True)
		self.assertEqual(30000, Wx.calls[-1][0])
		namespace["_resetEmbeddedBrowserProgress"](subject)
		self.assertFalse(subject._embeddedBrowserLoading)
		self.assertEqual("", subject._embeddedBrowserLoadIdentity)

	def test_embedded_browser_object_rejects_browser_menu_and_accepts_nested_document(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		functions = [
			node for node in tree.body
			if isinstance(node, ast.FunctionDef) and node.name in {"_roleName", "_isEmbeddedBrowserObject"}
		]
		namespace = {
			"_isChatGPTObject": lambda obj: True,
			"_isCodexPromptObject": lambda obj: False,
			"promptControlKind": lambda name: "",
			"isEmbeddedBrowserContainerText": browserAccess.isEmbeddedBrowserContainerText,
			"isEmbeddedBrowserContainerRole": browserAccess.isEmbeddedBrowserContainerRole,
			"isEmbeddedBrowserDocumentStructure": browserAccess.isEmbeddedBrowserDocumentStructure,
		}
		exec(compile(ast.Module(body=functions, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class Object:
			def __init__(self, role, name, parent=None):
				self.role = role
				self.name = name
				self.description = ""
				self.parent = parent
		outerDocument = Object("document", "ChatGPT")
		browserMenu = Object("menu", "Browser", outerDocument)
		self.assertFalse(namespace["_isEmbeddedBrowserObject"](browserMenu))
		innerDocument = Object("document", "Sign in to GitHub · GitHub", outerDocument)
		heading = Object("heading", "Sign in to GitHub", innerDocument)
		self.assertTrue(namespace["_isEmbeddedBrowserObject"](heading))
		self.assertFalse(namespace["_isEmbeddedBrowserObject"](browserMenu))

	def test_defunct_browser_objects_are_rejected_before_focus_or_reuse(self):
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		self.assertIn("if _isDefunctObject(obj) or not _isEmbeddedBrowserObject(obj):", plugin)
		self.assertIn(
			'if obj is None or _isDefunctObject(obj) or not _isChatGPTObject(obj):',
			plugin,
		)
		self.assertIn("self._embeddedBrowserBuffer = None", plugin)
		self.assertIn("candidates.append(api.getFocusObject())", plugin)

	def test_embedded_browser_detection_prefilters_prompt_and_status_objects(self):
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		self.assertIn('if _isCodexPromptObject(obj) or promptControlKind(getattr(obj, "name", "")):', plugin)
		self.assertIn("obj._codexEmbeddedBrowserDetected = False", plugin)
		chooseStart = plugin.index("\tdef chooseNVDAObjectOverlayClasses(self, obj, clsList):")
		chooseEnd = plugin.index("\n\tdef __init__(self):", chooseStart)
		chooseBody = plugin[chooseStart:chooseEnd]
		self.assertIn("promptControlKind(", chooseBody)
		self.assertNotIn("_isEmbeddedBrowserObject(", chooseBody)
		self.assertNotIn("CodexEmbeddedBrowserOverlay", chooseBody)

	def test_prompt_overlay_disables_only_generic_newline_announcement_script(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		overlayNode = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "CodexPromptEditableTextOverlay"
		)
		overlayNamespace = {}
		exec(compile(ast.Module(body=[overlayNode], type_ignores=[]), str(PLUGIN_PATH), "exec"), overlayNamespace)
		overlayClass = overlayNamespace["CodexPromptEditableTextOverlay"]
		self.assertFalse(overlayClass.announceNewLineText)
		self.assertFalse(hasattr(overlayClass, "__gestures"))

		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		chooseMethod = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "chooseNVDAObjectOverlayClasses"
		)

		class RoleStub:
			BUTTON = "button"
			COMBOBOX = "combobox"
			EDITABLETEXT = "editableText"
			DOCUMENT = "document"

		namespace = {
			"Role": RoleStub,
			"_isChatGPTObject": lambda obj: True,
			"_isCodexPromptObject": lambda obj: bool(getattr(obj, "isPrompt", False)),
			"promptControlKind": lambda name: "",
			"CodexPromptControlOverlay": object,
			"CodexPromptEditableTextOverlay": overlayClass,
			"CodexEmbeddedBrowserOverlay": object,
			"_settings": lambda: {"enhanceEmbeddedBrowser": False},
			"_embeddedBrowserKind": lambda obj: "",
		}
		exec(compile(ast.Module(body=[chooseMethod], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		prompt = type("Object", (), {"role": RoleStub.EDITABLETEXT, "isPrompt": True})()
		classes = []
		namespace["chooseNVDAObjectOverlayClasses"](object(), prompt, classes)
		self.assertEqual([overlayClass], classes)

	def test_embedded_browser_progress_is_bucketed_and_scoped(self):
		self.assertEqual(
			("loading page", 47, 40),
			browserAccess.embeddedBrowserProgress("Loading page", "47%"),
		)
		self.assertEqual(
			("loading page", 100, 100),
			browserAccess.embeddedBrowserProgress("Loading page", "100 percent"),
		)
		self.assertEqual(("loading page", None, None), browserAccess.embeddedBrowserProgress("Loading page"))
		self.assertEqual(("loading page", 5, 10), browserAccess.embeddedBrowserProgress("Loading page", "5"))
		self.assertIsNone(browserAccess.embeddedBrowserProgress("Downloading model"))

	def test_embedded_browser_focus_tracking_is_silent_and_resets_load_state_on_exit(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_updateEmbeddedBrowserFocus"
		)
		namespace = {
			"_isEmbeddedBrowserObject": lambda obj: obj.browser,
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class Subject:
			def __init__(self):
				self._embeddedBrowserFocused = False
				self.resetCount = 0
			def _resetEmbeddedBrowserProgress(self): self.resetCount += 1
		subject = Subject()
		browser = type("Object", (), {"browser": True})()
		conversation = type("Object", (), {"browser": False})()
		namespace["_updateEmbeddedBrowserFocus"](subject, browser)
		namespace["_updateEmbeddedBrowserFocus"](subject, browser)
		self.assertTrue(subject._embeddedBrowserFocused)
		self.assertEqual(0, subject.resetCount)
		namespace["_updateEmbeddedBrowserFocus"](subject, conversation)
		self.assertFalse(subject._embeddedBrowserFocused)
		self.assertEqual(1, subject.resetCount)

	def test_runtime_imports_include_required_helpers(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		self.assertIn(
			"re",
			{
				alias.name
				for node in tree.body
				if isinstance(node, ast.Import)
				for alias in node.names
			},
		)
		coreImport = next(
			node for node in tree.body
			if isinstance(node, ast.ImportFrom) and node.module == "core"
		)
		self.assertIn("soundKey", {alias.name for alias in coreImport.names})

	def test_package_builder_normalizes_text_but_preserves_binary_data(self):
		with tempfile.TemporaryDirectory() as tempDir:
			textPath = Path(tempDir) / "module.py"
			binaryPath = Path(tempDir) / "sound.wav"
			textPath.write_bytes(b"first\r\nsecond\rthird\n")
			binary = b"RIFF\r\n\x00\rdata"
			binaryPath.write_bytes(binary)
			self.assertEqual(b"first\nsecond\nthird\n", packageBuilder.packageData(textPath))
			self.assertEqual(binary, packageBuilder.packageData(binaryPath))

	def test_package_builder_includes_docs_and_only_current_tiered_sounds(self):
		paths = tuple(path.relative_to(PROJECT_ROOT).as_posix() for path in packageBuilder.packageFiles(PROJECT_ROOT))
		for required in ("manifest.ini", "readme.md", "changelog.md", "LICENSE.txt"):
			self.assertIn(required, paths)
		self.assertEqual(64, len(paths))
		self.assertEqual(51, sum(path.endswith(".wav") for path in paths))
		self.assertIn("globalPlugins/codexStatusAnnouncer/browserNavigatorDialog.py", paths)
		self.assertFalse(any(path.startswith("globalPlugins/codexStatusAnnouncer/sounds/") and path.count("/") == 3 for path in paths))
		self.assertFalse(any(path.endswith(".pot") for path in paths))

	def test_release_workflow_publishes_and_rechecks_only_the_audited_public_package(self):
		workflow = RELEASE_WORKFLOW_PATH.read_text(encoding="utf-8")
		self.assertIn('tags: ["v[0-9]*.[0-9]*.[0-9]*"]', workflow)
		self.assertIn("contents: write", workflow)
		self.assertIn(".\\build.ps1 -PythonPath python", workflow)
		self.assertIn('$package = "outputs/chatGPTDesktopAccess-$manifestVersion.nvda-addon"', workflow)
		self.assertIn("python tools/build_addon.py $reproduction", workflow)
		self.assertIn("gh release create", workflow)
		self.assertIn("gh release download", workflow)
		self.assertIn("python tools/audit_addon.py $downloaded $manifestVersion", workflow)
		self.assertNotIn("codexStatusAnnouncer-$manifestVersion.nvda-addon", workflow)

	def test_settings_page_controls_have_distinct_access_keys(self):
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		pageLabels = {
			"General": (
				"Announcement &detail:", "Enable &speech announcements",
				"Enable &braille flash messages",
				"&Redact likely secrets and personal path names in Full mode",
				"Test current announcement outputs (&T)",
			),
			"Speech and Braille": (
				"&Full speech profile:", "&Minimal speech profile:",
				"Command &punctuation for speech:", "Maximum spoken command &length:",
				"Braille &detail:",
				"Keep &conversation reading stable for speech and Braille during live updates",
				"Allow &urgent permission and failure announcements to interrupt current speech",
				"&Reset speech profile settings",
			),
			"Sounds": (
				"Play a sound for task &completion or failure",
				"Play &progress sounds for enabled announcements", "Progress sound style (&J):",
				"Click volume (&Z):", "Play a continuous &Working sound while ChatGPT or Codex is busy",
				"Working sound &interval (milliseconds):",
				"&Delay before repeating Working sounds (milliseconds):",
				"Play a distinct sound when a prompt is &submitted",
				"Play sounds when ChatGPT or Codex &monitoring becomes active or inactive",
				"Test command progress sound (&K)",
			),
			"Activity Output": (
				"Background progress &interval (seconds):", "Maximum background activity (&minutes):",
				"Announce a recurring background progress &pulse", "Activity &category:",
				"&Enable this activity category", "Output &route for this category:",
			),
			"Wording and Preview": (
				"Preview action (&V):", "Announcement &text (blank uses built-in):",
				"&Restore built-in announcement", "Preview selected &sound",
				"Preview selected s&peech",
			),
			"Browser Access": (
				"Announce when embedded browser pages start and finish &loading",
			),
			"Advanced": (
				"Idle compatibility &polling interval (milliseconds):",
				"Supported application &names, comma separated:",
				"Enable sanitized dia&gnostic logging",
			),
			"Support": (
				"&Check Codex usage statistics", "&Buy Codex usage credits",
				"View current release &notes…", "View complete release &history…",
				"Save sanitized support &report…", "&Export add-on settings…",
				"&Import add-on settings…",
			),
		}
		for page, labels in pageLabels.items():
			mnemonics = []
			for label in labels:
				self.assertIn(label, plugin, f"{page}: {label}")
				marker = label.index("&")
				mnemonics.append(label[marker + 1].casefold())
			self.assertEqual(len(mnemonics), len(set(mnemonics)), page)

	def test_manifest_version_audit_accepts_lf_and_crlf_archives(self):
		tree = ast.parse(AUDIT_PATH.read_text(encoding="utf-8"))
		function = next(
			node for node in tree.body
			if isinstance(node, ast.FunctionDef) and node.name == "manifestVersionMatches"
		)
		namespace = {"re": __import__("re")}
		exec(compile(ast.Module(body=[function], type_ignores=[]), str(AUDIT_PATH), "exec"), namespace)
		for lineEnding in ("\n", "\r\n"):
			manifest = lineEnding.join(("name = codexStatusAnnouncer", "version = 2026.2.2", ""))
			self.assertTrue(namespace["manifestVersionMatches"](manifest, "2026.2.2"))
			self.assertFalse(namespace["manifestVersionMatches"](manifest, "2026.2.3"))

	def test_activity_settings_editor_preserves_each_category(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		panelClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "CodexStatusAnnouncerSettingsPanel"
		)
		methods = [
			node for node in panelClass.body
			if isinstance(node, ast.FunctionDef) and node.name in {
				"_activityCategoryDisplay", "_refreshActivityCategoryDisplay",
				"_storeActivityCategory", "_loadActivityCategory", "_onActivityCategoryChanged",
				"_onActivitySettingChanged",
			}
		]
		namespace = {
			"OUTPUT_MODE_CHOICES": ("all", "speech", "sound", "braille", "off"),
			"_": lambda value: value,
		}
		exec(compile(ast.Module(body=methods, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class Check:
			def __init__(self, value=False): self.value = value
			def IsChecked(self): return self.value
			def SetValue(self, value): self.value = value
		class Choice:
			def __init__(self, selection=0): self.selection = selection
			def GetSelection(self): return self.selection
			def SetSelection(self, selection): self.selection = selection
			def SetString(self, index, value): self.lastString = (index, value)
		class Subject:
			pass
		for name in (
			"_activityCategoryDisplay", "_refreshActivityCategoryDisplay",
			"_storeActivityCategory", "_loadActivityCategory", "_onActivityCategoryChanged",
			"_onActivitySettingChanged",
		):
			setattr(Subject, name, namespace[name])
		subject = Subject()
		subject._activityCategories = (
			("announceThinking", "thinking", "Thinking"),
			("announceCommands", "command", "Commands"),
		)
		subject._categoryEnabledValues = {"announceThinking": True, "announceCommands": False}
		subject._categoryOutputValues = {"thinking": "all", "command": "speech"}
		subject._outputModeLabels = ("all enabled channels", "speech only", "sound only", "braille only", "off")
		subject._activityCategorySelection = 0
		subject.activityEnabled = Check(False)
		subject.activityOutput = Choice(2)
		subject.activityCategory = Choice(1)
		subject._onActivityCategoryChanged(None)
		self.assertFalse(subject._categoryEnabledValues["announceThinking"])
		self.assertEqual("sound", subject._categoryOutputValues["thinking"])
		self.assertEqual((0, "Thinking: disabled; sound only"), subject.activityCategory.lastString)
		self.assertFalse(subject.activityEnabled.IsChecked())
		self.assertEqual(1, subject.activityOutput.GetSelection())
		subject.activityEnabled.SetValue(True)
		subject.activityOutput.SetSelection(4)
		subject._storeActivityCategory()
		self.assertTrue(subject._categoryEnabledValues["announceCommands"])
		self.assertEqual("off", subject._categoryOutputValues["command"])
		self.assertEqual((1, "Commands: enabled; off"), subject.activityCategory.lastString)

	def test_addon_store_metadata_matches_manifest_and_package(self):
		with tempfile.TemporaryDirectory() as tempDir:
			package = Path(tempDir) / "chatGPTDesktopAccess-2026.2.5.nvda-addon"
			package.write_bytes(b"deterministic test package")
			url = "https://github.com/jcoffin1/chatgpt-desktop-access/releases/download/v2026.2.5/chatGPTDesktopAccess-2026.2.5.nvda-addon"
			metadata = storeMetadata.generate(PROJECT_ROOT, package, url)
		self.assertEqual("codexStatusAnnouncer", metadata["addonId"])
		self.assertEqual("2026.2.5", metadata["addonVersionName"])
		self.assertEqual({"major": 2026, "minor": 2, "patch": 5}, metadata["addonVersionNumber"])
		self.assertEqual({"major": 2026, "minor": 2, "patch": 0}, metadata["lastTestedVersion"])
		self.assertEqual(url, metadata["URL"])
		self.assertEqual(64, len(metadata["sha256"]))
		self.assertEqual("ChatGPT Desktop Access for NVDA", metadata["displayName"])
		self.assertEqual("https://github.com/jcoffin1/chatgpt-desktop-access", metadata["homepage"])
		self.assertEqual([], metadata["translations"])
		manifest = (PROJECT_ROOT / "manifest.ini").read_text(encoding="utf-8")
		self.assertEqual(storeMetadata._manifestValue(manifest, "changelog"), metadata["changelog"])
		self.assertNotIn("What to test", metadata["changelog"])
		for text in (
			"AI", "artificial intelligence", "AI-generated", "generated by ChatGPT",
			"written by OpenAI", "Co-authored-by: Example",
		):
			with self.subTest(publicText=text), self.assertRaises(ValueError):
				storeMetadata._validatePublicText(text)

	def test_every_nvda_event_hook_is_exception_isolated_and_continues_the_chain(self):
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
			if method.name == "event_caret":
				# This hook must run before NVDA's object-level caret handler, which
				# would otherwise flush the first cell of the next contracted word.
				tryNode = next(node for node in method.body if isinstance(node, ast.Try))
				self.assertTrue(tryNode.finalbody, method.name)
				self.assertTrue(any(
					isinstance(node, ast.Call)
					and getattr(node.func, "id", "") == "nextHandler"
					for node in ast.walk(tryNode.finalbody[0])
				), method.name)
				continue
			if method.name == "event_liveRegionChange":
				# This hook deliberately withholds only ordinary streamed Response
				# updates while browse-mode reading protection is active. Every other
				# live-region event must continue through NVDA's native handler.
				self.assertTrue(any(
					isinstance(node, ast.Call)
					and getattr(node.func, "id", "") == "nextHandler"
					for node in ast.walk(method)
				), method.name)
				self.assertIn("shouldSuppressNativeConversationUpdate", ast.unparse(method))
				continue
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
			def _updateAppFocusState(self, obj): return None
			def _rememberEmbeddedBrowserObject(self, obj): return False
			def _updateEmbeddedBrowserFocus(self, obj): pass
			def _announceEmbeddedBrowserTitle(self, obj): pass
			def _rememberBuffer(self, obj): pass
			def _schedulePopupDialogFocus(self, obj): pass
			def _announceUsageLimit(self, obj): return False
			def _schedulePoll(self, *args, **kwargs): self.polls += 1
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

	def test_chat_commands_are_truly_app_scoped_and_configurable(self):
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		appModule = CHATGPT_APP_MODULE_PATH.read_text(encoding="utf-8")
		codexAppModule = CODEX_APP_MODULE_PATH.read_text(encoding="utf-8")
		appTree = ast.parse(appModule)
		appClass = next(
			node for node in appTree.body
			if isinstance(node, ast.ClassDef) and node.name == "AppModule"
		)
		self.assertEqual("appModuleHandler.AppModule", ast.unparse(appClass.bases[0]))
		gestureAssignment = next(
			node for node in appClass.body
			if isinstance(node, ast.Assign)
			and any(isinstance(target, ast.Name) and target.id == "__gestures" for target in node.targets)
		)
		gestures = ast.literal_eval(gestureAssignment.value)
		self.assertEqual(12, len(gestures))
		self.assertEqual("toggleVoiceMode", gestures["kb:NVDA+alt+v"])
		self.assertEqual("toggleMicrophoneMute", gestures["kb:NVDA+alt+m"])
		for digit in "1234567890":
			self.assertIn(f"kb:control+{digit}", gestures)
		# NVDA's user gesture map is class-based. Keeping every binding and script
		# on the app module means both defaults and reassignments resolve only when
		# the ChatGPT/Codex app module is the focused application's module.
		globalClass = next(
			node for node in ast.parse(plugin).body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		globalNames = {node.name for node in globalClass.body if isinstance(node, ast.FunctionDef)}
		self.assertNotIn("getScript", globalNames)
		self.assertFalse(any(name.startswith("script_read") and name.endswith("ChatMessage") for name in globalNames))
		self.assertNotIn("script_toggleVoiceMode", globalNames)
		self.assertNotIn("script_toggleMicrophoneMute", globalNames)
		browserScripts = {
			"script_openEmbeddedBrowserNavigator", "script_readEmbeddedBrowserPageSummary",
			"script_showEmbeddedBrowserSnapshot", "script_openEmbeddedBrowserExternally",
			"script_returnToChatGPTPrompt",
		}
		appNames = {node.name for node in appClass.body if isinstance(node, ast.FunctionDef)}
		self.assertTrue(browserScripts.isdisjoint(appNames))
		self.assertNotIn("gesture.send()", plugin + appModule)
		self.assertIn("from appModules.chatgpt import AppModule", codexAppModule)

	def test_existing_app_command_gesture_customizations_are_migrated_safely(self):
		pluginSource = PLUGIN_PATH.read_text(encoding="utf-8")
		tree = ast.parse(pluginSource)
		function = next(
			node for node in tree.body
			if isinstance(node, ast.FunctionDef) and node.name == "_migrateApplicationGestureMappings"
		)
		class FakeGestureMap:
			def __init__(self):
				self.entries = {
					"globalPlugins.codexStatusAnnouncer.GlobalPlugin": {
						"toggleVoiceMode": "kb:NVDA+shift+v",
						"readMostRecentChatMessage": ["kb:control+shift+1", "kb:control+alt+1"],
						"openChatHistory": "kb:NVDA+alt+o",
						"None": ["kb:control+1", "kb:NVDA+alt+x"],
					},
					"appModules.chatgpt.AppModule": {
						"readMostRecentChatMessage": "kb:control+shift+1",
					},
				}
				self.removed = []
				self.added = []
				self.saveCalls = 0
			def export(self): return self.entries
			def remove(self, gesture, module, className, script):
				self.removed.append((gesture, module, className, script))
			def add(self, gesture, module, className, script):
				self.added.append((gesture, module, className, script))
			def save(self): self.saveCalls += 1
		userMap = FakeGestureMap()
		namespace = {
			"inputCore": type("InputCore", (), {
				"manager": type("Manager", (), {"userGestureMap": userMap})(),
				"normalizeGestureIdentifier": staticmethod(lambda gesture: gesture.casefold()),
			})(),
			"APP_SCOPED_SCRIPT_NAMES": (
				"readMostRecentChatMessage", "toggleVoiceMode", "toggleMicrophoneMute",
			),
			"APP_SCOPED_DEFAULT_GESTURES": ("kb:control+1", "kb:NVDA+alt+v", "kb:NVDA+alt+m"),
			"log": type("Log", (), {"debugWarning": staticmethod(lambda *args, **kwargs: None)})(),
		}
		exec(compile(ast.Module(body=[function], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		self.assertEqual(4, namespace["_migrateApplicationGestureMappings"]())
		self.assertEqual(1, userMap.saveCalls)
		self.assertEqual(4, len(userMap.removed))
		self.assertIn(
			("kb:nvda+shift+v", "appModules.chatgpt", "AppModule", "toggleVoiceMode"),
			userMap.added,
		)
		self.assertIn(
			("kb:control+alt+1", "appModules.chatgpt", "AppModule", "readMostRecentChatMessage"),
			userMap.added,
		)
		self.assertIn(("kb:control+1", "appModules.chatgpt", "AppModule", None), userMap.added)
		self.assertNotIn(
			("kb:nvda+alt+x", "appModules.chatgpt", "AppModule", None),
			userMap.added,
		)
		self.assertFalse(any(item[-1] == "openChatHistory" for item in userMap.removed))

	def test_voice_control_labels_are_exact_and_do_not_match_speaker_controls(self):
		for label, expected in (
			("Start voice chat", "start"), ("Start voice mode", "start"),
			("Stop voice chat", "stop"), ("End voice chat", "stop"),
			("Leave voice mode", "stop"), ("Exit voice mode", "stop"),
			("Mute microphone", "mute"), ("Mute mic", "mute"),
			("Unmute microphone", "unmute"), ("Unmute mic", "unmute"),
		):
			self.assertEqual(expected, voiceControlKind(label), label)
			self.assertTrue(isKnownNonStatusButton(label), label)
		for label in ("Mute speakers", "Unmute speakers", "Voice chat", "Microphone", "Mute"):
			self.assertEqual("", voiceControlKind(label), label)

	def test_voice_actions_report_transition_then_confirmed_result(self):
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		tree = ast.parse(plugin)
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		methods = [
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name in {
				"_activateVoiceControl", "_confirmVoiceControlAction",
			}
		]
		messages = []
		namespace = {
			"api": type("Api", (), {"getFocusObject": staticmethod(lambda: object())})(),
			"_isChatGPTObject": lambda obj: True,
			"ui": type("Ui", (), {"message": staticmethod(messages.append)})(),
			"_": lambda text: text,
			"VOICE_CONTROL_CONFIRMATION_ATTEMPTS": 2,
			"VOICE_CONTROL_CONFIRMATION_DELAY_MS": 500,
			"wx": type("Wx", (), {"CallLater": staticmethod(lambda *args: object())})(),
			"log": type("Log", (), {
				"info": staticmethod(lambda *args, **kwargs: None),
				"debugWarning": staticmethod(lambda *args, **kwargs: None),
			})(),
		}
		exec(compile(ast.Module(body=methods, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)

		class Control:
			def __init__(self): self.activated = 0
			def doAction(self): self.activated += 1
		control = Control()
		class Subject:
			def __init__(self):
				self._pendingVoiceControlConfirmation = None
				self._voiceControlConfirmationTimer = None
			def _cancelVoiceControlConfirmation(self):
				self._pendingVoiceControlConfirmation = None
			def _voiceControlObject(self, wantedKinds):
				if "mute" in wantedKinds:
					return control, "mute"
				return control, "unmute"
			def _scheduleVoiceControlConfirmation(self, kind):
				self._pendingVoiceControlConfirmation = (kind, 0)
		subject = Subject()
		namespace["_activateVoiceControl"](subject, ("unmute", "mute"))
		self.assertEqual(1, control.activated)
		self.assertEqual(["Muting microphone"], messages)
		self.assertEqual(("mute", 0), subject._pendingVoiceControlConfirmation)
		namespace["_confirmVoiceControlAction"](subject)
		self.assertEqual(["Muting microphone", "Microphone muted"], messages)
		self.assertIsNone(subject._pendingVoiceControlConfirmation)

	def test_voice_control_search_prefers_current_state_and_exact_button_role(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		methods = [
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name in {
				"_voiceControlFromObject", "_voiceControlObject",
			}
		]

		class Object:
			def __init__(self, name, role="button", parent=None, states=()):
				self.name = name
				self.role = role
				self.parent = parent
				self.states = states
		start = Object("Start voice chat")
		stop = Object("Stop voice chat")
		muteSpeakers = Object("Mute speakers", role="togglebutton")
		pressedMute = Object("Mute microphone", role="togglebutton", states={"pressed"})

		class Position:
			def __init__(self): self.NVDAObjectAtStart = None
			def find(self, label, reverse, caseSensitive):
				self.NVDAObjectAtStart = {
					"Stop voice chat": stop,
					"Start voice chat": start,
					"Mute microphone": muteSpeakers,
				}.get(label)
				return self.NVDAObjectAtStart is not None
		class Buffer:
			def makeTextInfo(self, position): return Position()
		class Subject:
			_buffer = Buffer()
			def _rememberBuffer(self, focus): pass

		namespace = {
			"api": type("Api", (), {
				"getFocusObject": staticmethod(lambda: Object("Do anything", role="editabletext")),
				"getFocusAncestors": staticmethod(lambda: ()),
			})(),
			"voiceControlKind": voiceControlKind,
			"_roleName": lambda obj: obj.role,
			"State": type("State", (), {"PRESSED": "pressed", "CHECKED": "checked"}),
			"VOICE_CONTROL_SEARCH_LABELS": (
				("stop", "Stop voice chat"), ("start", "Start voice chat"),
				("mute", "Mute microphone"),
			),
			"textInfos": type("TextInfos", (), {"POSITION_LAST": "last"})(),
		}
		exec(compile(ast.Module(body=methods, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		subject = Subject()
		subject._voiceControlFromObject = lambda obj, wanted: namespace["_voiceControlFromObject"](
			subject, obj, wanted,
		)
		control, kind = namespace["_voiceControlObject"](subject, ("stop", "start"))
		self.assertIs(stop, control)
		self.assertEqual("stop", kind)
		control, kind = namespace["_voiceControlObject"](subject, ("mute", "unmute"))
		self.assertIsNone(control)
		self.assertEqual("", kind)
		control, kind = namespace["_voiceControlFromObject"](
			subject, pressedMute, ("unmute", "mute"),
		)
		self.assertIs(pressedMute, control)
		self.assertEqual("unmute", kind)

	def test_release_metadata_and_requested_chat_message_gestures_are_consistent(self):
		manifest = (PROJECT_ROOT / "manifest.ini").read_text(encoding="utf-8")
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		appModule = CHATGPT_APP_MODULE_PATH.read_text(encoding="utf-8")
		codexAppModule = CODEX_APP_MODULE_PATH.read_text(encoding="utf-8")
		chatDialog = CHAT_DIALOG_PATH.read_text(encoding="utf-8")
		soundOutput = SOUND_OUTPUT_PATH.read_text(encoding="utf-8")
		self.assertIn("version = 2026.2.5", manifest)
		self.assertIn('summary = "ChatGPT Desktop Access for NVDA"', manifest)
		self.assertIn('ADDON_VERSION = "2026.2.5"', plugin)
		self.assertIn('DEFAULT_SUPPORTED_APP_NAMES = "chatgpt,codex"', plugin)
		self.assertIn("not _isConversationObject(obj)", plugin)
		self.assertIn("url = https://github.com/jcoffin1/chatgpt-desktop-access", manifest)
		self.assertIn("docFileName = readme.md", manifest)
		self.assertIn("minimumNVDAVersion = 2023.1.0", manifest)
		self.assertIn("lastTestedNVDAVersion = 2026.2.0", manifest)
		self.assertIn("updateChannel = None", manifest)
		self.assertIn('"protectBrailleReading": "boolean(default=True)"', plugin)
		self.assertIn('conf["protectBrailleReading"], self._appFocusState', plugin)
		self.assertIn("actualDelay = coalescedPollDelay(", plugin)
		self.assertIn("shouldReplaceScheduledPoll(self._nextPollAt, requestedDeadline)", plugin)
		self.assertIn('log.debugWarning("ChatGPT Desktop Access speech output failed"', plugin)
		self.assertIn('log.debugWarning("ChatGPT Desktop Access Braille output failed"', plugin)
		self.assertIn('log.debugWarning("ChatGPT Desktop Access tone output failed"', soundOutput)
		self.assertIn("def safeBeep(frequency, duration):", soundOutput)
		self.assertIn("safeBeep as _safeBeep", plugin)
		self.assertIn('log.debugWarning("ChatGPT Desktop Access could not cancel speech for an urgent message"', plugin)
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
		self.assertNotIn("obsolete Codex Status Announcer loaded", plugin)
		self.assertNotIn("Adds assignable focus- and browse-mode actions", manifest)
		self.assertIn('default=\'full\'', plugin)
		self.assertIn("fullSpeechProfile", plugin)
		self.assertIn("default='developer'", plugin)
		self.assertIn("minimalSpeechProfile", plugin)
		self.assertIn("default='balanced'", plugin)
		self.assertIn("brailleDetail", plugin)
		self.assertIn("interruptUrgentSpeech", plugin)
		self.assertIn("__gestures = {", appModule)
		for digit, scriptName in zip("1234567890", (
			"readMostRecentChatMessage", "readSecondMostRecentChatMessage",
			"readThirdMostRecentChatMessage", "readFourthMostRecentChatMessage",
			"readFifthMostRecentChatMessage", "readSixthMostRecentChatMessage",
			"readSeventhMostRecentChatMessage", "readEighthMostRecentChatMessage",
			"readNinthMostRecentChatMessage", "readTenthMostRecentChatMessage",
		)):
			self.assertIn(f'"kb:control+{digit}": "{scriptName}"', appModule)
			self.assertIn(f"def script_{scriptName}", appModule)
		self.assertIn('"kb:NVDA+alt+v": "toggleVoiceMode"', appModule)
		self.assertIn('"kb:NVDA+alt+m": "toggleMicrophoneMute"', appModule)
		self.assertIn("class AppModule(appModuleHandler.AppModule)", appModule)
		self.assertIn("from appModules.chatgpt import AppModule", codexAppModule)
		self.assertNotIn("gesture.send()", plugin + appModule)
		self.assertNotIn("_setChatMessageShortcutBindings", plugin)
		self.assertNotIn('"kb:enter"', plugin)
		self.assertNotIn("script_enter", plugin.casefold())
		self.assertTrue(CHATGPT_APP_MODULE_PATH.exists())
		self.assertTrue(CODEX_APP_MODULE_PATH.exists())
		self.assertNotIn("gesture=", plugin + appModule)
		self.assertNotIn("self._chatHistoryDialog.ShowModal", plugin)
		self.assertIn('label=_("Recent chats:")', chatDialog)
		self.assertIn('label=_("Archived chats:")', chatDialog)
		self.assertIn("self.recentList", chatDialog)
		self.assertIn("self.archivedList", chatDialog)
		self.assertIn("self.recentList.Bind(wx.EVT_CONTEXT_MENU, self._onContextMenu)", chatDialog)
		self.assertIn("self.archivedList.Bind(wx.EVT_CONTEXT_MENU, self._onContextMenu)", chatDialog)
		self.assertIn("self._showChatActionMenu(selection)", chatDialog)
		self.assertIn("self._retryDirectChatAction", plugin)
		self.assertIn('self._performSelectedAction(selection, "focusActions")', chatDialog)
		self.assertIn('actionButton.setFocus()', plugin)
		self.assertIn("self._scheduleUnarchiveButtonFocus()", plugin)
		self.assertIn('position.find("Unarchive and open"', plugin)
		self.assertIn("message = _completeChangelogMessage()", plugin)
		self.assertIn("_showBrowseableMessageAtTop(", plugin)
		self.assertIn('CURRENT_RELEASE_NOTES, _("ChatGPT Desktop Access — what\'s new")', plugin)
		self.assertIn('scriptCategory = _("ChatGPT Desktop Access")', plugin)
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
		self.assertIn("_onRefresh", chatDialog)
		self.assertIn("wx.Notebook(self)", plugin)
		self.assertIn('self._addPage(_("Activity Output"))', plugin)
		self.assertIn('self._addPage(_("Browser Access"))', plugin)
		self.assertIn('self._addPage(_("Advanced"))', plugin)
		self.assertIn('self._addPage(_("Support"))', plugin)
		self.assertNotIn('self._addPage(_("Advanced and Support"))', plugin)
		self.assertIn("_activityCategoryDisplay", plugin)
		self.assertIn("for index in range(len(self._activityCategories)):", plugin)
		self.assertIn('defaultFile="chatgpt-desktop-access-settings.json"', plugin)
		self.assertIn("_onSaveSupportReport", plugin)
		self.assertIn("script_saveSupportReport", plugin)
		self.assertNotIn("script_openAddFilesAndMore", plugin)
		self.assertNotIn("script_openModelSelector", plugin)
		self.assertNotIn("script_openChangePermissions", plugin)
		self.assertNotIn("_boundedDescendants", plugin)
		self.assertIn("class CodexPromptControlOverlay", plugin)
		self.assertNotIn("class CodexEmbeddedBrowserOverlay", plugin)
		self.assertNotIn("def script_showEmbeddedBrowserHelp", plugin)
		self.assertIn("def event_stateChange", plugin)
		self.assertIn('self._embeddedBrowserNotice(_("Loading page"))', plugin)
		self.assertIn('self._embeddedBrowserNotice(_("Loading complete"))', plugin)
		self.assertIn("chooseNVDAObjectOverlayClasses", plugin)
		self.assertIn("_codexNativeDescription", plugin)
		self.assertNotIn("could not enhance a prompt control", plugin)
		self.assertIn("_chatHistoryActionTimer", plugin)
		self.assertIn("chatTitleMatches(title", plugin)
		self.assertIn("unrecognized buttons: count=%d, lengths=%s", plugin)
		self.assertNotIn('unrecognized buttons: %s", list(snapshot)', plugin)

	def test_restricted_nvda_runtime_does_not_require_known_optional_modules(self):
		source = "\n".join(
			path.read_text(encoding="utf-8")
			for path in CORE_PATH.parent.glob("*.py")
		)
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

	def test_required_chatgpt_and_codex_app_hosts_survive_custom_settings(self):
		self.assertEqual("chatgpt,codex", mergeSupportedAppNames("chatgpt"))
		self.assertEqual("chatgpt,codex,customhost", mergeSupportedAppNames("CustomHost,CHATGPT"))

	def test_conversation_document_modes_exclude_nested_browser_documents(self):
		self.assertEqual("chatgpt", conversationModeFromDocumentNames(("ChatGPT",)))
		self.assertEqual("codex", conversationModeFromDocumentNames(("Codex",)))
		self.assertEqual("", conversationModeFromDocumentNames(("Purchase credits", "ChatGPT")))
		self.assertEqual("", conversationModeFromDocumentNames(("Settings",)))
		self.assertEqual("codex", conversationModeFromSwitchLabel("Switch mode, current mode: Codex"))
		self.assertEqual("chatgpt", conversationModeFromSwitchLabel("Switch mode, current mode: ChatGPT"))
		self.assertEqual("", conversationModeFromSwitchLabel("ChatGPT"))
		self.assertEqual("", conversationModeFromSwitchLabel("Switch mode"))

	def test_runtime_conversation_mode_accepts_both_modes_but_rejects_embedded_web_content(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		functions = [
			node for node in pluginTree.body
			if isinstance(node, ast.FunctionDef) and node.name in (
				"_roleName", "_conversationModeForObject", "_isConversationObject",
			)
		]
		namespace = {
			"_isChatGPTObject": lambda obj: bool(getattr(obj, "supportedApp", True)),
			"conversationModeFromDocumentNames": conversationModeFromDocumentNames,
			"isEmbeddedBrowserContainerText": browserAccess.isEmbeddedBrowserContainerText,
			"isEmbeddedBrowserContainerRole": browserAccess.isEmbeddedBrowserContainerRole,
		}
		exec(compile(ast.Module(body=functions, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class RoleName:
			def __init__(self, name): self.name = name
		class Object:
			def __init__(self, role, name="", parent=None, description="", supportedApp=True):
				self.role = RoleName(role)
				self.name = name
				self.parent = parent
				self.description = description
				self.supportedApp = supportedApp
		chatgptDocument = Object("document", "ChatGPT")
		codexDocument = Object("document", "Codex")
		self.assertEqual("chatgpt", namespace["_conversationModeForObject"](Object("button", "Thinking", chatgptDocument)))
		self.assertEqual("codex", namespace["_conversationModeForObject"](Object("button", "Thinking", codexDocument)))
		embeddedDocument = Object("document", "Purchase credits", chatgptDocument)
		self.assertFalse(namespace["_isConversationObject"](Object("button", "Buy", embeddedDocument)))
		self.assertFalse(namespace["_isConversationObject"](Object("button", "Thinking", chatgptDocument, supportedApp=False)))

	def test_conversation_event_accepts_rebuilt_main_buffer_but_rejects_embedded_browser(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin")
		method = next(node for node in pluginClass.body if isinstance(node, ast.FunctionDef) and node.name == "_eventUsesConversationBuffer")
		namespace = {
			"_isChatGPTObject": lambda obj: True,
			"_isConversationObject": lambda obj: bool(getattr(obj, "conversation", False)),
			"_isCodexPromptObject": lambda obj: bool(getattr(obj, "prompt", False)),
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		currentBuffer = object()
		subject = type("Subject", (), {"_buffer": currentBuffer})()
		rebuiltConversation = type(
			"Object", (), {"conversation": True, "prompt": False, "treeInterceptor": object(), "parent": None},
		)()
		embeddedBrowser = type(
			"Object", (), {"conversation": False, "prompt": False, "treeInterceptor": object(), "parent": None},
		)()
		self.assertTrue(namespace["_eventUsesConversationBuffer"](subject, rebuiltConversation))
		self.assertFalse(namespace["_eventUsesConversationBuffer"](subject, embeddedBrowser))

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

	def test_usage_limit_notice_uses_the_observed_error_and_rejects_settings_text(self):
		observed = (
			"You've hit your usage limit. Upgrade to Pro "
			"(https://chatgpt.com/explore/pro), visit "
			"https://chatgpt.com/codex/settings/usage to purchase more credits "
			"or try again at 9:45 PM."
		)
		self.assertEqual(
			"Usage limit reached. You can upgrade to Pro, purchase more credits in "
			"ChatGPT usage settings, or try again at 9:45 PM.",
			usageLimitNotice(observed),
		)
		self.assertEqual(
			"Usage limit reached. You can try again in 12 minutes.",
			usageLimitNotice("You have reached your weekly usage limit. Try again in 12 minutes."),
		)
		self.assertEqual(
			"Usage limit reached. Check ChatGPT usage settings for reset details.",
			usageLimitNotice("Not enough credits"),
		)
		percentageBanner = (
			"0% usage remainingDismiss usage alert Resets every week · "
			"Next reset is on Sep 10 at 5:25 PM Usage consumed Add credits Upgrade"
		)
		self.assertEqual(
			"Usage limit reached. You can upgrade your plan, purchase more credits in "
			"ChatGPT usage settings, or try again on Sep 10 at 5:25 PM.",
			usageLimitNotice(percentageBanner),
		)
		self.assertEqual(
			"Usage limit reached. You can purchase more credits in ChatGPT usage settings.",
			usageLimitNotice("100% usage consumed. Add credits"),
		)
		self.assertEqual("", usageLimitNotice(percentageBanner.replace("0%", "6%")))
		self.assertEqual("", usageLimitNotice("Open usage limits and credits settings"))
		self.assertEqual("", usageLimitNotice("Usage remaining: 20 percent"))
		self.assertEqual(("", ""), statusDetails(observed))
		translationTemplate = TRANSLATION_TEMPLATE_PATH.read_text(encoding="utf-8")
		self.assertIn('msgid "Usage limit reached"', translationTemplate)
		self.assertIn('msgid "purchase more credits in ChatGPT usage settings"', translationTemplate)

	def test_usage_limit_notice_stops_working_feedback_and_is_announced_once(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_applyUsageLimitNotice"
		)

		class Logger:
			def info(self, *args, **kwargs): pass

		class Subject:
			def __init__(self):
				self._pluginProgressOwnedBusy = {"plugin"}
				self._pendingResponseCompletionAt = 12.0
				self._pendingUserMessageIncrease = True
				self._stopControlVisible = True
				self._promptHadText = True
				self._lastScannedLabel = "Working"
				self._lastLabel = "Working"
				self._latestResponseMarker = 123
				self._responseMarkerInitialized = True
				self._busy = True
				self._active = True
				self._activeCategory = "working"
				self._usageLimitActive = False
				self._lastUsageLimitNotice = ""
				self._latestMessage = "Working"
				self._latestFullMessage = "Working"
				self.spoken = []
				self.states = []

			def _setBusy(self, busy, reason):
				self._busy = bool(busy)
				self.states.append((bool(busy), reason))

			def _speakOnce(self, *args, **kwargs):
				self.spoken.append((args, kwargs))

		namespace = {"log": Logger()}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		subject = Subject()
		notice = "Usage limit reached. You can try again at 9:45 PM."
		self.assertTrue(namespace["_applyUsageLimitNotice"](subject, notice))
		self.assertFalse(subject._busy)
		self.assertFalse(subject._active)
		self.assertEqual("attention", subject._activeCategory)
		self.assertEqual(set(), subject._pluginProgressOwnedBusy)
		self.assertEqual(0.0, subject._pendingResponseCompletionAt)
		self.assertFalse(subject._promptHadText)
		self.assertEqual("", subject._lastScannedLabel)
		self.assertEqual("", subject._lastLabel)
		self.assertIsNone(subject._latestResponseMarker)
		self.assertFalse(subject._responseMarkerInitialized)
		self.assertEqual([(False, "usage limit reached")], subject.states)
		self.assertEqual(1, len(subject.spoken))
		self.assertEqual("urgent", subject.spoken[0][1]["priority"])
		self.assertTrue(namespace["_applyUsageLimitNotice"](subject, notice))
		self.assertEqual(1, len(subject.spoken))

	def test_split_usage_limit_popover_is_bounded_and_unrelated_events_are_local(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		methods = [
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name in {
				"_usageLimitTextFromObject", "_usageLimitObjectIsPopup", "_announceUsageLimit",
			}
		]
		namespace = {
			"_isChatGPTObject": lambda obj: True,
			"_roleName": lambda obj: obj.role,
			"re": re,
			"usageLimitNotice": usageLimitNotice,
			"_": lambda text: text,
		}
		exec(compile(ast.Module(body=methods, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)

		class Object:
			def __init__(self, name="", role="section", parent=None):
				self.name = name
				self.value = ""
				self.description = ""
				self.role = role
				self.parent = parent
				self.firstChild = None
				self.next = None

		dialog = Object(role="dialog")
		message = Object("You've hit your usage limit.", parent=dialog)
		upgrade = Object("Upgrade to Pro", role="button", parent=dialog)
		credits = Object("Purchase more credits", role="button", parent=dialog)
		retry = Object("Try again at 9:45 PM.", parent=dialog)
		dialog.firstChild = message
		message.next = upgrade
		upgrade.next = credits
		credits.next = retry

		class Subject:
			def __init__(self):
				self.notices = []

			def _usageLimitTextFromObject(self, obj):
				return namespace["_usageLimitTextFromObject"](self, obj)

			def _usageLimitObjectIsPopup(self, obj):
				return namespace["_usageLimitObjectIsPopup"](self, obj)

			def _applyUsageLimitNotice(self, notice):
				self.notices.append(notice)
				return True

		subject = Subject()
		self.assertTrue(namespace["_announceUsageLimit"](subject, message))
		self.assertEqual(
			"Usage limit reached. You can upgrade to Pro, purchase more credits in "
			"ChatGPT usage settings, or try again at 9:45 PM.",
			subject.notices[0],
		)

		percentageDialog = Object(role="dialog")
		remaining = Object("0% usage remaining", parent=percentageDialog)
		reset = Object("Next reset is on Sep 10 at 5:25 PM", parent=percentageDialog)
		addCredits = Object("Add credits", role="button", parent=percentageDialog)
		upgradePlan = Object("Upgrade", role="button", parent=percentageDialog)
		percentageDialog.firstChild = remaining
		remaining.next = reset
		reset.next = addCredits
		addCredits.next = upgradePlan
		percentageSubject = Subject()
		self.assertTrue(namespace["_announceUsageLimit"](percentageSubject, addCredits))
		self.assertEqual(
			"Usage limit reached. You can upgrade your plan, purchase more credits in "
			"ChatGPT usage settings, or try again on Sep 10 at 5:25 PM.",
			percentageSubject.notices[0],
		)

		class LocalOnlySubject(Subject):
			def _usageLimitTextFromObject(self, obj):
				raise AssertionError("unrelated events must not walk ancestors")

		self.assertFalse(namespace["_announceUsageLimit"](LocalOnlySubject(), Object("Working")))

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
		self.assertEqual(
			"ChatGPT is still thinking, 12 seconds",
			currentActivitySummary(True, "thinking", "", 12, agentName="ChatGPT"),
		)

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
		self.assertTrue(looksLikeCodexConversation("Message ChatGPT"))
		self.assertTrue(looksLikeCodexConversation("Send a message"))
		self.assertFalse(looksLikeCodexConversation("Settings Account Archived chats"))

	def test_blank_chat_detection_ignores_existing_conversation_buffer_refreshes(self):
		self.assertTrue(looksLikeBlankCodexConversation("Main landmark Do anything New chat"))
		self.assertFalse(looksLikeBlankCodexConversation("Do anything User message 3 Response complete: done"))
		self.assertFalse(looksLikeBlankCodexConversation("Do anything ChatGPT said: existing answer"))
		self.assertFalse(looksLikeBlankCodexConversation("Settings General Archived chats"))

	def test_chat_history_snapshot_requires_settle_and_confirmation(self):
		self.assertEqual(
			"settle",
			chatHistorySnapshotDecision(0.1, 0.75, ("Chat",), (), False, None, 0.0, 0.25),
		)
		self.assertEqual(
			"otherMode",
			chatHistorySnapshotDecision(1.0, 0.75, ("Chat",), ("Chat",), True, None, 0.0, 0.25),
		)
		self.assertEqual(
			"confirm",
			chatHistorySnapshotDecision(1.0, 0.75, ("Chat",), (), False, None, 0.0, 0.25),
		)
		self.assertEqual(
			"confirm",
			chatHistorySnapshotDecision(1.0, 0.75, ("Chat",), (), False, ("Chat",), 0.1, 0.25),
		)
		self.assertEqual(
			"publish",
			chatHistorySnapshotDecision(1.0, 0.75, ("Chat",), (), False, ("Chat",), 0.3, 0.25),
		)

	def test_unified_recents_are_partitioned_by_active_codex_titles(self):
		unified = ("ChatGPT only", "Shared title", "Another Codex task")
		codex = (" shared   title ", "Another Codex task")
		self.assertEqual(
			("ChatGPT only",),
			modeSpecificRecentChatTitles("chatgpt", unified, codex),
		)
		self.assertEqual(
			("Shared title", "Another Codex task"),
			modeSpecificRecentChatTitles("codex", unified, codex),
		)
		self.assertEqual((), modeSpecificRecentChatTitles("unknown", unified, codex))

	def test_history_mode_uia_probe_runs_off_main_thread_and_applies_exact_button(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		methods = [
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name in {
				"_queueConversationModeProbe", "_completeConversationModeProbe", "_setConversationMode",
			}
		]
		conditionCalls = []
		scheduled = []
		class Control:
			CurrentName = "Switch mode, current mode: Codex"
		class Root:
			def FindFirst(self, scope, condition):
				self.scope = scope
				self.condition = condition
				return Control()
		class Client:
			def ElementFromHandleBuildCache(self, handle, cache):
				self.handle = handle
				return Root()
			def createPropertyCondition(self, propertyId, value):
				conditionCalls.append((propertyId, value))
				return (propertyId, value)
			def createOrConditionFromArray(self, conditions): return ("or", tuple(conditions))
			def createAndConditionFromArray(self, conditions): return ("and", tuple(conditions))
		client = Client()
		workerCallbacks = []
		class WorkerQueue:
			def put_nowait(self, callback): workerCallbacks.append(callback)
		fakeUIAHandler = type("UIAHandler", (), {
			"handler": type("Handler", (), {
				"clientObject": client,
				"baseCacheRequest": object(),
				"MTAThreadQueue": WorkerQueue(),
			})(),
			"UIA_NamePropertyId": 1,
			"UIA_ControlTypePropertyId": 2,
			"UIA_ButtonControlTypeId": 3,
			"TreeScope_Descendants": 4,
		})
		namespace = {
			"conversationModeFromSwitchLabel": conversationModeFromSwitchLabel,
			"time": type("Time", (), {"monotonic": staticmethod(lambda: 100.0)}),
			"queueHandler": type("QueueHandler", (), {
				"eventQueue": object(),
				"queueFunction": staticmethod(lambda queue, function, *args: function(*args)),
			}),
			"log": type("Log", (), {
				"debug": staticmethod(lambda *args, **kwargs: None),
				"debugWarning": staticmethod(lambda *args, **kwargs: None),
			}),
			"_activePluginInstance": None,
		}
		exec(compile(ast.Module(body=methods, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class Subject:
			_conversationModeProbeGeneration = 0
			_conversationModeProbePendingGeneration = 0
			_conversationWindowHandle = 1234
			_lastConversationModeProbeAt = 0.0
			_conversationMode = "chatgpt"
			_conversationModeObserved = False
			def _completeConversationModeProbe(self, *args):
				return namespace["_completeConversationModeProbe"](self, *args)
			def _setConversationMode(self, mode, reason, authoritative=False):
				changed = mode != self._conversationMode
				self._conversationMode = mode
				self._conversationModeObserved = self._conversationModeObserved or authoritative
				return changed
			def _schedulePoll(self, delay=150, requestInspection=True):
				scheduled.append((delay, requestInspection))
		subject = Subject()
		namespace["_activePluginInstance"] = subject
		previousUIAHandler = sys.modules.get("UIAHandler")
		sys.modules["UIAHandler"] = fakeUIAHandler
		try:
			self.assertTrue(namespace["_queueConversationModeProbe"](subject, "test verification"))
			self.assertEqual("chatgpt", subject._conversationMode)
			self.assertFalse(subject._conversationModeObserved)
			self.assertNotEqual(0, subject._conversationModeProbePendingGeneration)
			self.assertEqual(1, len(workerCallbacks))
			workerCallbacks.pop()()
		finally:
			if previousUIAHandler is None:
				del sys.modules["UIAHandler"]
			else:
				sys.modules["UIAHandler"] = previousUIAHandler
		self.assertEqual("codex", subject._conversationMode)
		self.assertTrue(subject._conversationModeObserved)
		self.assertEqual([(50, True)], scheduled)
		self.assertIn((1, "Switch mode, current mode: ChatGPT"), conditionCalls)
		self.assertIn((1, "Switch mode, current mode: Codex"), conditionCalls)
		self.assertIn((2, 3), conditionCalls)
		lateResultSubject = type("LateResultSubject", (), {
			"_conversationMode": "codex",
			"_conversationModeObserved": False,
			"_conversationModeProbeGeneration": 7,
			"_conversationModeProbePendingGeneration": 7,
		})()
		self.assertFalse(namespace["_setConversationMode"](
			lateResultSubject, "codex", "exact event", authoritative=True,
		))
		self.assertTrue(lateResultSubject._conversationModeObserved)
		self.assertEqual(0, lateResultSubject._conversationModeProbePendingGeneration)
		self.assertEqual(8, lateResultSubject._conversationModeProbeGeneration)

		pluginSource = PLUGIN_PATH.read_text(encoding="utf-8")
		self.assertIn('self._queueConversationModeProbe("history mode verification")', pluginSource)
		self.assertIn('self._queueConversationModeProbe("mode switch UI Automation retry")', pluginSource)
		self.assertIn('self._observeConversationModeControl(obj, "mode switch show event")', pluginSource)
		self.assertIn('self._observeConversationModeControl(obj, "mode switch state event")', pluginSource)

	def test_buffer_backend_refresh_preserves_task_state_but_blank_chat_resets_it(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		methods = [
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name in ("_setConversationMode", "_rememberBuffer")
		]
		method = next(node for node in methods if node.name == "_rememberBuffer")
		methodSource = ast.get_source_segment(PLUGIN_PATH.read_text(encoding="utf-8"), method)
		self.assertIn("POSITION_LAST", methodSource)
		self.assertIn("-BUFFER_TAIL_SCAN_CHARACTERS", methodSource)
		self.assertNotIn("POSITION_ALL", methodSource)
		class TextInfo:
			def __init__(self, text): self.text = text
			def move(self, unit, count, endPoint=None): return max(-len(self.text), count)
		class Buffer:
			def __init__(self, text): self.text = text
			def makeTextInfo(self, position): return TextInfo(self.text)
		class Subject:
			def __init__(self, oldBuffer):
				self._buffer = oldBuffer
				self._conversationMode = "chatgpt"
				self._conversationModeObserved = False
				self._conversationModeChangedAt = 0.0
				self._conversationWindowHandle = 1234
				self._chatHistoryCacheCurrent = {"chatgpt": False, "codex": False}
				self._pendingChatHistorySnapshots = {"chatgpt": None, "codex": None}
				self._pendingChatHistorySnapshotAt = {"chatgpt": 0.0, "codex": 0.0}
				self._chatHistoryMoreAvailable = {"chatgpt": False, "codex": False}
				self._recentHistoryShowMoreOrdinals = {"chatgpt": 0, "codex": 0}
				self._unifiedRecentCounts = {"chatgpt": 0, "codex": 0}
				self._chatHistoryScanGenerations = {"chatgpt": 0, "codex": 0}
				self._pendingChatHistoryAction = None
				self._chatHistoryActionTimer = None
				self._chatHistoryDialog = None
				self._pendingOpenedChatTitle = ""
				self._pendingOpenedChatAt = 0.0
				self._documentSwitchCount = 2
				self._monitoringAnnounced = True
				self._latestMessage = self._latestFullMessage = "Running command"
				self.resets = []
				self.spoken = []
			def _bufferCandidates(self, obj): return getattr(obj, "candidates", (obj,))
			def _conversationWindowHandleFrom(self, obj, buffer): return 1234
			def _queueConversationModeProbe(self, reason): return False
			def _setConversationMode(self, mode, reason, authoritative=False):
				return namespace["_setConversationMode"](self, mode, reason, authoritative)
			def _resetTaskState(self, reason): self.resets.append(reason)
			def _cancelChatHistoryExpansion(self): pass
			def _speakOnce(self, message, *args, **kwargs): self.spoken.append(message)
		namespace = {
			"_isChatGPTObject": lambda obj: True, "pendingChatTitle": pendingChatTitle,
			"conversationModeFromSwitchLabel": conversationModeFromSwitchLabel,
			"_isConversationObject": lambda obj: not bool(getattr(obj, "embeddedBrowser", False)),
			"_conversationModeForObject": lambda obj: "" if bool(getattr(obj, "embeddedBrowser", False)) else getattr(obj, "mode", "chatgpt"),
			"_isCodexPromptObject": lambda obj: False,
			"_isEmbeddedBrowserObject": lambda obj: bool(getattr(obj, "embeddedBrowser", False)),
			"looksLikeBlankCodexConversation": looksLikeBlankCodexConversation,
			"BUFFER_TAIL_SCAN_CHARACTERS": 8192,
			"time": type("Time", (), {"monotonic": staticmethod(lambda: 100.0)}),
			"textInfos": type("TextInfos", (), {"POSITION_LAST": object(), "UNIT_CHARACTER": object()}),
			"_": lambda text: text,
			"log": type("Log", (), {"info": lambda *args, **kwargs: None, "debug": lambda *args, **kwargs: None})(),
			"_settings": lambda: {"speech": True, "braille": True}, "_send": lambda *args, **kwargs: None,
		}
		exec(compile(ast.Module(body=methods, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		oldBuffer = Buffer("Do anything ChatGPT said: existing answer")
		refreshedBuffer = Buffer("Do anything User message 2 ChatGPT said: existing answer")
		subject = Subject(oldBuffer)
		browserBuffer = Buffer("Browser content")
		namespace["_rememberBuffer"](subject, type(
			"Object", (), {"treeInterceptor": browserBuffer, "embeddedBrowser": True},
		)())
		self.assertIs(oldBuffer, subject._buffer)
		self.assertEqual([], subject.resets)
		namespace["_rememberBuffer"](subject, type("Object", (), {"treeInterceptor": refreshedBuffer})())
		self.assertIs(refreshedBuffer, subject._buffer)
		self.assertEqual([], subject.resets)
		self.assertEqual([], subject.spoken)
		self.assertEqual(2, subject._documentSwitchCount)
		blankBuffer = Buffer("Main landmark Do anything New chat")
		namespace["_rememberBuffer"](subject, type("Object", (), {"treeInterceptor": blankBuffer})())
		self.assertEqual(["document changed"], subject.resets)
		self.assertEqual(["New chat opened"], subject.spoken)
		self.assertEqual(3, subject._documentSwitchCount)
		longBuffer = Buffer("Main landmark Do anything " + ("response body " * 900))
		longSubject = Subject(refreshedBuffer)
		namespace["_rememberBuffer"](longSubject, type("Object", (), {"treeInterceptor": longBuffer})())
		self.assertEqual([], longSubject.resets)
		self.assertEqual([], longSubject.spoken)
		namespace["_rememberBuffer"](subject, type(
			"Object", (), {"treeInterceptor": blankBuffer, "mode": "codex"},
		)())
		self.assertEqual(["document changed", "conversation mode changed"], subject.resets)
		self.assertEqual("codex", subject._conversationMode)
		namespace["_setConversationMode"](subject, "codex", "mode switch control scan", True)
		namespace["_rememberBuffer"](subject, type(
			"Object", (), {"treeInterceptor": blankBuffer, "mode": "chatgpt", "name": "Do anything"},
		)())
		self.assertEqual("codex", subject._conversationMode)
		self.assertEqual(["document changed", "conversation mode changed"], subject.resets)
		ancestorBuffer = Buffer("Main landmark Ask anything New chat")
		conversationDocument = type(
			"Object", (), {"treeInterceptor": ancestorBuffer, "mode": "chatgpt"},
		)()
		topLevelFocus = type(
			"Object", (), {"treeInterceptor": None, "mode": "", "candidates": ()},
		)()
		topLevelFocus.candidates = (topLevelFocus, conversationDocument)
		freshSubject = Subject(None)
		namespace["_rememberBuffer"](freshSubject, topLevelFocus)
		self.assertIs(ancestorBuffer, freshSubject._buffer)
		self.assertEqual("chatgpt", freshSubject._conversationMode)

	def test_chat_history_caches_are_isolated_by_conversation_mode(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		methods = [
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name in {
				"_chatHistoryTitles", "_cacheChatHistoryScan", "_loadArchivedChatHistory",
			}
		]
		namespace = {
			"Path": type("UnexpectedPath", (), {
				"home": staticmethod(lambda: (_ for _ in ()).throw(AssertionError("ChatGPT read Codex files"))),
			}),
			"os": type("Os", (), {"environ": {}}),
			"uniqueThreadLabels": uniqueThreadLabels,
			"loadArchivedThreads": loadArchivedThreads,
			"log": type("Log", (), {
				"info": lambda *args, **kwargs: None,
				"debugWarning": lambda *args, **kwargs: None,
			})(),
		}
		exec(compile(ast.Module(body=methods, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class Subject:
			_conversationMode = "chatgpt"
			_chatHistoryCacheCurrent = {"chatgpt": True, "codex": True}
			_chatHistoryCaches = {
				"chatgpt": ("ChatGPT recent",),
				"codex": ("Codex recent",),
			}
			_archivedChatHistoryCaches = {
				"chatgpt": ("ChatGPT archived",),
				"codex": ("Codex archived",),
			}
			_archivedChatHistoryLoaded = {"chatgpt": True, "codex": True}
			_archivedChatIds = {"chatgpt": {}, "codex": {"Codex archived": "thread-id"}}
		subject = Subject()
		subject._chatHistoryTitles = lambda mode=None: namespace["_chatHistoryTitles"](subject, mode)
		subject._cacheChatHistoryScan = lambda mode, recentTitles=None, archivedTitles=None: namespace[
			"_cacheChatHistoryScan"
		](subject, mode, recentTitles, archivedTitles)
		self.assertEqual(("ChatGPT recent",), subject._chatHistoryTitles("chatgpt"))
		self.assertEqual(("Codex recent",), subject._chatHistoryTitles("codex"))
		self.assertEqual(
			(("ChatGPT archived",), True),
			namespace["_loadArchivedChatHistory"](subject, "chatgpt"),
		)
		subject._cacheChatHistoryScan("chatgpt", ("New ChatGPT recent",), ())
		self.assertEqual(("New ChatGPT recent",), subject._chatHistoryTitles("chatgpt"))
		self.assertEqual((), subject._archivedChatHistoryCaches["chatgpt"])
		self.assertEqual(("Codex recent",), subject._chatHistoryTitles("codex"))
		self.assertEqual(("Codex archived",), subject._archivedChatHistoryCaches["codex"])
		dialogSource = CHAT_DIALOG_PATH.read_text(encoding="utf-8")
		self.assertIn('title=_("{agent} chat history").format(agent=agentName)', dialogSource)
		self.assertIn('selection[1], self._mode)', dialogSource)
		self.assertNotIn('title=_("Codex chat history")', dialogSource)
		pluginSource = PLUGIN_PATH.read_text(encoding="utf-8")
		self.assertIn('if source == "archived" and mode == "codex":', pluginSource)
		self.assertIn('if mode != self._conversationMode:', pluginSource)
		self.assertIn("CHAT_HISTORY_MODE_SETTLE_SECONDS = 0.75", pluginSource)
		self.assertIn("if not self._chatHistoryCacheCurrent.get(mode, False):", pluginSource)
		self.assertIn("CHAT_HISTORY_EXPANSION_MAX_PAGES = 20", pluginSource)
		self.assertIn("button = self._recentHistoryShowMoreButton(mode)", pluginSource)
		self.assertIn("button.doAction()", pluginSource)
		self.assertIn("self._showChatHistoryDialog(mode)", pluginSource)

	def test_chat_history_scan_stops_before_transcript_controls(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_latestButtonStatus"
		)
		class Role:
			BUTTON = "button"
			LANDMARK = "landmark"
		class Command:
			def __init__(self, command, role=None, name="", landmark=""):
				self.command = command
				self.field = {"role": role, "name": name, "landmark": landmark}
		class Info:
			def getTextWithFields(self):
				return (
					Command("controlStart", Role.BUTTON, "Switch mode, current mode: Codex"),
					"Codex",
					Command("controlEnd"),
					Command("controlStart", Role.BUTTON, "Show more"),
					"Show more",
					Command("controlEnd"),
					"Recents",
					Command("controlStart", Role.BUTTON, "Real chat title"),
					"Real chat title",
					Command("controlEnd"),
					Command("controlStart", Role.BUTTON, "Real chat title"),
					"Real chat title",
					Command("controlEnd"),
					Command("controlStart", Role.BUTTON, "Show more"),
					"Show more",
					Command("controlEnd"),
					"6% usage remaining",
					Command("controlStart", Role.BUTTON, "Account action from usage pop-over"),
					"Account action from usage pop-over",
					Command("controlEnd"),
					Command("controlStart", Role.BUTTON, "Add credits"),
					"Add credits",
					Command("controlEnd"),
					Command("controlStart", Role.BUTTON, "Update"),
					"Update",
					Command("controlEnd"),
					Command("controlStart", Role.BUTTON, "Jump to user message 1"),
					Command("controlEnd"),
					"Recents",
					Command("controlStart", Role.BUTTON, "Sources"),
					"SourcesWikipediaExample source",
					Command("controlEnd"),
					Command("controlStart", Role.BUTTON, "Copy response"),
					Command("controlEnd"),
					"Response complete",
				)
		cached = []
		scheduled = []
		class Time:
			now = 100.0
			@classmethod
			def monotonic(cls): return cls.now
		namespace = {
			"Role": Role,
			"conversationModeFromSwitchLabel": conversationModeFromSwitchLabel,
			"chatHistorySnapshotDecision": chatHistorySnapshotDecision,
			"CHAT_HISTORY_MODE_SETTLE_SECONDS": 0.75,
			"CHAT_HISTORY_SNAPSHOT_CONFIRM_SECONDS": 0.25,
			"CHAT_HISTORY_RETRY_MILLISECONDS": 300,
			"time": Time,
			"re": re,
			"log": type("Log", (), {"debug": lambda *args, **kwargs: None})(),
			"isChatHistoryConversationBoundary": isChatHistoryConversationBoundary,
			"isChatHistoryInterfaceText": isChatHistoryInterfaceText,
			"isStopControlLabel": isStopControlLabel,
			"userMessageNumber": userMessageNumber,
			"firstStatusLabel": firstStatusLabel,
			"isKnownNonStatusButton": isKnownNonStatusButton,
			"usageLimitNotice": usageLimitNotice,
			"_": lambda text: text,
			"_settings": lambda: {"diagnosticLogging": False},
			"userMessageSubmissionTransition": userMessageSubmissionTransition,
			"confirmedUserMessageSubmission": confirmedUserMessageSubmission,
			"stopControlTransition": stopControlTransition,
			"isResponseCompletionMarkerText": isResponseCompletionMarkerText,
			"responseCompletionScanMarker": responseCompletionScanMarker,
			"responseCompletionTransition": responseCompletionTransition,
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class Subject:
			_conversationMode = "chatgpt"
			_conversationModeObserved = False
			_conversationModeChangedAt = 0.0
			_chatHistoryCaches = {"chatgpt": (), "codex": ()}
			_chatHistoryCacheCurrent = {"chatgpt": False, "codex": False}
			_pendingChatHistorySnapshots = {"chatgpt": None, "codex": None}
			_pendingChatHistorySnapshotAt = {"chatgpt": 0.0, "codex": 0.0}
			_chatHistoryMoreAvailable = {"chatgpt": False, "codex": False}
			_recentHistoryShowMoreOrdinals = {"chatgpt": 0, "codex": 0}
			_unifiedRecentCounts = {"chatgpt": 0, "codex": 0}
			_chatHistoryScanGenerations = {"chatgpt": 0, "codex": 0}
			_lastUnknownButtons = ()
			_lastUnknownButtonsAt = 0.0
			_latestUserMessageNumber = None
			_pendingUserMessageIncrease = False
			_promptHadText = False
			_busy = False
			_stopControlVisible = False
			_latestResponseMarker = None
			_responseMarkerInitialized = False
			def _setConversationMode(self, mode, reason, authoritative=False):
				if mode != self._conversationMode:
					self._conversationModeChangedAt = Time.monotonic()
					self._chatHistoryCacheCurrent[mode] = False
					self._pendingChatHistorySnapshots[mode] = None
					self._pendingChatHistorySnapshotAt[mode] = 0.0
				self._conversationMode = mode
				self._conversationModeObserved = self._conversationModeObserved or authoritative
				return True
			def _schedulePoll(self, delay=150, requestInspection=True):
				scheduled.append((delay, requestInspection))
			def _cacheChatHistoryScan(self, mode, recentTitles=None, archivedTitles=None):
				cached.append((mode, recentTitles, archivedTitles))
			def _modeSpecificRecentChatTitles(self, mode, titles):
				return modeSpecificRecentChatTitles(mode, titles, ("Real chat title",))
			def _beginPromptSubmission(self, reason):
				raise AssertionError(reason)
			def _setBusy(self, busy, reason):
				raise AssertionError(reason)
			def _queueResponseCompletion(self):
				raise AssertionError("unexpected completion")
			def _applyUsageLimitNotice(self, notice):
				self.limitNotices.append(notice)
				self._busy = False
				return True
		subject = Subject()
		subject.limitNotices = []
		namespace["_latestButtonStatus"](subject, Info())
		self.assertEqual((1, None), subject._latestResponseMarker)
		self.assertTrue(subject._responseMarkerInitialized)
		self.assertEqual([], cached)
		self.assertEqual(1, len(scheduled))
		self.assertTrue(scheduled[0][1])
		Time.now = 101.0
		namespace["_latestButtonStatus"](subject, Info())
		self.assertEqual([], cached)
		self.assertEqual(2, len(scheduled))
		Time.now = 101.3
		namespace["_latestButtonStatus"](subject, Info())
		self.assertEqual([("codex", ("Real chat title",), None)], cached)
		self.assertTrue(subject._conversationModeObserved)
		self.assertTrue(subject._chatHistoryMoreAvailable["codex"])
		self.assertEqual(2, subject._recentHistoryShowMoreOrdinals["codex"])
		self.assertEqual(2, subject._unifiedRecentCounts["codex"])
		class LimitInfo(Info):
			def getTextWithFields(self):
				return tuple(
					(
						"0% usage remainingDismiss usage alert Resets every week · "
						"Next reset is on Sep 10 at 5:25 PM Usage consumed"
					) if item == "6% usage remaining" else item
					for item in super().getTextWithFields()
				)
		subject._busy = True
		self.assertEqual("", namespace["_latestButtonStatus"](subject, LimitInfo()))
		self.assertFalse(subject._busy)
		self.assertEqual(
			[
				"Usage limit reached. You can purchase more credits in ChatGPT usage settings "
				"or try again on Sep 10 at 5:25 PM."
			],
			subject.limitNotices,
		)

	def test_exact_named_button_resolver_honors_the_scanned_ordinal(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_exactNamedButtonObject"
		)
		class Role:
			BUTTON = "button"
		class Button:
			role = Role.BUTTON
			windowHandle = 99
			IA2UniqueID = 0
			def __init__(self, name): self.name = name
		class Child:
			role = "text"
			def __init__(self, parent): self.parent = parent
		first = Button("Show more")
		notExact = Button("Show more results")
		second = Button("Show more")
		class Info:
			def __init__(self):
				self.matches = (Child(first), Child(notExact), Child(second))
				self.index = -1
				self.NVDAObjectAtStart = None
			def find(self, text, reverse=False, caseSensitive=False):
				self.index += 1
				if self.index >= len(self.matches):
					return False
				self.NVDAObjectAtStart = self.matches[self.index]
				return True
			def collapse(self, end=False): pass
			def move(self, unit, count): return 1 if self.index < len(self.matches) - 1 else 0
		class Buffer:
			def makeTextInfo(self, position): return Info()
		namespace = {
			"Role": Role,
			"textInfos": type("TextInfos", (), {"POSITION_FIRST": object(), "UNIT_CHARACTER": object()}),
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		subject = type("Subject", (), {"_buffer": Buffer()})()
		self.assertIs(second, namespace["_exactNamedButtonObject"](subject, "Show more", 2))
		self.assertIsNone(namespace["_exactNamedButtonObject"](subject, "Show more", 3))

	def test_recent_history_expansion_waits_for_growth_and_is_bounded(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_continueChatHistoryExpansion"
		)
		messages = []
		class Api:
			focus = "chatgpt"
			@classmethod
			def getFocusObject(cls): return cls.focus
		class Button:
			def __init__(self): self.actions = 0
			def doAction(self): self.actions += 1
		class Subject:
			def __init__(self, pages=0, more=True, cacheCurrent=True, button=True):
				self._chatHistoryExpansionTimer = object()
				self._pendingChatHistoryExpansion = {
					"mode": "chatgpt", "pages": pages, "lastCount": 10,
					"lastGeneration": 1, "awaitingGrowth": False,
					"staleScans": 0, "settleScans": 0,
				}
				self._conversationMode = "chatgpt"
				self._buffer = object()
				self._unifiedRecentCounts = {"chatgpt": 10, "codex": 0}
				self._chatHistoryScanGenerations = {"chatgpt": 1, "codex": 0}
				self._chatHistoryMoreAvailable = {"chatgpt": more, "codex": False}
				self._recentHistoryShowMoreOrdinals = {"chatgpt": 1, "codex": 0}
				self._chatHistoryCacheCurrent = {"chatgpt": cacheCurrent, "codex": False}
				self._pendingChatHistorySnapshots = {"chatgpt": ("old",), "codex": None}
				self._pendingChatHistorySnapshotAt = {"chatgpt": 1.0, "codex": 0.0}
				self._bufferDirty = False
				self.button = Button() if button else None
				self.expansionSchedules = []
				self.pollSchedules = []
				self.finished = []
				self.cancelled = 0
			def _cancelChatHistoryExpansion(self):
				self.cancelled += 1
				self._pendingChatHistoryExpansion = None
			def _finishChatHistoryExpansion(self, mode, limitReached=False, failed=False):
				self.finished.append((mode, limitReached, failed))
			def _scheduleChatHistoryExpansion(self, delay): self.expansionSchedules.append(delay)
			def _schedulePoll(self, delay=150, requestInspection=True):
				self.pollSchedules.append((delay, requestInspection))
			def _recentHistoryShowMoreButton(self, mode): return self.button
		namespace = {
			"api": Api,
			"_isChatGPTObject": lambda obj: obj == "chatgpt",
			"_": lambda text: text,
			"ui": type("Ui", (), {"message": staticmethod(messages.append)}),
			"log": type("Log", (), {
				"info": staticmethod(lambda *args, **kwargs: None),
				"debugWarning": staticmethod(lambda *args, **kwargs: None),
			}),
			"CHAT_HISTORY_EXPANSION_MAX_PAGES": 20,
			"CHAT_HISTORY_EXPANSION_MAX_STALE_SCANS": 30,
			"CHAT_HISTORY_EXPANSION_RETRY_MILLISECONDS": 300,
			"CHAT_HISTORY_EXPANSION_DELAY_MILLISECONDS": 700,
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		continueExpansion = namespace["_continueChatHistoryExpansion"]

		subject = Subject()
		continueExpansion(subject)
		self.assertEqual(1, subject.button.actions)
		self.assertEqual(1, subject._pendingChatHistoryExpansion["pages"])
		self.assertTrue(subject._pendingChatHistoryExpansion["awaitingGrowth"])
		self.assertFalse(subject._chatHistoryCacheCurrent["chatgpt"])
		self.assertEqual([(150, True)], subject.pollSchedules)
		self.assertEqual([700], subject.expansionSchedules)

		continueExpansion(subject)
		self.assertEqual(1, subject.button.actions)
		self.assertEqual(1, subject._pendingChatHistoryExpansion["staleScans"])
		self.assertEqual(300, subject.expansionSchedules[-1])

		subject._unifiedRecentCounts["chatgpt"] = 20
		subject._chatHistoryScanGenerations["chatgpt"] = 2
		subject._chatHistoryMoreAvailable["chatgpt"] = False
		continueExpansion(subject)
		self.assertEqual([], subject.finished)
		self.assertEqual(1, subject._pendingChatHistoryExpansion["settleScans"])
		subject._chatHistoryCacheCurrent["chatgpt"] = True
		continueExpansion(subject)
		self.assertEqual([("chatgpt", False, False)], subject.finished)

		limited = Subject(pages=20, more=True, cacheCurrent=True)
		continueExpansion(limited)
		self.assertEqual([("chatgpt", True, False)], limited.finished)
		self.assertEqual(0, limited.button.actions)

		missing = Subject(button=False)
		continueExpansion(missing)
		self.assertEqual([("chatgpt", False, True)], missing.finished)

		stalled = Subject()
		continueExpansion(stalled)
		for generation in range(2, 33):
			stalled._chatHistoryScanGenerations["chatgpt"] = generation
			continueExpansion(stalled)
		self.assertEqual([("chatgpt", False, True)], stalled.finished)
		self.assertEqual(1, stalled.button.actions)

		focusLost = Subject()
		Api.focus = "other"
		continueExpansion(focusLost)
		self.assertEqual(1, focusLost.cancelled)
		self.assertIn("Recent chat history loading stopped because ChatGPT is no longer focused", messages)
		Api.focus = "chatgpt"

	def test_chatgpt_archived_action_never_uses_a_codex_thread_id(self):
		pluginTree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in pluginTree.body if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_performChatHistoryAction"
		)
		messages = []
		namespace = {
			"_": lambda text: text,
			"codexThreadUrl": lambda threadId: (_ for _ in ()).throw(
				AssertionError("ChatGPT archived history used a Codex thread ID")
			),
			"time": type("Time", (), {"monotonic": staticmethod(lambda: 10.0)}),
			"wx": type("Wx", (), {"LaunchDefaultBrowser": staticmethod(lambda url: True)}),
			"ui": type("Ui", (), {"message": staticmethod(messages.append)}),
			"log": type("Log", (), {
				"info": lambda *args, **kwargs: None,
				"debugWarning": lambda *args, **kwargs: None,
			})(),
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		class Button:
			def __init__(self): self.actions = 0
			def doAction(self): self.actions += 1
		button = Button()
		class Subject:
			_conversationMode = "chatgpt"
			_archivedChatIds = {"chatgpt": {}, "codex": {}}
			_pendingOpenedChatTitle = ""
			_pendingOpenedChatAt = 0.0
			def _chatButtonObject(self, title): return button
			def _startDirectChatAction(self, title, action): raise AssertionError(action)
			def _scheduleUnarchiveButtonFocus(self): raise AssertionError("Codex-only action")
		subject = Subject()
		namespace["_performChatHistoryAction"](
			subject, "ChatGPT archived", "open", "archived", "chatgpt",
		)
		self.assertEqual(1, button.actions)
		self.assertEqual("ChatGPT archived", subject._pendingOpenedChatTitle)
		namespace["_performChatHistoryAction"](
			subject, "Codex archived", "open", "archived", "codex",
		)
		self.assertEqual(1, button.actions)
		self.assertEqual(["The chat-history mode changed. Open chat history again"], messages)

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

	def test_active_codex_titles_deduplicate_index_and_exclude_archived_tasks(self):
		with tempfile.TemporaryDirectory() as directory:
			codexRoot = Path(directory)
			archiveDirectory = codexRoot / "archived_sessions"
			archiveDirectory.mkdir()
			activeId = "00000000-0000-0000-0000-000000000001"
			archivedId = "00000000-0000-0000-0000-000000000002"
			otherId = "00000000-0000-0000-0000-000000000003"
			(archiveDirectory / f"rollout-archived-{archivedId}.jsonl").write_text(
				"{}\n", encoding="utf-8",
			)
			(codexRoot / "session_index.jsonl").write_text(
				json.dumps({"id": activeId, "thread_name": "Old name", "updated_at": "2026-01-01"}) + "\n" +
				json.dumps({"id": archivedId, "thread_name": "Archived", "updated_at": "2026-03-01"}) + "\n" +
				json.dumps({"id": activeId, "thread_name": "Current name", "updated_at": "2026-04-01"}) + "\n" +
				json.dumps({"id": otherId, "thread_name": "Other active", "updated_at": "2026-02-01"}) + "\n",
				encoding="utf-8",
			)
			self.assertEqual(
				("Current name", "Other active"),
				loadActiveCodexThreadTitles(codexRoot),
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

	def test_anonymized_chatgpt_accessibility_snapshots(self):
		fixtures = json.loads(ACCESSIBILITY_FIXTURE_PATH.read_text(encoding="utf-8"))
		for snapshot in fixtures["conversationSnapshots"]:
			with self.subTest(snapshot=snapshot["name"]):
				self.assertEqual(
					tuple(tuple(item) for item in snapshot["expected"]),
					chatMessagesFromTokens(tuple(tuple(item) for item in snapshot["tokens"])),
				)
		for item in fixtures["promptLabels"]:
			with self.subTest(prompt=item["label"]):
				self.assertEqual(item["expected"], isCodexPromptLabel(item["label"]))
		for item in fixtures["stopControls"]:
			with self.subTest(stop=item["label"]):
				self.assertEqual(item["expected"], isStopControlLabel(item["label"]))
		for item in fixtures["chatActions"]:
			with self.subTest(action=item["label"]):
				self.assertEqual(item["expected"], chatActionMatches(item["action"], item["label"]))
		for item in fixtures["historyInterfaceText"]:
			with self.subTest(historyControl=item["label"]):
				self.assertEqual(item["expected"], isChatHistoryInterfaceText(item["label"]))
		for item in fixtures["permissionText"]:
			with self.subTest(permission=item["label"]):
				self.assertEqual(item["expected"], isPermissionPromptText(item["label"]))
		for item in fixtures["pluginProgress"]:
			expected = tuple(item["expected"]) if item["expected"] is not None else None
			with self.subTest(progress=item["label"]):
				self.assertEqual(expected, pluginInstallProgress(item["label"]))
		for item in fixtures["browserStructures"]:
			with self.subTest(browser=item["name"]):
				self.assertEqual(
					item["expected"], browserAccess.isEmbeddedBrowserDocumentStructure(*item["roles"]),
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

	def test_full_buffer_inspection_is_event_driven_and_typing_safe(self):
		# Dirty events are retained, but no whole-document read may interrupt typing.
		self.assertFalse(bufferInspectionDue(True, 0, False, False, True))
		self.assertTrue(bufferInspectionDue(True, 0, False, False, False))
		# A running task keeps a bounded fallback without scanning twice per second.
		self.assertFalse(bufferInspectionDue(False, 4.9, True, False, False))
		self.assertTrue(bufferInspectionDue(False, 5.0, True, False, False))
		# Prompt typing also suppresses fallback scans.
		self.assertFalse(bufferInspectionDue(False, 100, True, True, True))
		# Idle ChatGPT is event-only whether focused or in the background.
		self.assertFalse(bufferInspectionDue(False, 1000, False, False, False))
		self.assertFalse(bufferInspectionDue(False, 1000, False, True, False))
		self.assertFalse(bufferInspectionDue(False, float("nan"), True, True, False))

	def test_closed_conversation_window_requires_a_confirmed_grace_period(self):
		self.assertFalse(conversationWindowShouldDetach(False, False, False, 10, 2))
		self.assertFalse(conversationWindowShouldDetach(True, None, None, 10, 2))
		self.assertFalse(conversationWindowShouldDetach(True, True, True, 10, 2))
		self.assertFalse(conversationWindowShouldDetach(True, False, False, 1.99, 2))
		self.assertTrue(conversationWindowShouldDetach(True, False, False, 2, 2))
		self.assertTrue(conversationWindowShouldDetach(True, True, False, 2, 2))
		self.assertFalse(conversationWindowShouldDetach(True, False, False, float("nan"), 2))

	def test_runtime_window_close_detaches_stale_conversation_state(self):
		pluginSource = PLUGIN_PATH.read_text(encoding="utf-8")
		pluginTree = ast.parse(pluginSource)
		pluginClass = next(
			node for node in pluginTree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		methods = [
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name in (
				"_conversationWindowHandleFrom", "_detachConversationIfWindowClosed",
			)
		]
		class WinUser:
			GA_ROOT = 2
			exists = True
			visible = True
			@staticmethod
			def getAncestor(handle, relation): return handle + 100
			@classmethod
			def isWindow(cls, handle): return cls.exists
			@classmethod
			def isWindowVisible(cls, handle): return cls.visible
		class Subject:
			_buffer = object()
			_conversationWindowHandle = 110
			_conversationWindowUnavailableAt = 0.0
			_conversationMode = "codex"
			_conversationModeProbeGeneration = 2
			_conversationModeProbePendingGeneration = 2
			_monitoringAnnounced = True
			def __init__(self):
				self.resets = []
				self.scanCancelled = 0
				self._browserActionTimer = None
				self._pendingBrowserAction = object()
				self._browserNavigatorDialog = None
				self._browserNavigatorResult = object()
				self._lastEmbeddedBrowserObject = object()
				self._embeddedBrowserBuffer = object()
				self._embeddedBrowserPageTitle = "Example"
				self._embeddedBrowserAddress = "https://example.com"
				self._embeddedBrowserLoadingPercent = 50
				self._browserSavedLocations = {"page": "item"}
				self._chatHistoryExpansionTimer = None
				self._pendingChatHistoryExpansion = None
			def _resetTaskState(self, reason): self.resets.append(reason)
			def _resetEmbeddedBrowserProgress(self): self._embeddedBrowserLoadingPercent = None
			def _cancelEmbeddedBrowserScan(self): self.scanCancelled += 1
			def _cancelChatHistoryExpansion(self):
				self._chatHistoryExpansionTimer = None
				self._pendingChatHistoryExpansion = None
		namespace = {
			"winUser": WinUser,
			"conversationWindowShouldDetach": conversationWindowShouldDetach,
			"CONVERSATION_WINDOW_CLOSE_GRACE_SECONDS": 2.0,
			"log": type("Log", (), {"info": lambda *args, **kwargs: None})(),
		}
		exec(compile(ast.Module(body=methods, type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)
		subject = Subject()
		obj = type("Object", (), {"windowHandle": 10})()
		self.assertEqual(110, namespace["_conversationWindowHandleFrom"](subject, obj, object()))
		WinUser.visible = False
		self.assertFalse(namespace["_detachConversationIfWindowClosed"](subject, 100.0))
		self.assertFalse(namespace["_detachConversationIfWindowClosed"](subject, 101.99))
		self.assertTrue(namespace["_detachConversationIfWindowClosed"](subject, 102.0))
		self.assertIsNone(subject._buffer)
		self.assertEqual("", subject._conversationMode)
		self.assertEqual(0, subject._conversationModeProbePendingGeneration)
		self.assertFalse(subject._monitoringAnnounced)
		self.assertEqual(1, subject.scanCancelled)
		self.assertIsNone(subject._pendingBrowserAction)
		self.assertIsNone(subject._browserNavigatorResult)
		self.assertIsNone(subject._lastEmbeddedBrowserObject)
		self.assertEqual({}, subject._browserSavedLocations)
		self.assertEqual(["ChatGPT window closed"], subject.resets)

	def test_braille_display_chords_activate_typing_protection(self):
		self.assertTrue(isBrailleTypingGestureIdentifier("br(hims.BrailleSense):dot4+dot2"))
		self.assertTrue(isBrailleTypingGestureIdentifier("br(hims.BrailleSense):space"))
		self.assertTrue(isBrailleTypingGestureIdentifier("br(hims.BrailleSense):dot7"))
		self.assertFalse(isBrailleTypingGestureIdentifier("br(hims.BrailleSense):rightSideScrollDown"))
		self.assertFalse(isBrailleTypingGestureIdentifier("kb(laptop):a"))
		self.assertFalse(brailleTypingGestureCommitsText("br(hims.BrailleSense):dot4+dot2"))
		self.assertTrue(brailleTypingGestureCommitsText("br(hims.BrailleSense):space"))
		self.assertTrue(brailleTypingGestureCommitsText("br(hims.BrailleSense):dot8+dot3+space"))

	def test_delayed_caret_event_preserves_only_an_active_braille_composition(self):
		self.assertTrue(shouldPreserveBrailleComposition(True, True, True, 0.6))
		self.assertTrue(shouldPreserveBrailleComposition(True, True, True, 1.0))
		self.assertFalse(shouldPreserveBrailleComposition(True, True, True, 1.01))
		self.assertFalse(shouldPreserveBrailleComposition(False, True, True, 0.1))
		self.assertFalse(shouldPreserveBrailleComposition(True, False, True, 0.1))
		self.assertFalse(shouldPreserveBrailleComposition(True, True, False, 0.1))
		self.assertFalse(shouldPreserveBrailleComposition(True, True, True, float("nan")))

	def test_runtime_polling_preserves_state_and_coalesces_prompt_reads(self):
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		self.assertIn("self._bufferDirty = False", plugin)
		self.assertIn("self._skippedBufferInspectionCount += 1", plugin)
		self.assertIn("PROMPT_TYPING_QUIET_SECONDS", plugin)
		self.assertIn("RESPONSE_COMPLETION_SETTLE_SECONDS = 5.0", plugin)
		self.assertIn("self._detachConversationIfWindowClosed(now)", plugin)
		self.assertIn("winUser.isWindowVisible(handle)", plugin)
		self.assertEqual(2, plugin.count("if self._pendingResponseCompletionAt:\n\t\t\treturn"))
		self.assertIn("self._schedulePromptInspection(obj)", plugin)
		self.assertIn("self._promptInspectionTimer.Stop()", plugin)
		self.assertIn("inputCore.decide_executeGesture.register(self._observeInputGesture)", plugin)
		self.assertIn("inputCore.decide_executeGesture.unregister(self._observeInputGesture)", plugin)
		self.assertIn("self._brailleCompositionActive", plugin)
		self.assertIn("def event_caret(self, obj, nextHandler):", plugin)
		self.assertIn("shouldPreserveBrailleComposition(", plugin)
		self.assertIn("handler._uncontSentTime = time.time()", plugin)
		self.assertLess(
			plugin.index("from braille import input as brailleInputModule"),
			plugin.index("import brailleInput as brailleInputModule"),
		)
		self.assertNotIn("handlerClass.handleCaretMove =", plugin)
		self.assertIn('getattr(obj, "role", None) == Role.BUTTON', plugin)
		self.assertNotIn('getattr(obj, "role", None) != Role.EDITABLETEXT\n\t\t\t\tand self._eventUsesConversationBuffer(obj)', plugin)
		self.assertIn("preserving task state", plugin)
		self.assertNotIn('self._setBusy(False, "buffer inspection failed")', plugin)
		initializationPrefix = plugin.split("self._promptInspectionTimer = None", 1)[0]
		self.assertNotIn("if self._promptInspectionTimer", initializationPrefix)

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

	def test_prompt_submission_gesture_recognizes_only_unmodified_enter(self):
		for identifier in (
			"kb(laptop):enter", "kb(desktop):enter", "kb:enter",
			"kb(desktop):numpadEnter", "br(hims.BrailleSense):dot8",
		):
			self.assertTrue(isPromptSubmissionGestureIdentifier(identifier), identifier)
		for identifier in (
			"kb(laptop):shift+enter", "kb(laptop):control+enter",
			"br(hims.BrailleSense):dot7+dot8", "br(hims.BrailleSense):space",
			"kb(laptop):a", "enter", "",
		):
			self.assertFalse(isPromptSubmissionGestureIdentifier(identifier), identifier)

	def test_prompt_submission_gesture_requires_focus_mode_and_prompt_text_evidence(self):
		self.assertFalse(promptSubmissionGestureShouldStart(False, True, True))
		self.assertFalse(promptSubmissionGestureShouldStart(True, False, False))
		self.assertFalse(promptSubmissionGestureShouldStart(True, None, False))
		self.assertTrue(promptSubmissionGestureShouldStart(True, True, False))
		self.assertTrue(promptSubmissionGestureShouldStart(True, False, True))

	def test_prompt_enter_observer_queues_feedback_without_claiming_the_gesture(self):
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		observerStart = plugin.index("\tdef _observeInputGesture(self, gesture):")
		observerEnd = plugin.index("\n\tdef event_caret", observerStart)
		observer = plugin[observerStart:observerEnd]
		self.assertIn("isPromptSubmissionGestureIdentifier(identifier)", observer)
		self.assertIn("promptSubmissionGestureShouldStart(", observer)
		self.assertIn('getattr(self._buffer, "passThrough", True)', observer)
		self.assertIn("queueHandler.queueFunction(", observer)
		self.assertIn("queueHandler.eventQueue, self._beginPromptSubmissionFromGesture", observer)
		self.assertIn("self._conversationNavigationUntil", observer)
		self.assertIn("now < self._conversationNavigationUntil", plugin)
		self.assertIn("return True", observer)
		self.assertNotIn("gesture.send", observer)
		self.assertNotIn("raise NoInputGestureAction", observer)

	def test_prompt_enter_observer_ignores_browse_mode_activation_and_empty_focus_mode(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_observeInputGesture"
		)

		class Clock:
			@staticmethod
			def monotonic():
				return 10.0

		class Queue:
			eventQueue = object()
			calls = []

			@staticmethod
			def queueFunction(*args):
				Queue.calls.append(args)

		namespace = {
			"time": Clock,
			"queueHandler": Queue,
			"isPromptSubmissionGestureIdentifier": isPromptSubmissionGestureIdentifier,
			"promptSubmissionGestureShouldStart": promptSubmissionGestureShouldStart,
			"isBrailleTypingGestureIdentifier": isBrailleTypingGestureIdentifier,
			"brailleTypingGestureCommitsText": brailleTypingGestureCommitsText,
			"CONVERSATION_NAVIGATION_QUIET_SECONDS": 3.0,
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)

		class Buffer:
			def __init__(self, passThrough):
				self.passThrough = passThrough

		class Gesture:
			def __init__(self, identifier):
				self.identifiers = (identifier,)

		class Subject:
			_appFocusState = True
			_promptFocused = True
			_promptHadText = False
			_promptTypingUntil = 0.0
			_brailleCompositionActive = False
			_lastBrailleTextInjectionAt = 0.0
			_promptSubmissionGestureQueued = False
			_conversationNavigationUntil = 0.0

			def _beginPromptSubmissionFromGesture(self):
				pass

		subject = Subject()
		subject._buffer = Buffer(False)
		subject._promptHadText = True
		subject._promptTypingUntil = 20.0
		namespace["_observeInputGesture"](subject, Gesture("br(hims.BrailleSense):dot8"))
		self.assertEqual([], Queue.calls)
		self.assertFalse(subject._promptSubmissionGestureQueued)
		self.assertEqual(0.0, subject._promptTypingUntil)

		subject._buffer = Buffer(True)
		subject._promptHadText = False
		namespace["_observeInputGesture"](subject, Gesture("kb(laptop):enter"))
		self.assertEqual([], Queue.calls)

		subject._promptTypingUntil = 20.0
		namespace["_observeInputGesture"](subject, Gesture("br(hims.BrailleSense):dot8"))
		self.assertEqual(1, len(Queue.calls))
		self.assertTrue(subject._promptSubmissionGestureQueued)

		Queue.calls.clear()
		subject._promptSubmissionGestureQueued = False
		subject._buffer = Buffer(False)
		namespace["_observeInputGesture"](subject, Gesture("br(hims.BrailleSense):dot1+dot5"))
		self.assertEqual(0.0, subject._promptTypingUntil)
		self.assertFalse(subject._brailleCompositionActive)

		subject._promptFocused = False
		namespace["_observeInputGesture"](subject, Gesture("br(hims):rightSideScrollDown"))
		self.assertEqual(13.0, subject._conversationNavigationUntil)

	def test_queued_prompt_submission_starts_once_and_ignores_terminated_plugin(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "_beginPromptSubmissionFromGesture"
		)
		namespace = {"_activePluginInstance": None}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)

		class Subject:
			def __init__(self):
				self._promptSubmissionGestureQueued = True
				self._busy = False
				self._promptHadText = True
				self.started = []
				self.polls = []

			def _beginPromptSubmission(self, reason):
				self.started.append(reason)

			def _schedulePoll(self, delay, requestInspection):
				self.polls.append((delay, requestInspection))

		subject = Subject()
		namespace["_beginPromptSubmissionFromGesture"](subject)
		self.assertFalse(subject._promptSubmissionGestureQueued)
		self.assertEqual([], subject.started)
		namespace["_activePluginInstance"] = subject
		subject._promptSubmissionGestureQueued = True
		namespace["_beginPromptSubmissionFromGesture"](subject)
		self.assertFalse(subject._promptHadText)
		self.assertEqual(["unmodified Enter gesture"], subject.started)
		self.assertEqual([(50, True)], subject.polls)
		subject._busy = True
		namespace["_beginPromptSubmissionFromGesture"](subject)
		self.assertEqual(1, len(subject.started))

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
			"Download Codex Status Announcer 2026.2.1",
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

	def test_plain_response_complete_marker_ends_a_busy_submission(self):
		self.assertTrue(isResponseCompletionMarkerText("Response complete"))
		self.assertTrue(isResponseCompletionMarkerText(" Response   complete: finished answer "))
		self.assertFalse(isResponseCompletionMarkerText("Response completing"))
		previous = responseCompletionScanMarker(12)
		current = responseCompletionScanMarker(13)
		marker, initialized, completed = responseCompletionTransition(previous, True, current, True)
		self.assertEqual((current, True, True), (marker, initialized, completed))
		self.assertIsNone(responseCompletionScanMarker(0))

	def test_tentative_response_completion_requires_a_quiet_idle_scan(self):
		self.assertTrue(shouldFinalizeResponseCompletion(True, 30, 30, True, False, ""))
		self.assertTrue(shouldFinalizeResponseCompletion(True, 5, 5, True, False, ""))
		self.assertFalse(shouldFinalizeResponseCompletion(True, 4.99, 5, True, False, ""))
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
		for label in (
			"Share", "Copy", "Copy message", "Read aloud", "Regenerate response",
			"Good response", "Bad response", "More actions", "Previous response",
			"Sources", "Sources 4", "Outputs (2)", "Copy response", "Share link",
			"Show more", "Show less", "Loading", "Loading…", "Add credits", "Upgrade",
			"Update", "Update now", "Dismiss usage alert", "6% usage remaining",
			"Resets every week", "Next reset is on Sep 10", "Usage consumed", "Manage plan",
		):
			self.assertTrue(isChatHistoryInterfaceText(label), label)
		self.assertFalse(isChatHistoryInterfaceText("Plan an accessible vacation"))
		self.assertFalse(isChatHistoryInterfaceText("Sources of accessible software"))
		self.assertFalse(isChatHistoryInterfaceText("Update NVDA add-on documentation"))
		self.assertFalse(isChatHistoryInterfaceText("Upgrade an accessible computer"))
		for label in (
			"Jump to user message 1", "You said:", "ChatGPT said:", "Dismiss usage alert",
			"6% usage remaining", "Resets every week", "Next reset is tomorrow", "Usage consumed",
		):
			self.assertTrue(isChatHistoryConversationBoundary(label), label)
		self.assertFalse(isChatHistoryConversationBoundary("Discuss message navigation"))
		plugin = PLUGIN_PATH.read_text(encoding="utf-8")
		self.assertEqual(2, plugin.count("not isChatHistoryInterfaceText("))
		self.assertIn("if not recentsSeen and plainText.casefold() == \"recents\":", plugin)
		self.assertEqual(2, plugin.count("inRecents = inArchived = False"))

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
		self.assertFalse(shouldSuppressRoutineBraille(True, True, "command", "high"))
		self.assertFalse(shouldSuppressRoutineBraille(True, True, "completion", "high"))
		self.assertTrue(shouldSuppressRoutineBraille(True, True, "completion", "high", True))
		self.assertFalse(shouldSuppressRoutineBraille(True, True, "completion", "urgent", True))
		self.assertFalse(shouldSuppressRoutineBraille(True, True, "attention", "urgent"))
		self.assertFalse(shouldSuppressRoutineBraille(True, True, "other", "normal"))
		self.assertEqual(
			{"speech": False, "braille": False, "sound": False},
			categoryOutputActions("off", True, True, True),
		)

	def test_conversation_reading_protection_suppresses_only_browse_mode_response_updates(self):
		self.assertTrue(shouldSuppressNativeConversationUpdate(
			True, True, True, True, False, "Response: streamed assistant text",
		))
		self.assertTrue(shouldSuppressNativeConversationUpdate(
			True, True, True, True, False, "Response complete: finished text",
		))
		self.assertTrue(shouldSuppressNativeConversationUpdate(
			True, True, True, True, False, "Response complete",
		))
		self.assertTrue(shouldSuppressNativeConversationUpdate(
			True, True, True, True, False, "ChatGPT said: streamed assistant text",
		))
		for arguments in (
			(False, True, True, True, False, "Response: text"),
			(True, False, True, True, False, "Response: text"),
			(True, True, False, True, False, "Response: text"),
			(True, True, True, False, False, "Response: text"),
			(True, True, True, True, True, "Response: text"),
			(True, True, True, True, False, "Permission required: Allow or deny"),
			(True, True, True, True, False, "Running command"),
			(True, True, True, True, False, ""),
		):
			self.assertFalse(shouldSuppressNativeConversationUpdate(*arguments), arguments)

	def test_live_region_hook_withholds_response_but_passes_focus_mode_and_permissions(self):
		tree = ast.parse(PLUGIN_PATH.read_text(encoding="utf-8"))
		pluginClass = next(
			node for node in tree.body
			if isinstance(node, ast.ClassDef) and node.name == "GlobalPlugin"
		)
		method = next(
			node for node in pluginClass.body
			if isinstance(node, ast.FunctionDef) and node.name == "event_liveRegionChange"
		)

		class Logger:
			def debug(self, *args, **kwargs): pass
			def debugWarning(self, *args, **kwargs): pass

		class Roles:
			BUTTON = "button"

		namespace = {
			"shouldSuppressNativeConversationUpdate": shouldSuppressNativeConversationUpdate,
			"usageLimitNotice": usageLimitNotice,
			"_isChatGPTObject": lambda obj: True,
			"_": lambda text: text,
			"_settings": lambda: {"protectBrailleReading": True},
			"statusDetails": statusDetails,
			"Role": Roles,
			"log": Logger(),
		}
		exec(compile(ast.Module(body=[method], type_ignores=[]), str(PLUGIN_PATH), "exec"), namespace)

		class Buffer:
			passThrough = False

		class Object:
			def __init__(self, name, buffer):
				self.name = name
				self.value = ""
				self.treeInterceptor = buffer
				self.role = "section"

		class Subject:
			def __init__(self):
				self._buffer = Buffer()
				self._appFocusState = True
				self._suppressedConversationUpdates = 0
				self.commentary = 0
				self.limitAlerts = []

			def _eventUsesConversationBuffer(self, obj): return True
			def _popupDialogFromObject(self, obj): return None
			def _conversationBrowseModeActive(self): return not self._buffer.passThrough
			def _schedulePopupDialogFocus(self, obj): pass
			def _announceUsageLimit(self, obj, text=""):
				notice = usageLimitNotice(text)
				if notice:
					self.limitAlerts.append(notice)
					return True
				return False
			def _announceStatus(self, obj): return False
			def _announceCommentary(self, obj):
				self.commentary += 1
				return True

		subject = Subject()
		passed = []
		response = Object("Response: streamed assistant text", subject._buffer)
		namespace["event_liveRegionChange"](subject, response, lambda: passed.append(True))
		self.assertEqual([], passed)
		self.assertEqual(0, subject.commentary)
		self.assertEqual(1, subject._suppressedConversationUpdates)

		permission = Object("Permission required: Allow or deny", subject._buffer)
		namespace["event_liveRegionChange"](subject, permission, lambda: passed.append(True))
		self.assertEqual([True], passed)
		self.assertEqual(1, subject.commentary)

		limit = Object("You've hit your usage limit. Try again at 9:45 PM.", subject._buffer)
		namespace["event_liveRegionChange"](subject, limit, lambda: passed.append(True))
		self.assertEqual([True], passed)
		self.assertEqual(1, len(subject.limitAlerts))
		self.assertEqual(1, subject.commentary)

		subject._buffer.passThrough = True
		namespace["event_liveRegionChange"](subject, response, lambda: passed.append(True))
		self.assertEqual([True, True], passed)
		self.assertEqual(2, subject.commentary)

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
