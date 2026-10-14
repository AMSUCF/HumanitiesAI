# Export every slide of each deck to PNG via PowerPoint, for visual review.
# Usage (from undergrad/slides/):  powershell -File export_pngs.ps1 [-OutDir <dir>]
param([string]$OutDir = "$env:TEMP\eng3861-pptx-review")
$pp = New-Object -ComObject PowerPoint.Application
try {
  Get-ChildItem -Path $PSScriptRoot -Filter *.pptx | ForEach-Object {
    $deck = $pp.Presentations.Open($_.FullName, $true, $false, $false)
    $dest = Join-Path $OutDir $_.BaseName
    $deck.SaveAs($dest, 18)   # ppSaveAsPNG: one PNG per slide in $dest
    $deck.Close()
    Write-Output "$($_.Name) -> $dest"
  }
} finally { $pp.Quit() }
