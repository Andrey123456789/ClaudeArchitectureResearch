<#
.SYNOPSIS
    Publishes sibling workspace folders into external/ of the Git repository.
.EXAMPLE
    .\Publish-External.ps1 -Folders ClaudeArchitectureResearchRuns,ClaudeArchitectureResearchUtils
.EXAMPLE
    .\Publish-External.ps1 -Folders ClaudeArchitectureResearchRuns -DryRun
.NOTES
    Run from Windows PowerShell 5.1 or PowerShell 7 with Git and robocopy available.
    Source folders are never moved or modified. Selected remote folders are mirrored:
    deleted source files are deleted from the corresponding remote folders.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string[]]$Folders,

    [string]$WorkspaceRoot = 'C:\Projects\AI Learning',
    [string]$RepositoryName = 'ClaudeArchitectureResearch',
    [string]$Branch = 'main',
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git was not found in PATH.'
}
if (-not (Get-Command robocopy -ErrorAction SilentlyContinue)) {
    throw 'Robocopy was not found in PATH.'
}

$WorkspaceRoot = (Resolve-Path -LiteralPath $WorkspaceRoot -ErrorAction Stop).Path
$repoPath = Join-Path $WorkspaceRoot $RepositoryName
if (-not (Test-Path -LiteralPath $repoPath -PathType Container)) {
    throw "Repository directory not found: $repoPath"
}

$actualRepoRoot = & git -C $repoPath rev-parse --show-toplevel
if ($LASTEXITCODE -ne 0 -or -not $actualRepoRoot) {
    throw "Not a Git working tree: $repoPath"
}
if ([IO.Path]::GetFullPath($actualRepoRoot).TrimEnd('\') -ne [IO.Path]::GetFullPath($repoPath).TrimEnd('\')) {
    throw "The expected repository root is not the Git root: $repoPath"
}

$remoteUrl = & git -C $repoPath remote get-url origin
if ($LASTEXITCODE -ne 0 -or -not $remoteUrl) {
    throw "Git remote 'origin' is missing in $repoPath"
}

$gitUserName = & git -C $repoPath config user.name
$gitUserEmail = & git -C $repoPath config user.email
if (-not $gitUserName -or -not $gitUserEmail) {
    throw 'Git author identity is missing. Set user.name and user.email in the local repository.'
}

# Only immediate child directory names are allowed, not paths or traversal.
$selected = @($Folders | Select-Object -Unique)
foreach ($folder in $selected) {
    if ([string]::IsNullOrWhiteSpace($folder) -or
        $folder -in @('.', '..') -or
        $folder -match '[\\/:*?"<>|]' -or
        $folder.EndsWith('.') -or
        $folder.EndsWith(' ') -or
        $folder -ieq $RepositoryName) {
        throw "Invalid sibling folder name: $folder"
    }

    $source = Join-Path $WorkspaceRoot $folder
    if (-not (Test-Path -LiteralPath $source -PathType Container)) {
        throw "Source folder not found: $source"
    }
    $sourceInfo = Get-Item -LiteralPath $source -Force
    if (($sourceInfo.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw "Linked source folders are not supported: $source"
    }
}

# Avoid publishing a separate remote commit when local main has unpushed commits.
# This check does not touch local working files or the working tree index.
& git -C $repoPath fetch --quiet origin $Branch
if ($LASTEXITCODE -ne 0) { throw 'Git fetch failed.' }
& git -C $repoPath merge-base --is-ancestor "refs/heads/$Branch" "refs/remotes/origin/$Branch"
if ($LASTEXITCODE -eq 1) {
    throw "Local $Branch contains unpushed or divergent commits. Synchronize it before publishing external folders."
}
if ($LASTEXITCODE -ne 0) { throw 'Unable to compare local and remote branches.' }

$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ('publish-external-' + [Guid]::NewGuid().ToString('N'))

try {
    Write-Host "Cloning $remoteUrl ($Branch) into a temporary directory..."
    & git clone --quiet --depth 1 --single-branch --branch $Branch $remoteUrl $tempRoot
    if ($LASTEXITCODE -ne 0) { throw 'Git clone failed.' }

    $externalRoot = Join-Path $tempRoot 'external'
    New-Item -ItemType Directory -Path $externalRoot -Force | Out-Null

    foreach ($folder in $selected) {
        $source = Join-Path $WorkspaceRoot $folder
        $target = Join-Path $externalRoot $folder
        Write-Host "Mirroring $source -> external/$folder"

        # The temporary clone is disposable; replace only the selected folder.
        if (Test-Path -LiteralPath $target) {
            $targetInfo = Get-Item -LiteralPath $target -Force
            if (($targetInfo.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Refusing to replace a linked destination: $target"
            }
            Remove-Item -LiteralPath $target -Force -Recurse
        }
        New-Item -ItemType Directory -Path $target -Force | Out-Null

        # Keep build outputs, Git internals, local settings, and common secrets out.
        $robocopyArgs = @(
            $source, $target, '/E', '/XJ', '/R:1', '/W:1', '/NFL', '/NDL', '/NP',
            '/XD', '.git', '.vs', '.idea', 'bin', 'obj', 'node_modules', '__pycache__',
            '/XF', '.git', '.env', '.env.*', 'secrets.json', 'credentials.json',
                   '*.pfx', '*.p12', '*.pem', '*.key', 'id_rsa*', 'id_ed25519*', '*.pyc'
        )
        & robocopy @robocopyArgs | Out-Null
        $copyExitCode = $LASTEXITCODE
        if ($copyExitCode -ge 8) {
            throw "Robocopy failed for '$folder' (exit code $copyExitCode)."
        }

        # Git does not track empty directories.
        $firstFile = Get-ChildItem -LiteralPath $target -File -Recurse -Force |
            Select-Object -First 1
        if (-not $firstFile) {
            Set-Content -LiteralPath (Join-Path $target '.gitkeep') -Value '' -Encoding Ascii
        }
    }

    & git -C $tempRoot add -A -- external
    if ($LASTEXITCODE -ne 0) { throw 'Git add failed.' }

    & git -C $tempRoot diff --cached --quiet
    $diffCode = $LASTEXITCODE
    if ($diffCode -eq 0) {
        Write-Host 'No changes to publish.'
        return
    }
    if ($diffCode -ne 1) { throw 'Git diff failed.' }

    & git -C $tempRoot diff --cached --stat
    if ($LASTEXITCODE -ne 0) { throw 'Git diff --stat failed.' }

    if ($DryRun) {
        Write-Host 'Dry run: no commit or push was made.'
        return
    }

    $commitMessage = 'Sync external: ' + ($selected -join ', ')
    & git -C $tempRoot -c "user.name=$gitUserName" -c "user.email=$gitUserEmail" commit -m $commitMessage
    if ($LASTEXITCODE -ne 0) { throw 'Git commit failed.' }

    # No --force: an intervening remote update will reject the push safely.
    & git -C $tempRoot push origin "HEAD:refs/heads/$Branch"
    if ($LASTEXITCODE -ne 0) {
        throw 'Git push failed. Re-run to clone the latest branch and retry.'
    }

    Write-Host 'Published successfully.'
    Write-Host "Local repository may now be behind origin/$Branch; pull before your next push."
}
finally {
    if (Test-Path -LiteralPath $tempRoot) {
        # This is only the unique temporary clone created for this execution.
        Remove-Item -LiteralPath $tempRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
