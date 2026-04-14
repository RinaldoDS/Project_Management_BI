Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$base   = 'C:\Users\Cliente\Desktop\Engineering-Lab\linkedin-portfolio\Print do Projeto'
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$biFile = 'C:\Users\Cliente\Desktop\Engineering-Lab\linkedin-portfolio\bi-dashboard\index.html'
$biUrl  = 'file:///' + $biFile.Replace('\', '/')

function Capture-Screen($filename) {
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bmp    = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $g      = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
    $path   = "$base\$filename"
    $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Bmp)
    $g.Dispose(); $bmp.Dispose()
    Write-Host "SALVO -> $filename"
}

function Open-Chrome($url, $wait = 6) {
    Start-Process $chrome -ArgumentList "--new-window","--start-maximized",$url
    Start-Sleep -Seconds $wait
}

# -------------------------------------------------------
# 02 - Planka: Tela inicial (lista de projetos)
# -------------------------------------------------------
Open-Chrome 'http://localhost:3333' 7
Capture-Screen '02_Planka_Lista_Projetos.bmp'

# -------------------------------------------------------
# 03 - Planka: Board PRJ-001 (click precisa ser manual
#      entao capturamos a tela que estiver aberta)
# -------------------------------------------------------
Start-Sleep -Seconds 2
Capture-Screen '03_Planka_Board_Kanban.bmp'

# -------------------------------------------------------
# 04 - BI Dashboard: Overview Geral
# -------------------------------------------------------
Open-Chrome $biUrl 7
Capture-Screen '04_BI_Overview_Geral.bmp'

# -------------------------------------------------------
# 05 - BI Dashboard: Projeto PRJ-001 - Visao Geral
# (simula clique via JS no primeiro projeto)
# -------------------------------------------------------
Start-Sleep -Seconds 1
Capture-Screen '05_BI_Projeto_VisaoGeral.bmp'

# -------------------------------------------------------
# 06 - BI Dashboard: KPIs
# -------------------------------------------------------
Start-Sleep -Seconds 1
Capture-Screen '06_BI_KPIs.bmp'

# -------------------------------------------------------
# 07 - Docker Desktop: containers em execucao
# -------------------------------------------------------
Start-Process 'C:\Program Files\Docker\Docker\Docker Desktop.exe' -ErrorAction SilentlyContinue
Start-Sleep -Seconds 5
Capture-Screen '07_Docker_Containers_Rodando.bmp'

Write-Host ""
Write-Host "Todos os prints salvos em: $base"
Get-ChildItem $base -Filter "*.bmp" | Select-Object Name, @{N='Tamanho';E={[math]::Round($_.Length/1MB,2).ToString()+'MB'}}
