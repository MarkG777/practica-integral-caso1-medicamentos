# Orquestador: abre psql (cliente oficial PostgreSQL), ejecuta consultas y captura la pantalla real.
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$ErrorActionPreference = 'Stop'
$PSQL = 'C:\Program Files\PostgreSQL\17\bin\psql.exe'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$outDir = Join-Path $here '..\..\docs\evidencias'
$outDir = [System.IO.Path]::GetFullPath($outDir)
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$env:PGPASSWORD = 'postgres'

function Capture-Screen($path) {
    $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($b.Location, [System.Drawing.Point]::Empty, $b.Size)
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
}

$jobs = @(
    @{ sql = 'cap1.sql'; png = 'psql_evidencia_1_tablas_conteos.png' },
    @{ sql = 'cap2.sql'; png = 'psql_evidencia_2_estructura.png' },
    @{ sql = 'cap3.sql'; png = 'psql_evidencia_3_join.png' }
)

foreach ($j in $jobs) {
    $sqlPath = Join-Path $here $j.sql
    $title = "PostgreSQL 17 - psql - uteq_data_mining - $($j.sql)"
    $cmd = "`$host.UI.RawUI.WindowTitle='$title'; `$host.UI.RawUI.BackgroundColor='Black'; `$host.UI.RawUI.ForegroundColor='Gray'; Clear-Host; & '$PSQL' -U postgres -d uteq_data_mining -f '$sqlPath'"
    $p = Start-Process powershell -PassThru -WindowStyle Maximized -ArgumentList '-NoLogo','-NoExit','-Command', $cmd
    Start-Sleep -Seconds 5
    $dest = Join-Path $outDir $j.png
    Capture-Screen $dest
    Write-Host "[OK] Captura guardada: $dest"
    Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
}

Write-Host "FIN: capturas reales de psql generadas en $outDir"
