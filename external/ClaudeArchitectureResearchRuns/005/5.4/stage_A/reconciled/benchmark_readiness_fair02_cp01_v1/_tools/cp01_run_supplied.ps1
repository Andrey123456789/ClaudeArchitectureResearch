# Runs the supplied, unmodified Test-IDE0005.ps1 from a hash-verified copy in a new temp folder.
# Archives its console output, exit code, and the logs it leaves in its own IDE0005-Probe-<guid> folder.
# Writes only to the new temp folders and to -OutDir.
[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string] $KitDir,
    [Parameter(Mandatory)] [string] $OutDir
)
$ErrorActionPreference = 'Stop'

function Get-Sha256([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Write-Utf8([string] $Path, [string] $Text) { [System.IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false))) }

New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
$KitDir = (Resolve-Path -LiteralPath $KitDir).Path
$OutDir = (Resolve-Path -LiteralPath $OutDir).Path

# 1. Hash-verified copy of the kit in a new temp folder.
$copyRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('CP01-KitCopy-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $copyRoot | Out-Null
Copy-Item -Path (Join-Path $KitDir '*') -Destination $copyRoot -Recurse
$copyCheck = @()
Get-ChildItem -LiteralPath $KitDir -Recurse -File -Force | ForEach-Object {
    $rel = $_.FullName.Substring($KitDir.Length).TrimStart('\')
    $copied = Join-Path $copyRoot $rel
    $copyCheck += [pscustomobject]@{ file = $rel; kit = (Get-Sha256 $_.FullName); copy = (Get-Sha256 $copied) }
}
if (@($copyCheck | Where-Object { $_.kit -ne $_.copy }).Count -gt 0) { throw 'Kit copy hash mismatch.' }

# 2. Process-scoped environment: no telemetry, no background workload-update check, no lingering nodes.
$envVars = [ordered]@{
    DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE = '1'
    DOTNET_NOLOGO = '1'
    DOTNET_SKIP_FIRST_TIME_EXPERIENCE = '1'
    MSBUILDDISABLENODEREUSE = '1'
}
foreach ($k in $envVars.Keys) { Set-Item -Path "env:$k" -Value $envVars[$k] }

# 3. Run the supplied script exactly as its README instructs, working directory = %TEMP%.
$tempDir = [System.IO.Path]::GetTempPath()
$psExe = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$scriptPath = Join-Path $copyRoot 'Test-IDE0005.ps1'
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = $psExe
$psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
$psi.WorkingDirectory = $tempDir
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.CreateNoWindow = $true
$started = (Get-Date).ToString('o')
$proc = [System.Diagnostics.Process]::Start($psi)
$outTask = $proc.StandardOutput.ReadToEndAsync()
$errTask = $proc.StandardError.ReadToEndAsync()
$proc.WaitForExit()
$stdout = $outTask.Result
$stderr = $errTask.Result
$exit = $proc.ExitCode
$ended = (Get-Date).ToString('o')
Write-Utf8 (Join-Path $OutDir 'console.stdout.log') $stdout
Write-Utf8 (Join-Path $OutDir 'console.stderr.log') $stderr

# 4. Archive the probe folder the script created (logs, inputs, summary; not bin/obj).
$probeRoot = $null
$m = [regex]::Match($stdout, 'All artifacts and full build logs:\s*(?<p>\S.*?)\s*$', 'Multiline')
if ($m.Success) { $probeRoot = $m.Groups['p'].Value.Trim() }
if (-not $probeRoot) {
    $cand = Get-ChildItem -LiteralPath $tempDir -Directory -Filter 'IDE0005-Probe-*' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($cand -and $cand.LastWriteTime -ge [datetime]$started) { $probeRoot = $cand.FullName }
}
$archived = @()
if ($probeRoot -and (Test-Path -LiteralPath $probeRoot)) {
    $dest = Join-Path $OutDir 'probe_root_copy'
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
    Get-ChildItem -LiteralPath $probeRoot -Recurse -File -Force | Where-Object { $_.FullName -notmatch '\\(bin|obj)\\' } | ForEach-Object {
        $rel = $_.FullName.Substring($probeRoot.Length).TrimStart('\')
        $target = Join-Path $dest $rel
        New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $target
        $archived += [pscustomobject]@{ file = $rel; sha256 = (Get-Sha256 $_.FullName) }
    }
}

$meta = [ordered]@{
    purpose = 'Run of the supplied, unmodified Test-IDE0005.ps1 (CP-01)'
    script_sha256 = (Get-Sha256 $scriptPath)
    kit_copy_dir = $copyRoot
    kit_copy_hash_check = 'MATCH'
    kit_copy_files = $copyCheck
    command = "`"$psExe`" $($psi.Arguments)"
    working_directory = $tempDir
    powershell_host_version = $PSVersionTable.PSVersion.ToString()
    process_environment = $envVars
    started = $started
    ended = $ended
    exit_code = $exit
    probe_root = $probeRoot
    archived_files = $archived
}
Write-Utf8 (Join-Path $OutDir 'RUN_METADATA.json') ($meta | ConvertTo-Json -Depth 5)
Write-Host "exit=$exit probeRoot=$probeRoot archived=$($archived.Count)"
