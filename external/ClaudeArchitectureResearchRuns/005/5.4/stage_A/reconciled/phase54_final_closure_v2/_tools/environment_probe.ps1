# Static, read-only environment probe for the Phase 5.4 final closure. Launches nothing: file metadata, hashes and process listings only.
# Usage: powershell -NoProfile -File environment_probe.ps1
$out = Join-Path (Split-Path -Parent $PSScriptRoot) 'evidence\ENVIRONMENT_PROBE.txt'
$lines = New-Object System.Collections.ArrayList
function Add-Line([string]$s) { [void]$lines.Add($s) }

Add-Line "probe_time: $((Get-Date).ToString('o'))"
Add-Line 'scope: observations at probe time; not a recording made during the Desktop test sessions'
Add-Line ''
Add-Line '[Claude Desktop package]'
$pkg = Get-AppxPackage -Name 'Claude' | Select-Object -First 1
Add-Line "name: $($pkg.Name)"
Add-Line "version: $($pkg.Version)"
Add-Line "package_family: $($pkg.PackageFamilyName)"
Add-Line "install_location: $($pkg.InstallLocation)"
$dir = Get-Item -LiteralPath $pkg.InstallLocation
Add-Line "install_dir_created: $($dir.CreationTime.ToString('o'))"
$manifest = Join-Path $pkg.InstallLocation 'AppxManifest.xml'
Add-Line "appx_manifest_sha256: $((Get-FileHash -LiteralPath $manifest -Algorithm SHA256).Hash.ToLower())"
Add-Line "appx_manifest_identity_version: $(([xml](Get-Content -LiteralPath $manifest)).Package.Identity.Version)"
$app = Get-Item -LiteralPath (Join-Path $pkg.InstallLocation 'app\claude.exe')
Add-Line "desktop_exe_file_version: $($app.VersionInfo.FileVersion)"
Add-Line ''
Add-Line '[Claude Desktop processes from the package]'
Get-Process -Name claude -ErrorAction SilentlyContinue | Where-Object { $_.Path -like '*WindowsApps*' } | Sort-Object StartTime | ForEach-Object { Add-Line ("pid={0} start={1} path={2}" -f $_.Id, $_.StartTime.ToString('o'), $_.Path) }
Add-Line ''
Add-Line '[Claude Code CLI binaries, static]'
$root = Join-Path $env:LOCALAPPDATA 'Claude-Data\claude_pzs8sxrjxfjjc\claude-code'
Get-ChildItem -LiteralPath $root -Recurse -Filter claude.exe | ForEach-Object {
    $sig = Get-AuthenticodeSignature -LiteralPath $_.FullName
    Add-Line "path: $($_.FullName)"
    Add-Line "size_bytes: $($_.Length)"
    Add-Line "last_write_time: $($_.LastWriteTime.ToString('o'))"
    Add-Line "file_version_resource: $($_.VersionInfo.FileVersion)"
    Add-Line "sha256: $((Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower())"
    Add-Line "authenticode_status: $($sig.Status)"
    Add-Line "authenticode_signer: $($sig.SignerCertificate.Subject)"
    Add-Line ''
}
Add-Line '[Paths recorded by the 2026-11-08 recheck, existence now]'
foreach ($p in @("$env:APPDATA\Claude\claude-code\2.1.317\a33aa5518497\claude.exe", "$env:LOCALAPPDATA\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude-code\2.1.317\a33aa5518497\claude.exe")) { Add-Line ("{0} => {1}" -f $p, (Test-Path -LiteralPath $p)) }
Add-Line ''
Add-Line '[Claude Code CLI processes at probe time]'
Add-Line 'note: start times only; bound_to_test_session reports whether the process command line names a test session id'
$ids = '9fe6ddea-d2e5-442a-b5b3-d50708fcc695', '41e9d77f-7c86-43f6-9462-5848bdaa0cfb'
Get-CimInstance Win32_Process -Filter "Name='claude.exe'" | Where-Object { $_.ExecutablePath -like '*claude-code*' } | Sort-Object CreationDate | ForEach-Object {
    $cl = [string]$_.CommandLine
    $hit = ($ids | Where-Object { $cl -match $_ }) -join ','
    Add-Line ("pid={0} start={1} path={2} bound_to_test_session=[{3}]" -f $_.ProcessId, $_.CreationDate.ToString('o'), $_.ExecutablePath, $hit)
}
Add-Line ''
Add-Line "claude_on_PATH: $((Get-Command claude -ErrorAction SilentlyContinue).Source)"
Add-Line "windows: $((Get-CimInstance Win32_OperatingSystem).Caption) $((Get-CimInstance Win32_OperatingSystem).Version)"
[System.IO.File]::WriteAllLines($out, [string[]]$lines, (New-Object System.Text.UTF8Encoding($false)))
$lines
