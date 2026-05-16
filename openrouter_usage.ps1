# Brief OpenRouter usage check. Reads $env:OPENROUTER_API_KEY.
# Usage: .\openrouter_usage.ps1

$key = $env:OPENROUTER_API_KEY
if (-not $key) {
    Write-Host "OPENROUTER_API_KEY not set." -ForegroundColor Red
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
