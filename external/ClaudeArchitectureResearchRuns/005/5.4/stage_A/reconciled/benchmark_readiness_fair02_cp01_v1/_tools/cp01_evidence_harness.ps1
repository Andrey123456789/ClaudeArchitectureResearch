# CP-01 replica and evidence harness.
# Re-creates the supplied probe's cases with the SAME commands and arguments as Test-IDE0005.ps1,
# but captures stdout and stderr separately (no PowerShell 5.1 NativeCommandError abort), counts only
# compiler-format diagnostics, queries effective MSBuild properties, and hashes every case input.
# Writes only to a new %TEMP%\CP01-Evidence-<guid> folder and to -OutDir. Never edits the kit.
[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string] $KitDir,
    [Parameter(Mandatory)] [string] $OutDir
)
$ErrorActionPreference = 'Stop'

function Get-Sha256([string] $Path) { (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Write-Utf8([string] $Path, [string] $Text) { [System.IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false))) }

function Invoke-Logged {
    param([string] $Exe, [string[]] $ArgList, [string] $Cwd, [string] $LogBase)
    $quoted = $ArgList | ForEach-Object { if ($_ -match '[\s"]') { '"' + ($_ -replace '"', '\"') + '"' } else { $_ } }
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $Exe
    $psi.Arguments = ($quoted -join ' ')
    $psi.WorkingDirectory = $Cwd
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true
    $p = [System.Diagnostics.Process]::Start($psi)
    $o = $p.StandardOutput.ReadToEndAsync()
    $e = $p.StandardError.ReadToEndAsync()
    $p.WaitForExit()
    Write-Utf8 "$LogBase.stdout.log" $o.Result
    Write-Utf8 "$LogBase.stderr.log" $e.Result
    [pscustomobject]@{
        command = "dotnet $($psi.Arguments)"
        cwd = $Cwd
        exit_code = $p.ExitCode
        stdout_log = (Split-Path -Leaf "$LogBase.stdout.log")
        stderr_log = (Split-Path -Leaf "$LogBase.stderr.log")
        stdout = $o.Result
        stderr = $e.Result
    }
}

# Compiler-format diagnostics only: "<file>(<line>,<col>): warning|error <ID>: <message> [<project>]"
# and tool-level "CSC : warning <ID>: <message> [<project>]". Deduplicated (MSBuild repeats them in the summary).
function Get-Diagnostics([string] $Text) {
    $set = [ordered]@{}
    $rx = '(?m)^\s*(?:\d+>)?(?<loc>(?:[A-Za-z]:\\[^(\r\n]*?\(\d+,\d+\))|CSC)\s*:\s*(?<sev>warning|error)\s+(?<id>[A-Za-z]+\d*[A-Za-z]*):\s*(?<msg>[^\r\n]*?)\s*(?:\[[^\]\r\n]*\])?\s*$'
    foreach ($m in [regex]::Matches($Text, $rx)) {
        $loc = $m.Groups['loc'].Value
        if ($loc -ne 'CSC') { $loc = (Split-Path -Leaf ($loc -replace '\(\d+,\d+\)$', '')) + ($loc -replace '^.*(\(\d+,\d+\))$', '$1') }
        $key = "$loc|$($m.Groups['sev'].Value)|$($m.Groups['id'].Value)"
        if (-not $set.Contains($key)) {
            $set[$key] = [pscustomobject]@{ location = $loc; severity = $m.Groups['sev'].Value; id = $m.Groups['id'].Value; message = $m.Groups['msg'].Value }
        }
    }
    @($set.Values)
}

New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
$KitDir = (Resolve-Path -LiteralPath $KitDir).Path
$OutDir = (Resolve-Path -LiteralPath $OutDir).Path

$envVars = [ordered]@{
    DOTNET_CLI_TELEMETRY_OPTOUT = '1'
    DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE = '1'
    DOTNET_NOLOGO = '1'
    DOTNET_SKIP_FIRST_TIME_EXPERIENCE = '1'
    MSBUILDDISABLENODEREUSE = '1'
}
foreach ($k in $envVars.Keys) { Set-Item -Path "env:$k" -Value $envVars[$k] }

