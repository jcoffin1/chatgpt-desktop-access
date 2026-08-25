"""NVDA-independent parsing and privacy helpers for Codex activity."""

import json
import re
from collections import deque
from pathlib import Path


def loadArchivedThreads(codexRoot, limit=200):
	"""Read archived thread IDs and titles from Codex's JSONL metadata."""
	if limit < 1:
		return ()
	codexRoot = Path(codexRoot)
	archiveDirectory = codexRoot / "archived_sessions"
	if not archiveDirectory.is_dir():
		return ()
	def modifiedTime(path):
		try:
			return path.stat().st_mtime
		except OSError:
			return 0
	paths = sorted(archiveDirectory.glob("*.jsonl"), key=modifiedTime, reverse=True)[:int(limit)]
	threadIds = tuple(path.stem[-36:] for path in paths)
	targetIds = set(threadIds)
	titles = {}
	indexPath = codexRoot / "session_index.jsonl"
	if indexPath.is_file() and targetIds:
		with indexPath.open("r", encoding="utf-8") as indexFile:
			for line in indexFile:
				try:
					record = json.loads(line)
				except (TypeError, ValueError):
					continue
				if not isinstance(record, dict):
					continue
				threadId = str(record.get("id") or "").strip()
				if threadId not in targetIds:
					continue
				title = " ".join(str(record.get("thread_name") or "").split())
				if title:
					titles[threadId] = title
	result = []
	for threadId in threadIds:
		title = titles.get(threadId, f"Archived task {threadId}")
		result.append((threadId, title))
	return tuple(result)


def repairConfigurationValues(values, choiceDefaults, numericDefaults, booleanDefaults=(), stringDefaults=()):
	"""Repair imported or migrated configuration values in place."""
	repaired = []
	for key, (choices, default) in choiceDefaults.items():
		if values.get(key) not in choices:
			values[key] = default
			repaired.append(key)
	for key, (minimum, maximum, default) in numericDefaults.items():
		original = values.get(key, default)
		try:
			value = default if isinstance(original, bool) else int(original)
		except (TypeError, ValueError, OverflowError):
			value = default
		if value < minimum or value > maximum:
			value = default
		if original != value:
			repaired.append(key)
		values[key] = value
	for key, default in booleanDefaults:
		original = values.get(key, default)
		if isinstance(original, bool):
			value = original
		elif original in (0, 1):
			value = bool(original)
		elif isinstance(original, str) and original.strip().casefold() in ("true", "yes", "on", "1", "false", "no", "off", "0"):
			value = original.strip().casefold() in ("true", "yes", "on", "1")
		else:
			value = default
		if original != value:
			repaired.append(key)
		values[key] = value
	for key, default in stringDefaults:
		original = values.get(key, default)
		value = original.strip() if isinstance(original, str) else default
		if not value and default:
			value = default
		if original != value:
			repaired.append(key)
		values[key] = value
	return tuple(dict.fromkeys(repaired))


def chatTitleMatches(selectedTitle, buttonName):
	"""Require an exact normalized title before activating a sidebar button."""
	selected = " ".join(str(selectedTitle or "").casefold().split())
	button = " ".join(str(buttonName or "").casefold().split())
	return bool(selected and selected == button)


class AnnouncementHistory:
	"""A bounded, in-memory announcement history with review navigation."""

	def __init__(self, limit=20):
		self._items = deque(maxlen=limit)
		self._index = -1

	def add(self, message):
		message = str(message or "").strip()
		if not message or (self._items and self._items[-1] == message):
			return False
		self._items.append(message)
		self._index = len(self._items) - 1
		return True

	def move(self, offset):
		if not self._items:
			return ""
		self._index = min(max(self._index + offset, 0), len(self._items) - 1)
		return self._items[self._index]

	def clear(self):
		self._items.clear()
		self._index = -1

	def items(self):
		return tuple(self._items)

	def __len__(self):
		return len(self._items)

CATEGORY_SETTING = {"thinking": "announceThinking", "working": "announceWorking", "command": "announceCommands", "search": "announceSearches", "file": "announceFiles", "build": "announceBuilds", "tool": "announceTools", "completion": "announceCompletions", "attention": "announceAttention", "other": "announceOther", "commentary": "announceCommentary"}

