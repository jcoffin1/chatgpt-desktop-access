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

from .core import AnnouncementHistory, CATEGORY_SETTING, announcementPriority, categoryOutputActions, changelogForDisplay, chatTitleMatches, completedTextDelta, confirmedUserMessageSubmission, elapsedSeconds, firstStatusLabel, focusStateTransition, formatCommandSpeech, formatCustomAnnouncement, intermediateCompletionCategory, isKnownNonStatusButton, isStopControlLabel, isTaskCompletionLabel, loadArchivedThreads, nextBusyState, outputActions, pollDelay, previewSelection, promptControlKind, promptSubmissionTransition, redactSensitive, repairConfigurationValues, responseCompletionTransition, shouldFinalizeResponseCompletion, shouldLogDiagnosticSnapshot, shouldPlayContinuousWorkingClick, shouldSuppressSemanticDuplicate, soundKey, statusDetails, statusMessage, stopControlTransition, tonePattern, userMessageNumber, userMessageSubmissionTransition, viewerTitleMatches

addonHandler.initTranslation()

CONFIG_SECTION = "codexStatusAnnouncer"
ADDON_VERSION = "2026.1.17"
CODEX_USAGE_URL = "https://chatgpt.com/codex/settings/usage"
CURRENT_RELEASE_NOTES = _(
	"Version 2026.1.17\n\n"
	"What's new:\n"
	"• Completed a whole-add-on reliability and accessibility audit.\n"
	"• Repaired every imported output, timing, boolean, and application setting safely.\n"
	"• Prevented stale progress from carrying into a new task or document.\n"
	"• Hardened chat-history activation and add-on reload cleanup.\n"
	"• Preserved native Codex control descriptions and added no prompt-control gestures."
)
VERBOSITY_CHOICES = ("minimal", "full")
FULL_SPEECH_PROFILE_CHOICES = ("standard", "developer", "raw")
MINIMAL_SPEECH_PROFILE_CHOICES = ("essential", "balanced", "informative")
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
_lastConfigurationRepairs = ()
config.conf.spec[CONFIG_SECTION] = {
	"verbosity": "option('minimal', 'full', default='full')",
	"fullSpeechProfile": "option('standard', 'developer', 'raw', default='developer')",
	"minimalSpeechProfile": "option('essential', 'balanced', 'informative', default='balanced')",
	"commandPunctuation": "option('normal', 'enhanced', 'literal', default='enhanced')",
	"maximumSpokenCommandCharacters": "integer(default=240, min=40, max=2000)",
	"speech": "boolean(default=True)",
	"braille": "boolean(default=True)",
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
		"speech": True, "braille": True, "redactSensitive": False,
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
		log.warning("Codex Status Announcer repaired configuration fields: %s", ", ".join(repaired))
	_lastConfigurationRepairs = repaired
	return tuple(repaired)


def _customizeAnnouncement(message, action, activity="", seconds=0, values=None):
	conf = values or _settings()
	key = ANNOUNCEMENT_CONFIG_BY_ACTION.get(action)
	return formatCustomAnnouncement(conf.get(key, "") if key else "", message, activity, seconds)


def _playProgressTone(category, message=""):
	delay = 0
	for index, (frequency, duration) in enumerate(tonePattern(category, message)):
		if index == 0:
			tones.beep(frequency, duration)
		else:
			wx.CallLater(delay, tones.beep, frequency, duration)
		delay += duration + 25


def _playProgressSound(category, message="", style="clicks", volume="normal"):
	if style == "tones":
		_playProgressTone(category, message)
		return
	path = os.path.join(os.path.dirname(__file__), "sounds", volume, f"{soundKey(category, message)}.wav")
	try:
		nvwave.playWaveFile(path)
	except Exception:
		log.debugWarning("Codex Status Announcer could not play click earcon; using tones", exc_info=True)
		_playProgressTone(category, message)


def _speechIsOff():
	try:
		return speech.getState().speechMode == speech.SpeechMode.off
	except (AttributeError, RuntimeError):
		return False


def _send(message, speak=True, showBraille=True, toneCategory=None, progressSoundsEnabled=True, soundStyle=None, clickVolume=None, priority="normal", brailleMessage=None):
	actions = outputActions(speak, _speechIsOff(), showBraille, progressSoundsEnabled, toneCategory)
	if actions["speech"]:
		if priority == "urgent":
			try:
				speech.cancelSpeech()
			except AttributeError:
				pass
		speech.speakMessage(message)
	if actions["braille"]:
		braille.handler.message(message if brailleMessage is None else brailleMessage)
	if actions["tone"]:
		_playProgressSound(
			toneCategory, message, soundStyle or _settings()["progressSoundStyle"],
			clickVolume or _settings()["clickVolume"],
		)
		return True
	return False


def _moveBrowseableMessageToTop(expectedTitle):
	foreground = api.getForegroundObject()
	foregroundName = str(getattr(foreground, "name", "") or "")
	if not viewerTitleMatches(expectedTitle, foregroundName):
		log.debug("Codex Status Announcer did not move document focus; expected viewer is not foreground")
		return
	keyboardHandler.KeyboardInputGesture.fromName("control+home").send()


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
			self._onActionCallback(selection[0], "context", selection[1])
			self.Close()
			return
		evt.Skip()

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
	title = _("Codex Status Announcer")

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
			self, label=_("Play a continuous Working click while Codex is busy"),
		))
		self.continuousWorkingClicks.SetValue(conf["continuousWorkingClicks"])
		self.workingClickIntervalMs = helper.addLabeledControl(
			_("Working click interval (milliseconds):"), wx.SpinCtrl,
			min=500, max=5000, initial=conf["workingClickIntervalMs"],
		)
		self.workingClickStartDelayMs = helper.addLabeledControl(
			_("Delay before repeating Working clicks (milliseconds):"), wx.SpinCtrl,
			min=0, max=10000, initial=conf["workingClickStartDelayMs"],
		)
		self.promptSubmissionClick = helper.addItem(wx.CheckBox(
			self, label=_("Play a distinct click when a prompt is submitted"),
		))
		self.promptSubmissionClick.SetValue(conf["promptSubmissionClick"])
		self.monitoringFocusClicks = helper.addItem(wx.CheckBox(
			self, label=_("Play clicks when Codex monitoring becomes active or inactive"),
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
			"Available placeholders: {message}, {activity}, and {seconds}."
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
		brailleMessage = statusMessage(label, _, verbosity, self.redactSensitive.IsChecked(), "developer", "balanced")
		_send(
			speechMessage,
			self.speech.IsChecked(), self.braille.IsChecked(), "command",
			self.progressSounds.IsChecked(),
			SOUND_STYLE_CHOICES[self.progressSoundStyle.GetSelection()],
			CLICK_VOLUME_CHOICES[self.clickVolume.GetSelection()],
			brailleMessage=brailleMessage,
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
			CURRENT_RELEASE_NOTES, _("Codex Status Announcer — current release notes"),
		)

	def _onViewCompleteHistory(self, evt):
		try:
			message = _completeChangelogMessage()
		except Exception:
			log.error("Unable to open the Codex Status Announcer changelog", exc_info=True)
			ui.message(_("The complete release history could not be opened"))
			return
		_showBrowseableMessageAtTop(
			message, _("Codex Status Announcer — complete release history"),
		)

	def _onExportSettings(self, evt):
		with wx.FileDialog(
			self, _("Export Codex Status Announcer settings"),
			wildcard=_("JSON files (*.json)|*.json"), style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
		) as dialog:
			if dialog.ShowModal() != wx.ID_OK:
				return
			path = Path(dialog.GetPath())
		try:
			values = {key: value for key, value in _settings().items() if isinstance(value, (str, int, float, bool))}
			path.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf-8")
		except Exception:
			log.error("Unable to export Codex Status Announcer settings", exc_info=True)
			ui.message(_("Settings could not be exported"))
			return
		ui.message(_("Codex Status Announcer settings exported"))

	def _onImportSettings(self, evt):
		with wx.FileDialog(
			self, _("Import Codex Status Announcer settings"),
			wildcard=_("JSON files (*.json)|*.json"), style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
		) as dialog:
			if dialog.ShowModal() != wx.ID_OK:
				return
			path = Path(dialog.GetPath())
		try:
			if path.stat().st_size > 1024 * 1024:
				raise ValueError("settings file exceeds 1 MB")
			values = json.loads(path.read_text(encoding="utf-8"))
			if not isinstance(values, dict):
				raise ValueError("settings root is not an object")
			conf = _settings()
			for key, value in values.items():
				if key in config.conf.spec[CONFIG_SECTION] and isinstance(value, (str, int, float, bool)):
					conf[key] = value
			_repairConfiguration()
			config.conf.save()
			self._loadControlsFromConfiguration()
		except Exception:
			log.error("Unable to import Codex Status Announcer settings", exc_info=True)
			ui.message(_("Settings could not be imported"))
			return
		ui.message(_("Settings imported and loaded into this panel."))

	def _loadControlsFromConfiguration(self):
		"""Refresh every editable control after an in-place settings import."""
		conf = _settings()
		self.verbosity.SetSelection(VERBOSITY_CHOICES.index(conf["verbosity"]))
		self.fullSpeechProfile.SetSelection(FULL_SPEECH_PROFILE_CHOICES.index(conf["fullSpeechProfile"]))
		self.minimalSpeechProfile.SetSelection(MINIMAL_SPEECH_PROFILE_CHOICES.index(conf["minimalSpeechProfile"]))
		self.commandPunctuation.SetSelection(COMMAND_PUNCTUATION_CHOICES.index(conf["commandPunctuation"]))
		self.maximumSpokenCommandCharacters.SetValue(conf["maximumSpokenCommandCharacters"])
		for name in ("speech", "braille", "redactSensitive", "completionSound", "diagnosticLogging", "announceHeartbeat"):
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
		conf["commandPunctuation"] = COMMAND_PUNCTUATION_CHOICES[self.commandPunctuation.GetSelection()]
		conf["maximumSpokenCommandCharacters"] = self.maximumSpokenCommandCharacters.GetValue()
		for name in ("speech", "braille", "redactSensitive", "completionSound", "diagnosticLogging", "announceHeartbeat"):
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
	appName = getattr(getattr(obj, "appModule", None), "appName", "").lower()
	supported = {name.strip().lower() for name in _settings()["supportedAppNames"].split(",") if name.strip()}
	return appName in supported


def _isCodexObject(obj):
	if not _isChatGPTObject(obj):
		return False
	current = obj
	for _ in range(20):
		if current is None:
			break
		if getattr(current, "role", None) == Role.DOCUMENT and str(getattr(current, "name", "")).strip().lower() == "codex":
			return True
		current = getattr(current, "parent", None)
	return False


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
	scriptCategory = _("Codex Status Announcer")

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		"""Enhance known prompt controls without adding or intercepting gestures."""
		try:
			if obj.role not in (Role.BUTTON, Role.COMBOBOX) or not _isCodexObject(obj):
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
		self._history = AnnouncementHistory(20)
		self._busyStartedAt = 0.0
		self._activeCategory = "other"
		self._lastProgressSoundAt = 0.0
		self._appFocusState = None
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
		self._latestResponseMarker = None
		self._responseMarkerInitialized = False
		self._pendingResponseCompletionAt = 0.0
		self._chatHistoryDialog = None
		self._pendingChatHistoryAction = None
		self._chatHistoryActionTimer = None
		self._chatHistoryCache = ()
		self._archivedChatHistoryCache = ()
		self._archivedChatIds = {}
		self._whatsNewTimer = None
		log.info(
			"Codex Status Announcer 2026.1.17 loaded (verbosity=%s, fullProfile=%s, minimalProfile=%s, soundStyle=%s)",
			_settings()["verbosity"], _settings()["fullSpeechProfile"],
			_settings()["minimalSpeechProfile"], _settings()["progressSoundStyle"],
		)
		if CodexStatusAnnouncerSettingsPanel not in NVDASettingsDialog.categoryClasses:
			NVDASettingsDialog.categoryClasses.append(CodexStatusAnnouncerSettingsPanel)
		self._timer = wx.CallLater(100, self._poll)
		self._whatsNewTimer = wx.CallLater(1500, self._showWhatsNewIfNeeded)

	def terminate(self):
		if self._timer:
			self._timer.Stop()
			self._timer = None
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
		self._pendingChatHistoryAction = None
		try:
			NVDASettingsDialog.categoryClasses.remove(CodexStatusAnnouncerSettingsPanel)
		except ValueError:
			pass
		super().terminate()

	def _schedulePoll(self, delay=10):
		if self._timer:
			self._timer.Stop()
		self._timer = wx.CallLater(delay, self._poll)

	def _showWhatsNewIfNeeded(self):
		self._whatsNewTimer = None
		conf = _settings()
		if conf["lastShownVersion"] == ADDON_VERSION:
			return
		_showBrowseableMessageAtTop(
			CURRENT_RELEASE_NOTES, _("Codex Status Announcer — what's new"),
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
		self._history.clear()
		self._latestMessage = ""
		self._latestFullMessage = ""
		self._lastMessage = ""
		self._lastMessageAt = 0.0
		self._activeCategory = "other"
		self._backgroundPulseCount = 0

	def _recordHistory(self, message):
		message = str(message or "").strip()
		self._history.add(message)

	def _historyMessage(self, offset):
		if not self._history:
			ui.message(_("No Codex announcement history is available"))
			return
		ui.message(self._history.move(offset))

	def _diagnosticReport(self):
		conf = _settings()
		return _(
			"Version: 2026.1.17\nVerbosity: {verbosity}\nFull speech profile: {profile}\nMinimal speech profile: {minimalProfile}\nSound style: {style}\nClick volume: {volume}\n"
			"Monitoring attached: {attached}\nBackground state: {state}\nPaused: {paused}\n"
			"Active category: {category}\nLast state reason: {reason}\nLast submission signal: {signal}\n"
			"Codex document switches: {switches}\nLast inspection error: {error}\n"
			"History entries: {history}\nRecent chats cached: {recent}\nArchived chats cached: {archived}\n"
			"Configuration repairs this session: {repairs}\nSupported applications: {apps}\n"
			"Speech: {speech}\nBraille: {braille}\nProgress sounds: {sounds}"
		).format(
			verbosity=conf["verbosity"], profile=conf["fullSpeechProfile"], minimalProfile=conf["minimalSpeechProfile"],
			style=conf["progressSoundStyle"], volume=conf["clickVolume"],
			attached=bool(self._buffer), state="active" if self._busy else "idle", paused=self._paused,
			category=self._activeCategory, reason=self._lastStateReason, signal=self._lastSubmissionSignal,
			switches=self._documentSwitchCount, error=self._lastInspectionError,
			history=len(self._history), recent=len(self._chatHistoryCache), archived=len(self._archivedChatHistoryCache),
			repairs=", ".join(_lastConfigurationRepairs) or "none", apps=conf["supportedAppNames"], speech=conf["speech"],
			braille=conf["braille"], sounds=conf["soundWhenSpeechUnavailable"],
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
			entries = loadArchivedThreads(codexRoot)
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
		return obj if chatTitleMatches(title, getattr(obj, "name", "")) else None

	def _performChatHistoryAction(self, title, action, source="recent"):
		try:
			button = self._chatButtonObject(title)
			if button is None:
				raise LookupError("selected chat button not found")
			if action == "context":
				button.setFocus()
				keyboardHandler.KeyboardInputGesture.fromName("shift+f10").send()
			else:
				button.doAction()
			log.info("Codex Status Announcer performed chat history action: %s", action)
		except Exception:
			log.debugWarning("Codex Status Announcer could not act on the selected chat", exc_info=True)
			if source == "archived":
				ui.message(_("Open ChatGPT Settings, then Archived chats, before acting on this archived chat"))
			else:
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
			if self._buffer is not None and buffer is not self._buffer:
				self._documentSwitchCount += 1
				self._resetTaskState("document changed")
			self._buffer = buffer
			if wasMissing:
				log.info("Codex Status Announcer attached to %s", type(buffer).__name__)
			if not self._monitoringAnnounced:
				self._monitoringAnnounced = True
				conf = _settings()
				_send(_("Codex status monitoring active"), conf["speech"], conf["braille"], None, False)
			return

	def _updateAppFocusState(self, obj):
		self._appFocusState, cue = focusStateTransition(self._appFocusState, _isChatGPTObject(obj))
		if not cue or not _settings()["monitoringFocusClicks"]:
			return
		category = "monitoringActive" if cue == "active" else "monitoringInactive"
		_playProgressSound(category, cue, "clicks", _settings()["clickVolume"])
		self._lastProgressSoundAt = time.monotonic()

	def _trackPromptSubmission(self, obj):
		try:
			isEditable = obj.role == Role.EDITABLETEXT
		except Exception:
			return False
		if not isEditable or not _isCodexObject(obj):
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
		if conf["promptSubmissionClick"] and not self._paused and conf["progressSoundStyle"] == "clicks":
			mode = conf[CATEGORY_OUTPUT_CONFIG["working"]]
			actions = categoryOutputActions(mode, conf["speech"], conf["braille"], conf["soundWhenSpeechUnavailable"])
			if actions["sound"]:
				_playProgressSound("submission", _("Prompt submitted"), "clicks", conf["clickVolume"])
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
						"open profile menu", "new chat", "view activity",
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
		# Any explicit status supersedes a tentative virtual-buffer completion.
		# This also prevents an explicit completion from being repeated later.
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
		brailleMessage = statusMessage(
			label, _, conf["verbosity"], conf["redactSensitive"], "developer", "balanced",
		)
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
			tones.beep(880, 80)

	def _poll(self):
		try:
			self._rememberBuffer(api.getFocusObject())
			if not self._buffer:
				return
			now = time.monotonic()
			if self._busy and self._busyStartedAt and now - self._busyStartedAt >= _settings()["maximumBusyMinutes"] * 60:
				self._setBusy(False, "maximum activity timeout")
			label = self._latestButtonStatus(self._buffer.makeTextInfo(textInfos.POSITION_ALL))
			if label and not isTaskCompletionLabel(label) and label != self._lastLabel:
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

	def _speakOnce(self, message, category="other", soundCategory=None, priority=None, brailleMessage=None):
		if self._paused:
			return False
		now = time.monotonic()
		comparisonMessage = message or brailleMessage or category
		if shouldSuppressSemanticDuplicate(comparisonMessage, self._lastMessage, now - self._lastMessageAt):
			if _settings()["diagnosticLogging"]:
				log.debug("Codex Status Announcer suppressed duplicate %s event", category)
			return False
		self._lastMessage, self._lastMessageAt = comparisonMessage, now
		conf = _settings()
		mode = conf[CATEGORY_OUTPUT_CONFIG.get(category, "outputOther")]
		actions = categoryOutputActions(mode, conf["speech"], conf["braille"], conf["soundWhenSpeechUnavailable"])
		if category not in ("backgroundPulse1", "backgroundPulse2"):
			self._recordHistory(message or brailleMessage)
		return _send(
			message, actions["speech"] and bool(message), actions["braille"], soundCategory or category, actions["sound"],
			priority=priority or announcementPriority(category, message), brailleMessage=brailleMessage,
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
		_playProgressSound("working", _("Working"), "clicks", conf["clickVolume"])
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
		categoryNames = {
			"command": _("Command"), "build": _("Tests"), "tool": _("Tool"),
			"search": _("Search"), "file": _("File operation"), "thinking": _("Thinking"),
			"working": _("Processing"),
		}
		name = categoryNames.get(self._activeCategory, _("Work"))
		fullMessage = _("{activity} still running, {seconds} seconds").format(activity=name, seconds=elapsed)
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
			self._setBusy(nextBusyState(self._busy, commentary=True), "commentary")
			if self._busy:
				self._lastHeartbeatAt = time.monotonic()
			log.info("Codex Status Announcer detected activity: Commentary update")
			fullMessage = message
			conf = _settings()
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
			self._speakOnce(message, "commentary", brailleMessage=fullMessage)

	@script(description=_("Repeat the latest Codex progress message"))
	def script_repeatLatestStatus(self, gesture):
		if self._latestMessage:
			conf = _settings()
			_send(self._latestMessage, conf["speech"], conf["braille"], "other", conf["soundWhenSpeechUnavailable"])
		else:
			ui.message(_("No Codex progress message is available"))

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
		if not self._history:
			ui.message(_("No Codex announcement history is available"))
			return
		ui.browseableMessage("\n".join(self._history.items()), title=_("Codex announcement history"))

	@script(description=_("Clear Codex announcement history"))
	def script_clearHistory(self, gesture):
		self._history.clear()
		ui.message(_("Codex announcement history cleared"))

	@script(description=_("Toggle Codex privacy redaction"))
	def script_togglePrivacy(self, gesture):
		conf = _settings()
		conf["redactSensitive"] = not conf["redactSensitive"]
		ui.message(_("Codex privacy redaction on") if conf["redactSensitive"] else _("Codex privacy redaction off"))

	@script(description=_("Show sanitized Codex Status Announcer diagnostics"))
	def script_showDiagnostics(self, gesture):
		ui.browseableMessage(self._diagnosticReport(), title=_("Codex Status Announcer diagnostics"))

	@script(description=_("Copy sanitized Codex Status Announcer diagnostics"))
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

	@script(description=_("Run Codex Status Announcer compatibility self-test"))
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
		_showBrowseableMessageAtTop("\n".join(checks), _("Codex Status Announcer — compatibility self-test"))

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
		self._rememberBuffer(focus)
		if not self._buffer:
			ui.message(_("Codex chat history is not available"))
			return
		try:
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
		nextHandler(); self._updateAppFocusState(obj); self._rememberBuffer(obj)
		try:
			isPrompt = obj.role == Role.EDITABLETEXT and _isCodexObject(obj)
		except Exception:
			isPrompt = False
		if isPrompt:
			self._trackPromptSubmission(obj)
		elif _isChatGPTObject(obj):
			# Do not carry a draft-state transition across task/sidebar navigation.
			self._promptHadText = None
			self._pendingUserMessageIncrease = False
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_foreground(self, obj, nextHandler):
		nextHandler(); self._updateAppFocusState(obj); self._rememberBuffer(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_nameChange(self, obj, nextHandler):
		nextHandler(); self._rememberBuffer(obj); self._announceStatus(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_valueChange(self, obj, nextHandler):
		nextHandler(); submitted = self._trackPromptSubmission(obj); self._announceStatus(obj)
		if _isChatGPTObject(obj) and (submitted or getattr(obj, "role", None) != Role.EDITABLETEXT):
			self._schedulePoll()

	def event_liveRegionChange(self, obj, nextHandler):
		nextHandler(); self._announceStatus(obj); self._announceCommentary(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_show(self, obj, nextHandler):
		nextHandler(); self._announceStatus(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_textChange(self, obj, nextHandler):
		nextHandler(); submitted = self._trackPromptSubmission(obj)
		if _isChatGPTObject(obj) and (submitted or getattr(obj, "role", None) != Role.EDITABLETEXT):
			self._schedulePoll()
