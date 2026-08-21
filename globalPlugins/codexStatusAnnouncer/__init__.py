"""Announce activity shown by the Codex desktop interface."""

import os
import time
from pathlib import Path

import addonHandler
import api
import braille
import config
import globalPluginHandler
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

from .core import AnnouncementHistory, CATEGORY_SETTING, announcementPriority, categoryOutputActions, changelogForDisplay, completedTextDelta, elapsedSeconds, firstStatusLabel, formatCustomAnnouncement, nextBusyState, outputActions, previewSelection, redactSensitive, shouldClearBusyAfterStatusGap, soundKey, statusDetails, statusMessage, tonePattern, viewerTitleMatches

addonHandler.initTranslation()

CONFIG_SECTION = "codexStatusAnnouncer"
ADDON_VERSION = "2.2.4"
CODEX_USAGE_URL = "https://chatgpt.com/codex/settings/usage"
CURRENT_RELEASE_NOTES = _(
	"Version 2.2.4\n\n"
	"NVDA Settings and Input Gestures now provide direct access to the official Codex usage dashboard for checking current usage and purchasing credits. No purchase is made automatically."
)
VERBOSITY_CHOICES = ("minimal", "full")
SOUND_STYLE_CHOICES = ("clicks", "tones")
CLICK_VOLUME_CHOICES = ("soft", "normal", "loud")
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
)
ANNOUNCEMENT_CONFIG_BY_ACTION = {item[0]: item[1] for item in PREVIEW_ITEMS if item[0] != "completion"}
ANNOUNCEMENT_CONFIG_BY_ACTION.update({"completion": "announcementCompletion", "failure": "announcementFailure"})
NO_STATUS_BUSY_GRACE_SECONDS = 2.0
config.conf.spec[CONFIG_SECTION] = {
	"verbosity": "option('minimal', 'full', default='full')",
	"speech": "boolean(default=True)",
	"braille": "boolean(default=True)",
	"redactSensitive": "boolean(default=False)",
	"workingIntervalSeconds": "integer(default=5, min=1, max=300)",
	"idlePollMs": "integer(default=500, min=100, max=5000)",
	"completionSound": "boolean(default=False)",
	"soundWhenSpeechUnavailable": "boolean(default=True)",
	"progressSoundStyle": "option('clicks', 'tones', default='clicks')",
	"clickVolume": "option('soft', 'normal', 'loud', default='normal')",
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
}


def _settings():
	return config.conf[CONFIG_SECTION]


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


def _send(message, speak=True, showBraille=True, toneCategory=None, progressSoundsEnabled=True, soundStyle=None, clickVolume=None, priority="normal"):
	actions = outputActions(speak, _speechIsOff(), showBraille, progressSoundsEnabled, toneCategory)
	if actions["speech"]:
		if priority == "urgent":
			try:
				speech.cancelSpeech()
			except AttributeError:
				pass
		speech.speakMessage(message)
	if actions["braille"]:
		braille.handler.message(message)
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


