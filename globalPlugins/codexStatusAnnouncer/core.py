"""NVDA-independent parsing and privacy helpers for Codex activity."""

import re
import string
from collections import deque


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


def shouldClearBusyAfterStatusGap(currentBusy, gapSeconds, graceSeconds=2.0):
	"""Return whether an active task should be cleared after status disappears."""
	return bool(currentBusy) and float(gapSeconds) >= float(graceSeconds)


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
	if lower.startswith(("finished", "completed", "done", "cancelled", "canceled")):
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
	text = re.sub(r"(?i)\b(api[_-]?key|token|secret|password|passwd|pwd|authorization)\s*[:=]\s*([^\s;]+)", r"\1=[redacted]", text)
	text = re.sub(r"(?i)(C:\\Users\\)[^\\\s]+", r"\1[user]", text)
	text = re.sub(r"(?i)(/home/|/users/)[^/\s]+", r"\1[user]", text)
	text = re.sub(r"(?i)\b(remote\s+(?:key|password)|connection\s+key)\s*[:=]\s*([^\s;]+)", r"\1=[redacted]", text)
	text = re.sub(r"(?i)\b(bearer)\s+[a-z0-9._~+/-]+=*", r"\1 [redacted]", text)
	return text


def statusMessage(label, translate=lambda text: text, verbosity="minimal", redact=False):
	text = " ".join(str(label or "").split())
	category, minimal = statusDetails(text)
	if not category:
		return ""
	if verbosity == "full":
		return redactSensitive(text) if redact else text
	return translate(minimal)


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
	return bool(expected and expected in foreground)


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
	except (KeyError, IndexError, ValueError):
		return template


def unknownAnnouncementPlaceholders(template):
	"""Return unsupported replacement fields used by a custom announcement."""
	unknown = set()
	try:
		for literal, field, formatSpec, conversion in string.Formatter().parse(str(template or "")):
			if field and field not in ("message", "activity", "seconds"):
				unknown.add(field)
	except ValueError:
		unknown.add("invalid format")
	return tuple(sorted(unknown))
