// Kind: ENF | Scope: backend-tests | Capability: backend-testing/nunit | Loading: scaffold asset copied to the test location the architecture workflow facet assigns; runs inside dotnet test
// Runs the neutral architecture checker (.claude/scripts/check-architecture.mjs) as an NUnit test so reference
// violations fail the backend test suite locally and in CI. Requires Node.js on PATH; fails clearly when it is missing.
// NUnit.Framework comes from the global using that `dotnet new nunit` adds to the test project.
using System.ComponentModel;
using System.Diagnostics;

namespace ProjectName.IntegrationTests.Architecture;

[TestFixture]
[Category("Architecture")]
public sealed class ArchitectureConformanceTests
{
    private const string CheckerRelativePath = ".claude/scripts/check-architecture.mjs";

    [Test]
    public void ProjectReferencesAndPackages_FollowArchitectureRules()
    {
        var root = FindRepositoryRoot();
        var startInfo = new ProcessStartInfo("node")
        {
            WorkingDirectory = root,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
        };
        startInfo.ArgumentList.Add(Path.Combine(root, CheckerRelativePath));

        Process? process;
        try
        {
            process = Process.Start(startInfo);
        }
        catch (Win32Exception exception)
        {
            Assert.Fail($"Node.js is required to run the architecture checks but could not be started: {exception.Message}");
            return;
        }

        Assert.That(process, Is.Not.Null, "The architecture checker process could not be started.");

        using (process)
        {
            var output = process!.StandardOutput.ReadToEndAsync();
            var error = process.StandardError.ReadToEndAsync();

            if (!process.WaitForExit(TimeSpan.FromSeconds(60)))
            {
                process.Kill(entireProcessTree: true);
                Assert.Fail("The architecture checker did not finish within 60 seconds.");
            }

            Assert.That(
                process.ExitCode,
                Is.EqualTo(0),
                $"Architecture check failed:{Environment.NewLine}{output.Result}{error.Result}");
        }
    }

    private static string FindRepositoryRoot()
    {
        for (var directory = new DirectoryInfo(TestContext.CurrentContext.TestDirectory);
             directory is not null;
             directory = directory.Parent)
        {
            if (File.Exists(Path.Combine(directory.FullName, CheckerRelativePath)))
            {
                return directory.FullName;
            }
        }

        Assert.Fail($"No directory above the test output contains {CheckerRelativePath}.");
        return string.Empty;
    }
}
