"""Audit source metadata and a built NVDA add-on archive."""

import argparse
import ast
import re
import zipfile
from pathlib import Path

from build_addon import packageFiles


FORBIDDEN_SOURCE = (
	"import sqlite3", "import requests", "import numpy", "import yaml",
	"gesture=", '"kb:enter"', "script_enter", "script_openAddFilesAndMore",
	"script_openModelSelector", "script_openChangePermissions",
)


def manifestVersionMatches(text, version):
	"""Match a manifest version from either LF or CRLF archive content."""
	return bool(re.search(rf"(?m)^version = {re.escape(version)}\r?$", text))


def audit(projectRoot, packagePath, version):
	projectRoot = Path(projectRoot).resolve()
	packagePath = Path(packagePath).resolve()
	assert packagePath.name == f"chatGPTDesktopAccess-{version}.nvda-addon", "public package filename mismatch"
	pythonPaths = tuple(
		path for path in projectRoot.rglob("*.py")
		if "__pycache__" not in path.parts
		and "outputs" not in path.relative_to(projectRoot).parts
	)
	for path in pythonPaths:
		ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
	plugin = (projectRoot / "globalPlugins/codexStatusAnnouncer/__init__.py").read_text(encoding="utf-8")
	manifest = (projectRoot / "manifest.ini").read_text(encoding="utf-8")
	build = (projectRoot / "build.ps1").read_text(encoding="utf-8")
	changelog = (projectRoot / "changelog.md").read_text(encoding="utf-8")
	assert f'ADDON_VERSION = "{version}"' in plugin, "source version mismatch"
	assert manifestVersionMatches(manifest, version), "manifest version mismatch"
	assert re.search(r'(?m)^author = "?.+<[^<>\s]+@[^<>\s]+>"?$', manifest), "manifest author email missing"
	assert re.search(r"(?m)^url = https://.+$", manifest), "manifest HTTPS homepage missing"
	assert re.search(r"(?m)^docFileName = readme\.md$", manifest), "manifest documentation field missing"
	assert re.search(r"(?m)^minimumNVDAVersion = 2023\.1\.0$", manifest), "minimum stable NVDA compatibility mismatch"
	assert re.search(r"(?m)^lastTestedNVDAVersion = 2026\.2\.0$", manifest), "tested stable NVDA compatibility mismatch"
	assert re.search(r"(?m)^updateChannel = None$", manifest), "stable package update channel mismatch"
	assert f'[string]$Version = "{version}"' in build, "build default version mismatch"
	assert f"## {version}" in changelog, "changelog version heading missing"
	assert "Adds assignable focus- and browse-mode actions" not in manifest, "stale gesture changelog in manifest"
	chatGPTAppModule = (projectRoot / "appModules/chatgpt.py").read_text(encoding="utf-8")
	codexAppModule = (projectRoot / "appModules/codex.py").read_text(encoding="utf-8")
	browserDialogPath = projectRoot / "globalPlugins/codexStatusAnnouncer/browserNavigatorDialog.py"
	assert browserDialogPath.is_file(), "Embedded Browser Navigator module missing"
	browserDialog = browserDialogPath.read_text(encoding="utf-8")
	gesturePairs = re.findall(r'"kb:control\+([0-9])": "([A-Za-z0-9]+ChatMessage)"', chatGPTAppModule)
	assert len(gesturePairs) == 10, "expected ten configurable recent-message default gestures"
	assert len({digit for digit, scriptName in gesturePairs}) == 10, "duplicate recent-message gesture"
	assert len({scriptName for digit, scriptName in gesturePairs}) == 10, "recent-message actions must be independent"
	assert '"kb:NVDA+alt+v": "toggleVoiceMode"' in chatGPTAppModule, "voice-mode default gesture missing"
	assert '"kb:NVDA+alt+m": "toggleMicrophoneMute"' in chatGPTAppModule, "microphone default gesture missing"
	browserScripts = (
		"openEmbeddedBrowserNavigator", "readEmbeddedBrowserPageSummary", "showEmbeddedBrowserSnapshot",
		"openEmbeddedBrowserExternally", "returnToChatGPTPrompt",
	)
	for scriptName in browserScripts:
		assert f"def script_{scriptName}(" in chatGPTAppModule, f"browser command missing: {scriptName}"
		assert f'": "{scriptName}"' not in chatGPTAppModule, f"browser command must be unassigned: {scriptName}"
	assert "class AppModule(appModuleHandler.AppModule)" in chatGPTAppModule, "commands are not app scoped"
	assert "from appModules.chatgpt import AppModule" in codexAppModule, "alternate Codex host is not app scoped"
	assert "__gestures" not in plugin, "application commands must not be bound by the global plugin"
	assert "gesture.send()" not in plugin + chatGPTAppModule, "application commands must not emulate keys outside ChatGPT"
	assert "def _migrateApplicationGestureMappings():" in plugin, "existing gesture assignments are not migrated"
	assert "Unrelated global mappings are never moved." in changelog, "gesture migration is missing from changelog"
	for expectedLimit in (
		"BROWSER_SCAN_SLICE_OBJECTS = 20", "BROWSER_SCAN_SLICE_SECONDS = 0.008",
		"BROWSER_SCAN_YIELD_MILLISECONDS = 15",
		"BROWSER_SCAN_MAX_OBJECTS = 900", "BROWSER_SCAN_MAX_ITEMS = 500",
		"BROWSER_SNAPSHOT_MAX_LINES = 700",
	):
		assert expectedLimit in plugin, f"browser scan safety limit missing: {expectedLimit}"
	assert plugin.count("BROWSER_SCAN_YIELD_MILLISECONDS, self._continueEmbeddedBrowserScan") == 2, "browser scans are not time sliced"
	assert "evt.GetKeyCode() == wx.WXK_F10 and evt.ShiftDown()" in browserDialog, "browser context menu missing"
	assert '"rememberEmbeddedBrowserLocations": "boolean(default=True)"' in plugin, "location setting missing"
	assert 'self._chatHistoryCaches = {"chatgpt": (), "codex": ()}' in plugin, "mode-specific recent history missing"
	assert 'self._archivedChatHistoryCaches = {"chatgpt": (), "codex": ()}' in plugin, "mode-specific archived history missing"
	assert "conversationModeFromSwitchLabel(fieldName)" in plugin, "authoritative mode-switch control is not scanned"
	assert "self._conversationModeObserved = True" in plugin, "authoritative mode precedence is not retained"
	assert "CHAT_HISTORY_MODE_SETTLE_SECONDS = 0.75" in plugin, "mode-specific history settle delay is missing"
	assert "CHAT_HISTORY_SNAPSHOT_CONFIRM_SECONDS = 0.25" in plugin, "history snapshot confirmation is missing"
	assert "chatHistorySnapshotDecision(" in plugin, "settled history decision is not applied"
	assert "loadActiveCodexThreadTitles(codexRoot)" in plugin, "unified Recents list is not classified with the Codex index"
	assert "self._modeSpecificRecentChatTitles(scanMode, recentSnapshot)" in plugin, "mixed recent entries can reach a mode cache"
	assert "if not self._chatHistoryCacheCurrent.get(mode, False):" in plugin, "unsettled chat history can still open"
	assert 'if source == "archived" and mode == "codex":' in plugin, "archived history source is not mode-specific"
	assert plugin.count("not isChatHistoryInterfaceText(") == 2, "history interface controls are not filtered from both lists"
	assert 'if not recentsSeen and plainText.casefold() == "recents":' in plugin, "recent history region can restart inside a conversation"
	assert plugin.count("inRecents = inArchived = False") == 2, "conversation boundaries do not close both history regions"
	assert 'title=_("{agent} chat history").format(agent=agentName)' in (
		projectRoot / "globalPlugins/codexStatusAnnouncer/chatHistoryDialog.py"
	).read_text(encoding="utf-8"), "history dialog does not identify the active mode"
	assert re.search(r'(?m)^summary = "ChatGPT Desktop Access for NVDA"$', manifest), "public display name mismatch"
	assert re.search(r"(?m)^url = https://github\.com/jcoffin1/chatgpt-desktop-access$", manifest), "public repository mismatch"
	assert (projectRoot / "locale/chatGPTDesktopAccess.pot").is_file(), "translation template missing"
	packagedPaths = tuple(packageFiles(projectRoot))
	combinedSource = "\n".join(path.read_text(encoding="utf-8") for path in packagedPaths if path.suffix == ".py")
	for forbidden in FORBIDDEN_SOURCE:
		assert forbidden not in combinedSource, f"forbidden source found: {forbidden}"
	expected = tuple(path.relative_to(projectRoot).as_posix() for path in packagedPaths)
	with zipfile.ZipFile(packagePath) as archive:
		names = tuple(archive.namelist())
		assert archive.testzip() is None, "archive CRC failure"
		assert len(names) == len(set(names)), "duplicate archive entries"
		for required in ("manifest.ini", "readme.md", "changelog.md", "LICENSE.txt"):
			assert required in names, f"required package file missing: {required}"
		assert "globalPlugins/codexStatusAnnouncer/browserNavigatorDialog.py" in names, "navigator module not packaged"
		assert not any(name.endswith(".pot") for name in names), "developer translation template packaged"
		assert not any(
			name.startswith("globalPlugins/codexStatusAnnouncer/sounds/") and name.count("/") == 3
			for name in names
		), "obsolete un-tiered sound packaged"
		assert names == expected, "archive layout or ordering mismatch"
		assert not any("__pycache__" in name or name.endswith((".pyc", ".pyo")) for name in names), "cache file packaged"
		packagedManifest = archive.read("manifest.ini").decode("utf-8")
		assert manifestVersionMatches(packagedManifest, version), "packaged manifest mismatch"
		assert sum(name.endswith(".wav") for name in names) == 51, "sound inventory mismatch"
	return len(pythonPaths), len(expected)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("package")
	parser.add_argument("version")
	args = parser.parse_args()
	root = Path(__file__).resolve().parents[1]
	pythonCount, entryCount = audit(root, args.package, args.version)
	print(f"Audit valid: {pythonCount} Python files; {entryCount} archive entries")
