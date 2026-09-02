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
	pythonPaths = tuple(path for path in projectRoot.rglob("*.py") if "__pycache__" not in path.parts)
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
	assert re.search(r"(?m)^minimumNVDAVersion = 2026\.3\.0$", manifest), "minimum NVDA alpha compatibility mismatch"
	assert re.search(r"(?m)^lastTestedNVDAVersion = 2026\.3\.0$", manifest), "tested NVDA alpha compatibility mismatch"
	assert re.search(r"(?m)^updateChannel = dev$", manifest), "alpha-targeted package must use the dev channel"
	assert f'[string]$Version = "{version}"' in build, "build default version mismatch"
	assert f"## {version}" in changelog, "changelog version heading missing"
	assert "Adds assignable focus- and browse-mode actions" not in manifest, "stale gesture changelog in manifest"
	gesturePairs = re.findall(r'"kb:control\+([0-9])": "([A-Za-z0-9]+ChatMessage)"', plugin)
	assert len(gesturePairs) == 10, "expected ten configurable recent-message default gestures"
	assert len({digit for digit, scriptName in gesturePairs}) == 10, "duplicate recent-message gesture"
	assert len({scriptName for digit, scriptName in gesturePairs}) == 10, "recent-message actions must be independent"
	assert (projectRoot / "locale/codexAccessToolkit.pot").is_file(), "translation template missing"
	packagedPaths = tuple(packageFiles(projectRoot))
	combinedSource = "\n".join(path.read_text(encoding="utf-8") for path in packagedPaths if path.suffix == ".py")
	for forbidden in FORBIDDEN_SOURCE:
		assert forbidden not in combinedSource, f"forbidden source found: {forbidden}"
	expected = tuple(path.relative_to(projectRoot).as_posix() for path in packagedPaths)
	with zipfile.ZipFile(packagePath) as archive:
		names = tuple(archive.namelist())
		assert archive.testzip() is None, "archive CRC failure"
		assert len(names) == len(set(names)), "duplicate archive entries"
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
