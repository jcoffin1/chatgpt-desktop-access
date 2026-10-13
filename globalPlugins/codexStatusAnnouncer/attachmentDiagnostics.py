"""Bounded, content-free capture of what the Add files and more popup exposes.

ChatGPT's Add files and more button can report expanded while NVDA finds no
menu choices. This module records, without chat text, where the popup appears
(if anywhere): NVDA's focus and IA2 view, UI Automation focus and menu-like
elements under ChatGPT's own windows, and new top-level windows of the ChatGPT
process. Expensive UI Automation calls run on NVDA's UIA worker thread and are
limited to ChatGPT's top-level windows; the desktop is never searched.
"""

import ctypes
import time
from ctypes import wintypes

import addonHandler
import api
import queueHandler
import winUser
from logHandler import log

from .core import attachmentDiagnosticLines, redactSensitive


addonHandler.initTranslation()


MAX_PROCESS_WINDOWS = 8
MAX_UIA_ELEMENTS = 400
MAX_FOCUS_ANCESTORS = 6
CAPTURE_COOLDOWN_SECONDS = 3.0
_ENUM_WINDOWS_PROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def _text(value, limit=60):
	return redactSensitive(" ".join(str(value or "").split()))[:limit]


def processWindows(processId):
	"""Return bounded facts about the visible top-level windows of one process."""
	handles = []

	def collect(handle, _lParam):
		try:
			if winUser.getWindowThreadProcessID(handle)[0] == processId:
				handles.append(int(handle))
		except Exception:
			pass
		return len(handles) < 64

	try:
		ctypes.windll.user32.EnumWindows(_ENUM_WINDOWS_PROC(collect), 0)
	except Exception:
		log.debugWarning("ChatGPT Desktop Access could not enumerate ChatGPT windows", exc_info=True)
	windows = []
	for handle in handles:
		try:
			if not winUser.isWindowVisible(handle):
				continue
			windows.append({
				"handle": handle,
				"className": str(winUser.getClassName(handle) or ""),
				"owner": int(winUser.getWindow(handle, 4) or 0),
			})
		except Exception:
			continue
	return tuple(windows)


def _controlTypeNames(UIAHandler):
	names = {}
	for name, kind in (
		("UIA_MenuControlTypeId", "menu"), ("UIA_MenuItemControlTypeId", "menuitem"),
		("UIA_MenuBarControlTypeId", "menubar"), ("UIA_ListControlTypeId", "list"),
		("UIA_ListItemControlTypeId", "listitem"), ("UIA_WindowControlTypeId", "window"),
		("UIA_CheckBoxControlTypeId", "checkbox"), ("UIA_RadioButtonControlTypeId", "radiobutton"),
	):
		value = getattr(UIAHandler, name, None)
		if value is not None:
			names[value] = kind
	return names


