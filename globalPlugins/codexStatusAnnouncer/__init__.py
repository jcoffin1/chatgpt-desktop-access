"""Announce activity shown by the Codex desktop interface."""

import os
import json
import time
from pathlib import Path

import addonHandler
import api
import braille
import config
import globalPluginHandler
import gui
import keyboardHandler
import nvwave
import speech
import textInfos
import tones
import ui
import wx
from controlTypes import Role
from gui import guiHelper
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from logHandler import log
from scriptHandler import script

from .core import AnnouncementHistory, CATEGORY_SETTING, announcementPriority, backgroundActivityName, brailleStatusMessage, categoryOutputActions, changelogForDisplay, chatActionMatches, chatMessageShortcutIndex, chatMessagesFromTokens, chatTitleMatches, codexThreadUrl, coalescedPollDelay, completedTextDelta, confirmedUserMessageSubmission, currentActivitySummary, duplicateChannelActions, elapsedSeconds, firstStatusLabel, focusStateTransition, formatCommandSpeech, formatCustomAnnouncement, formatElapsedDuration, intermediateCompletionCategory, isCodexPromptLabel, isKnownNonStatusButton, isPermissionDecisionLabel, isPermissionPromptText, isStopControlLabel, isTaskCompletionLabel, loadArchivedThreads, looksLikeBlankCodexConversation, nextBusyState, outputActions, pendingChatTitle, pluginInstallProgress, pluginProgressBusyTransition, pollDelay, previewSelection, promptControlKind, promptSubmissionTransition, redactSensitive, repairConfigurationValues, responseCompletionTransition, shouldFinalizeResponseCompletion, shouldLogDiagnosticSnapshot, shouldPlayContinuousWorkingClick, shouldReplaceScheduledPoll, shouldSuppressRoutineBraille, shouldSuppressSemanticDuplicate, soundKey, statusDetails, statusMessage, stopControlTransition, supersedesResponseCompletionCandidate, tonePattern, uniqueThreadLabels, userMessageNumber, userMessageSubmissionTransition, viewerTitleMatches

addonHandler.initTranslation()

CONFIG_SECTION = "codexStatusAnnouncer"
ADDON_VERSION = "2026.1.42"
CODEX_USAGE_URL = "https://chatgpt.com/codex/settings/usage"
CURRENT_RELEASE_NOTES = _(
	"Version 2026.1.42\n\n"
	"What's new:\n"
	"• Control+1 reads the most recent chat message; Control+2 through Control+0 read progressively older messages, up to ten.\n"
	"• The shortcuts work in ChatGPT focus and browse modes and pass through normally in other applications.\n"
	"• Conversation extraction ignores hidden response copies, controls, timestamps, and progress metadata.\n"
	"• Chat-action retries are bounded, and transient Chromium failures cannot interrupt NVDA's event chain.\n"
	"• Prompt submitted sounds now survive ChatGPT's temporary focus change after Enter."
)
VERBOSITY_CHOICES = ("minimal", "full")
FULL_SPEECH_PROFILE_CHOICES = ("standard", "developer", "raw")
MINIMAL_SPEECH_PROFILE_CHOICES = ("essential", "balanced", "informative")
BRAILLE_DETAIL_CHOICES = ("concise", "informative", "full")
SOUND_STYLE_CHOICES = ("clicks", "tones")
CLICK_VOLUME_CHOICES = ("soft", "normal", "loud")
COMMAND_PUNCTUATION_CHOICES = ("normal", "enhanced", "literal")
OUTPUT_MODE_CHOICES = ("all", "speech", "sound", "braille", "off")
CATEGORY_OUTPUT_CONFIG = {
	"thinking": "outputThinking", "working": "outputWorking", "command": "outputCommands",
	"search": "outputSearches", "file": "outputFiles", "build": "outputBuilds",
	"tool": "outputTools", "completion": "outputCompletions", "attention": "outputAttention",
	"other": "outputOther", "commentary": "outputCommentary",
}
PREVIEW_ITEMS = (
	("thinking", "announcementThinking", _("Thinking"), _("Thinking")),
	("working", "announcementWorking", _("Working"), _("Working")),
	("command", "announcementCommand", _("Command"), _("Running command")),
	("search", "announcementSearch", _("Search"), _("Searching the web")),
	("file", "announcementFile", _("File"), _("Editing file")),
	("build", "announcementBuild", _("Build and test"), _("Running tests")),
	("tool", "announcementTool", _("Tool"), _("Using tool")),
	("commentary", "announcementCommentary", _("Commentary"), _("I am inspecting the current task.")),
	("backgroundPulse1", "announcementPulse1", _("Background progress one"), _("Command still running, 5 seconds")),
	("backgroundPulse2", "announcementPulse2", _("Background progress two"), _("Command still running, 10 seconds")),
	("completion", "announcementCompletion", _("Completion"), _("Command finished")),
	("completion", "announcementFailure", _("Failure"), _("Command failed")),
	("attention", "announcementAttention", _("Permission required"), _("Permission required")),
	("other", "announcementOther", _("Other progress"), _("Waiting")),
	("monitoringActive", "announcementMonitoringActive", _("Monitoring active"), _("Codex status monitoring active")),
	("monitoringInactive", "announcementMonitoringInactive", _("Monitoring inactive"), _("Codex status monitoring inactive")),
	("submission", "announcementSubmission", _("Prompt submitted"), _("Prompt submitted")),
)
ANNOUNCEMENT_CONFIG_BY_ACTION = {item[0]: item[1] for item in PREVIEW_ITEMS if item[0] != "completion"}
ANNOUNCEMENT_CONFIG_BY_ACTION.update({"completion": "announcementCompletion", "failure": "announcementFailure"})
RESPONSE_COMPLETION_SETTLE_SECONDS = 30.0
CHAT_MESSAGE_GESTURES = tuple("kb:control+{digit}".format(digit=digit) for digit in "1234567890")
_lastConfigurationRepairs = ()
config.conf.spec[CONFIG_SECTION] = {
	"verbosity": "option('minimal', 'full', default='full')",
	"fullSpeechProfile": "option('standard', 'developer', 'raw', default='developer')",
	"minimalSpeechProfile": "option('essential', 'balanced', 'informative', default='balanced')",
	"commandPunctuation": "option('normal', 'enhanced', 'literal', default='enhanced')",
	"maximumSpokenCommandCharacters": "integer(default=240, min=40, max=2000)",
	"speech": "boolean(default=True)",
	"braille": "boolean(default=True)",
	"brailleDetail": "option('concise', 'informative', 'full', default='full')",
	"protectBrailleReading": "boolean(default=True)",
	"interruptUrgentSpeech": "boolean(default=True)",
	"redactSensitive": "boolean(default=False)",
	"workingIntervalSeconds": "integer(default=5, min=1, max=300)",
	"idlePollMs": "integer(default=500, min=100, max=5000)",
	"completionSound": "boolean(default=False)",
	"soundWhenSpeechUnavailable": "boolean(default=True)",
	"progressSoundStyle": "option('clicks', 'tones', default='clicks')",
	"clickVolume": "option('soft', 'normal', 'loud', default='normal')",
	"continuousWorkingClicks": "boolean(default=True)",
	"workingClickIntervalMs": "integer(default=1400, min=500, max=5000)",
	"workingClickStartDelayMs": "integer(default=750, min=0, max=10000)",
	"promptSubmissionClick": "boolean(default=True)",
	"monitoringFocusClicks": "boolean(default=True)",
	"maximumBusyMinutes": "integer(default=60, min=1, max=240)",
	"welcomeShown": "boolean(default=False)",
	"lastShownVersion": "string(default='')",
	"supportedAppNames": "string(default='chatgpt')",
	"diagnosticLogging": "boolean(default=False)",
	"announceThinking": "boolean(default=True)",
	"announceWorking": "boolean(default=True)",
	"announceCommands": "boolean(default=True)",
	"announceSearches": "boolean(default=True)",
	"announceFiles": "boolean(default=True)",
	"announceBuilds": "boolean(default=True)",
	"announceTools": "boolean(default=True)",
	"announceCompletions": "boolean(default=True)",
	"announceOther": "boolean(default=True)",
	"announceCommentary": "boolean(default=True)",
	"announceHeartbeat": "boolean(default=True)",
	"announceAttention": "boolean(default=True)",
	"outputThinking": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputWorking": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputCommands": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputSearches": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputFiles": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputBuilds": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputTools": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputCompletions": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputAttention": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputOther": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"outputCommentary": "option('all', 'speech', 'sound', 'braille', 'off', default='all')",
	"announcementThinking": "string(default='')",
	"announcementWorking": "string(default='')",
	"announcementCommand": "string(default='')",
	"announcementSearch": "string(default='')",
	"announcementFile": "string(default='')",
	"announcementBuild": "string(default='')",
	"announcementTool": "string(default='')",
	"announcementCommentary": "string(default='')",
	"announcementPulse1": "string(default='')",
	"announcementPulse2": "string(default='')",
	"announcementCompletion": "string(default='')",
	"announcementFailure": "string(default='')",
	"announcementAttention": "string(default='')",
	"announcementOther": "string(default='')",
	"announcementMonitoringActive": "string(default='')",
	"announcementMonitoringInactive": "string(default='')",
	"announcementSubmission": "string(default='')",
}


def _settings():
	return config.conf[CONFIG_SECTION]


def _repairConfiguration():
	"""Repair migrated choice and numeric values without discarding valid preferences."""
	global _lastConfigurationRepairs
	conf = _settings()
	choiceDefaults = {
		"verbosity": (VERBOSITY_CHOICES, "full"),
		"fullSpeechProfile": (FULL_SPEECH_PROFILE_CHOICES, "developer"),
		"minimalSpeechProfile": (MINIMAL_SPEECH_PROFILE_CHOICES, "balanced"),
		"brailleDetail": (BRAILLE_DETAIL_CHOICES, "full"),
		"commandPunctuation": (COMMAND_PUNCTUATION_CHOICES, "enhanced"),
		"progressSoundStyle": (SOUND_STYLE_CHOICES, "clicks"),
		"clickVolume": (CLICK_VOLUME_CHOICES, "normal"),
	}
	for key in CATEGORY_OUTPUT_CONFIG.values():
		choiceDefaults[key] = (OUTPUT_MODE_CHOICES, "all")
	numericDefaults = {
		"maximumSpokenCommandCharacters": (40, 2000, 240),
		"workingIntervalSeconds": (1, 300, 5),
		"idlePollMs": (100, 5000, 500),
		"workingClickIntervalMs": (500, 5000, 1400),
		"workingClickStartDelayMs": (0, 10000, 750),
		"maximumBusyMinutes": (1, 240, 60),
	}
	booleanKeys = tuple((key, default) for key, default in {
		"speech": True, "braille": True, "protectBrailleReading": True,
		"interruptUrgentSpeech": True, "redactSensitive": False,
		"completionSound": False, "soundWhenSpeechUnavailable": True,
		"continuousWorkingClicks": True, "promptSubmissionClick": True,
		"monitoringFocusClicks": True, "welcomeShown": False,
		"diagnosticLogging": False, "announceThinking": True,
		"announceWorking": True, "announceCommands": True,
		"announceSearches": True, "announceFiles": True,
		"announceBuilds": True, "announceTools": True,
		"announceCompletions": True, "announceOther": True,
		"announceCommentary": True, "announceHeartbeat": True,
		"announceAttention": True,
	}.items())
	repaired = repairConfigurationValues(
		conf, choiceDefaults, numericDefaults, booleanKeys,
		(("supportedAppNames", "chatgpt"), ("lastShownVersion", "")),
	)
	if repaired:
		log.warning("Codex Access Toolkit repaired configuration fields: %s", ", ".join(repaired))
	_lastConfigurationRepairs = repaired
	return tuple(repaired)


def _customizeAnnouncement(message, action, activity="", seconds=0, values=None):
	conf = values or _settings()
	key = ANNOUNCEMENT_CONFIG_BY_ACTION.get(action)
	return formatCustomAnnouncement(conf.get(key, "") if key else "", message, activity, seconds)


def _safeBeep(frequency, duration):
	try:
		tones.beep(frequency, duration)
	except Exception:
		log.debugWarning("Codex Access Toolkit tone output failed", exc_info=True)


def _playProgressTone(category, message=""):
	delay = 0
	for index, (frequency, duration) in enumerate(tonePattern(category, message)):
		if index == 0:
			_safeBeep(frequency, duration)
		else:
			wx.CallLater(delay, _safeBeep, frequency, duration)
		delay += duration + 25


def _playProgressSound(category, message="", style="clicks", volume="normal"):
	if style == "tones":
		_playProgressTone(category, message)
		return
	path = os.path.join(os.path.dirname(__file__), "sounds", volume, f"{soundKey(category, message)}.wav")
	try:
		nvwave.playWaveFile(path)
	except Exception:
		log.debugWarning("Codex Access Toolkit could not play click earcon; using tones", exc_info=True)
		_playProgressTone(category, message)


def _speechIsOff():
	try:
		return speech.getState().speechMode == speech.SpeechMode.off
	except Exception:
		log.debugWarning("Codex Access Toolkit could not read NVDA's speech mode", exc_info=True)
		return False


