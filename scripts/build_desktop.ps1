param([string]$Python = 'python', [string]$Destination = '')
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $taskRoot
if (-not $Destination) { $Destination = Join-Path $taskRoot 'dist' }
$taskSamples = Join-Path $taskRoot 'examples/pdfs'
# Build dependencies are for developers only. End users receive the complete bundle.
& $Python -m PyInstaller --noconfirm --clean --onedir --windowed --noupx `
    --name SheetAudit --distpath $Destination --workpath build/desktop `
    --specpath build --paths src --add-data "${taskSamples}:samples" `
    --collect-all pypdfium2 --collect-all pypdfium2_raw desktop_launcher.py
if ($LASTEXITCODE -ne 0) { throw 'Desktop build failed.' }
Copy-Item -LiteralPath (Join-Path $taskRoot 'DESKTOP.md') -Destination (Join-Path $Destination 'SheetAudit/USAGE.md')
Copy-Item -LiteralPath (Join-Path $taskRoot 'THIRD_PARTY_NOTICES.md') -Destination (Join-Path $Destination 'SheetAudit/THIRD_PARTY_NOTICES.md')
Copy-Item -LiteralPath (Join-Path $taskRoot 'LICENSE') -Destination (Join-Path $Destination 'SheetAudit/LICENSE.txt')
& $Python (Join-Path $PSScriptRoot 'collect_desktop_licenses.py') (Join-Path $Destination 'SheetAudit')
if ($LASTEXITCODE -ne 0) { throw 'License collection failed.' }
Write-Host ('Ready: ' + (Join-Path $Destination 'SheetAudit/SheetAudit.exe'))
