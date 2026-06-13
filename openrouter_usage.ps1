# Brief OpenRouter usage check. Reads $env:OPENROUTER_API_KEY,
# or falls back to Input_Cache\settings.yaml's OpenRouter.API_KEY.
# Usage: .\openrouter_usage.ps1

$key = $env:OPENROUTER_API_KEY
if (-not $key) {
    $settingsPath = Join-Path $PSScriptRoot 'Input_Cache\settings.yaml'
    if (Test-Path $settingsPath) {
        $inOR = $false
        foreach ($line in Get-Content $settingsPath) {
            if ($line -match '^\s*OpenRouter\s*:') { $inOR = $true; continue }
            if ($inOR) {
                if ($line -match '^\S' -and $line -notmatch '^\s*$') { break }
                if ($line -match '^\s*API_KEY\s*:\s*(\S+)\s*$') {
                    $candidate = $Matches[1]
                    if ($candidate -ne 'null' -and $candidate -ne '~') { $key = $candidate }
                    break
                }
            }
        }
    }
}
if (-not $key) {
    Write-Host "OPENROUTER_API_KEY not set and no OpenRouter key found in Input_Cache\settings.yaml." -ForegroundColor Red
    exit 1
}

try {
    $r = Invoke-RestMethod -Uri https://openrouter.ai/api/v1/auth/key `
                           -Headers @{ Authorization = "Bearer $key" } `
                           -ErrorAction Stop
} catch {
    Write-Host "Request failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

$d = if ($r.data) { $r.data } else { $r }
$limit     = [double]$d.limit
$remaining = [double]$d.limit_remaining
$used      = $limit - $remaining
$pct       = if ($limit -gt 0) { 100 * $used / $limit } else { 0 }

"Used:      `${0:N4} / `${1:N2}" -f $used, $limit
"Remaining: `${0:N4}"            -f $remaining
"Percent:   {0:N4}%"             -f $pct
