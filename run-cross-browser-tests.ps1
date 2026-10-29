$ErrorActionPreference = "Stop"

$browsers = @(
    @{ Name = "Chrome";  ComposeFile = "compose.chrome.yaml" },
    @{ Name = "Firefox"; ComposeFile = "compose.firefox.yaml" },
    @{ Name = "Edge";    ComposeFile = "compose.edge.yaml" }
)

foreach ($browser in $browsers) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Running $($browser.Name) UI tests" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan

    docker compose -f $browser.ComposeFile up --build --abort-on-container-exit --exit-code-from test-runner

    $testExitCode = $LASTEXITCODE

    if ($testExitCode -ne 0) {
        Write-Host "$($browser.Name) tests FAILED. Stopping the cross-browser run." -ForegroundColor Red
        exit $testExitCode
    }

    Write-Host "$($browser.Name) test run completed successfully." -ForegroundColor Green
}

Write-Host ""
Write-Host "All three browser test runs completed successfully." -ForegroundColor Green
Write-Host "Check Reports\chrome-report.html, Reports\firefox-report.html, and Reports\edge-report.html."