$dotnet = (Get-Command dotnet).Source
# The folder name deliberately avoids the string "IDE0005" (the supplied script's folder name matched its own regex).
$root = Join-Path ([System.IO.Path]::GetTempPath()) ('CP01-Evidence-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path (Join-Path $root 'emptyfeed') -Force | Out-Null
$nugetConfig = Join-Path $root 'NuGet.Config'
# Same content as the supplied script writes.
@'
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="local-empty" value="emptyfeed" />
  </packageSources>
</configuration>
'@ | Set-Content -LiteralPath $nugetConfig -Encoding UTF8

$kitHashes = @{}
foreach ($f in @('Probe.csproj', 'Source.cs', 'configs\M\.editorconfig', 'configs\M\Directory.Build.props', 'configs\L0\.editorconfig', 'configs\L0\Directory.Build.props')) {
    $kitHashes[$f] = Get-Sha256 (Join-Path $KitDir $f)
}

$properties = @('NETCoreSdkVersion', 'TargetFramework', 'EnforceCodeStyleInBuild', 'GenerateDocumentationFile', 'DocumentationFile',
                'NoWarn', 'TreatWarningsAsErrors', 'AnalysisLevel', 'Nullable', 'ImplicitUsings')
$docsOverride = @('-p:GenerateDocumentationFile=true', '-p:NoWarn=CS1591')

# kind: build | format. origin: SUPPLIED_CASE (same commands as Test-IDE0005.ps1) | SUPPLEMENTARY.
$cases = @(
    [pscustomobject]@{ Name = 'A_M_as_is'; Candidate = 'M'; Kind = 'build'; Extra = @(); Origin = 'SUPPLIED_CASE'; Expected = 'IDE0005 absent' }
    [pscustomobject]@{ Name = 'B_M_docs_override'; Candidate = 'M'; Kind = 'build'; Extra = $docsOverride; Origin = 'SUPPLIED_CASE'; Expected = 'IDE0005 present' }
    [pscustomobject]@{ Name = 'B2_M_docs_only'; Candidate = 'M'; Kind = 'build'; Extra = @('-p:GenerateDocumentationFile=true'); Origin = 'SUPPLEMENTARY'; Expected = 'IDE0005 present (isolates GenerateDocumentationFile from the NoWarn override)' }
    [pscustomobject]@{ Name = 'C_L0_as_is'; Candidate = 'L0'; Kind = 'build'; Extra = @(); Origin = 'SUPPLIED_CASE'; Expected = 'IDE0005 present' }
    [pscustomobject]@{ Name = 'F_M_format_style'; Candidate = 'M'; Kind = 'format_style'; Extra = @(); Origin = 'SUPPLIED_CASE'; Expected = 'not predeclared by the kit (nonzero exit can indicate IDE0005)' }
    [pscustomobject]@{ Name = 'V_M_verify_format'; Candidate = 'M'; Kind = 'format_verify'; Extra = @(); Origin = 'SUPPLEMENTARY'; Expected = "not predeclared (M verify skill command 'dotnet format --verify-no-changes', run with --no-restore as in M's ci-cd skill)" }
)

$results = @()
foreach ($case in $cases) {
    $dir = Join-Path $root $case.Name
    $logDir = Join-Path $OutDir $case.Name
    New-Item -ItemType Directory -Path $dir, $logDir -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $KitDir 'Probe.csproj') -Destination $dir
    Copy-Item -LiteralPath (Join-Path $KitDir 'Source.cs') -Destination $dir
    foreach ($file in @('.editorconfig', 'Directory.Build.props')) {
        Copy-Item -LiteralPath (Join-Path $KitDir "configs\$($case.Candidate)\$file") -Destination $dir
    }
    $project = Join-Path $dir 'Probe.csproj'
    $inputsBefore = [ordered]@{}
    foreach ($f in @('Probe.csproj', 'Source.cs', '.editorconfig', 'Directory.Build.props')) { $inputsBefore[$f] = Get-Sha256 (Join-Path $dir $f) }
    $kitMatch = ($inputsBefore['Probe.csproj'] -eq $kitHashes['Probe.csproj']) -and ($inputsBefore['Source.cs'] -eq $kitHashes['Source.cs']) -and
                ($inputsBefore['.editorconfig'] -eq $kitHashes["configs\$($case.Candidate)\.editorconfig"]) -and
                ($inputsBefore['Directory.Build.props'] -eq $kitHashes["configs\$($case.Candidate)\Directory.Build.props"])

    $steps = @()
    $ver = Invoke-Logged $dotnet @('--version') $dir (Join-Path $logDir '00_dotnet_version')
    $steps += $ver
    # Same restore command as the supplied script.
    $restore = Invoke-Logged $dotnet @('restore', $project, '--configfile', $nugetConfig, '--ignore-failed-sources', '--nologo') $dir (Join-Path $logDir '01_restore')
    $steps += $restore
    # Effective properties, evaluated with the same global properties the case uses.
    $propArgs = @('msbuild', $project, '-nologo') + ($properties | ForEach-Object { "-getProperty:$_" }) + $case.Extra
    $props = Invoke-Logged $dotnet $propArgs $dir (Join-Path $logDir '02_properties')
    $steps += $props
    $effective = $null
    try { $effective = ($props.stdout | ConvertFrom-Json).Properties } catch { $effective = 'UNPARSEABLE' }

    $main = $null
    $docSwitch = $null
    if ($case.Kind -eq 'build') {
        # Same build command as the supplied script.
        $main = Invoke-Logged $dotnet (@('build', $project, '--no-restore', '--nologo', '--verbosity', 'normal') + $case.Extra) $dir (Join-Path $logDir '03_build')
        $cscLine = ($main.stdout -split "`r?`n") | Where-Object { $_ -match 'csc(\.exe|\.dll)?["]?\s' -and $_ -match '/noconfig' } | Select-Object -First 1
        $docSwitch = if ($cscLine) { [bool]($cscLine -match '\s/doc:') } else { 'CSC_COMMAND_LINE_NOT_LOGGED' }
    } elseif ($case.Kind -eq 'format_style') {
        # Same format command as the supplied script.
        $main = Invoke-Logged $dotnet @('format', 'style', $project, '--verify-no-changes', '--diagnostics', 'IDE0005', '--severity', 'warn', '--no-restore', '--verbosity', 'normal') $dir (Join-Path $logDir '03_format_style')
    } else {
        $main = Invoke-Logged $dotnet @('format', '--verify-no-changes', '--no-restore', '--verbosity', 'normal') $dir (Join-Path $logDir '03_format_verify')
    }
    $steps += $main
    $diags = @(Get-Diagnostics ($main.stdout + "`n" + $main.stderr))
    $stream = @()
    if ($main.stdout -match 'IDE0005:') { $stream += 'stdout' }
    if ($main.stderr -match 'IDE0005:') { $stream += 'stderr' }
    $ide = @($diags | Where-Object { $_.id -eq 'IDE0005' })

    $inputsAfter = [ordered]@{}
    foreach ($f in @('Probe.csproj', 'Source.cs', '.editorconfig', 'Directory.Build.props')) { $inputsAfter[$f] = Get-Sha256 (Join-Path $dir $f) }
    $unchanged = (($inputsBefore.Keys | Where-Object { $inputsBefore[$_] -ne $inputsAfter[$_] }).Count -eq 0)

    $results += [pscustomobject]@{
        case = $case.Name
        origin = $case.Origin
        candidate = $case.Candidate
        kind = $case.Kind
        cli_property_overrides = $case.Extra
        expected = $case.Expected
        muxer_sdk_version_in_case_dir = $ver.stdout.Trim()
        effective_properties = $effective
        restore_exit = $restore.exit_code
        main_command = $main.command
        main_exit = $main.exit_code
        csc_doc_switch_present = $docSwitch
        diagnostics = $diags
        diagnostic_count = $diags.Count
        ide0005_diagnostic_count = $ide.Count
        ide0005_emitted = ($ide.Count -gt 0)
        ide0005_stream = $stream
        inputs_sha256_before = $inputsBefore
        inputs_match_kit = $kitMatch
        inputs_unchanged_after = $unchanged
        steps = @($steps | Select-Object command, cwd, exit_code, stdout_log, stderr_log)
    }
    Write-Host ("{0}: exit={1} IDE0005={2} diags={3}" -f $case.Name, $main.exit_code, $ide.Count, (($diags | ForEach-Object { $_.id }) -join ','))
}

$summary = [ordered]@{
    purpose = 'CP-01 replica and evidence harness (same commands as Test-IDE0005.ps1 plus property queries, hashes, strict diagnostics)'
    harness_sha256 = (Get-Sha256 $PSCommandPath)
    run_at = (Get-Date).ToString('o')
    temp_root = $root
    dotnet_path = $dotnet
    powershell_version = $PSVersionTable.PSVersion.ToString()
    os = [System.Environment]::OSVersion.VersionString
    process_environment = $envVars
    kit_input_sha256 = $kitHashes
    nuget_config_sha256 = (Get-Sha256 $nugetConfig)
    results = $results
}
Write-Utf8 (Join-Path $OutDir 'EVIDENCE_SUMMARY.json') ($summary | ConvertTo-Json -Depth 8)
Write-Host "temp_root=$root"
