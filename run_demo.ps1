$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) {
    $taskBasePython = $null
    if (Get-Command py -ErrorAction SilentlyContinue) {
        $taskInstalled = & py -0p
        foreach ($taskLine in $taskInstalled) {
            if ($taskLine -match '^\s*-(?:V:)?3\.(?:10|11|12)\s+\*?\s*(.+python(?:\.exe)?)\s*$') {
                $taskBasePython = $Matches[1]
                break
            }
        }
    }
    if (-not $taskBasePython) {
        $taskBundled = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
        if (Test-Path -LiteralPath $taskBundled) { $taskBasePython = $taskBundled }
        elseif (Get-Command python -ErrorAction SilentlyContinue) { $taskBasePython = (Get-Command python).Source }
        else { throw 'Python 3.10+ is required. Install it, then run this script again.' }
    }
    & $taskBasePython -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the project Python environment.' }
}
$taskPackagePresent = & $taskPython -c "import importlib.util; print(int(importlib.util.find_spec('sheetaudit') is not None))"
if ($LASTEXITCODE -ne 0) { throw 'The project Python environment is not working.' }
if ($taskPackagePresent -ne '1') {
    & $taskPython -m pip install -e .
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. Check your network and retry pip install -e .' }
}
$taskOutput = 'reports\demo-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')
& $taskPython -m sheetaudit audit examples/pdfs examples/regressions --out $taskOutput
if ($LASTEXITCODE -ne 0) { throw 'The run had errors. Inspect the report and summary.json if created.' }
Write-Host ('Open the report: ' + (Join-Path $PSScriptRoot ($taskOutput + '\report.xlsx')))
