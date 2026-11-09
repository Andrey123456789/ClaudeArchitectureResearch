# A controlled IDE0005 diagnostic reproduction using unmodified M/L0 assets from frozen Step 2 v3.
# Runs in a fresh temp folder; never touches the research repository or the supplied configurations.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$sourceRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$dotnet = Get-Command dotnet -ErrorAction SilentlyContinue
if (-not $dotnet) { throw 'The .NET SDK is unavailable. Install the .NET 10 SDK, then retry.' }
$sdks = (& dotnet --list-sdks) -join "`n"
Write-Host "Installed SDKs:`n$sdks"
$selectedSdk = (& dotnet --version | Select-Object -First 1).Trim()
Write-Host "Selected SDK: $selectedSdk"
if ($selectedSdk -notmatch '^10\.') {
    throw "The ACTIVE .NET SDK is $selectedSdk, not 10.x. Run from an SDK-10-pinned directory or with an appropriate global.json before interpreting build results."
}
if ($sdks -notmatch '(?m)^10\.') {
    throw 'The study configurations target net10.0. Install the .NET 10 SDK for a faithful test.'
}
$probeRoot = Join-Path ([System.IO.Path]::GetTempPath()) ('IDE0005-Probe-' + [Guid]::NewGuid().ToString('N'))
$feed = Join-Path $probeRoot 'emptyfeed'
New-Item -ItemType Directory -Path $feed -Force | Out-Null
$nugetConfig = Join-Path $probeRoot 'NuGet.Config'
@'
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="local-empty" value="emptyfeed" />
  </packageSources>
</configuration>
'@ | Set-Content -LiteralPath $nugetConfig -Encoding UTF8
$cases = @(
  [pscustomobject]@{ Name = 'A_M_as_is'; Candidate = 'M'; DocsEnabled = $false; ExpectedIDE0005 = $false },
  [pscustomobject]@{ Name = 'B_M_docs_override'; Candidate = 'M'; DocsEnabled = $true; ExpectedIDE0005 = $true },
  [pscustomobject]@{ Name = 'C_L0_as_is'; Candidate = 'L0'; DocsEnabled = $false; ExpectedIDE0005 = $true }
)
$results = @()
foreach ($case in $cases) {
    $directory = Join-Path $probeRoot $case.Name
    New-Item -ItemType Directory -Path $directory -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $sourceRoot 'Probe.csproj') -Destination $directory
    Copy-Item -LiteralPath (Join-Path $sourceRoot 'Source.cs') -Destination $directory
    foreach ($file in @('.editorconfig','Directory.Build.props')) {
        Copy-Item -LiteralPath (Join-Path (Join-Path (Join-Path $sourceRoot 'configs') $case.Candidate) $file) -Destination $directory
    }
    $project = Join-Path $directory 'Probe.csproj'
    Write-Host "`n=== $($case.Name) ==="
    $restoreLog = Join-Path $directory 'restore.log'
    # Restore only from an empty local feed. The installed .NET reference packs must suffice.
    $restoreOutput = & dotnet restore $project --configfile $nugetConfig --ignore-failed-sources --nologo 2>&1
    $restoreCode = $LASTEXITCODE
    @($restoreOutput) | Out-File -LiteralPath $restoreLog -Encoding utf8
    if ($restoreCode -ne 0) {
        Write-Warning "Restore failed for $($case.Name). Inspect $restoreLog"
        $results += [pscustomobject]@{Case=$case.Name;BuildExit='RESTORE_FAILED';IDE0005=$false;Expected=$case.ExpectedIDE0005;Pass=$false}
        continue
    }
    $args = @('build',$project,'--no-restore','--nologo','--verbosity','normal')
    if ($case.DocsEnabled) {
        $args += '-p:GenerateDocumentationFile=true'
        $args += '-p:NoWarn=CS1591'
    }
    $buildOutput = & dotnet @args 2>&1
    $buildCode = $LASTEXITCODE
    $buildLog = Join-Path $directory 'build.log'
    @($buildOutput) | Out-File -LiteralPath $buildLog -Encoding utf8
    $text = (@($buildOutput) | Out-String)
    $ideHit = $text -match '\bIDE0005\b'
    $passed = ($buildCode -eq 0) -and ($ideHit -eq $case.ExpectedIDE0005)
    $results += [pscustomobject]@{Case=$case.Name;BuildExit=$buildCode;IDE0005=$ideHit;Expected=$case.ExpectedIDE0005;Pass=$passed}
    Write-Host "Build exit: $buildCode; IDE0005 present: $ideHit; expected: $($case.ExpectedIDE0005); PASS: $passed"
    if ($ideHit) {
        @($buildOutput) | Where-Object { "$_" -match 'IDE0005' } | ForEach-Object { Write-Host "$_" }
    }
    if ($case.Name -eq 'A_M_as_is') {
        # M's verify skill also instructs a risk-scoped dotnet format check.
        # This is a separate enforcement route, not proof of build-time reporting.
        $formatOutput = & dotnet format style $project --verify-no-changes --diagnostics IDE0005 --severity warn --no-restore --verbosity normal 2>&1
        $formatCode = $LASTEXITCODE
        $formatLog = Join-Path $directory 'format-style.log'
        @($formatOutput) | Out-File -LiteralPath $formatLog -Encoding utf8
        Write-Host "M's alternate formatter route: dotnet format style exit $formatCode (nonzero can indicate IDE0005; review $formatLog)."
        $results[-1] | Add-Member -NotePropertyName 'FormatStyleExit' -NotePropertyValue $formatCode
    }
}
$results | Format-Table -AutoSize
$results | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $probeRoot 'summary.json') -Encoding UTF8
Write-Host "`nAll artifacts and full build logs: $probeRoot"
if (($results | Where-Object { -not $_.Pass }).Count -gt 0) {
    Write-Warning 'At least one expected result was not reproduced. Preserve the logs and inspect SDK-specific behavior before making a candidate change.'
    exit 1
}
Write-Host 'All three expected outcomes reproduced. No candidate files were changed.'
exit 0
