"""Generate NVDA Add-on Store submission metadata for a built package."""

import argparse
import hashlib
import json
import re
from pathlib import Path


def _manifestValue(text, name):
	match = re.search(rf"(?m)^{re.escape(name)}\s*=\s*(.+)$", text)
	if not match:
		raise ValueError(f"manifest field is missing: {name}")
	return match.group(1).strip().strip('"')


def _versionObject(value):
	parts = [int(part) for part in value.split(".")]
	if len(parts) == 2:
		parts.append(0)
	if len(parts) != 3:
		raise ValueError(f"invalid version: {value}")
	return {"major": parts[0], "minor": parts[1], "patch": parts[2]}


def _releaseNotes(changelog, version):
	match = re.search(
		rf"(?ms)^## {re.escape(version)}\s*(.*?)(?=^##\s|\Z)",
		changelog,
	)
	if not match:
		raise ValueError(f"changelog section is missing: {version}")
	return match.group(1).strip()


def generate(projectRoot, packagePath, downloadUrl, channel="stable"):
	if not downloadUrl.startswith("https://") or not downloadUrl.endswith(".nvda-addon"):
		raise ValueError("download URL must be direct HTTPS and end in .nvda-addon")
	manifest = (projectRoot / "manifest.ini").read_text(encoding="utf-8")
	version = _manifestValue(manifest, "version")
	summary = _manifestValue(manifest, "summary")
	description = _manifestValue(manifest, "description")
	homepage = _manifestValue(manifest, "url")
	minimum = _manifestValue(manifest, "minimumNVDAVersion")
	lastTested = _manifestValue(manifest, "lastTestedNVDAVersion")
	packagePath = Path(packagePath)
	if not packagePath.is_file():
		raise FileNotFoundError(packagePath)
	return {
		"addonId": _manifestValue(manifest, "name"),
		"channel": channel,
		"addonVersionNumber": _versionObject(version),
		"addonVersionName": version,
		"displayName": summary,
		"publisher": "Justin Coffin",
		"description": description,
		"homepage": homepage,
		"minNVDAVersion": _versionObject(minimum),
		"lastTestedVersion": _versionObject(lastTested),
		"URL": downloadUrl,
		"sha256": hashlib.sha256(packagePath.read_bytes()).hexdigest().upper(),
		"sourceURL": homepage,
		"license": "GPL v2 or later",
		"licenseURL": homepage.rstrip("/") + "/blob/main/LICENSE.txt",
		"changelog": _releaseNotes(
			(projectRoot / "changelog.md").read_text(encoding="utf-8"), version,
		),
	}


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("package")
	parser.add_argument("downloadUrl")
	parser.add_argument("--channel", choices=("stable", "beta", "dev"), default="stable")
	parser.add_argument("--output")
	args = parser.parse_args()
	root = Path(__file__).resolve().parents[1]
	metadata = generate(root, args.package, args.downloadUrl, args.channel)
	serialized = json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"
	if args.output:
		Path(args.output).write_text(serialized, encoding="utf-8", newline="\n")
	else:
		print(serialized, end="")