def _send(message, speak=True, showBraille=True, toneCategory=None, progressSoundsEnabled=True, soundStyle=None, clickVolume=None, priority="normal", brailleMessage=None, interruptUrgent=None):
	actions = outputActions(speak, _speechIsOff(), showBraille, progressSoundsEnabled, toneCategory)
	if actions["speech"]:
		if interruptUrgent is None:
			interruptUrgent = _settings()["interruptUrgentSpeech"]
		if priority == "urgent" and interruptUrgent:
			try:
				speech.cancelSpeech()
			except Exception:
				log.debugWarning("Codex Access Toolkit could not cancel speech for an urgent message", exc_info=True)
		try:
			speech.speakMessage(message)
		except Exception:
			log.debugWarning("Codex Access Toolkit speech output failed", exc_info=True)
	if actions["braille"]:
		try:
			braille.handler.message(message if brailleMessage is None else brailleMessage)
		except Exception:
			log.debugWarning("Codex Access Toolkit Braille output failed", exc_info=True)
	if actions["tone"]:
		try:
			_playProgressSound(
				toneCategory, message, soundStyle or _settings()["progressSoundStyle"],
				clickVolume or _settings()["clickVolume"],
			)
			return True
		except Exception:
			log.debugWarning("Codex Access Toolkit progress sound output failed", exc_info=True)
	return False


def _moveBrowseableMessageToTop(expectedTitle):
	try:
		foreground = api.getForegroundObject()
		foregroundName = str(getattr(foreground, "name", "") or "")
		if not viewerTitleMatches(expectedTitle, foregroundName):
			log.debug("Codex Access Toolkit did not move document focus; expected viewer is not foreground")
			return
		keyboardHandler.KeyboardInputGesture.fromName("control+home").send()
	except Exception:
		log.debugWarning("Codex Access Toolkit could not move the document viewer to the top", exc_info=True)


def _showBrowseableMessageAtTop(message, title):
	ui.browseableMessage(message, title=title, closeButton=True)
	wx.CallLater(350, _moveBrowseableMessageToTop, title)


def _completeChangelogMessage():
	changelogPath = Path(addonHandler.getCodeAddon().path) / "changelog.md"
	return changelogForDisplay(changelogPath.read_text(encoding="utf-8"))


def _openUsageDashboard(message):
	try:
		opened = wx.LaunchDefaultBrowser(CODEX_USAGE_URL)
	except Exception:
		log.error("Unable to open the Codex usage dashboard", exc_info=True)
		opened = False
	ui.message(message if opened else _("The Codex usage dashboard could not be opened"))