TONE_PATTERNS = {
	"thinking": ((392, 45), (440, 45)),
	"working": ((440, 45),),
	"command": ((523, 55), (659, 65)),
	"search": ((659, 50), (784, 60)),
	"file": ((494, 45), (587, 55)),
	"build": ((587, 55), (698, 70)),
	"tool": ((698, 55),),
	"completion": ((659, 55), (784, 55), (988, 85)),
	"failure": ((659, 65), (523, 65), (392, 100)),
	"other": ((392, 50),),
	"commentary": ((554, 45),),
	"attention": ((784, 70), (988, 100)),
	"backgroundPulse1": ((392, 35), (523, 55)),
	"backgroundPulse2": ((440, 35), (587, 55)),
	"monitoringActive": ((523, 45), (784, 65)),
	"monitoringInactive": ((587, 45), (392, 70)),
	"submission": ((523, 40), (659, 50), (784, 65)),
}


def tonePattern(category, message=""):
	"""Return a short earcon pattern for a progress category and message."""
	message = str(message or "").lower()
	if category == "completion" and any(word in message for word in ("fail", "error", "cancel")):
		return TONE_PATTERNS["failure"]
	return TONE_PATTERNS.get(category, TONE_PATTERNS["other"])


def soundKey(category, message=""):
	"""Return the bundled click-earcon name for a category and message."""
	message = str(message or "").lower()
	if category == "completion" and any(word in message for word in ("fail", "error", "cancel")):
		return "failure"
	return category if category in TONE_PATTERNS else "other"


def userMessageNumber(label):
	"""Return the number from a Codex 'Jump to user message' control."""
	match = re.search(r"(?i)\bjump to user message\s+(\d+)\b", str(label or ""))
	return int(match.group(1)) if match else None


def userMessageSubmissionTransition(previousNumber, currentNumber):
	"""Detect a newly posted user message without firing on the initial baseline."""
	if currentNumber is None:
		return previousNumber, False
	return currentNumber, previousNumber is not None and currentNumber > previousNumber


def confirmedUserMessageSubmission(pendingIncrease, messageNumberIncreased, stopControlVisible):
	"""Retain and confirm a message-count increase once active work is visible.

	Loading a different Codex task can expose a larger historical user-message
	count.  The active Stop/Cancel control distinguishes that navigation change
	from a request that ChatGPT is currently processing. Retaining an increase
	also covers Chromium exposing the new message one scan before the Stop control.
	"""
	pending = bool(pendingIncrease or messageNumberIncreased)
	confirmed = bool(pending and stopControlVisible)
	return False if confirmed else pending, confirmed


def isStopControlLabel(label):
	"""Return whether a button is the active-task stop or cancel control."""
	lower = " ".join(str(label or "").lower().split())
	return lower in ("stop", "stop generating", "cancel", "cancel task", "cancel request")


def stopControlTransition(previousVisible, currentVisible):
	"""Detect disappearance of a previously visible task stop control."""
	currentVisible = bool(currentVisible)
	return currentVisible, bool(previousVisible and not currentVisible)


def shouldSuppressDuplicate(message, previousMessage, elapsedSeconds, windowSeconds=1.5):
	"""Suppress rapid duplicate accessibility events without hiding later updates."""
	return bool(message == previousMessage and float(elapsedSeconds) < float(windowSeconds))


def semanticStatusKey(message):
	"""Collapse cosmetic wording differences into a stable activity key."""
	text = " ".join(str(message or "").casefold().split())
	replacements = (
		("editing file", "editing code"), ("editing source", "editing code"),
		("reading files", "checking files"), ("reading", "checking files"),
		("file edit finished", "file updated"), ("changes finished", "file updated"),
		("build or test still running", "tests still running"),
	)
	for old, new in replacements:
		if text.startswith(old):
			text = new + text[len(old):]
	return text


def shouldSuppressSemanticDuplicate(message, previousMessage, elapsedSeconds, windowSeconds=1.5):
	return bool(
		semanticStatusKey(message)
		and semanticStatusKey(message) == semanticStatusKey(previousMessage)
		and float(elapsedSeconds) < float(windowSeconds)
	)


def formatCommandSpeech(message, punctuation="normal", maximumCharacters=240):
	"""Prepare long command text for speech without changing stored or braille text."""
	text = str(message or "")
	if punctuation == "enhanced":
		text = text.replace("&&", " and then ").replace("||", " or else ").replace("|", " pipe ")
		text = text.replace(">>", " append to ").replace(">", " redirect to ")
	elif punctuation == "literal":
		for symbol, word in (("&&", " ampersand ampersand "), ("||", " pipe pipe "), ("|", " pipe "), (">", " greater than "), ("<", " less than ")):
			text = text.replace(symbol, word)
	text = " ".join(text.split())
	maximumCharacters = max(40, int(maximumCharacters or 240))
	if len(text) <= maximumCharacters:
		return text, False
	return text[:maximumCharacters].rstrip(" ,;:-") + "…", True


