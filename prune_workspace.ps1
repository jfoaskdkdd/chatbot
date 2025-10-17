<#
PowerShell helper to list files in the repository that are likely unrelated to the bot runtime
and optionally move them to a separate folder for manual review. This script is conservative
and will NOT move or delete anything unless -Run is provided.
#>
param(
  [switch]$Run
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ignorePatterns = @(
  '*.csv',
  '*.py',
  '*.ipynb',
  'task1.csv',
  'task1.*',
  'lista.txt',
  'contatos.csv',
  'filtrados.csv',
  'processa_contatos.py',
  'export.py',
  'exporta_google*.py',
  'checker.py'
)

$found = @()
foreach ($p in $ignorePatterns) {
  $found += Get-ChildItem -Path $root -Filter $p -Recurse -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer }
}

if ($found.Count -eq 0) {
  Write-Host "No candidate files found for pruning."
  return
}

Write-Host "Found $($found.Count) candidate files for review:" -ForegroundColor Yellow
$found | ForEach-Object { Write-Host " - $($_.FullName)" }

if ($Run) {
  $target = Join-Path $root "pruned_files_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
  New-Item -Path $target -ItemType Directory -Force | Out-Null
  foreach ($f in $found) {
    $dest = Join-Path $target $f.Name
    Move-Item -Path $f.FullName -Destination $dest -Force
    Write-Host "Moved $($f.FullName) -> $dest"
  }
  Write-Host "Prune completed. Review files in: $target"
} else {
  Write-Host "Run the script with -Run to actually move the files to a 'pruned_files' folder for manual review."
}