class ChatHistoryDialog(wx.Dialog):
	"""Search and operate recent and archived titles exposed by ChatGPT."""

	_ARCHIVED_PLACEHOLDER = _("Archived chats have not been loaded. Open ChatGPT Settings, then Archived chats.")

	def __init__(self, parent, recentTitles, archivedTitles, archivedLoaded, onRefresh, onAction, onClose):
		super().__init__(parent, title=_("Codex chat history"))
		self._allRecentTitles = tuple(recentTitles)
		self._allArchivedTitles = tuple(archivedTitles)
		self._onActionCallback = onAction
		self._onRefreshCallback = onRefresh
		self._onCloseCallback = onClose
		self._closing = False
		self._lastList = None
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(wx.StaticText(self, label=_("Search chats:")), flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
		self.search = wx.TextCtrl(self)
		mainSizer.Add(self.search, flag=wx.EXPAND | wx.ALL, border=10)
		mainSizer.Add(wx.StaticText(self, label=_("Recent chats:")), flag=wx.LEFT | wx.RIGHT, border=10)
		self.recentList = wx.ListBox(self, choices=list(self._allRecentTitles), style=wx.LB_SINGLE)
		mainSizer.Add(self.recentList, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
		mainSizer.Add(wx.StaticText(self, label=_("Archived chats:")), flag=wx.LEFT | wx.RIGHT, border=10)
		self._archivedLoaded = archivedLoaded
		self._archivedEmptyMessage = _("No archived chats") if archivedLoaded else self._ARCHIVED_PLACEHOLDER
		archivedChoices = list(self._allArchivedTitles) or [self._archivedEmptyMessage]
		self.archivedList = wx.ListBox(self, choices=archivedChoices, style=wx.LB_SINGLE)
		mainSizer.Add(self.archivedList, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
		self.resultStatus = wx.StaticText(self, label="")
		mainSizer.Add(self.resultStatus, flag=wx.LEFT | wx.RIGHT, border=10)
		self.refreshButton = wx.Button(self, label=_("&Refresh chat lists"))
		mainSizer.Add(self.refreshButton, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
		buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		mainSizer.Add(buttons, flag=wx.EXPAND | wx.ALL, border=10)
		self.SetSizerAndFit(mainSizer)
		self.SetMinSize((520, 420))
		self.search.Bind(wx.EVT_TEXT, self._onFilter)
		self.search.Bind(wx.EVT_KEY_DOWN, self._onSearchKey)
		self.recentList.Bind(wx.EVT_LISTBOX_DCLICK, self._onOpen)
		self.archivedList.Bind(wx.EVT_LISTBOX_DCLICK, self._onOpen)
		self.recentList.Bind(wx.EVT_CONTEXT_MENU, self._onContextMenu)
		self.archivedList.Bind(wx.EVT_CONTEXT_MENU, self._onContextMenu)
		self.recentList.Bind(wx.EVT_SET_FOCUS, lambda evt: self._rememberListFocus(evt, self.recentList))
		self.archivedList.Bind(wx.EVT_SET_FOCUS, lambda evt: self._rememberListFocus(evt, self.archivedList))
		self.refreshButton.Bind(wx.EVT_BUTTON, self._onRefresh)
		self.Bind(wx.EVT_BUTTON, self._onOpen, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, lambda evt: self.Close(), id=wx.ID_CANCEL)
		self.Bind(wx.EVT_CHAR_HOOK, self._onCharHook)
		self.Bind(wx.EVT_CLOSE, self._onClose)
		self._selectFirst(self.recentList)
		self._selectFirst(self.archivedList)
		self._lastList = self.recentList
		self._updateResultStatus()
		self.search.SetFocus()

	def _rememberListFocus(self, evt, control):
		self._lastList = control
		evt.Skip()

	def _selectFirst(self, control):
		if control.GetCount():
			control.SetSelection(0)

	def _onFilter(self, evt):
		query = self.search.GetValue().strip().casefold()
		recentChoices = [title for title in self._allRecentTitles if query in title.casefold()]
		archivedChoices = [title for title in self._allArchivedTitles if query in title.casefold()]
		self.recentList.Set(recentChoices)
		self.archivedList.Set(archivedChoices or ([self._archivedEmptyMessage] if not self._allArchivedTitles else []))
		self._selectFirst(self.recentList)
		self._selectFirst(self.archivedList)
		self._updateResultStatus()

	def _updateResultStatus(self):
		recentCount = self.recentList.GetCount()
		archivedCount = len(self._allArchivedTitles) if self.archivedList.GetCount() and not self._allArchivedTitles else self.archivedList.GetCount()
		self.resultStatus.SetLabel(
			_("{recent} recent results; {archived} archived results").format(
				recent=recentCount, archived=archivedCount,
			)
		)

	def _onRefresh(self, evt):
		recentTitles, archivedTitles, archivedLoaded = self._onRefreshCallback()
		self._allRecentTitles = tuple(recentTitles)
		self._allArchivedTitles = tuple(archivedTitles)
		self._archivedLoaded = archivedLoaded
		self._archivedEmptyMessage = _("No archived chats") if archivedLoaded else self._ARCHIVED_PLACEHOLDER
		self._onFilter(None)
		ui.message(self.resultStatus.GetLabel())

	def _onSearchKey(self, evt):
		if evt.GetKeyCode() in (wx.WXK_DOWN, wx.WXK_UP) and self.recentList.GetCount():
			self.recentList.SetFocus()
			self.recentList.SetSelection(0 if evt.GetKeyCode() == wx.WXK_DOWN else self.recentList.GetCount() - 1)
			return
		evt.Skip()

	def _onOpen(self, evt):
		selection = self.selectedEntry()
		if selection is None:
			if self._lastList is self.archivedList and not self._allArchivedTitles:
				ui.message(self._archivedEmptyMessage)
			else:
				ui.message(_("No matching Codex chats"))
			return
		self._onActionCallback(selection[0], "open", selection[1])
		self.Close()

	def _onCharHook(self, evt):
		selection = self.selectedEntry()
		if evt.GetKeyCode() == wx.WXK_F10 and evt.ShiftDown() and selection is not None:
			self._showChatActionMenu(selection)
			return
		evt.Skip()

	def _onContextMenu(self, evt):
		"""Handle Shift+F10 and the Context Menu key emitted by native list boxes."""
		control = evt.GetEventObject()
		if control in (self.recentList, self.archivedList):
			self._lastList = control
		selection = self.selectedEntry()
		if selection is None:
			ui.message(_("No matching Codex chats"))
			return
		self._showChatActionMenu(selection)

	def _showChatActionMenu(self, selection):
		"""Move recent-chat focus to ChatGPT's actions; retain an archived-chat menu."""
		if selection[1] != "archived":
			self._performSelectedAction(selection, "focusActions")
			return
		menu = wx.Menu()
		chosen = []
		openItem = menu.Append(wx.ID_ANY, _("Open archived chat"))
		menu.Bind(wx.EVT_MENU, lambda evt: chosen.append("open"), openItem)
		try:
			self.PopupMenu(menu)
		finally:
			menu.Destroy()
		if chosen:
			self._performSelectedAction(selection, chosen[0])

	def _performSelectedAction(self, selection, action):
		if self._closing:
			return
		self._onActionCallback(selection[0], action, selection[1])
		self.Close()

	def _onClose(self, evt):
		if self._closing:
			return
		self._closing = True
		self.Hide()
		self.Destroy()
		self._onCloseCallback()

	def selectedEntry(self):
		focused = wx.Window.FindFocus()
		control = focused if focused in (self.recentList, self.archivedList) else self._lastList
		selection = control.GetSelection()
		if selection == wx.NOT_FOUND:
			return None
		title = control.GetString(selection)
		if title == self._archivedEmptyMessage:
			return None
		return title, ("archived" if control is self.archivedList else "recent")


class CodexStatusAnnouncerSettingsPanel(SettingsPanel):
	title = _("Codex Access Toolkit")

	def makeSettings(self, settingsSizer):
		helper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		conf = _settings()
		self.verbosity = helper.addLabeledControl(_("Announcement &detail:"), wx.Choice, choices=[
			_("Minimal — brief activity summaries"),
			_("Full — complete progress labels and commands"),
		])
		self.verbosity.SetSelection(VERBOSITY_CHOICES.index(conf["verbosity"]))
		self.fullSpeechProfile = helper.addLabeledControl(
			_("Full speech &profile:"), wx.Choice,
			choices=[
				_("Standard — action, target, counts, and useful timing"),
				_("Developer — complete normalized commands and progress"),
				_("Raw — exact exposed Codex progress text"),
			],
		)
		self.fullSpeechProfile.SetSelection(FULL_SPEECH_PROFILE_CHOICES.index(conf["fullSpeechProfile"]))
		self.minimalSpeechProfile = helper.addLabeledControl(
			_("Minimal speech p&rofile:"), wx.Choice,
			choices=[
				_("Essential — thinking, attention, failures, and task completion"),
				_("Balanced — concise activity changes and results"),
				_("Informative — Balanced plus filenames, counts, and timing"),
			],
		)
		self.minimalSpeechProfile.SetSelection(MINIMAL_SPEECH_PROFILE_CHOICES.index(conf["minimalSpeechProfile"]))
		self.commandPunctuation = helper.addLabeledControl(
			_("Command &punctuation for speech:"), wx.Choice,
			choices=[_("Normal"), _("Enhanced — speak pipes and redirects naturally"), _("Literal — name command symbols")],
		)
		self.commandPunctuation.SetSelection(COMMAND_PUNCTUATION_CHOICES.index(conf["commandPunctuation"]))
		self.maximumSpokenCommandCharacters = helper.addLabeledControl(
			_("Maximum spoken command characters:"), wx.SpinCtrl,
			min=40, max=2000, initial=conf["maximumSpokenCommandCharacters"],
		)
		self.speech = helper.addItem(wx.CheckBox(self, label=_("Enable &speech announcements")))
		self.braille = helper.addItem(wx.CheckBox(self, label=_("Enable &braille flash messages")))
		self.brailleDetail = helper.addLabeledControl(
			_("Braille &detail:"), wx.Choice,
			choices=[_("Concise"), _("Informative"), _("Full — complete commands and progress")],
		)
		self.brailleDetail.SetSelection(BRAILLE_DETAIL_CHOICES.index(conf["brailleDetail"]))
		self.protectBrailleReading = helper.addItem(wx.CheckBox(
			self, label=_("Protect Braille reading from routine progress while focused in ChatGPT"),
		))
		self.protectBrailleReading.SetValue(conf["protectBrailleReading"])
		self.interruptUrgentSpeech = helper.addItem(wx.CheckBox(
			self, label=_("Allow urgent permission and failure announcements to interrupt current speech"),
		))
		self.interruptUrgentSpeech.SetValue(conf["interruptUrgentSpeech"])
		self.redactSensitive = helper.addItem(wx.CheckBox(self, label=_("&Redact likely secrets and personal path names in Full mode")))
		for name in ("speech", "braille", "redactSensitive"):
			getattr(self, name).SetValue(conf[name])
		self.workingIntervalSeconds = helper.addLabeledControl(
			_("Announce background progress every (&interval in seconds):"), wx.SpinCtrl,
			min=1, max=300, initial=conf["workingIntervalSeconds"],
		)
		self.idlePollMs = helper.addLabeledControl(
			_("Idle compatibility &polling interval (milliseconds):"), wx.SpinCtrl,
			min=100, max=5000, initial=conf["idlePollMs"],
		)
		self.supportedAppNames = helper.addLabeledControl(
			_("Supported application process names, comma separated:"), wx.TextCtrl,
		)
		self.supportedAppNames.SetValue(conf["supportedAppNames"])
		labels = {
			"announceThinking": _("Announce t&hinking"), "announceWorking": _("Announce &working and analysis"),
			"announceCommands": _("Announce co&mmands"), "announceSearches": _("Announce web s&earches"),
			"announceFiles": _("Announce &file activity"), "announceBuilds": _("Announce b&uilds, compilation, and tests"),
			"announceTools": _("Announce &tool use"), "announceCompletions": _("Announce comp&letions and failures"),
			"announceOther": _("Announce &other recognized progress"),
			"announceCommentary": _("Announce Codex plain-language commentar&y updates"),
			"announceAttention": _("Announce permission and user-input alerts (&A)"),
		}
		self.categoryControls = {}
		for name, label in labels.items():
			control = helper.addItem(wx.CheckBox(self, label=label))
			control.SetValue(conf[name])
			self.categoryControls[name] = control
		self.completionSound = helper.addItem(wx.CheckBox(self, label=_("Play a sound for task &completion or failure")))
		self.progressSounds = helper.addItem(
			wx.CheckBox(self, label=_("Play progress sounds for all a&nnouncements")),
		)
		self.progressSoundStyle = helper.addLabeledControl(
			_("Progress sound style (&J):"), wx.Choice,
			choices=[_("Clicks — soft percussive earcons"), _("Tones — musical earcons")],
		)
		self.progressSoundStyle.SetSelection(SOUND_STYLE_CHOICES.index(conf["progressSoundStyle"]))
		self.clickVolume = helper.addLabeledControl(
			_("Click volume (&Z):"), wx.Choice,
			choices=[_("Soft"), _("Normal"), _("Loud")],
		)
		self.clickVolume.SetSelection(CLICK_VOLUME_CHOICES.index(conf["clickVolume"]))
		self.continuousWorkingClicks = helper.addItem(wx.CheckBox(
			self, label=_("Play a continuous Working sound while Codex is busy"),
		))
		self.continuousWorkingClicks.SetValue(conf["continuousWorkingClicks"])
		self.workingClickIntervalMs = helper.addLabeledControl(
			_("Working sound interval (milliseconds):"), wx.SpinCtrl,
			min=500, max=5000, initial=conf["workingClickIntervalMs"],
		)
		self.workingClickStartDelayMs = helper.addLabeledControl(
			_("Delay before repeating Working sounds (milliseconds):"), wx.SpinCtrl,
			min=0, max=10000, initial=conf["workingClickStartDelayMs"],
		)
		self.promptSubmissionClick = helper.addItem(wx.CheckBox(
			self, label=_("Play a distinct sound when a prompt is submitted"),
		))
		self.promptSubmissionClick.SetValue(conf["promptSubmissionClick"])
		self.monitoringFocusClicks = helper.addItem(wx.CheckBox(
			self, label=_("Play sounds when Codex monitoring becomes active or inactive"),
		))
		self.monitoringFocusClicks.SetValue(conf["monitoringFocusClicks"])
		self.maximumBusyMinutes = helper.addLabeledControl(
			_("Maximum background activity (minutes):"), wx.SpinCtrl,
			min=1, max=240, initial=conf["maximumBusyMinutes"],
		)
		outputLabels = {
			"thinking": _("Thinking output"), "working": _("Working output"),
			"command": _("Command output"), "search": _("Search output"),
			"file": _("File output"), "build": _("Build and test output"),
			"tool": _("Tool output"), "completion": _("Completion and failure output"),
			"attention": _("Permission and input-request output"),
			"other": _("Other progress output"), "commentary": _("Commentary output"),
		}
		outputChoices = [_("All enabled channels"), _("Speech only"), _("Sound only"), _("Braille only"), _("Off")]
		self.outputControls = {}
		for category, label in outputLabels.items():
			control = helper.addLabeledControl(label + ":", wx.Choice, choices=outputChoices)
			control.SetSelection(OUTPUT_MODE_CHOICES.index(conf[CATEGORY_OUTPUT_CONFIG[category]]))
			self.outputControls[category] = control
		self.diagnosticLogging = helper.addItem(wx.CheckBox(self, label=_("Enable sanitized dia&gnostic logging")))
		self.announceHeartbeat = helper.addItem(wx.CheckBox(self, label=_("Announce a recurring background progress pulse (&Q)")))
		self.completionSound.SetValue(conf["completionSound"])
		self.progressSounds.SetValue(conf["soundWhenSpeechUnavailable"])
		self.diagnosticLogging.SetValue(conf["diagnosticLogging"])
		self.announceHeartbeat.SetValue(conf["announceHeartbeat"])
		helper.addItem(wx.StaticText(self, label=_(
			"Warning: NVDA debug logging records spoken Full-mode text, including commands, even when add-on diagnostics are sanitized."
		)))
		self.testButton = helper.addItem(wx.Button(self, label=_("Test current announcement outputs (&X)")))
		self.testButton.Bind(wx.EVT_BUTTON, self._onTest)
		self.testSoundButton = helper.addItem(wx.Button(self, label=_("Test command progress sound (&K)")))
		self.testSoundButton.Bind(wx.EVT_BUTTON, self._onTestSound)
		self.previewItem = helper.addLabeledControl(
			_("Preview action (&V):"), wx.Choice,
			choices=[label for category, key, label, message in PREVIEW_ITEMS],
		)
		self.previewItem.SetSelection(0)
		self._announcementEdits = {key: str(conf[key]) for category, key, label, message in PREVIEW_ITEMS}
		self.previewItem.Bind(wx.EVT_CHOICE, self._onPreviewItemChanged)
		self.announcementText = helper.addLabeledControl(
			_("Announcement text (blank uses built-in):"), wx.TextCtrl,
		)
		self.announcementText.SetValue(self._announcementEdits[PREVIEW_ITEMS[0][1]])
		self.restoreAnnouncementButton = helper.addItem(wx.Button(self, label=_("Restore built-in announcement")))
		self.restoreAnnouncementButton.Bind(wx.EVT_BUTTON, self._onRestoreAnnouncement)
		helper.addItem(wx.StaticText(self, label=_(
			"Available placeholders: {message}, {activity}, {seconds}, and {duration}."
		)))
		self.previewSoundButton = helper.addItem(wx.Button(self, label=_("Preview selected sound")))
		self.previewSoundButton.Bind(wx.EVT_BUTTON, self._onPreviewSelectedSound)
		self.previewSpeechButton = helper.addItem(wx.Button(self, label=_("Preview selected speech")))
		self.previewSpeechButton.Bind(wx.EVT_BUTTON, self._onPreviewSelectedSpeech)
		self.checkUsageButton = helper.addItem(wx.Button(self, label=_("Check Codex usage statistics")))
		self.checkUsageButton.Bind(wx.EVT_BUTTON, self._onCheckUsage)
		self.buyCreditsButton = helper.addItem(wx.Button(self, label=_("Buy Codex usage credits")))
		self.buyCreditsButton.Bind(wx.EVT_BUTTON, self._onBuyCredits)
		self.viewCurrentRelease = helper.addItem(wx.Button(self, label=_("View current release notes…")))
		self.viewCurrentRelease.Bind(wx.EVT_BUTTON, self._onViewCurrentRelease)
		self.viewCompleteHistory = helper.addItem(wx.Button(self, label=_("View complete release history…")))
		self.viewCompleteHistory.Bind(wx.EVT_BUTTON, self._onViewCompleteHistory)
		self.exportSettings = helper.addItem(wx.Button(self, label=_("&Export add-on settings…")))
		self.exportSettings.Bind(wx.EVT_BUTTON, self._onExportSettings)
		self.importSettings = helper.addItem(wx.Button(self, label=_("&Import add-on settings…")))
		self.importSettings.Bind(wx.EVT_BUTTON, self._onImportSettings)
		self.resetSpeechSettings = helper.addItem(wx.Button(self, label=_("Reset speech profile settings")))
		self.resetSpeechSettings.Bind(wx.EVT_BUTTON, self._onResetSpeechSettings)

	def _onTest(self, evt):
		verbosity = VERBOSITY_CHOICES[self.verbosity.GetSelection()]
		label = "Testing project: 43 tests for 12 seconds" if verbosity == "minimal" else "Running shell command: python -m unittest discover -s tests"
		fullProfile = FULL_SPEECH_PROFILE_CHOICES[self.fullSpeechProfile.GetSelection()]
		minimalProfile = MINIMAL_SPEECH_PROFILE_CHOICES[self.minimalSpeechProfile.GetSelection()]
		speechMessage = statusMessage(
			label, _, verbosity, self.redactSensitive.IsChecked(), fullProfile, minimalProfile,
		)
		brailleMessage = brailleStatusMessage(
			label, _, BRAILLE_DETAIL_CHOICES[self.brailleDetail.GetSelection()], self.redactSensitive.IsChecked(),
		)
		_send(
			speechMessage,
			self.speech.IsChecked(), self.braille.IsChecked(), "command",
			self.progressSounds.IsChecked(),
			SOUND_STYLE_CHOICES[self.progressSoundStyle.GetSelection()],
			CLICK_VOLUME_CHOICES[self.clickVolume.GetSelection()],
			brailleMessage=brailleMessage,
			interruptUrgent=self.interruptUrgentSpeech.IsChecked(),
		)

	def _onTestSound(self, evt):
		_playProgressSound(
			"command", _("Running command"),
			SOUND_STYLE_CHOICES[self.progressSoundStyle.GetSelection()],
			CLICK_VOLUME_CHOICES[self.clickVolume.GetSelection()],
		)

	def _selectedPreview(self):
		return previewSelection(PREVIEW_ITEMS, self.previewItem.GetSelection())

	def _storeCurrentAnnouncementEdit(self):
		category, key, label, message = self._selectedPreview()
		self._announcementEdits[key] = self.announcementText.GetValue()

	def _onPreviewItemChanged(self, evt):
		oldSelection = getattr(self, "_previousPreviewSelection", 0)
		oldItem = previewSelection(PREVIEW_ITEMS, oldSelection)
		if oldItem:
			self._announcementEdits[oldItem[1]] = self.announcementText.GetValue()
		category, key, label, message = self._selectedPreview()
		self.announcementText.SetValue(self._announcementEdits[key])
		self._previousPreviewSelection = self.previewItem.GetSelection()

	def _onRestoreAnnouncement(self, evt):
		category, key, label, message = self._selectedPreview()
		self._announcementEdits[key] = ""
		self.announcementText.SetValue("")

	def _onPreviewSelectedSound(self, evt):
		style = SOUND_STYLE_CHOICES[self.progressSoundStyle.GetSelection()]
		volume = CLICK_VOLUME_CHOICES[self.clickVolume.GetSelection()]
		category, key, label, message = self._selectedPreview()
		_playProgressSound(category, message, style, volume)

	def _onPreviewSelectedSpeech(self, evt):
		self._storeCurrentAnnouncementEdit()
		category, key, label, message = self._selectedPreview()
		speech.speakMessage(formatCustomAnnouncement(self._announcementEdits[key], message, label, 0))

	def _onCheckUsage(self, evt):
		_openUsageDashboard(_("Opening Codex usage statistics"))

	def _onBuyCredits(self, evt):
		_openUsageDashboard(_("Opening Codex usage credits. No purchase will be made automatically."))

	def _onViewCurrentRelease(self, evt):
		_showBrowseableMessageAtTop(
			CURRENT_RELEASE_NOTES, _("Codex Access Toolkit — current release notes"),
		)

	def _onViewCompleteHistory(self, evt):
		try:
			message = _completeChangelogMessage()
		except Exception:
			log.error("Unable to open the Codex Access Toolkit changelog", exc_info=True)
			ui.message(_("The complete release history could not be opened"))
			return
		_showBrowseableMessageAtTop(
			message, _("Codex Access Toolkit — complete release history"),
		)

	def _onExportSettings(self, evt):
		with wx.FileDialog(
			self, _("Export Codex Access Toolkit settings"),
			wildcard=_("JSON files (*.json)|*.json"), style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
		) as dialog:
			if dialog.ShowModal() != wx.ID_OK:
				return
			path = Path(dialog.GetPath())
		try:
			values = {key: value for key, value in _settings().items() if isinstance(value, (str, int, float, bool))}
			path.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf-8")
		except Exception:
			log.error("Unable to export Codex Access Toolkit settings", exc_info=True)
			ui.message(_("Settings could not be exported"))
			return
		ui.message(_("Codex Access Toolkit settings exported"))

	def _onImportSettings(self, evt):
		with wx.FileDialog(
			self, _("Import Codex Access Toolkit settings"),
			wildcard=_("JSON files (*.json)|*.json"), style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
		) as dialog:
			if dialog.ShowModal() != wx.ID_OK:
				return
			path = Path(dialog.GetPath())
		conf = _settings()
		previousValues = {
			key: value for key, value in conf.items()
			if key in config.conf.spec[CONFIG_SECTION] and isinstance(value, (str, int, float, bool))
		}
		try:
			if path.stat().st_size > 1024 * 1024:
				raise ValueError("settings file exceeds 1 MB")
			values = json.loads(path.read_text(encoding="utf-8"))
			if not isinstance(values, dict):
				raise ValueError("settings root is not an object")
			for key, value in values.items():
				if key in config.conf.spec[CONFIG_SECTION] and isinstance(value, (str, int, float, bool)):
					conf[key] = value
			_repairConfiguration()
			config.conf.save()
			self._loadControlsFromConfiguration()
		except Exception:
			for key, value in previousValues.items():
				conf[key] = value
			_repairConfiguration()
			try:
				config.conf.save()
			except Exception:
				log.debugWarning("Unable to save restored Codex Access Toolkit settings", exc_info=True)
			self._loadControlsFromConfiguration()
			log.error("Unable to import Codex Access Toolkit settings", exc_info=True)
			ui.message(_("Settings could not be imported"))
			return
		ui.message(_("Settings imported and loaded into this panel."))

	def _loadControlsFromConfiguration(self):
		"""Refresh every editable control after an in-place settings import."""
		conf = _settings()
		self.verbosity.SetSelection(VERBOSITY_CHOICES.index(conf["verbosity"]))
		self.fullSpeechProfile.SetSelection(FULL_SPEECH_PROFILE_CHOICES.index(conf["fullSpeechProfile"]))
		self.minimalSpeechProfile.SetSelection(MINIMAL_SPEECH_PROFILE_CHOICES.index(conf["minimalSpeechProfile"]))
		self.brailleDetail.SetSelection(BRAILLE_DETAIL_CHOICES.index(conf["brailleDetail"]))
		self.interruptUrgentSpeech.SetValue(conf["interruptUrgentSpeech"])
		self.commandPunctuation.SetSelection(COMMAND_PUNCTUATION_CHOICES.index(conf["commandPunctuation"]))
		self.maximumSpokenCommandCharacters.SetValue(conf["maximumSpokenCommandCharacters"])
		for name in ("speech", "braille", "protectBrailleReading", "redactSensitive", "completionSound", "diagnosticLogging", "announceHeartbeat"):
			getattr(self, name).SetValue(conf[name])
		self.workingIntervalSeconds.SetValue(conf["workingIntervalSeconds"])
		self.idlePollMs.SetValue(conf["idlePollMs"])
		self.supportedAppNames.SetValue(conf["supportedAppNames"])
		self.progressSounds.SetValue(conf["soundWhenSpeechUnavailable"])
		self.progressSoundStyle.SetSelection(SOUND_STYLE_CHOICES.index(conf["progressSoundStyle"]))
		self.clickVolume.SetSelection(CLICK_VOLUME_CHOICES.index(conf["clickVolume"]))
		self.continuousWorkingClicks.SetValue(conf["continuousWorkingClicks"])
		self.workingClickIntervalMs.SetValue(conf["workingClickIntervalMs"])
		self.workingClickStartDelayMs.SetValue(conf["workingClickStartDelayMs"])
		self.promptSubmissionClick.SetValue(conf["promptSubmissionClick"])
		self.monitoringFocusClicks.SetValue(conf["monitoringFocusClicks"])
		self.maximumBusyMinutes.SetValue(conf["maximumBusyMinutes"])
		for name, control in self.categoryControls.items():
			control.SetValue(conf[name])
		for category, control in self.outputControls.items():
			control.SetSelection(OUTPUT_MODE_CHOICES.index(conf[CATEGORY_OUTPUT_CONFIG[category]]))
		self._announcementEdits = {key: str(conf[key]) for category, key, label, message in PREVIEW_ITEMS}
		selected = self._selectedPreview()
		self.announcementText.SetValue(self._announcementEdits[selected[1]])
		self._previousPreviewSelection = self.previewItem.GetSelection()

	def _onResetSpeechSettings(self, evt):
		self.verbosity.SetSelection(VERBOSITY_CHOICES.index("full"))
		self.fullSpeechProfile.SetSelection(FULL_SPEECH_PROFILE_CHOICES.index("developer"))
		self.minimalSpeechProfile.SetSelection(MINIMAL_SPEECH_PROFILE_CHOICES.index("balanced"))
		self.commandPunctuation.SetSelection(COMMAND_PUNCTUATION_CHOICES.index("enhanced"))
		self.maximumSpokenCommandCharacters.SetValue(240)
		self.redactSensitive.SetValue(False)
		ui.message(_("Speech profile settings reset. Select OK to save."))

	def onSave(self):
		conf = _settings()
		self._storeCurrentAnnouncementEdit()
		conf["verbosity"] = VERBOSITY_CHOICES[self.verbosity.GetSelection()]
		conf["fullSpeechProfile"] = FULL_SPEECH_PROFILE_CHOICES[self.fullSpeechProfile.GetSelection()]
		conf["minimalSpeechProfile"] = MINIMAL_SPEECH_PROFILE_CHOICES[self.minimalSpeechProfile.GetSelection()]
		conf["brailleDetail"] = BRAILLE_DETAIL_CHOICES[self.brailleDetail.GetSelection()]
		conf["interruptUrgentSpeech"] = self.interruptUrgentSpeech.IsChecked()
		conf["commandPunctuation"] = COMMAND_PUNCTUATION_CHOICES[self.commandPunctuation.GetSelection()]
		conf["maximumSpokenCommandCharacters"] = self.maximumSpokenCommandCharacters.GetValue()
		for name in ("speech", "braille", "protectBrailleReading", "redactSensitive", "completionSound", "diagnosticLogging", "announceHeartbeat"):
			conf[name] = getattr(self, name).IsChecked()
		conf["soundWhenSpeechUnavailable"] = self.progressSounds.IsChecked()
		conf["progressSoundStyle"] = SOUND_STYLE_CHOICES[self.progressSoundStyle.GetSelection()]
		conf["clickVolume"] = CLICK_VOLUME_CHOICES[self.clickVolume.GetSelection()]
		conf["continuousWorkingClicks"] = self.continuousWorkingClicks.IsChecked()
		conf["workingClickIntervalMs"] = self.workingClickIntervalMs.GetValue()
		conf["workingClickStartDelayMs"] = self.workingClickStartDelayMs.GetValue()
		conf["promptSubmissionClick"] = self.promptSubmissionClick.IsChecked()
		conf["monitoringFocusClicks"] = self.monitoringFocusClicks.IsChecked()
		conf["maximumBusyMinutes"] = self.maximumBusyMinutes.GetValue()
		for key, value in self._announcementEdits.items():
			conf[key] = value.strip()
		for category, control in self.outputControls.items():
			conf[CATEGORY_OUTPUT_CONFIG[category]] = OUTPUT_MODE_CHOICES[control.GetSelection()]
		for name, control in self.categoryControls.items():
			conf[name] = control.IsChecked()
		conf["workingIntervalSeconds"] = self.workingIntervalSeconds.GetValue()
		conf["idlePollMs"] = self.idlePollMs.GetValue()
		conf["supportedAppNames"] = self.supportedAppNames.GetValue().strip() or "chatgpt"


def _isChatGPTObject(obj):
	try:
		appName = str(getattr(getattr(obj, "appModule", None), "appName", "") or "").lower()
		supported = {name.strip().lower() for name in _settings()["supportedAppNames"].split(",") if name.strip()}
		return appName in supported
	except Exception:
		return False


def _isCodexObject(obj):
	if not _isChatGPTObject(obj):
		return False
	current = obj
	for _ in range(20):
		try:
			if current is None:
				break
			if getattr(current, "role", None) == Role.DOCUMENT and str(getattr(current, "name", "")).strip().lower() == "codex":
				return True
			current = getattr(current, "parent", None)
		except Exception:
			return False
	return False


def _isCodexPromptObject(obj):
	"""Recognize the prompt without relying solely on a sometimes-stale document ancestor."""
	try:
		if obj.role != Role.EDITABLETEXT or not _isChatGPTObject(obj):
			return False
	except Exception:
		return False
	for attribute in ("name", "placeholder", "description"):
		try:
			if isCodexPromptLabel(getattr(obj, attribute, "")):
				return True
		except Exception:
			continue
	return _isCodexObject(obj)


class CodexPromptControlOverlay:
	"""Add concise help to recognized native controls beside the Codex prompt."""

	def _get_description(self):
		descriptions = {
			"files": _("Opens file and attachment options. Press Enter or Space to open."),
			"model": _("Opens the model list. Press Enter or Space to open, then use arrow keys and Enter."),
			"permissions": _("Opens permission choices. Press Enter or Space to open, then use arrow keys and Enter."),
		}
		nativeDescription = str(getattr(self, "_codexNativeDescription", "") or "").strip()
		helpDescription = descriptions.get(getattr(self, "_codexPromptControlKind", ""), "")
		if nativeDescription and helpDescription.casefold() not in nativeDescription.casefold():
			return _("{native} {help}").format(native=nativeDescription, help=helpDescription)
		return nativeDescription or helpDescription


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Codex Access Toolkit")

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		"""Enhance known prompt controls without adding or intercepting gestures."""
		try:
			if obj.role not in (Role.BUTTON, Role.COMBOBOX) or not _isChatGPTObject(obj):
				return
			kind = promptControlKind(getattr(obj, "name", ""))
			if not kind:
				return
			obj._codexPromptControlKind = kind
			obj._codexNativeDescription = getattr(obj, "description", "")
			clsList.insert(0, CodexPromptControlOverlay)
		except Exception:
			return

	def __init__(self):
		super().__init__()
		_repairConfiguration()
		self._lastMessage = ""
		self._lastMessageAt = 0.0
		self._lastSpeechMessage = ""
		self._lastSpeechMessageAt = 0.0
		self._lastBrailleMessage = ""
		self._lastBrailleMessageAt = 0.0
		self._lastLabel = ""
		self._latestMessage = ""
		self._latestFullMessage = ""
		self._haveBaseline = False
		self._buffer = None
		self._monitoringAnnounced = False
		self._lastNoStatusLogAt = 0.0
		self._active = False
		self._lastHeartbeatAt = 0.0
		self._busy = False
		self._backgroundPulseCount = 0
		self._commentaryOffsets = {}
		self._paused = False
		self._speechHistory = AnnouncementHistory(20)
		self._brailleHistory = AnnouncementHistory(20)
		self._history = self._speechHistory
		self._busyStartedAt = 0.0
		self._activeCategory = "other"
		self._lastProgressSoundAt = 0.0
		self._appFocusState = None
		self._chatMessageShortcutsBound = False
		self._promptHadText = None
		self._latestUserMessageNumber = None
		self._pendingUserMessageIncrease = False
		self._stopControlVisible = False
		self._continuousClicksStartAt = 0.0
		self._lastStateReason = "startup"
		self._lastSubmissionSignal = "none"
		self._documentSwitchCount = 0
		self._lastInspectionError = "none"
		self._lastUnknownButtons = ()
		self._lastUnknownButtonsAt = 0.0
		self._lastPollAt = 0.0
		self._nextPollAt = 0.0
		self._latestResponseMarker = None
		self._responseMarkerInitialized = False
		self._pendingResponseCompletionAt = 0.0
		self._chatHistoryDialog = None
		self._pendingChatHistoryAction = None
		self._chatHistoryActionTimer = None
		self._chatActionRetryTimer = None
		self._pendingDirectChatAction = None
		self._unarchiveFocusTimer = None
		self._unarchiveFocusAttempts = 0
		self._popupFocusTimer = None
		self._pendingPopupDialog = None
		self._lastFocusedPopupDialog = None
		self._pluginProgressBuckets = {}
		self._pluginProgressOwnedBusy = set()
		self._pendingOpenedChatTitle = ""
		self._pendingOpenedChatAt = 0.0
		self._chatHistoryCache = ()
		self._archivedChatHistoryCache = ()
		self._archivedChatIds = {}
		self._whatsNewTimer = None
		log.info(
			"Codex Access Toolkit %s loaded (verbosity=%s, fullProfile=%s, minimalProfile=%s, brailleDetail=%s, soundStyle=%s)",
			ADDON_VERSION,
			_settings()["verbosity"], _settings()["fullSpeechProfile"],
			_settings()["minimalSpeechProfile"], _settings()["brailleDetail"], _settings()["progressSoundStyle"],
		)
		if CodexStatusAnnouncerSettingsPanel not in NVDASettingsDialog.categoryClasses:
			NVDASettingsDialog.categoryClasses.append(CodexStatusAnnouncerSettingsPanel)
		self._timer = wx.CallLater(100, self._poll)
		self._nextPollAt = time.monotonic() + 0.1
		self._whatsNewTimer = wx.CallLater(1500, self._showWhatsNewIfNeeded)

	def terminate(self):
		self._setChatMessageShortcutBindings(False)
		if self._timer:
			self._timer.Stop()
			self._timer = None
		self._nextPollAt = 0.0
		if self._whatsNewTimer:
			self._whatsNewTimer.Stop()
			self._whatsNewTimer = None
		if self._chatHistoryDialog:
			self._chatHistoryDialog.Destroy()
			self._chatHistoryDialog = None
			gui.mainFrame.postPopup()
		if self._chatHistoryActionTimer:
			self._chatHistoryActionTimer.Stop()
			self._chatHistoryActionTimer = None
		if self._chatActionRetryTimer:
			self._chatActionRetryTimer.Stop()
			self._chatActionRetryTimer = None
		self._pendingDirectChatAction = None
		if self._unarchiveFocusTimer:
			self._unarchiveFocusTimer.Stop()
			self._unarchiveFocusTimer = None
		if self._popupFocusTimer:
			self._popupFocusTimer.Stop()
			self._popupFocusTimer = None
		self._pendingPopupDialog = None
		self._lastFocusedPopupDialog = None
		self._pluginProgressBuckets.clear()
		self._pluginProgressOwnedBusy.clear()
		self._pendingChatHistoryAction = None
		try:
			NVDASettingsDialog.categoryClasses.remove(CodexStatusAnnouncerSettingsPanel)
		except ValueError:
			pass
		super().terminate()

	def _setChatMessageShortcutBindings(self, active):
		"""Bind fixed message-review keys only while focus is within ChatGPT."""
		active = bool(active)
		if active == self._chatMessageShortcutsBound:
			return
		succeeded = True
		for gestureIdentifier in CHAT_MESSAGE_GESTURES:
			try:
				if active:
					self.bindGesture(gestureIdentifier, "readPreviousChatMessage")
				else:
					self.removeGestureBinding(gestureIdentifier)
			except LookupError:
				# An already absent binding is a successful inactive state.
				if active:
					succeeded = False
			except Exception:
				succeeded = False
				log.debugWarning("Codex Access Toolkit could not update a chat-message shortcut", exc_info=True)
		self._chatMessageShortcutsBound = active if succeeded else not active

	def _schedulePoll(self, delay=150):
		now = time.monotonic()
		actualDelay = coalescedPollDelay(
			delay, now - self._lastPollAt if self._lastPollAt else float("inf"),
		)
		requestedDeadline = now + actualDelay / 1000.0
		if self._timer and not shouldReplaceScheduledPoll(self._nextPollAt, requestedDeadline):
			return
		if self._timer:
			self._timer.Stop()
		self._timer = wx.CallLater(actualDelay, self._poll)
		self._nextPollAt = requestedDeadline

	def _showWhatsNewIfNeeded(self):
		self._whatsNewTimer = None
		conf = _settings()
		if conf["lastShownVersion"] == ADDON_VERSION:
			return
		_showBrowseableMessageAtTop(
			CURRENT_RELEASE_NOTES, _("Codex Access Toolkit — what's new"),
		)
		conf["lastShownVersion"] = ADDON_VERSION
		conf["welcomeShown"] = True
		try:
			config.conf.save()
		except Exception:
			log.debugWarning("Unable to save the last displayed add-on version", exc_info=True)

	def _resetTaskState(self, reason):
		self._setBusy(False, reason)
		self._lastLabel = ""
		self._haveBaseline = False
		self._commentaryOffsets.clear()
		self._promptHadText = None
		self._latestUserMessageNumber = None
		self._pendingUserMessageIncrease = False
		self._stopControlVisible = False
		self._continuousClicksStartAt = 0.0
		self._lastUnknownButtons = ()
		self._lastUnknownButtonsAt = 0.0
		self._latestResponseMarker = None
		self._responseMarkerInitialized = False
		self._pendingResponseCompletionAt = 0.0
		self._speechHistory.clear()
		self._brailleHistory.clear()
		self._latestMessage = ""
		self._latestFullMessage = ""
		self._lastMessage = ""
		self._lastMessageAt = 0.0
		self._lastSpeechMessage = ""
		self._lastSpeechMessageAt = 0.0
		self._lastBrailleMessage = ""
		self._lastBrailleMessageAt = 0.0
		self._activeCategory = "other"
		self._backgroundPulseCount = 0

	def _recordHistory(self, speechMessage, brailleMessage=None):
		brailleText = str(brailleMessage if brailleMessage is not None else speechMessage or "").strip()
		# Keep navigation aligned even when an Essential speech profile intentionally
		# omits a live event; explicit history review may still expose its details.
		self._speechHistory.add(str(speechMessage or brailleText).strip())
		self._brailleHistory.add(brailleText or str(speechMessage or "").strip())

	def _historyMessage(self, offset):
		if not self._speechHistory and not self._brailleHistory:
			ui.message(_("No Codex announcement history is available"))
			return
		speechMessage = self._speechHistory.move(offset) if self._speechHistory else ""
		brailleMessage = self._brailleHistory.move(offset) if self._brailleHistory else speechMessage
		conf = _settings()
		_send(
			speechMessage or brailleMessage, conf["speech"] and bool(speechMessage), conf["braille"],
			None, False, brailleMessage=brailleMessage,
		)

	def _currentChatMessages(self):
		"""Return the newest ten real conversation turns from the current virtual buffer."""
		focus = api.getFocusObject()
		if not _isChatGPTObject(focus):
			return ()
		self._rememberBuffer(focus)
		if not self._buffer:
			return ()
		info = self._buffer.makeTextInfo(textInfos.POSITION_ALL)
		def tokens():
			ignoredDepth = 0
			interactiveRoles = {
				Role.BUTTON, Role.EDITABLETEXT, Role.COMBOBOX, Role.LIST, Role.TREEVIEW,
				Role.CHECKBOX, Role.RADIOBUTTON,
			}
			for item in info.getTextWithFields():
				if isinstance(item, str):
					if ignoredDepth:
						continue
					text = " ".join(item.split())
					marker = text.casefold()
					if marker == "you said:":
						yield "speaker", "user"
					elif marker == "chatgpt said:":
						yield "speaker", "assistant"
					elif marker != "response complete":
						yield "text", item
					continue
				command = getattr(item, "command", "")
				field = getattr(item, "field", {}) or {}
				if command == "controlStart":
					name = " ".join(str(field.get("name", "") or "").split()).casefold()
					if not ignoredDepth and name == "you said:":
						yield "speaker", "user"
					elif not ignoredDepth and name == "chatgpt said:":
						yield "speaker", "assistant"
					role = field.get("role")
					if ignoredDepth:
						ignoredDepth += 1
					elif role in interactiveRoles:
						ignoredDepth = 1
						if role == Role.EDITABLETEXT:
							yield "end", ""
				elif command == "controlEnd" and ignoredDepth:
					ignoredDepth -= 1
		return chatMessagesFromTokens(tokens(), 10)

	@script(description=_("Read one of the ten most recent ChatGPT messages with Control+1 through Control+0"))
	def script_readPreviousChatMessage(self, gesture):
		focus = api.getFocusObject()
		if not _isChatGPTObject(focus):
			gesture.send()
			return
		position = chatMessageShortcutIndex(getattr(gesture, "mainKeyName", ""))
		if position is None:
			ui.message(_("Chat message shortcut could not be identified"))
			return
		try:
			messages = self._currentChatMessages()
		except Exception:
			log.debugWarning("Codex Access Toolkit could not read recent chat messages", exc_info=True)
			ui.message(_("Recent chat messages could not be read"))
			return
		if not messages:
			ui.message(_("No recent chat messages are available"))
			return
		if len(messages) < position:
			ui.message(_("Only {count} recent chat messages are available").format(count=len(messages)))
			return
		speaker, text = messages[-position]
		speakerLabel = _("You") if speaker == "user" else _("ChatGPT")
		ui.message(_("Chat message {position}, {speaker}: {text}").format(
			position=position, speaker=speakerLabel, text=text,
		))

	def _diagnosticReport(self):
		conf = _settings()
		return _(
			"Version: {version}\nVerbosity: {verbosity}\nFull speech profile: {profile}\nMinimal speech profile: {minimalProfile}\nBraille detail: {brailleDetail}\nSound style: {style}\nClick volume: {volume}\n"
			"Monitoring attached: {attached}\nBackground state: {state}\nPaused: {paused}\n"
			"Active category: {category}\nLast state reason: {reason}\nLast submission signal: {signal}\n"
			"Codex document switches: {switches}\nLast inspection error: {error}\n"
			"Speech history entries: {speechHistory}\nBraille history entries: {brailleHistory}\nRecent chats cached: {recent}\nArchived chats cached: {archived}\n"
			"Configuration repairs this session: {repairs}\nSupported applications: {apps}\n"
			"Speech: {speech}\nBraille: {braille}\nProtect Braille reading: {protectBraille}\nUrgent speech interruption: {interrupt}\nProgress sounds: {sounds}\nCategory output routing:\n{routing}"
		).format(
			version=ADDON_VERSION,
			verbosity=conf["verbosity"], profile=conf["fullSpeechProfile"], minimalProfile=conf["minimalSpeechProfile"],
			brailleDetail=conf["brailleDetail"],
			style=conf["progressSoundStyle"], volume=conf["clickVolume"],
			attached=bool(self._buffer), state="active" if self._busy else "idle", paused=self._paused,
			category=self._activeCategory, reason=self._lastStateReason, signal=self._lastSubmissionSignal,
			switches=self._documentSwitchCount, error=self._lastInspectionError,
			speechHistory=len(self._speechHistory), brailleHistory=len(self._brailleHistory), recent=len(self._chatHistoryCache), archived=len(self._archivedChatHistoryCache),
			repairs=", ".join(_lastConfigurationRepairs) or "none", apps=conf["supportedAppNames"], speech=conf["speech"],
			braille=conf["braille"], protectBraille=conf["protectBrailleReading"],
			interrupt=conf["interruptUrgentSpeech"], sounds=conf["soundWhenSpeechUnavailable"],
			routing="\n".join(
				"{category}: {mode}".format(category=category, mode=conf[key])
				for category, key in CATEGORY_OUTPUT_CONFIG.items()
			),
		)

	def _bufferCandidates(self, obj):
		seen = set()
		current = obj
		for _ in range(24):
			if current is None or id(current) in seen:
				break
			seen.add(id(current))
			yield current
			current = getattr(current, "parent", None)
		for current in reversed(api.getFocusAncestors() or []):
			if current is not None and id(current) not in seen:
				yield current

	def _chatHistoryTitles(self):
		"""Return chat titles cached by the normal background buffer inspection."""
		return self._chatHistoryCache

	def _refreshChatHistoryData(self):
		archivedTitles, archivedLoaded = self._loadArchivedChatHistory()
		return self._chatHistoryTitles(), archivedTitles, archivedLoaded

	def _loadArchivedChatHistory(self):
		"""Load archived titles from Codex's read-only JSONL metadata."""
		codexRoot = Path(os.environ.get("CODEX_HOME") or (Path.home() / ".codex"))
		try:
			entries = uniqueThreadLabels(loadArchivedThreads(codexRoot))
			self._archivedChatHistoryCache = tuple(title for threadId, title in entries)
			self._archivedChatIds = {title: threadId for threadId, title in entries}
			log.info("Codex Status Announcer loaded %d archived chats from the local index", len(entries))
			return self._archivedChatHistoryCache, True
		except Exception:
			log.debugWarning("Codex Status Announcer could not read archived chat metadata", exc_info=True)
			return self._archivedChatHistoryCache, False

	def _chatButtonObject(self, title):
		"""Resolve an exact accessible sidebar title to its button."""
		position = self._buffer.makeTextInfo(textInfos.POSITION_FIRST)
		if not position.find(title, reverse=False, caseSensitive=True):
			return None
		obj = getattr(position, "NVDAObjectAtStart", None)
		for _ in range(8):
			if obj is None or getattr(obj, "role", None) == Role.BUTTON:
				break
			obj = getattr(obj, "parent", None)
		if getattr(obj, "role", None) != Role.BUTTON:
			return None
		return obj if chatTitleMatches(title, getattr(obj, "name", ""), titleFoundInsideButton=True) else None

	def _namedChatActionButton(self, chatButton, action):
		"""Resolve the action exposed beside the focused chat, not matching transcript text."""
		container = getattr(chatButton, "parent", None)
		for _ in range(2):
			if container is None:
				break
			pending = [getattr(container, "firstChild", None)]
			seen = set()
			while pending and len(seen) < 32:
				obj = pending.pop()
				if obj is None or id(obj) in seen:
					continue
				seen.add(id(obj))
				if obj is not chatButton and getattr(obj, "role", None) == Role.BUTTON and chatActionMatches(
					action, getattr(obj, "name", ""),
				):
					return obj
				nextObject = getattr(obj, "next", None)
				firstChild = getattr(obj, "firstChild", None)
				if nextObject is not None:
					pending.append(nextObject)
				if firstChild is not None:
					pending.append(firstChild)
			container = getattr(container, "parent", None)
		return None

	def _startDirectChatAction(self, title, action):
		if self._chatActionRetryTimer:
			self._chatActionRetryTimer.Stop()
			self._chatActionRetryTimer = None
		self._pendingDirectChatAction = (title, action, 0)
		self._retryDirectChatAction()

	def _retryDirectChatAction(self):
		self._chatActionRetryTimer = None
		pending = self._pendingDirectChatAction
		if not pending:
			return
		title, action, attempt = pending
		try:
			chatButton = self._chatButtonObject(title)
			if chatButton is None:
				raise LookupError("selected chat button not found")
			chatButton.setFocus()
			if action == "focusActions":
				actionButton = self._namedChatActionButton(chatButton, "pin")
				if actionButton is None:
					actionButton = self._namedChatActionButton(chatButton, "archive")
			else:
				actionButton = self._namedChatActionButton(chatButton, action)
			if actionButton is not None:
				if action == "focusActions":
					actionButton.setFocus()
				else:
					actionButton.doAction()
				self._pendingDirectChatAction = None
				if action == "focusActions":
					focusedAction = " ".join(str(getattr(actionButton, "name", "") or "").split())
					log.info("Codex Access Toolkit focused selected chat action: %s", focusedAction)
				else:
					ui.message(_("Chat action opened"))
					log.info("Codex Status Announcer activated the selected chat action: %s", action)
				return
		except Exception:
			if attempt >= 11:
				self._pendingDirectChatAction = None
				if action == "focusActions":
					log.debugWarning("Codex Access Toolkit could not focus Pin, Unpin, or Archive", exc_info=True)
					ui.message(_("The selected chat's Pin or Archive button could not be focused"))
				else:
					log.debugWarning("Codex Access Toolkit could not activate the selected chat action", exc_info=True)
					ui.message(_("The selected chat action could not be opened"))
				return
		# A missing action control is a normal transient state while Chromium updates
		# the selected sidebar row, so it does not raise above. Apply the same retry
		# limit here; otherwise this path can schedule a main-thread timer forever.
		if attempt >= 11:
			self._pendingDirectChatAction = None
			if action == "focusActions":
				log.debugWarning("Codex Access Toolkit could not find Pin, Unpin, or Archive after retrying")
				ui.message(_("The selected chat's Pin or Archive button could not be focused"))
			else:
				log.debugWarning("Codex Access Toolkit could not find the selected chat action after retrying")
				ui.message(_("The selected chat action could not be opened"))
			return
		self._pendingDirectChatAction = (title, action, attempt + 1)
		self._chatActionRetryTimer = wx.CallLater(100, self._retryDirectChatAction)

	def _scheduleUnarchiveButtonFocus(self):
		self._unarchiveFocusAttempts = 0
		if self._unarchiveFocusTimer:
			self._unarchiveFocusTimer.Stop()
		self._unarchiveFocusTimer = wx.CallLater(100, self._focusUnarchiveButton)

	def _focusUnarchiveButton(self):
		"""Focus Codex's confirmation after its new document becomes accessible."""
		self._unarchiveFocusTimer = None
		self._unarchiveFocusAttempts += 1
		try:
			if self._buffer:
				position = self._buffer.makeTextInfo(textInfos.POSITION_FIRST)
				if position.find("Unarchive and open", reverse=False, caseSensitive=False):
					obj = getattr(position, "NVDAObjectAtStart", None)
					for _ in range(8):
						if obj is None or getattr(obj, "role", None) == Role.BUTTON:
							break
						obj = getattr(obj, "parent", None)
					if getattr(obj, "role", None) == Role.BUTTON and " ".join(
						str(getattr(obj, "name", "") or "").casefold().split()
					) == "unarchive and open":
						obj.setFocus()
						log.info("Codex Status Announcer focused the Unarchive and open button")
						return
		except Exception:
			log.debugWarning("Codex Status Announcer could not yet focus the unarchive confirmation", exc_info=True)
		if self._unarchiveFocusAttempts < 25:
			self._unarchiveFocusTimer = wx.CallLater(150, self._focusUnarchiveButton)
		else:
			ui.message(_("Unarchive confirmation opened; move to the Unarchive and open button"))

	def _popupDialogFromObject(self, obj):
		for _ in range(10):
			if obj is None or getattr(obj, "role", None) == Role.DIALOG:
				return obj
			obj = getattr(obj, "parent", None)
		return None

	def _schedulePopupDialogFocus(self, obj):
		if not _isChatGPTObject(obj):
			return
		try:
			dialog = self._popupDialogFromObject(obj)
		except Exception:
			log.debugWarning("Codex Status Announcer could not inspect a possible ChatGPT pop-up", exc_info=True)
			return
		if dialog is None or dialog is self._pendingPopupDialog or dialog is self._lastFocusedPopupDialog:
			return
		self._pendingPopupDialog = dialog
		if self._popupFocusTimer:
			self._popupFocusTimer.Stop()
		self._popupFocusTimer = wx.CallLater(50, self._focusPopupDialog)

	def _focusPopupDialog(self):
		"""Move focus into a newly displayed ChatGPT dialog without activating a control."""
		self._popupFocusTimer = None
		dialog, self._pendingPopupDialog = self._pendingPopupDialog, None
		if dialog is None:
			return
		try:
			focused = api.getFocusObject()
			current = focused
			for _ in range(12):
				if current is dialog:
					self._lastFocusedPopupDialog = dialog
					return
				current = getattr(current, "parent", None) if current is not None else None
			pending = [dialog]
			seen = set()
			objects = []
			while pending and len(seen) < 100:
				obj = pending.pop()
				if obj is None or id(obj) in seen:
					continue
				seen.add(id(obj))
				objects.append(obj)
				nextObject = getattr(obj, "next", None) if obj is not dialog else None
				firstChild = getattr(obj, "firstChild", None)
				if nextObject is not None:
					pending.append(nextObject)
				if firstChild is not None:
					pending.append(firstChild)
			text = " ".join(str(getattr(obj, "name", "") or "") for obj in objects)
			permissionPrompt = isPermissionPromptText(text)
			interactiveRoles = (
				Role.EDITABLETEXT, Role.COMBOBOX, Role.LIST, Role.TREEVIEW,
				Role.CHECKBOX, Role.RADIOBUTTON, Role.BUTTON,
			)
			candidates = [obj for obj in objects if getattr(obj, "role", None) in interactiveRoles]
			if permissionPrompt:
				decisions = [obj for obj in candidates if isPermissionDecisionLabel(getattr(obj, "name", ""))]
				candidates = decisions or candidates
			else:
				useful = [obj for obj in candidates if " ".join(
					str(getattr(obj, "name", "") or "").casefold().split()
				) not in ("close", "cancel", "dismiss")]
				candidates = useful or candidates
			for obj in candidates:
				try:
					obj.setFocus()
					self._lastFocusedPopupDialog = dialog
					log.info("Codex Status Announcer focused a ChatGPT pop-up dialog control")
					return
				except Exception:
					continue
			dialog.setFocus()
			self._lastFocusedPopupDialog = dialog
			log.info("Codex Status Announcer focused a ChatGPT pop-up dialog")
		except Exception:
			log.debugWarning("Codex Status Announcer could not focus the ChatGPT pop-up dialog", exc_info=True)

	def _announcePluginInstallProgress(self, obj):
		try:
			if getattr(obj, "role", None) != Role.PROGRESSBAR or not _isChatGPTObject(obj):
				return
			parts = []
			current = obj
			for _ in range(7):
				if current is None:
					break
				for attribute in ("name", "value", "description"):
					value = " ".join(str(getattr(current, attribute, "") or "").split())
					if value and value not in parts:
						parts.append(value)
				current = getattr(current, "parent", None)
			parsed = pluginInstallProgress(" ".join(parts))
		except Exception:
			log.debugWarning("Codex Status Announcer could not inspect a plug-in progress event", exc_info=True)
			return
		if parsed is None:
			return
		identity, percent, bucket = parsed
		if self._pluginProgressBuckets.get(identity, object()) == bucket:
			return
		if len(self._pluginProgressBuckets) >= 32 and identity not in self._pluginProgressBuckets:
			expiredIdentity = next(iter(self._pluginProgressBuckets))
			self._pluginProgressBuckets.pop(expiredIdentity)
			self._pluginProgressOwnedBusy.discard(expiredIdentity)
		self._pluginProgressBuckets[identity] = bucket
		if percent is None:
			message = _("Plugin installation in progress")
		elif percent >= 100:
			message = _("Plugin installation complete")
		else:
			message = _("Plugin installation {percent} percent").format(percent=percent)
		complete = percent is not None and percent >= 100
		busy, ownsBusy = pluginProgressBusyTransition(
			self._busy, identity in self._pluginProgressOwnedBusy, complete,
		)
		if ownsBusy:
			self._pluginProgressOwnedBusy.add(identity)
		else:
			self._pluginProgressOwnedBusy.discard(identity)
		self._setBusy(busy, "plugin installation progress")
		self._activeCategory = "tool"
		self._latestMessage = self._latestFullMessage = message
		self._speakOnce(message, "tool", "tool", brailleMessage=message)
		log.info("Codex Status Announcer announced plug-in installation progress")

	def _performChatHistoryAction(self, title, action, source="recent"):
		if source == "archived":
			threadUrl = codexThreadUrl(self._archivedChatIds.get(title))
			if not threadUrl:
				log.debugWarning("Codex Status Announcer has no valid thread ID for the selected archived chat")
				ui.message(_("The selected archived Codex task could not be opened"))
				return
			try:
				self._pendingOpenedChatTitle = title
				self._pendingOpenedChatAt = time.monotonic()
				opened = wx.LaunchDefaultBrowser(threadUrl)
			except Exception:
				opened = False
				log.debugWarning("Codex Status Announcer could not launch the archived task link", exc_info=True)
			if opened:
				log.info("Codex Status Announcer opened an archived task with the native Codex thread link")
				self._scheduleUnarchiveButtonFocus()
			else:
				self._pendingOpenedChatTitle = ""
				self._pendingOpenedChatAt = 0.0
				ui.message(_("The selected archived Codex task could not be opened"))
			return
		try:
			if action in ("focusActions", "pin", "archive"):
				self._startDirectChatAction(title, action)
				return
			button = self._chatButtonObject(title)
			if button is None:
				raise LookupError("selected chat button not found")
			self._pendingOpenedChatTitle = title
			self._pendingOpenedChatAt = time.monotonic()
			button.doAction()
			log.info("Codex Status Announcer performed chat history action: %s", action)
		except Exception:
			log.debugWarning("Codex Status Announcer could not act on the selected chat", exc_info=True)
			ui.message(_("The selected Codex chat could not be opened"))

	def _queueChatHistoryAction(self, title, action, source):
		self._pendingChatHistoryAction = (title, action, source)

	def _chatHistoryClosed(self):
		self._chatHistoryDialog = None
		gui.mainFrame.postPopup()
		pending, self._pendingChatHistoryAction = self._pendingChatHistoryAction, None
		if pending:
			self._chatHistoryActionTimer = wx.CallLater(
				100, self._runChatHistoryAction, pending[0], pending[1], pending[2],
			)

	def _runChatHistoryAction(self, title, action, source):
		self._chatHistoryActionTimer = None
		self._performChatHistoryAction(title, action, source)

	def _rememberBuffer(self, obj):
		if not _isChatGPTObject(obj):
			return
		for current in self._bufferCandidates(obj):
			buffer = getattr(current, "treeInterceptor", None)
			if not buffer:
				continue
			wasMissing = self._buffer is None
			bufferChanged = self._buffer is not None and buffer is not self._buffer
			if bufferChanged:
				title = pendingChatTitle(
					self._pendingOpenedChatTitle,
					time.monotonic() - self._pendingOpenedChatAt if self._pendingOpenedChatAt else float("inf"),
				)
				self._pendingOpenedChatTitle = ""
				self._pendingOpenedChatAt = 0.0
				try:
					bufferText = buffer.makeTextInfo(textInfos.POSITION_ALL).text
				except Exception:
					bufferText = ""
				conversationChanged = bool(title or looksLikeBlankCodexConversation(bufferText))
				if conversationChanged:
					self._documentSwitchCount += 1
					self._resetTaskState("document changed")
					message = _("Chat opened: {title}").format(title=title) if title else _("New Codex chat opened")
					self._latestMessage = self._latestFullMessage = message
					self._speakOnce(message, "other", "other", brailleMessage=message)
					log.info("Codex Status Announcer detected a newly opened chat document")
				else:
					log.debug("Codex Access Toolkit refreshed the Chromium virtual buffer without resetting task state")
			self._buffer = buffer
			if wasMissing:
				log.info("Codex Status Announcer attached to %s", type(buffer).__name__)
			if not self._monitoringAnnounced:
				self._monitoringAnnounced = True
				conf = _settings()
				_send(_("Codex status monitoring active"), conf["speech"], conf["braille"], None, False)
			return

	def _updateAppFocusState(self, obj):
		appFocused = _isChatGPTObject(obj)
		self._setChatMessageShortcutBindings(appFocused)
		self._appFocusState, cue = focusStateTransition(self._appFocusState, appFocused)
		conf = _settings()
		if not cue or self._paused or not conf["monitoringFocusClicks"] or not conf["soundWhenSpeechUnavailable"]:
			return
		category = "monitoringActive" if cue == "active" else "monitoringInactive"
		_playProgressSound(category, cue, conf["progressSoundStyle"], conf["clickVolume"])
		self._lastProgressSoundAt = time.monotonic()

	def _trackPromptSubmission(self, obj):
		try:
			isEditable = obj.role == Role.EDITABLETEXT
		except Exception:
			return False
		if not isEditable or not _isCodexPromptObject(obj):
			return False
		valueRead = False
		text = ""
		try:
			value = obj.value
			if value is not None:
				valueRead = True
				text = str(value)
		except Exception:
			pass
		if not text.strip():
			try:
				text = str(obj.makeTextInfo(textInfos.POSITION_ALL).text or "")
				valueRead = True
			except Exception:
				pass
		if not valueRead:
			return False
		self._promptHadText, submitted = promptSubmissionTransition(self._promptHadText, bool(text.strip()))
		if not submitted:
			return False
		self._beginPromptSubmission("prompt became empty")
		return True

	def _beginPromptSubmission(self, reason):
		if self._pluginProgressOwnedBusy:
			# A real task supersedes installation-owned background state. Otherwise a
			# later installation completion could incorrectly end the new task.
			self._pluginProgressOwnedBusy.clear()
			self._setBusy(False, "prompt superseded plugin installation")
		if self._busy:
			return
		self._latestMessage = ""
		self._latestFullMessage = ""
		self._lastMessage = ""
		self._lastMessageAt = 0.0
		self._backgroundPulseCount = 0
		self._pendingResponseCompletionAt = 0.0
		self._lastSubmissionSignal = reason
		self._active = True
		self._activeCategory = "working"
		self._setBusy(True, reason)
		conf = _settings()
		if conf["promptSubmissionClick"] and not self._paused:
			mode = conf[CATEGORY_OUTPUT_CONFIG["working"]]
			actions = categoryOutputActions(mode, conf["speech"], conf["braille"], conf["soundWhenSpeechUnavailable"])
			if actions["sound"]:
				_playProgressSound(
					"submission", _("Prompt submitted"), conf["progressSoundStyle"], conf["clickVolume"],
				)
				self._lastProgressSoundAt = time.monotonic()
		else:
			self._announceContinuousWorkingClick(force=True)
		log.info("Codex Status Announcer submission detected: %s", reason)

	def _queueResponseCompletion(self):
		if self._busy and not self._pendingResponseCompletionAt:
			self._pendingResponseCompletionAt = time.monotonic()
			log.debug("Codex Status Announcer queued response completion candidate")

	def _latestButtonStatus(self, info):
		latest = ""
		latestUserMessageNumber = None
		stopControlVisible = False
		latestResponseMarker = None
		buttonDepth = 0
		buttonText = []
		buttonName = ""
		unknown = []
		inRecents = False
		recentsSeen = False
		recentTitles = []
		inArchived = False
		archivedSeen = False
		archivedTitles = []
		for item in info.getTextWithFields():
			if isinstance(item, str):
				plainText = " ".join(item.split())
				if not inRecents and plainText.casefold() == "recents":
					inRecents = recentsSeen = True
				if plainText.casefold() == "archived chats":
					inArchived = archivedSeen = True
				if plainText.lower().startswith("response complete:"):
					# Python's per-process hash avoids retaining or logging response text.
					latestResponseMarker = hash(plainText)
				if buttonDepth:
					buttonText.append(item)
				continue
			command = getattr(item, "command", "")
			field = getattr(item, "field", {}) or {}
			if command == "controlStart":
				role = field.get("role")
				fieldName = " ".join(str(field.get("name", "") or "").split())
				if inRecents and role == Role.LANDMARK and fieldName.casefold() == "main":
					inRecents = False
				if inArchived and role == Role.LANDMARK and fieldName.casefold() == "main":
					inArchived = False
				if buttonDepth:
					buttonDepth += 1
				elif role == Role.BUTTON:
					buttonDepth, buttonText, buttonName = 1, [], field.get("name", "")
			elif command == "controlEnd" and buttonDepth:
				buttonDepth -= 1
				if buttonDepth == 0:
					textLabel = " ".join("".join(buttonText).split())
					historyLabel = textLabel or " ".join(str(buttonName or "").split())
					if inRecents and historyLabel and historyLabel.casefold() not in (
						"recents", "open profile menu", "new chat", "view activity",
					) and historyLabel not in recentTitles:
						recentTitles.append(historyLabel)
					archivedKey = historyLabel.casefold()
					if inArchived and historyLabel and archivedKey not in (
						"archived chats", "close", "cancel", "done", "delete", "unarchive",
					) and not archivedKey.startswith(("delete ", "unarchive ")) and historyLabel not in archivedTitles:
						archivedTitles.append(historyLabel)
					for candidate in (textLabel, buttonName):
						if isStopControlLabel(candidate):
							stopControlVisible = True
						number = userMessageNumber(candidate)
						if number is not None:
							latestUserMessageNumber = max(latestUserMessageNumber or number, number)
					label = firstStatusLabel(textLabel, buttonName)
					if label:
						latest = label
					elif textLabel or buttonName:
						candidate = textLabel or buttonName
						if not isKnownNonStatusButton(candidate) and not isStopControlLabel(candidate):
							unknown.append(candidate)
		if recentsSeen:
			self._chatHistoryCache = tuple(recentTitles)
		if archivedSeen:
			self._archivedChatHistoryCache = tuple(archivedTitles)
		if _settings()["diagnosticLogging"] and unknown:
			now = time.monotonic()
			# Arbitrary button labels can contain private task titles. Keep only
			# ephemeral hashes for change detection and log non-content metadata.
			snapshot = tuple((len(x), hash(x)) for x in unknown[-5:])
			if shouldLogDiagnosticSnapshot(snapshot, self._lastUnknownButtons, now - self._lastUnknownButtonsAt):
				log.debug(
					"Codex Status Announcer unrecognized buttons: count=%d, lengths=%s",
					len(unknown), [len(x) for x in unknown[-5:]],
				)
				self._lastUnknownButtons = snapshot
				self._lastUnknownButtonsAt = now
		self._latestUserMessageNumber, submitted = userMessageSubmissionTransition(
			self._latestUserMessageNumber, latestUserMessageNumber,
		)
		self._pendingUserMessageIncrease, confirmedSubmission = confirmedUserMessageSubmission(
			self._pendingUserMessageIncrease, submitted, stopControlVisible,
		)
		if confirmedSubmission:
			self._beginPromptSubmission("new user message detected")
		if stopControlVisible and self._promptHadText and not self._busy:
			self._promptHadText = False
			self._beginPromptSubmission("Send button activated")
		self._stopControlVisible, stopped = stopControlTransition(self._stopControlVisible, stopControlVisible)
		if stopped and self._busy and not latest:
			self._setBusy(False, "stop control disappeared")
		self._latestResponseMarker, self._responseMarkerInitialized, responseCompleted = responseCompletionTransition(
			self._latestResponseMarker, self._responseMarkerInitialized, latestResponseMarker, self._busy,
		)
		if responseCompleted:
			self._queueResponseCompletion()
		return latest

	def _shouldAnnounce(self, label, category):
		conf = _settings()
		if not conf[CATEGORY_SETTING[category]] or conf[CATEGORY_OUTPUT_CONFIG.get(category, "outputOther")] == "off":
			return False
		seconds = elapsedSeconds(label)
		if category == "working" and seconds is not None:
			interval = conf["workingIntervalSeconds"]
			return seconds == 0 or seconds % interval == 0
		return True

	def _announceLabel(self, label):
		category, safeMessage = statusDetails(label)
		if not category:
			return
		# Explicit Codex activity owns the busy state from this point onward.
		self._pluginProgressOwnedBusy.clear()
		# New work supersedes a tentative virtual-buffer completion. Intermediate
		# completion labels must preserve it so trailing Chromium events cannot
		# leave the continuous Working sound active indefinitely.
		if supersedesResponseCompletionCandidate(label):
			self._pendingResponseCompletionAt = 0.0
		stateCategory = category if category != "completion" or isTaskCompletionLabel(label) else ""
		self._setBusy(nextBusyState(self._busy, stateCategory), category)
		if category != "completion":
			self._activeCategory = category
		elif not isTaskCompletionLabel(label):
			self._activeCategory = intermediateCompletionCategory(label) or self._activeCategory
		if not self._shouldAnnounce(label, category):
			return
		conf = _settings()
		message = statusMessage(
			label, _, conf["verbosity"], conf["redactSensitive"], conf["fullSpeechProfile"],
			conf["minimalSpeechProfile"],
		)
		brailleMessage = brailleStatusMessage(label, _, conf["brailleDetail"], conf["redactSensitive"])
		self._latestFullMessage = brailleMessage
		if category == "command" and conf["verbosity"] == "full":
			message, shortened = formatCommandSpeech(
				message, conf["commandPunctuation"], conf["maximumSpokenCommandCharacters"],
			)
			if shortened:
				message += _(" Complete command available with Copy latest full Codex progress.")
		priority = announcementPriority(category, message)
		action = soundKey(category, message) if category == "completion" else category
		message = _customizeAnnouncement(message, action)
		log.info("Codex Status Announcer detected activity: %s", safeMessage)
		self._latestMessage = message
		fallbackPlayed = self._speakOnce(message, category, action, priority, brailleMessage)
		if fallbackPlayed:
			self._lastProgressSoundAt = time.monotonic()
		self._lastHeartbeatAt = time.monotonic()
		completionMode = conf[CATEGORY_OUTPUT_CONFIG["completion"]]
		if category == "completion" and conf["completionSound"] and completionMode in ("all", "sound") and not fallbackPlayed:
				_safeBeep(880, 80)

	def _poll(self):
		try:
			self._nextPollAt = 0.0
			self._lastPollAt = time.monotonic()
			self._rememberBuffer(api.getFocusObject())
			if not self._buffer:
				return
			now = time.monotonic()
			if self._busy and self._busyStartedAt and now - self._busyStartedAt >= _settings()["maximumBusyMinutes"] * 60:
				self._setBusy(False, "maximum activity timeout")
			label = self._latestButtonStatus(self._buffer.makeTextInfo(textInfos.POSITION_ALL))
			if label and label != self._lastLabel and supersedesResponseCompletionCandidate(label):
				self._pendingResponseCompletionAt = 0.0
			if shouldFinalizeResponseCompletion(
				self._pendingResponseCompletionAt,
				now - self._pendingResponseCompletionAt if self._pendingResponseCompletionAt else 0.0,
				RESPONSE_COMPLETION_SETTLE_SECONDS,
				self._busy, self._stopControlVisible, label,
			):
				self._pendingResponseCompletionAt = 0.0
				self._haveBaseline, self._lastLabel = True, "Response complete"
				self._announceLabel("Response complete")
				label = ""
			self._active = bool(label) or self._busy
			if not label:
				if not self._busy:
					self._lastHeartbeatAt = 0.0
				if not self._haveBaseline:
					self._haveBaseline, self._lastLabel = True, ""
					log.info("Codex Status Announcer baseline established: no activity")
				elif self._lastLabel:
					self._lastLabel = ""
					log.debug("Codex Status Announcer activity cleared")
				if now - self._lastNoStatusLogAt >= 30.0:
					self._lastNoStatusLogAt = now
					log.debug("Codex Status Announcer scanned buffer; no activity button found")
				if self._busy:
					# Status controls can disappear while computer use or another autonomous
					# action continues. Do not let that create minutes of unexplained silence.
					self._announceBackgroundPulse()
				return
			if not self._haveBaseline:
				self._lastLabel, self._haveBaseline = label, True
				baselineCategory = statusDetails(label)[0]
				stateCategory = baselineCategory if baselineCategory != "completion" or isTaskCompletionLabel(label) else ""
				self._setBusy(nextBusyState(self._busy, stateCategory), "baseline")
				self._lastHeartbeatAt = time.monotonic()
				return
			if label != self._lastLabel:
				self._lastLabel = label
				self._announceLabel(label)
			else:
				self._announceBackgroundPulse()
		except Exception:
			log.debugWarning("Codex Status Announcer could not inspect the virtual buffer", exc_info=True)
			self._lastInspectionError = "virtual buffer inspection failed"
			self._setBusy(False, "buffer inspection failed")
			self._buffer = None
		finally:
			if self._timer is not None:
				self._announceContinuousWorkingClick()
				delay = pollDelay(self._active, _settings()["idlePollMs"])
				self._timer = wx.CallLater(delay, self._poll)
				self._nextPollAt = time.monotonic() + delay / 1000.0

	def _speakOnce(self, message, category="other", soundCategory=None, priority=None, brailleMessage=None):
		if self._paused:
			return False
		now = time.monotonic()
		brailleOutput = brailleMessage if brailleMessage is not None else message
		comparisonMessage = brailleOutput or message or category
		soundDuplicate = shouldSuppressSemanticDuplicate(comparisonMessage, self._lastMessage, now - self._lastMessageAt)
		channelDuplicates = duplicateChannelActions(
			message, brailleOutput, self._lastSpeechMessage, self._lastBrailleMessage,
			now - self._lastSpeechMessageAt, now - self._lastBrailleMessageAt,
		)
		speechDuplicate = channelDuplicates["speech"]
		brailleDuplicate = channelDuplicates["braille"]
		self._lastMessage, self._lastMessageAt = comparisonMessage, now
		conf = _settings()
		mode = conf[CATEGORY_OUTPUT_CONFIG.get(category, "outputOther")]
		actions = categoryOutputActions(mode, conf["speech"], conf["braille"], conf["soundWhenSpeechUnavailable"])
		effectivePriority = priority or announcementPriority(category, message)
		if shouldSuppressRoutineBraille(
			conf["protectBrailleReading"], self._appFocusState, category, effectivePriority,
		):
			actions["braille"] = False
		if category not in ("backgroundPulse1", "backgroundPulse2"):
			self._recordHistory(message, brailleOutput)
		if actions["speech"] and message and not speechDuplicate:
			self._lastSpeechMessage, self._lastSpeechMessageAt = message, now
		if actions["braille"] and brailleOutput and not brailleDuplicate:
			self._lastBrailleMessage, self._lastBrailleMessageAt = brailleOutput, now
		if conf["diagnosticLogging"] and speechDuplicate and brailleDuplicate and soundDuplicate:
			log.debug("Codex Access Toolkit suppressed duplicate %s event on all enabled channels", category)
		return _send(
			message, actions["speech"] and bool(message) and not speechDuplicate,
			actions["braille"] and bool(brailleOutput) and not brailleDuplicate,
			soundCategory or category, actions["sound"] and not soundDuplicate,
			priority=effectivePriority, brailleMessage=brailleOutput,
		)

	def _setBusy(self, busy, reason):
		busy = bool(busy)
		if busy == self._busy:
			self._lastStateReason = reason
			return
		self._busy = busy
		self._lastStateReason = reason
		if busy:
			self._busyStartedAt = time.monotonic()
			self._lastProgressSoundAt = self._busyStartedAt
			self._continuousClicksStartAt = self._busyStartedAt + _settings()["workingClickStartDelayMs"] / 1000.0
		log.info(
			"Codex Status Announcer background state: %s (%s)",
			"active" if busy else "idle", reason,
		)
		if not busy:
			self._lastHeartbeatAt = 0.0
			self._busyStartedAt = 0.0
			self._continuousClicksStartAt = 0.0

	def _announceContinuousWorkingClick(self, force=False):
		conf = _settings()
		now = time.monotonic()
		if not force and now < self._continuousClicksStartAt:
			return
		mode = conf[CATEGORY_OUTPUT_CONFIG.get(self._activeCategory, "outputOther")]
		actions = categoryOutputActions(mode, conf["speech"], conf["braille"], conf["soundWhenSpeechUnavailable"])
		interval = 0.0 if force else conf["workingClickIntervalMs"] / 1000.0
		if not shouldPlayContinuousWorkingClick(
			self._busy, conf["continuousWorkingClicks"] and not self._paused,
			conf["progressSoundStyle"], actions["sound"],
			now - self._lastProgressSoundAt, interval,
		):
			return
		_playProgressSound("working", _("Working"), conf["progressSoundStyle"], conf["clickVolume"])
		self._lastProgressSoundAt = now

	def _announceBackgroundPulse(self):
		conf = _settings()
		if not self._busy or not conf["announceHeartbeat"]:
			return
		now = time.monotonic()
		if not self._lastHeartbeatAt:
			self._lastHeartbeatAt = now
			return
		if now - self._lastHeartbeatAt < conf["workingIntervalSeconds"]:
			return
		self._lastHeartbeatAt = now
		self._backgroundPulseCount += 1
		toneCategory = "backgroundPulse1" if self._backgroundPulseCount % 2 else "backgroundPulse2"
		elapsed = max(0, round(now - self._busyStartedAt)) if self._busyStartedAt else 0
		# Use the original detailed status, not customized speech. A custom template
		# may omit words such as "finished" and must not make a completed file step
		# sound as though it is still editing.
		name = _(backgroundActivityName(self._activeCategory, self._latestFullMessage))
		duration = formatElapsedDuration(elapsed, _)
		fullMessage = _("{activity} still running, {duration}").format(activity=name, duration=duration)
		minimalProfile = conf["minimalSpeechProfile"]
		if conf["verbosity"] == "minimal" and minimalProfile == "essential":
			message = ""
		elif conf["verbosity"] == "minimal" and minimalProfile == "balanced" and elapsed < 30:
			message = _("{activity} still running").format(activity=name)
		else:
			message = fullMessage
		if message:
			message = _customizeAnnouncement(message, toneCategory, name, elapsed)
		mode = conf[CATEGORY_OUTPUT_CONFIG.get(self._activeCategory, "outputOther")]
		actions = categoryOutputActions(mode, conf["speech"], conf["braille"], conf["soundWhenSpeechUnavailable"])
		if shouldSuppressRoutineBraille(
			conf["protectBrailleReading"], self._appFocusState, toneCategory, "low",
		):
			actions["braille"] = False
		if not self._paused:
			played = _send(
				message, actions["speech"] and bool(message), actions["braille"], toneCategory,
				actions["sound"], priority="low", brailleMessage=fullMessage,
			)
			if played:
				self._lastProgressSoundAt = time.monotonic()

	def _announceStatus(self, obj):
		if getattr(obj, "role", None) != Role.BUTTON or not _isCodexObject(obj):
			return
		label = getattr(obj, "name", "")
		if statusDetails(label)[0]:
			self._haveBaseline, self._lastLabel = True, label
			self._announceLabel(label)

	def _announceCommentary(self, obj):
		if not _settings()["announceCommentary"] or not _isCodexObject(obj):
			return
		if getattr(obj, "role", None) in (Role.BUTTON, Role.EDITABLETEXT):
			return
		text = " ".join(str(getattr(obj, "name", "") or getattr(obj, "value", "") or "").split())
		if not text:
			return
		category = statusDetails(text)[0]
		if category:
			# Chromium can expose completion and progress as a non-button live region.
			# Route it through the normal state machine instead of discarding it as
			# status-like commentary. Avoid repeating response text in Full mode.
			label = "Response complete" if text.lower().startswith("response complete") else text
			if label == "Response complete":
				self._queueResponseCompletion()
				return
			if category == "completion" and self._haveBaseline and label == self._lastLabel:
				return
			self._haveBaseline, self._lastLabel = True, label
			self._announceLabel(label)
			return
		key = id(obj)
		if key not in self._commentaryOffsets and len(self._commentaryOffsets) >= 256:
			self._commentaryOffsets.pop(next(iter(self._commentaryOffsets)))
		previousText, offset = self._commentaryOffsets.get(key, ("", 0))
		if previousText and not text.startswith(previousText[:offset]):
			offset = 0
		message, newOffset = completedTextDelta(text, offset)
		self._commentaryOffsets[key] = (text, newOffset)
		if message:
			# Final-response commentary can arrive after the completion control.
			# It may refresh an active task, but must never restart one.
			self._pluginProgressOwnedBusy.clear()
			self._setBusy(nextBusyState(self._busy, commentary=True), "commentary")
			if self._busy:
				self._lastHeartbeatAt = time.monotonic()
			log.info("Codex Status Announcer detected activity: Commentary update")
			conf = _settings()
			fullMessage = redactSensitive(message) if conf["redactSensitive"] else message
			message = fullMessage
			if conf["verbosity"] == "minimal":
				profile = conf["minimalSpeechProfile"]
				if profile == "essential":
					message = ""
				else:
					wordLimit = 18 if profile == "balanced" else 30
					words = message.split()
					message = " ".join(words[:wordLimit]) + ("…" if len(words) > wordLimit else "")
			if message:
				message = _customizeAnnouncement(message, "commentary")
			self._latestMessage = message or fullMessage
			self._latestFullMessage = fullMessage
			self._speakOnce(message, "commentary", brailleMessage=fullMessage)

	@script(description=_("Report current Codex activity or repeat the latest message"))
	def script_repeatLatestStatus(self, gesture):
		elapsed = time.monotonic() - self._busyStartedAt if self._busyStartedAt else 0
		message = currentActivitySummary(self._busy, self._activeCategory, self._latestMessage, elapsed, _)
		conf = _settings()
		_send(
			message, conf["speech"], conf["braille"], "other", conf["soundWhenSpeechUnavailable"],
			brailleMessage=self._latestFullMessage or message,
		)

	@script(description=_("Toggle Minimal and Full Codex announcements"))
	def script_toggleVerbosity(self, gesture):
		conf = _settings()
		conf["verbosity"] = "minimal" if conf["verbosity"] == "full" else "full"
		message = _("Codex announcements: {mode}").format(mode=conf["verbosity"])
		_send(message, conf["speech"], conf["braille"], "other", conf["soundWhenSpeechUnavailable"])

	@script(description=_("Pause or resume Codex announcements"))
	def script_togglePause(self, gesture):
		self._paused = not self._paused
		ui.message(_("Codex announcements paused") if self._paused else _("Codex announcements resumed"))

	@script(description=_("Read the previous Codex announcement"))
	def script_previousHistory(self, gesture):
		self._historyMessage(-1)

	@script(description=_("Read the next Codex announcement"))
	def script_nextHistory(self, gesture):
		self._historyMessage(1)

	@script(description=_("Show Codex announcement history"))
	def script_showHistory(self, gesture):
		if not self._speechHistory and not self._brailleHistory:
			ui.message(_("No Codex announcement history is available"))
			return
		sections = []
		if self._speechHistory:
			sections.append(_("Speech history") + "\n" + "\n".join(self._speechHistory.items()))
		if self._brailleHistory and self._brailleHistory.items() != self._speechHistory.items():
			sections.append(_("Braille history") + "\n" + "\n".join(self._brailleHistory.items()))
		ui.browseableMessage("\n\n".join(sections), title=_("Codex Access Toolkit announcement history"))

	@script(description=_("Clear Codex announcement history"))
	def script_clearHistory(self, gesture):
		self._speechHistory.clear()
		self._brailleHistory.clear()
		ui.message(_("Codex announcement history cleared"))

	@script(description=_("Toggle Codex privacy redaction"))
	def script_togglePrivacy(self, gesture):
		conf = _settings()
		conf["redactSensitive"] = not conf["redactSensitive"]
		ui.message(_("Codex privacy redaction on") if conf["redactSensitive"] else _("Codex privacy redaction off"))

	@script(description=_("Show sanitized Codex Access Toolkit diagnostics"))
	def script_showDiagnostics(self, gesture):
		ui.browseableMessage(self._diagnosticReport(), title=_("Codex Access Toolkit diagnostics"))

	@script(description=_("Copy sanitized Codex Access Toolkit diagnostics"))
	def script_copyDiagnostics(self, gesture):
		if not wx.TheClipboard.Open():
			ui.message(_("Could not open the clipboard"))
			return
		try:
			wx.TheClipboard.SetData(wx.TextDataObject(self._diagnosticReport()))
			wx.TheClipboard.Flush()
		finally:
			wx.TheClipboard.Close()
		ui.message(_("Sanitized Codex diagnostics copied"))

	@script(description=_("Copy latest full Codex progress"))
	def script_copyLatestFullProgress(self, gesture):
		if not self._latestFullMessage:
			ui.message(_("No complete Codex progress message is available"))
			return
		if not wx.TheClipboard.Open():
			ui.message(_("Could not open the clipboard"))
			return
		try:
			wx.TheClipboard.SetData(wx.TextDataObject(self._latestFullMessage))
			wx.TheClipboard.Flush()
		finally:
			wx.TheClipboard.Close()
		ui.message(_("Latest full Codex progress copied"))

	@script(description=_("Run Codex Access Toolkit compatibility self-test"))
	def script_runCompatibilitySelfTest(self, gesture):
		checks = [
			_("Global plugin loaded: yes"),
			_("Codex monitoring attached: {value}").format(value=_("yes") if self._buffer else _("no")),
			_("Speech enabled: {value}").format(value=_("yes") if _settings()["speech"] else _("no")),
			_("Braille enabled: {value}").format(value=_("yes") if _settings()["braille"] else _("no")),
			_("Sound inventory: {count} files").format(count=len(list((Path(__file__).parent / "sounds").rglob("*.wav")))),
			_("Recent chats cached: {count}").format(count=len(self._chatHistoryCache)),
			_("Archived chats cached: {count}").format(count=len(self._loadArchivedChatHistory()[0])),
			_("Last inspection error: {value}").format(value=self._lastInspectionError),
		]
		_showBrowseableMessageAtTop("\n".join(checks), _("Codex Access Toolkit — compatibility self-test"))

	@script(description=_("Open Codex usage statistics"))
	def script_openUsageStatistics(self, gesture):
		_openUsageDashboard(_("Opening Codex usage statistics"))

	@script(description=_("Open Codex usage credits"))
	def script_openUsageCredits(self, gesture):
		_openUsageDashboard(_("Opening Codex usage credits. No purchase will be made automatically."))

	@script(description=_("Open searchable and arrow-navigable Codex chat history"))
	def script_openChatHistory(self, gesture):
		"""Show bounded, searchable Recent and Archived chat lists."""
		focus = api.getFocusObject()
		if not _isChatGPTObject(focus):
			ui.message(_("Move to ChatGPT Codex before opening chat history"))
			return
		try:
			self._rememberBuffer(focus)
			if not self._buffer:
				ui.message(_("Codex chat history is not available"))
				return
			recentTitles = self._chatHistoryTitles()
			archivedTitles, archivedLoaded = self._loadArchivedChatHistory()
			if not recentTitles and not archivedTitles:
				ui.message(_("No recent chats are cached yet. Wait a moment in Codex and try again"))
				return
			if self._chatHistoryDialog:
				self._chatHistoryDialog.Raise()
				self._chatHistoryDialog.search.SetFocus()
				return
			gui.mainFrame.prePopup()
			try:
				self._chatHistoryDialog = ChatHistoryDialog(
					gui.mainFrame, recentTitles, archivedTitles, archivedLoaded,
					self._refreshChatHistoryData, self._queueChatHistoryAction, self._chatHistoryClosed,
				)
				self._chatHistoryDialog.Show()
			except Exception:
				self._chatHistoryDialog = None
				gui.mainFrame.postPopup()
				raise
			log.info(
				"Codex Status Announcer displayed %d recent and %d archived chats",
				len(recentTitles), len(archivedTitles),
			)
		except Exception:
			log.debugWarning("Codex Status Announcer could not display chat history", exc_info=True)
			ui.message(_("Codex chat history could not be opened"))

	def event_gainFocus(self, obj, nextHandler):
		nextHandler()
		try:
			self._updateAppFocusState(obj)
			self._rememberBuffer(obj)
			isPrompt = _isCodexPromptObject(obj)
			if isPrompt:
				self._trackPromptSubmission(obj)
			# ChatGPT briefly focuses an intermediate section after Enter and before
			# returning to the now-empty prompt. Preserve draft/submission state across
			# those in-app focus events; _resetTaskState handles real task switches.
			if _isChatGPTObject(obj):
				self._schedulePoll()
		except Exception:
			log.debugWarning("Codex Access Toolkit focus-event handling failed", exc_info=True)

	def event_foreground(self, obj, nextHandler):
		nextHandler()
		try:
			self._updateAppFocusState(obj)
			self._rememberBuffer(obj)
			if _isChatGPTObject(obj):
				self._schedulePoll()
		except Exception:
			log.debugWarning("Codex Access Toolkit foreground-event handling failed", exc_info=True)

	def event_nameChange(self, obj, nextHandler):
		nextHandler()
		try:
			self._rememberBuffer(obj)
			self._schedulePopupDialogFocus(obj)
			self._announceStatus(obj)
			if _isChatGPTObject(obj):
				self._schedulePoll()
		except Exception:
			log.debugWarning("Codex Access Toolkit name-change handling failed", exc_info=True)

	def event_valueChange(self, obj, nextHandler):
		nextHandler()
		try:
			submitted = self._trackPromptSubmission(obj)
			self._announcePluginInstallProgress(obj)
			self._announceStatus(obj)
			if _isChatGPTObject(obj) and (submitted or getattr(obj, "role", None) != Role.EDITABLETEXT):
				self._schedulePoll()
		except Exception:
			log.debugWarning("Codex Access Toolkit value-change handling failed", exc_info=True)

	def event_liveRegionChange(self, obj, nextHandler):
		nextHandler()
		try:
			self._schedulePopupDialogFocus(obj)
			self._announceStatus(obj)
			self._announceCommentary(obj)
			if _isChatGPTObject(obj):
				self._schedulePoll()
		except Exception:
			log.debugWarning("Codex Access Toolkit live-region handling failed", exc_info=True)

	def event_show(self, obj, nextHandler):
		nextHandler()
		try:
			self._schedulePopupDialogFocus(obj)
			self._announcePluginInstallProgress(obj)
			self._announceStatus(obj)
			if _isChatGPTObject(obj):
				self._schedulePoll()
		except Exception:
			log.debugWarning("Codex Access Toolkit show-event handling failed", exc_info=True)

	def event_textChange(self, obj, nextHandler):
		nextHandler()
		try:
			submitted = self._trackPromptSubmission(obj)
			if _isChatGPTObject(obj) and (submitted or getattr(obj, "role", None) != Role.EDITABLETEXT):
				self._schedulePoll()
		except Exception:
			log.debugWarning("Codex Access Toolkit text-change handling failed", exc_info=True)