def shouldLogDiagnosticSnapshot(snapshot, previousSnapshot, elapsedSeconds, repeatSeconds=30.0):
	"""Log changed diagnostic data immediately and unchanged data only periodically."""
	snapshot = tuple(snapshot or ())
	return bool(snapshot and (snapshot != tuple(previousSnapshot or ()) or float(elapsedSeconds) >= float(repeatSeconds)))


def responseCompletionTransition(previousMarker, initialized, currentMarker, busy):
	"""Detect a new completed-response marker after establishing a buffer baseline."""
	if currentMarker is None:
		return previousMarker, True, False
	completed = bool(initialized and busy and currentMarker != previousMarker)
	return currentMarker, True, completed


def shouldFinalizeResponseCompletion(pending, elapsedSeconds, settleSeconds, busy, stopControlVisible, activityLabel):
	"""Finalize a tentative response only after a quiet, explicitly idle scan."""
	return bool(
		pending
		and busy
		and not stopControlVisible
		and not str(activityLabel or "").strip()
		and float(elapsedSeconds) >= float(settleSeconds)
	)


def isTaskCompletionLabel(label):
	"""Distinguish whole-task completion from an intermediate operation finishing."""
	lower = " ".join(str(label or "").lower().split())
	return lower.startswith(("response complete", "finished", "completed", "done", "cancelled", "canceled"))


def intermediateCompletionCategory(label):
	"""Map an operation completion back to the activity category it belongs to."""
	lower = " ".join(str(label or "").lower().split())
	if lower.startswith("ran") or "command" in lower or "process" in lower:
		return "command"
	if "search" in lower and ("web" in lower or "internet" in lower):
		return "search"
	if lower.startswith(("compiled", "transpiled", "generated", "built")):
		return "build"
	if lower.startswith(("file edit", "file editing", "file edited", "wrote", "created", "edited", "updated", "modified", "applied", "patched", "read", "inspected", "reviewed")):
		return "file"
	return ""


def isKnownNonStatusButton(label):
	"""Filter stable Codex controls that are not progress statuses."""
	text = " ".join(str(label or "").lower().split())
	return bool(
		userMessageNumber(text) is not None
		or promptControlKind(text)
		or text in (
			"outputs", "sources", "view all", "copy", "copy message", "retry", "edit", "share", "more",
			"fork chat from here", "scroll to bottom", "add files and more", "dictate", "start voice chat", "send",
			"review", "review changed files", "undo", "open chat", "edit message",
		)
		or re.fullmatch(r"worked for (?:\d+h )?(?:\d+m )?\d+s", text) is not None
		or text.startswith("download codex status announcer ")
		or re.fullmatch(r"show \d+ more files?", text) is not None
		or re.search(r"\+\d+-\d+$", text) is not None
	)


def promptControlKind(name):
	"""Classify stable and dynamic prompt-toolbar control names."""
	text = " ".join(str(name or "").casefold().split())
	if text == "add files and more" or text.startswith(("add files", "attach files", "upload files")):
		return "files"
	if text == "change permissions" or ("permission" in text and text.startswith(("change", "select", "choose"))):
		return "permissions"
	if text in ("model", "select model", "choose model", "change model"):
		return "model"
	if re.search(r"\b(?:gpt[- ]?\d|o[1345](?:[- ]|$)|codex model|reasoning model)\b", text):
		return "model"
	return ""


def categoryOutputActions(mode, speechEnabled=True, brailleEnabled=True, soundEnabled=True):
	"""Resolve a category output mode through the global master switches."""
	mode = mode if mode in ("all", "speech", "sound", "braille", "off") else "all"
	return {
		"speech": bool(speechEnabled and mode in ("all", "speech")),
		"braille": bool(brailleEnabled and mode in ("all", "braille")),
		"sound": bool(soundEnabled and mode in ("all", "sound")),
	}


