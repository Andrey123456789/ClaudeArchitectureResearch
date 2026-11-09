# Records the executable identity facts as raw evidence. Read-only toward the executables.
# Usage: powershell -NoProfile -File host_probe.ps1 <output-file>
param([string]$OutFile)
$lines = New-Object System.Collections.ArrayList
function Add($s) { [void]$lines.Add([string]$s) }
$pinned = "$env:LOCALAPPDATA\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude-code\2.1.317\a33aa5518497\claude.exe"
$alias = "$env:APPDATA\Claude\claude-code\2.1.317\a33aa5518497\claude.exe"
$old = "$env:APPDATA\Claude\claude-code\2.1.293\83cb0bd7fed4\claude.exe"
Add "probe_time: $((Get-Date).ToString('o'))"
Add "claude_on_PATH: $(@(Get-Command claude -All -ErrorAction SilentlyContinue | ForEach-Object Source) -join '; ')"
Add "orchestrator_CLAUDE_CODE_EXECPATH: $env:CLAUDE_CODE_EXECPATH"
foreach ($p in @($pinned, $alias, $old)) {
    Add ""
    Add "path: $p"
    Add "exists: $(Test-Path $p)"
    $i = Get-Item $p
    Add "size_bytes: $($i.Length)"
    Add "last_write_time: $($i.LastWriteTime.ToString('o'))"
    Add "file_version_resource: $($i.VersionInfo.FileVersion)"
    Add "sha256: $((Get-FileHash $p -Algorithm SHA256).Hash.ToLower())"
    $s = Get-AuthenticodeSignature $p
    Add "authenticode_status: $($s.Status)"
    Add "authenticode_subject: $($s.SignerCertificate.Subject)"
    Add "file_id: $(fsutil file queryfileid $p)"
    Add "version_output: $(& $p --version)"
    Add "version_exit_code: $LASTEXITCODE"
}
Add ""
$d = Split-Path $pinned
Add ".payload: $((Get-Content (Join-Path $d '.payload') -Raw) -replace '\s+',' ')"
Add ".verified: $((Get-Content (Join-Path $d '.verified') -Raw).Trim())"
$lines | Out-File -FilePath $OutFile -Encoding utf8
$lines
