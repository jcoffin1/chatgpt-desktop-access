param(
	[string]$Version = "2.2.5"
)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$outputRoot = Join-Path $projectRoot "outputs"
if (-not (Test-Path -LiteralPath $outputRoot)) {
	New-Item -ItemType Directory -Path $outputRoot | Out-Null
}
$package = Join-Path $outputRoot "codexStatusAnnouncer-$Version.nvda-addon"
$env:PYTHONDONTWRITEBYTECODE = "1"

Push-Location $projectRoot
try {
	python -m unittest discover -s .\tests -v
	if ($LASTEXITCODE -ne 0) { throw "Automated tests failed" }
	python -c "from pathlib import Path; files=list(Path('.').rglob('*.py')); [compile(p.read_text(encoding='utf-8'), str(p), 'exec') for p in files]; print(f'Syntax valid: {len(files)} Python files')"
	if ($LASTEXITCODE -ne 0) { throw "Python syntax validation failed" }
	if (Test-Path -LiteralPath $package) { Remove-Item -LiteralPath $package -Force }
	tar --format zip -cf $package manifest.ini readme.md changelog.md LICENSE.txt globalPlugins\__init__.py globalPlugins\codexStatusAnnouncer\__init__.py globalPlugins\codexStatusAnnouncer\core.py globalPlugins\codexStatusAnnouncer\sounds\soft globalPlugins\codexStatusAnnouncer\sounds\normal globalPlugins\codexStatusAnnouncer\sounds\loud
	if ($LASTEXITCODE -ne 0) { throw "Package creation failed" }
	$entries = tar -tf $package
	if ($entries -match "__pycache__|\.pyc$") { throw "Generated cache file found in package" }
	if (($entries | Where-Object { $_ -match "\.wav$" }).Count -ne 42) { throw "Expected 42 WAV files" }
	$packagedManifest = (tar -xOf $package manifest.ini) -join "`n"
	if ($packagedManifest -notmatch "(?m)^version = $([regex]::Escape($Version))$") { throw "Packaged manifest version mismatch" }
	Copy-Item -LiteralPath (Join-Path $projectRoot "changelog.md") -Destination (Join-Path $outputRoot "CHANGELOG-$Version.md") -Force
	Copy-Item -LiteralPath (Join-Path $projectRoot "readme.md") -Destination (Join-Path $outputRoot "README-$Version.md") -Force
	Get-FileHash -Algorithm SHA256 -LiteralPath $package
} finally {
	Pop-Location
}