def announcementPriority(category, message=""):
	"""Return low, normal, high, or urgent output priority."""
	message = str(message or "").lower()
	if category == "attention" or any(word in message for word in ("permission", "input required", "needs your")):
		return "urgent"
	if category == "completion" and any(word in message for word in ("fail", "error", "cancel")):
		return "urgent"
	if category == "completion":
		return "high"
	if category in ("commentary", "backgroundPulse1", "backgroundPulse2"):
		return "low"
	return "normal"


def outputActions(speechEnabled, speechOff, brailleEnabled, progressSoundsEnabled, toneCategory):
	"""Return which output channels should be used for one announcement."""
	speechUnavailable = not speechEnabled or speechOff
	return {
		"speech": bool(speechEnabled and not speechUnavailable),
		"braille": bool(brailleEnabled),
		"tone": bool(progressSoundsEnabled and toneCategory),
	}


def nextBusyState(currentBusy, category="", commentary=False):
	"""Update task activity without allowing final commentary to restart it."""
	if commentary:
		return bool(currentBusy)
	if category:
		return category not in ("completion", "attention")
	return bool(currentBusy)


def pollDelay(active, idlePollMs, activePollMs=250):
	"""Use event-driven updates with a lower-cost active fallback poll."""
	return int(activePollMs if active else max(1000, idlePollMs))


def shouldPlayContinuousWorkingClick(busy, enabled, soundStyle, soundAllowed, elapsedSinceSound, intervalSeconds):
	"""Play a working click only in a quiet gap between other progress sounds."""
	return bool(
		busy
		and enabled
		and soundStyle == "clicks"
		and soundAllowed
		and float(elapsedSinceSound) >= float(intervalSeconds)
	)


def focusStateTransition(previousState, isFocused):
	"""Return the new focus state and a cue only when the state changes."""
	isFocused = bool(isFocused)
	if previousState is None:
		return isFocused, "active" if isFocused else ""
	if bool(previousState) == isFocused:
		return isFocused, ""
	return isFocused, "active" if isFocused else "inactive"


def promptSubmissionTransition(previousHadText, currentHasText):
	"""Detect a prompt edit changing from populated to empty without storing text."""
	currentHasText = bool(currentHasText)
	return currentHasText, bool(previousHadText and not currentHasText)


def statusDetails(label):
	"""Return ``(category, minimal message)`` for a recognized activity label."""
	text = " ".join(str(label or "").split())
	lower = text.lower()
	if not lower:
		return "", ""
	if lower.startswith(("permission required", "approval required", "waiting for approval", "needs your approval", "requires permission")):
		return "attention", "Permission required"
	if lower.startswith(("input required", "waiting for user input", "waiting for your input", "needs your input", "question for you")):
		return "attention", "User input required"
	if lower.startswith(("file edit complete", "file editing complete", "file edited")):
		return "completion", "File edit finished"
	if lower.startswith(("compiled", "transpiled")):
		return "completion", "Compilation finished"
	if lower.startswith(("searched the web", "search complete", "search finished")):
		return "completion", "Web search finished"
	if lower.startswith("ran"):
		hasSearch = "search" in lower and "web" in lower
		if hasSearch:
			return "completion", "Command and web search finished"
		# Codex normally formats completed shell activity as "Ran <command>"
		# without including the literal word "command".
		return "completion", "Command finished"
	if lower.startswith(("command failed", "failed command", "process failed")):
		return "completion", "Command failed"
	if lower.startswith(("command succeeded", "process succeeded")):
		return "completion", "Command finished"
	if lower.startswith(("tests failed", "testing failed", "test failed")):
		return "completion", "Tests failed"
	if lower.startswith(("tests passed", "testing passed", "test passed")):
		return "completion", "Tests passed"
	if lower.startswith(("build failed", "compilation failed")):
		return "completion", "Build failed"
	if lower.startswith(("finished", "completed", "done", "cancelled", "canceled", "response complete")):
		return "completion", "Finished"
	if lower == "read" or lower.startswith(("read ", "read:", "inspected", "reviewed")):
		return "completion", "Reading finished"
	if lower.startswith(("wrote", "created")):
		return "completion", "Writing finished"
	if lower.startswith(("edited", "updated", "modified", "applied", "patched")):
		return "completion", "Changes finished"
	if lower.startswith(("generated", "built")):
		return "completion", "Generation finished"
	if lower.startswith(("planning", "thinking")):
		return "thinking", "Thinking"
	if lower.startswith(("working", "processing")):
		return "working", "Working"
	if lower.startswith(("analyzing", "analysing")):
		return "working", "Analyzing"
	if lower.startswith(("running", "executing")):
		if "search" in lower and ("web" in lower or "internet" in lower):
			return "search", "Searching the web"
		if lower.startswith(("running tests", "running test", "executing tests", "executing test", "running build", "executing build")):
			return "build", "Running tests" if "test" in lower else "Generating"
		if lower.startswith(("running tool", "executing tool")):
			return "tool", "Using tool"
		return "command", "Running command"
	if lower.startswith("searching"):
		return "search", "Searching the web"
	if lower.startswith(("reading", "inspecting", "reviewing")):
		return "file", "Reading"
	if lower.startswith(("writing", "creating")):
		return "file", "Writing"
	if lower.startswith(("file edit", "editing", "updating", "modifying")):
		return "file", "Editing file" if lower.startswith("file edit") else "Editing"
	if lower.startswith(("applying", "patching")):
		return "file", "Applying changes"
	if lower.startswith(("compiling", "transpiling", "generating", "building", "testing")):
		if lower.startswith(("compiling", "transpiling")):
			return "build", "Compiling"
		if lower.startswith("testing"):
			return "build", "Running tests"
		return "build", "Generating"
	if lower.startswith(("using", "calling")):
		return "tool", "Using tool"
	if lower.startswith("waiting"):
		return "other", "Waiting"
	return "", ""