def _openUsageDashboard(message):
	try:
		opened = wx.LaunchDefaultBrowser(CODEX_USAGE_URL)
	except Exception:
		log.error("Unable to open the Codex usage dashboard", exc_info=True)
		opened = False
	ui.message(message if opened else _("The Codex usage dashboard could not be opened"))


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

	def _onTest(self, evt):
		_send(
			_("Codex Status Announcer test: Running command"),
			self.speech.IsChecked(), self.braille.IsChecked(), "command",
			self.progressSounds.IsChecked(),
			SOUND_STYLE_CHOICES[self.progressSoundStyle.GetSelection()],
			CLICK_VOLUME_CHOICES[self.clickVolume.GetSelection()],
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
			changelogPath = Path(addonHandler.getCodeAddon().path) / "changelog.md"
			message = changelogForDisplay(changelogPath.read_text(encoding="utf-8"))
		except Exception:
			log.error("Unable to open the Codex Status Announcer changelog", exc_info=True)
			ui.message(_("The complete release history could not be opened"))
			return
		_showBrowseableMessageAtTop(
			message, _("Codex Status Announcer — complete release history"),
		)

	def onSave(self):
		conf = _settings()
		self._storeCurrentAnnouncementEdit()
		conf["verbosity"] = VERBOSITY_CHOICES[self.verbosity.GetSelection()]
		for name in ("speech", "braille", "redactSensitive", "completionSound", "diagnosticLogging", "announceHeartbeat"):
			conf[name] = getattr(self, name).IsChecked()
		conf["soundWhenSpeechUnavailable"] = self.progressSounds.IsChecked()
		conf["progressSoundStyle"] = SOUND_STYLE_CHOICES[self.progressSoundStyle.GetSelection()]
		conf["clickVolume"] = CLICK_VOLUME_CHOICES[self.clickVolume.GetSelection()]
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


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	scriptCategory = _("Codex Status Announcer")

	def __init__(self):
		super().__init__()
		self._lastMessage = ""
		self._lastMessageAt = 0.0
		self._lastLabel = ""
		self._latestMessage = ""
		self._haveBaseline = False
		self._buffer = None
		self._monitoringAnnounced = False
		self._lastNoStatusLogAt = 0.0
		self._active = False
		self._lastHeartbeatAt = 0.0
		self._busy = False
		self._noStatusSince = 0.0
		self._backgroundPulseCount = 0
		self._commentaryOffsets = {}
		self._paused = False
		self._history = AnnouncementHistory(20)
		self._busyStartedAt = 0.0
		self._activeCategory = "other"
		self._whatsNewTimer = None
		log.info(
			"Codex Status Announcer 2.2.4 loaded (verbosity=%s, soundStyle=%s)",
			_settings()["verbosity"], _settings()["progressSoundStyle"],
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
		message = _(
			"Codex Status Announcer {version}\n\n"
			"What's new:\n"
			"• Open current Codex usage statistics directly.\n"
			"• Open the official credit-purchase page directly.\n"
			"• Assign either action in NVDA's Input Gestures dialog if desired."
		).format(version=ADDON_VERSION)
		ui.browseableMessage(message, title=_("What's new?"), closeButton=True)
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
		self._history.clear()
		self._latestMessage = ""

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
			"Version: 2.2.4\nVerbosity: {verbosity}\nSound style: {style}\nClick volume: {volume}\n"
			"Monitoring attached: {attached}\nBackground state: {state}\nPaused: {paused}\n"
			"Active category: {category}\nHistory entries: {history}\nSupported applications: {apps}\n"
			"Speech: {speech}\nBraille: {braille}\nProgress sounds: {sounds}"
		).format(
			verbosity=conf["verbosity"], style=conf["progressSoundStyle"], volume=conf["clickVolume"],
			attached=bool(self._buffer), state="active" if self._busy else "idle", paused=self._paused,
			category=self._activeCategory, history=len(self._history), apps=conf["supportedAppNames"], speech=conf["speech"],
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

	def _rememberBuffer(self, obj):
		if not _isChatGPTObject(obj):
			return
		for current in self._bufferCandidates(obj):
			buffer = getattr(current, "treeInterceptor", None)
			if not buffer:
				continue
			wasMissing = self._buffer is None
			if self._buffer is not None and buffer is not self._buffer:
				self._resetTaskState("document changed")
			self._buffer = buffer
			if wasMissing:
				log.info("Codex Status Announcer attached to %s", type(buffer).__name__)
			if not self._monitoringAnnounced:
				self._monitoringAnnounced = True
				conf = _settings()
				_send(_("Codex status monitoring active"), conf["speech"], conf["braille"], "other", conf["soundWhenSpeechUnavailable"])
			return

	def _latestButtonStatus(self, info):
		latest = ""
		buttonDepth = 0
		buttonText = []
		buttonName = ""
		unknown = []
		for item in info.getTextWithFields():
			if isinstance(item, str):
				if buttonDepth:
					buttonText.append(item)
				continue
			command = getattr(item, "command", "")
			field = getattr(item, "field", {}) or {}
			if command == "controlStart":
				if buttonDepth:
					buttonDepth += 1
				elif field.get("role") == Role.BUTTON:
					buttonDepth, buttonText, buttonName = 1, [], field.get("name", "")
			elif command == "controlEnd" and buttonDepth:
				buttonDepth -= 1
				if buttonDepth == 0:
					textLabel = " ".join("".join(buttonText).split())
					label = firstStatusLabel(textLabel, buttonName)
					if label:
						latest = label
					elif textLabel or buttonName:
						unknown.append(textLabel or buttonName)
		if _settings()["diagnosticLogging"] and unknown:
			log.debug("Codex Status Announcer unrecognized buttons: %s", [redactSensitive(x) for x in unknown[-5:]])
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
		self._setBusy(nextBusyState(self._busy, category), category)
		self._activeCategory = category
		if not self._shouldAnnounce(label, category):
			return
		conf = _settings()
		message = statusMessage(label, _, conf["verbosity"], conf["redactSensitive"])
		priority = announcementPriority(category, message)
		action = soundKey(category, message) if category == "completion" else category
		message = _customizeAnnouncement(message, action)
		log.info("Codex Status Announcer detected activity: %s", safeMessage)
		self._latestMessage = message
		fallbackPlayed = self._speakOnce(message, category, action, priority)
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
			self._active = bool(label) or self._busy
			if not label:
				if self._busy:
					if not self._noStatusSince:
						self._noStatusSince = now
					elif shouldClearBusyAfterStatusGap(
						self._busy, now - self._noStatusSince, NO_STATUS_BUSY_GRACE_SECONDS,
					):
						self._setBusy(False, "status absent")
				else:
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
			self._noStatusSince = 0.0
			if not self._haveBaseline:
				self._lastLabel, self._haveBaseline = label, True
				self._setBusy(nextBusyState(self._busy, statusDetails(label)[0]), "baseline")
				self._lastHeartbeatAt = time.monotonic()
				return
			if label != self._lastLabel:
				self._lastLabel = label
				self._announceLabel(label)
			else:
				self._announceBackgroundPulse()
		except Exception:
			log.debugWarning("Codex Status Announcer could not inspect the virtual buffer", exc_info=True)
			self._setBusy(False, "buffer inspection failed")
			self._buffer = None
		finally:
			if self._timer is not None:
				delay = 100 if self._active else _settings()["idlePollMs"]
				self._timer = wx.CallLater(delay, self._poll)

	def _speakOnce(self, message, category="other", soundCategory=None, priority=None):
		if self._paused:
			return False
		now = time.monotonic()
		if message == self._lastMessage and now - self._lastMessageAt < 0.5:
			return False
		self._lastMessage, self._lastMessageAt = message, now
		conf = _settings()
		mode = conf[CATEGORY_OUTPUT_CONFIG.get(category, "outputOther")]
		actions = categoryOutputActions(mode, conf["speech"], conf["braille"], conf["soundWhenSpeechUnavailable"])
		if category not in ("backgroundPulse1", "backgroundPulse2"):
			self._recordHistory(message)
		return _send(
			message, actions["speech"], actions["braille"], soundCategory or category, actions["sound"],
			priority=priority or announcementPriority(category, message),
		)

	def _setBusy(self, busy, reason):
		busy = bool(busy)
		if busy == self._busy:
			return
		self._busy = busy
		if busy:
			self._busyStartedAt = time.monotonic()
		log.info(
			"Codex Status Announcer background state: %s (%s)",
			"active" if busy else "idle", reason,
		)
		if not busy:
			self._lastHeartbeatAt = 0.0
			self._busyStartedAt = 0.0

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
			"command": _("Command"), "build": _("Build or test"), "tool": _("Tool"),
			"search": _("Search"), "file": _("File operation"), "thinking": _("Thinking"),
			"working": _("Processing"),
		}
		name = categoryNames.get(self._activeCategory, _("Work"))
		message = _("{activity} still running, {seconds} seconds").format(activity=name, seconds=elapsed)
		message = _customizeAnnouncement(message, toneCategory, name, elapsed)
		mode = conf[CATEGORY_OUTPUT_CONFIG.get(self._activeCategory, "outputOther")]
		actions = categoryOutputActions(mode, conf["speech"], conf["braille"], conf["soundWhenSpeechUnavailable"])
		if not self._paused:
			_send(message, actions["speech"], actions["braille"], toneCategory, actions["sound"], priority="low")

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
		if not text or statusDetails(text)[0]:
			return
		key = id(obj)
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
			message = _customizeAnnouncement(message, "commentary")
			self._latestMessage = message
			self._speakOnce(message, "commentary")

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

	@script(description=_("Open Codex usage statistics"))
	def script_openUsageStatistics(self, gesture):
		_openUsageDashboard(_("Opening Codex usage statistics"))

	@script(description=_("Open Codex usage credits"))
	def script_openUsageCredits(self, gesture):
		_openUsageDashboard(_("Opening Codex usage credits. No purchase will be made automatically."))

	def event_gainFocus(self, obj, nextHandler):
		nextHandler(); self._rememberBuffer(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_foreground(self, obj, nextHandler):
		nextHandler(); self._rememberBuffer(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_nameChange(self, obj, nextHandler):
		nextHandler(); self._rememberBuffer(obj); self._announceStatus(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_valueChange(self, obj, nextHandler):
		nextHandler(); self._announceStatus(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_liveRegionChange(self, obj, nextHandler):
		nextHandler(); self._announceStatus(obj); self._announceCommentary(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_show(self, obj, nextHandler):
		nextHandler(); self._announceStatus(obj)
		if _isChatGPTObject(obj): self._schedulePoll()

	def event_textChange(self, obj, nextHandler):
		nextHandler()
		if _isChatGPTObject(obj): self._schedulePoll()