class AttachmentMenuDiagnostics:
	"""Capture the Add files and more popup's accessibility exposure on request."""

	def __init__(self, plugin):
		self._plugin = plugin
		self._baseline = None
		self._baselineWindowHandles = ()
		self._lastCaptureAt = 0.0
		self._pending = False
		self.report = ""

	def noteButtonFocused(self, button):
		"""Record what exists before the popup opens so the capture can show only changes."""
		if not self._enabled():
			return
		self._queueCapture("baseline", button)

	def noteButtonActivated(self, button, reason):
		"""Capture shortly after an explicit activation or expanded event."""
		if not self._enabled():
			return
		now = time.monotonic()
		if self._pending or now - self._lastCaptureAt < CAPTURE_COOLDOWN_SECONDS:
			return
		self._lastCaptureAt = now
		import wx
		wx.CallLater(600, self._queueCapture, "capture", button, reason)

	def captureNow(self, announce=True):
		"""Capture immediately for the explicit diagnostics command."""
		self._lastCaptureAt = time.monotonic()
		return self._queueCapture("capture", None, "diagnostics command", announce)

	def _enabled(self):
		try:
			from . import _settings
			return bool(_settings()["diagnosticLogging"])
		except Exception:
			return False

	def _queueCapture(self, purpose, button, reason="", announce=False):
		plugin = self._plugin
		windowHandle = plugin._conversationWindowHandle
		if not windowHandle:
			if announce:
				import ui
				ui.message(_("Open ChatGPT and its Add files and more menu first"))
			return False
		processId = plugin._windowProcessId(windowHandle)
		mainThreadFacts = self._mainThreadFacts(button) if purpose == "capture" else ()
		windows = processWindows(processId)
		try:
			import UIAHandler
			handler = UIAHandler.handler
			client = handler.clientObject
		except Exception:
			if purpose == "capture":
				self._finish(purpose, reason, mainThreadFacts, windows, (), ("UI Automation unavailable",), announce)
			return False
		self._pending = True

		def probe():
			elements = ()
			focusLines = ()
			try:
				focusLines = self._uiaFocus(client, UIAHandler)
				elements = self._uiaElements(client, UIAHandler, windows)
			except Exception:
				log.debugWarning("ChatGPT Desktop Access attachment diagnostics UIA probe failed", exc_info=True)
			finally:
				queueHandler.queueFunction(
					queueHandler.eventQueue, self._finish,
					purpose, reason, mainThreadFacts, windows, elements, focusLines, announce,
				)

		try:
			handler.MTAThreadQueue.put_nowait(probe)
		except Exception:
			self._pending = False
			log.debugWarning("ChatGPT Desktop Access could not schedule attachment diagnostics", exc_info=True)
			return False
		return True

	def _mainThreadFacts(self, button):
		"""Read NVDA's own focus and IA2 view of the button; cheap and main-thread only."""
		lines = []

		def describe(label, obj):
			if obj is None:
				lines.append(f"{label}: none")
				return
			try:
				role = getattr(getattr(obj, "role", None), "name", "") or str(getattr(obj, "role", ""))
				states = sorted(getattr(state, "name", str(state)) for state in (getattr(obj, "states", ()) or ()))
				lines.append("{label}: role {role}; name {name}; value {value}; states {states}; window class {cls}".format(
					label=label, role=role, name=_text(getattr(obj, "name", "")) or "(none)",
					value=_text(getattr(obj, "value", "")) or "(none)",
					states=", ".join(states) or "none", cls=_text(getattr(obj, "windowClassName", "")),
				))
				attributes = getattr(obj, "IA2Attributes", {}) or {}
				keys = ("tag", "xml-roles", "haspopup", "id", "explicit-name", "display")
				attributeText = "; ".join(f"{key}={_text(attributes[key], 40)}" for key in keys if key in attributes)
				if attributeText:
					lines.append(f"{label} IA2 attributes: {attributeText}")
				targets = tuple(getattr(obj, "controllerFor", ()) or ())[:4]
				for target in targets:
					targetRole = getattr(getattr(target, "role", None), "name", "") or str(getattr(target, "role", ""))
					lines.append(f"{label} controls: role {targetRole}; name {_text(getattr(target, 'name', '')) or '(none)'}")
				if not targets:
					lines.append(f"{label} controls: nothing exposed")
			except Exception:
				lines.append(f"{label}: unreadable")

		try:
			describe("NVDA focus", api.getFocusObject())
		except Exception:
			lines.append("NVDA focus: unreadable")
		describe("Add files and more button", button)
		try:
			foreground = int(winUser.getForegroundWindow() or 0)
			lines.append(f"Foreground window class: {winUser.getClassName(foreground)}")
		except Exception:
			pass
		lines.extend(self._documentTailAfterPrompt())
		return tuple(lines)

	def _documentTailAfterPrompt(self, maximumEntries=40):
		"""List controls and short labels after the prompt, where ChatGPT adds the popup.

		Recording starts only after the prompt field, so conversation text before
		it is never included.
		"""
		buffer = getattr(self._plugin, "_buffer", None)
		if buffer is None:
			return ("Page after prompt: no conversation buffer",)
		try:
			import textInfos
			from controlTypes import Role
			from . import _extendScanStart
			from .core import isCodexPromptLabel
			position = buffer.makeTextInfo(textInfos.POSITION_LAST)
			_extendScanStart(position, 6000)
			entries = []
			afterPrompt = False
			for item in position.getTextWithFields():
				if isinstance(item, str):
					if afterPrompt and item.strip():
						entries.append(f"text: {_text(item)}")
					continue
				if getattr(item, "command", "") != "controlStart":
					continue
				field = getattr(item, "field", {}) or {}
				role = field.get("role")
				name = field.get("name", "")
				if role == Role.EDITABLETEXT and isCodexPromptLabel(name):
					afterPrompt = True
					entries = []
					continue
				if afterPrompt:
					roleName = getattr(role, "name", str(role)).casefold()
					states = sorted(getattr(state, "name", str(state)).casefold() for state in field.get("states", ()) or ())
					entries.append("{role}: {name}{states}".format(
						role=roleName, name=_text(name) or "(no name)",
						states=f" [{', '.join(states)}]" if states else "",
					))
			if not afterPrompt:
				return ("Page after prompt: prompt not found in the last part of the page",)
			lines = [f"Page after prompt: {len(entries)} entries"]
			lines.extend(f"  {entry}" for entry in entries[-maximumEntries:])
			return tuple(lines)
		except Exception:
			log.debugWarning("ChatGPT Desktop Access could not read the page after the prompt", exc_info=True)
			return ("Page after prompt: unreadable",)

	def _uiaFocus(self, client, UIAHandler):
		"""Describe UI Automation's focused element and a few ancestors."""
		lines = []
		focused = client.GetFocusedElement()
		if not focused:
			return ("UIA focus: none",)
		typeNames = _controlTypeNames(UIAHandler)
		walker = client.ControlViewWalker
		element = focused
		for depth in range(MAX_FOCUS_ANCESTORS):
			if not element:
				break
			try:
				kind = typeNames.get(element.CurrentControlType, str(element.CurrentControlType))
				lines.append("UIA focus{suffix}: type {kind}; name {name}; class {cls}; process {pid}".format(
					suffix="" if depth == 0 else f" ancestor {depth}", kind=kind,
					name=_text(element.CurrentName) or "(none)", cls=_text(element.CurrentClassName),
					pid=element.CurrentProcessId,
				))
				element = walker.GetParentElement(element)
			except Exception:
				break
		return tuple(lines)

	def _uiaElements(self, client, UIAHandler, windows):
		"""Find menu-like elements only under ChatGPT's own visible top-level windows."""
		typeNames = _controlTypeNames(UIAHandler)
		conditions = [
			client.createPropertyCondition(UIAHandler.UIA_ControlTypePropertyId, typeId)
			for typeId in typeNames
		]
		condition = client.createOrConditionFromArray(conditions)
		cacheRequest = client.CreateCacheRequest()
		propertyIds = [
			UIAHandler.UIA_ControlTypePropertyId, UIAHandler.UIA_NamePropertyId,
			UIAHandler.UIA_ClassNamePropertyId, UIAHandler.UIA_IsOffscreenPropertyId,
		]
		ariaRoleId = getattr(UIAHandler, "UIA_AriaRolePropertyId", 30101)
		propertyIds.append(ariaRoleId)
		for propertyId in propertyIds:
			cacheRequest.AddProperty(propertyId)
		elements = []
		for window in windows[:MAX_PROCESS_WINDOWS]:
			try:
				root = client.ElementFromHandle(window["handle"])
				found = root.FindAllBuildCache(UIAHandler.TreeScope_Descendants, condition, cacheRequest) if root else None
			except Exception:
				continue
			count = found.Length if found else 0
			for index in range(min(count, MAX_UIA_ELEMENTS - len(elements))):
				try:
					element = found.GetElement(index)
					elements.append((
						typeNames.get(element.GetCachedPropertyValue(UIAHandler.UIA_ControlTypePropertyId), "other"),
						str(element.GetCachedPropertyValue(UIAHandler.UIA_NamePropertyId) or ""),
						str(element.GetCachedPropertyValue(ariaRoleId) or ""),
						str(element.GetCachedPropertyValue(UIAHandler.UIA_ClassNamePropertyId) or ""),
						bool(element.GetCachedPropertyValue(UIAHandler.UIA_IsOffscreenPropertyId)),
					))
				except Exception:
					continue
			if len(elements) >= MAX_UIA_ELEMENTS:
				break
		return tuple(elements)

	def _finish(self, purpose, reason, mainThreadFacts, windows, elements, focusLines, announce):
		self._pending = False
		if purpose == "baseline":
			self._baseline = elements
			self._baselineWindowHandles = tuple(window["handle"] for window in windows)
			return
		newWindows = [window for window in windows if window["handle"] not in self._baselineWindowHandles]
		lines = [
			"Attachment menu capture ({reason}) at {time}".format(
				reason=reason or "expanded", time=time.strftime("%H:%M:%S"),
			),
			*mainThreadFacts,
			*focusLines,
			"ChatGPT visible top-level windows: {count}; classes: {classes}".format(
				count=len(windows), classes=", ".join(window["className"] for window in windows) or "none",
			),
		]
		if self._baselineWindowHandles:
			lines.append("New top-level windows since Add files and more was focused: {count}{classes}".format(
				count=len(newWindows),
				classes=(" (" + ", ".join(window["className"] for window in newWindows) + ")") if newWindows else "",
			))
		lines.extend(attachmentDiagnosticLines(elements, self._baseline))
		self.report = "\n".join(lines)
		log.info("ChatGPT Desktop Access attachment menu diagnostics:\n%s", self.report)
		if announce:
			import ui
			ui.message(_("Attachment menu diagnostics captured. Save a support report to share them."))