def redactSensitive(text):
	text = " ".join(str(text or "").split())
	text = re.sub(r"(?i)(https?://[^\s?]+)\?\S+", r"\1?[query redacted]", text)
	text = re.sub(r"(?i)\b[\w.-]+@[\w.-]+\.[a-z]{2,}\b", "[email redacted]", text)
	secretValue = r'''(?:"[^"]*"|'[^']*'|[^\s;]+)'''
	text = re.sub(r"(?i)\b(api[_-]?key|token|secret|password|passwd|pwd|authorization)\s*[:=]\s*" + secretValue, r"\1=[redacted]", text)
	text = re.sub(r"(?i)(C:\\Users\\)[^\\]+", r"\1[user]", text)
	text = re.sub(r"(?i)(/home/|/users/)[^/\s]+", r"\1[user]", text)
	text = re.sub(r"(?i)\b(remote\s+(?:key|password)|connection\s+key)\s*[:=]\s*" + secretValue, r"\1=[redacted]", text)
	text = re.sub(r"(?i)\b(bearer)\s+[a-z0-9._~+/-]+=*", r"\1 [redacted]", text)
	return text


def standardFullMessage(label, translate=lambda text: text):
	"""Return an action-first Full message with useful targets, counts, and timing."""
	text = " ".join(str(label or "").split())
	category, minimal = statusDetails(text)
	if not category:
		return ""
	details = []
	if category == "command":
		command = re.sub(r"(?i)^(?:running|executing)(?:\s+(?:shell|terminal))?\s+command\s*:?\s*", "", text)
		if command and command != text:
			executable = command.split()[0].strip("'\"")
			executable = re.split(r"[\\/]", executable)[-1]
			if executable:
				details.append(executable)
	else:
		fileMatch = re.search(r"(?i)(?:^|\s)([^\s<>|*?\"]+\.[a-z0-9]{1,8})(?:\s|$)", text)
		if fileMatch:
			details.append(re.split(r"[\\/]", fileMatch.group(1))[-1])
	countMatch = re.search(r"(?i)\b\d+\s+(?:files?|tests?|warnings?|errors?|failures?|passed|failed)\b", text)
	if countMatch and countMatch.group(0).casefold() not in {item.casefold() for item in details}:
		details.append(countMatch.group(0))
	seconds = elapsedSeconds(text)
	if seconds is not None and seconds >= 5:
		details.append(f"{seconds} seconds")
	message = translate(minimal)
	return f"{message}: {', '.join(details)}" if details else message


