"""Pure classification helpers for ChatGPT's embedded browser surface."""

import re


_CONTAINER_PATTERN = re.compile(
	r"\b(?:browser|web\s*view|webview|web preview|website preview)\b",
	re.IGNORECASE,
)
_GENERIC_TITLES = {
	"browser", "browser content", "browser page", "embedded browser", "web preview", "web view", "webview",
}


def normalizedText(value):
	return " ".join(str(value or "").split())


def isEmbeddedBrowserContainerText(*values):
	"""Return whether accessible container text explicitly identifies a browser view."""
	text = " ".join(normalizedText(value) for value in values if normalizedText(value))
	return bool(_CONTAINER_PATTERN.search(text))


def isEmbeddedBrowserContainerRole(roleName):
	"""Exclude browser-launch controls while tolerating unknown Chromium container roles."""
	role = normalizedText(roleName).casefold()
	return role not in {
		"button", "checkbutton", "combobox", "edit", "editabletext", "link", "menu", "menuitem",
	}


def isEmbeddedBrowserDocumentStructure(*roleNames):
	"""Recognize a web document nested inside ChatGPT's outer Chromium document."""
	roles = tuple(normalizedText(role).casefold() for role in roleNames)
	return sum(role == "document" for role in roles) >= 2


def embeddedBrowserControlKind(name, roleName=""):
	"""Classify conservatively named embedded-browser controls."""
	text = normalizedText(name).casefold()
	role = normalizedText(roleName).casefold()
	if text in ("back", "go back", "previous page"):
		return "back"
	if text in ("forward", "go forward", "next page"):
		return "forward"
	if text in ("reload", "reload page", "refresh", "refresh page"):
		return "reload"
	if text in ("stop loading", "stop page loading"):
		return "stop"
	if text in (
		"address", "address bar", "address and search bar", "search or enter address",
		"search or type url", "url",
	):
		return "address"
	if text in (
		"open externally", "open in browser", "open in default browser",
		"open in external browser", "open in system browser",
	):
		return "external"
	if text in ("close browser", "close browser view", "close preview", "close web view"):
		return "close"
	if role == "document":
		return "content"
	return ""


def embeddedBrowserTitle(name):
	"""Return a bounded useful page title, excluding generic browser container names."""
	title = normalizedText(name)
	if not title or title.casefold() in _GENERIC_TITLES:
		return ""
	return title[:200]


def embeddedBrowserProgress(*values):
	"""Return ``(identity, percent, bucket)`` for browser loading progress."""
	parts = tuple(normalizedText(value) for value in values if normalizedText(value))
	text = " ".join(parts)
	if not text:
		return None
	match = re.search(r"(?<!\d)(100|[0-9]{1,2})\s*(?:%|percent\b)", text, re.IGNORECASE)
	lower = text.casefold()
	hasLoadingState = re.search(r"\b(?:loading|opening page|navigating)\b", lower) is not None
	directPercent = next(
		(int(part) for part in parts if re.fullmatch(r"100|[0-9]{1,2}", part)),
		None,
	)
	if not match and directPercent is None and not hasLoadingState:
		return None
	percent = int(match.group(1)) if match else directPercent
	bucket = None if percent is None else (
		100 if percent >= 100 else (0 if percent == 0 else max(10, (percent // 10) * 10))
	)
	identity = re.sub(r"(?<!\d)(?:100|[0-9]{1,2})\s*(?:%|percent\b)", "", lower)
	if directPercent is not None:
		identity = " ".join(part for part in identity.split() if part != str(directPercent))
	identity = " ".join(identity.split()) or "embedded browser"
	return identity[:160], percent, bucket