def minimalProfileMessage(label, translate=lambda text: text, profile="balanced"):
	"""Return Essential, Balanced, or Informative Minimal speech."""
	text = " ".join(str(label or "").split())
	category, minimal = statusDetails(text)
	if not category:
		return ""
	lower = text.casefold()
	if profile == "essential":
		isFailure = any(word in lower for word in ("fail", "error", "cancel"))
		if category not in ("thinking", "attention") and not (
			category == "completion" and (isFailure or isTaskCompletionLabel(text))
		):
			return ""
	balanced = minimal
	if category == "file":
		if lower.startswith(("reading", "inspecting", "reviewing")):
			balanced = "Checking files"
		elif lower.startswith(("writing", "creating", "file edit", "editing", "updating", "modifying")):
			balanced = "Editing code"
	elif category == "completion":
		if isTaskCompletionLabel(text):
			balanced = "Task canceled" if lower.startswith(("cancelled", "canceled")) else "Task finished"
		elif lower.startswith(("file edit", "file edited", "edited", "updated", "modified", "applied", "patched")):
			balanced = "File updated"
	elif category == "other" and lower.startswith("waiting"):
		if "command" in lower or "process" in lower:
			balanced = "Waiting for command"
		elif "tool" in lower:
			balanced = "Waiting for tool"
	message = translate(balanced)
	if profile != "informative":
		return message
	details = []
	fileMatch = re.search(r"(?i)(?:^|\s)([^\s<>|*?\"]+\.[a-z0-9]{1,8})(?:\s|$)", text)
	if fileMatch:
		details.append(re.split(r"[\\/]", fileMatch.group(1))[-1])
	countMatch = re.search(r"(?i)\b\d+\s+(?:files?|tests?|warnings?|errors?|failures?|passed|failed)\b", text)
	if countMatch:
		details.append(countMatch.group(0))
	seconds = elapsedSeconds(text)
	if seconds is not None and seconds >= 10:
		details.append(f"{seconds} seconds")
	return f"{message}: {', '.join(details)}" if details else message


def statusMessage(label, translate=lambda text: text, verbosity="minimal", redact=False, fullProfile="developer", minimalProfile="balanced"):
	text = " ".join(str(label or "").split())
	category, minimal = statusDetails(text)
	if not category:
		return ""
	if verbosity == "full":
		if fullProfile == "standard":
			message = standardFullMessage(text, translate)
		elif fullProfile == "raw":
			message = str(label or "").strip()
		else:
			message = text
		return redactSensitive(message) if redact else message
	return minimalProfileMessage(text, translate, minimalProfile)


def firstStatusLabel(*labels):
	for label in labels:
		text = " ".join(str(label or "").split())
		if statusDetails(text)[0]:
			return text
	return ""


def elapsedSeconds(label):
	match = re.search(r"(?i)\b(?:for\s+)?(\d+)\s*s(?:ec(?:ond)?s?)?\b", str(label or ""))
	return int(match.group(1)) if match else None


def completedTextDelta(text, spokenOffset=0):
	"""Return newly completed streamed sentences and the updated offset."""
	text = " ".join(str(text or "").split())
	spokenOffset = min(max(int(spokenOffset or 0), 0), len(text))
	end = 0
	for match in re.finditer(r"[.!?](?:[\"'”’\)]*)($|\s)", text):
		end = match.end()
	if end <= spokenOffset:
		return "", spokenOffset
	return text[spokenOffset:end].strip(), end


def changelogForDisplay(markdownText):
	"""Convert the installed Markdown history into clean accessible text."""
	lines = []
	for rawLine in str(markdownText or "").splitlines():
		line = rawLine.strip()
		if line == "# Changelog":
			lines.append("Complete release history")
		elif line.startswith("## "):
			lines.extend(("", f"Version {line[3:].strip()}"))
		elif line.startswith("### "):
			lines.extend(("", line[4:].strip()))
		elif line.startswith("- "):
			lines.append(line[2:])
		else:
			lines.append(line)
	cleanLines = []
	for line in lines:
		if line or not cleanLines or cleanLines[-1]:
			cleanLines.append(line)
	return "\n".join(cleanLines).replace("**", "").replace("`", "").strip()


def viewerTitleMatches(expectedTitle, foregroundName):
	"""Return whether the intended browseable-message viewer is foreground."""
	expected = str(expectedTitle or "").strip().lower()
	foreground = str(foregroundName or "").strip().lower()
	return bool(expected and (foreground == expected or foreground.startswith(expected + " ")))


def previewSelection(items, selection):
	"""Return one preview item, falling back safely to the first item."""
	if not items:
		return None
	if not 0 <= selection < len(items):
		selection = 0
	return items[selection]


def formatCustomAnnouncement(template, message, activity="", seconds=0):
	"""Format a user announcement without allowing unknown fields to break output."""
	template = str(template or "").strip()
	if not template:
		return str(message or "")
	try:
		return template.format(message=message, activity=activity, seconds=seconds)
	except (AttributeError, KeyError, IndexError, ValueError):
		return template
