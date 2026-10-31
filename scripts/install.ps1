param(
    [string]$Thema = "BMW bei Nacht",
    [string]$Stil = "aggressive",
    [int]$Laenge = 15
)

$ErrorActionPreference = "Stop"

$jarvisHome = if ($env:JARVIS_HOME) { $env:JARVIS_HOME } else { (Get-Location).Path }

function Ensure-Directory([string]$Path) {
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Force -Path $Path | Out-Null
    }
}

function Ensure-PythonDeps {
    python -m pip install --upgrade pip
    python -m pip install -r "$jarvisHome/requirements.txt"
}

function Ensure-Ffmpeg {
    if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
        winget install --id Gyan.Dev.FFmpeg -e
    }
}

function Ensure-Playwright {
    python -m playwright install
}

function Install-All {
    Ensure-Directory "$jarvisHome/kern"
    Ensure-Directory "$jarvisHome/tools"
    Ensure-Directory "$jarvisHome/web"
    Ensure-Directory "$jarvisHome/scripts"
    Ensure-Directory "$jarvisHome/docs"
    Ensure-Directory "$jarvisHome/output"
    Ensure-Directory "$jarvisHome/input/eigene_clips"
    Ensure-Directory "$jarvisHome/Gedaechtnis"
    Ensure-Directory "$jarvisHome/Logs"

    Ensure-PythonDeps
    Ensure-Ffmpeg
    Ensure-Playwright

    $env:JARVIS_HOME = $jarvisHome
    python "$jarvisHome/check.py"
}

function jcheck {
    python "$jarvisHome/check.py"
}

function jhelp {
    Write-Host "Jarvis Hilfen"
    Write-Host "  jcheck        - Schnellprüfung"
    Write-Host "  jhelp         - Hilfe"
    Write-Host "  jweb          - Web-App starten"
    Write-Host "  jedit <thema> - Edit-Auftrag starten"
    Write-Host "  jupdate       - git pull + Pakete installieren"
}

function jweb {
    python -m uvicorn web.app:app --host 127.0.0.1 --port 8000
}

function jedit {
    param([string]$Thema = $Thema)
    python "$jarvisHome/tools/pipeline/edit_auftrag.py" --thema "$Thema" --stil "$Stil" --laenge $Laenge
}

function jupdate {
    git pull --ff-only
    python -m pip install -r "$jarvisHome/requirements.txt"
}

function jkey {
    Write-Host "Vorhandene Schlüssel-Namen aus .env.example:"
    Get-Content "$jarvisHome/.env.example" | Select-String "_API_KEY|_TOKEN|_ID"
}

function jtg {
    Write-Host "Telegram-Bot starten."
    python "$jarvisHome/tools/telegram/bot.py"
}

function jsuche {
    python "$jarvisHome/tools/recherche/material_suche.py" --thema "$Thema"
}

function jschnitt {
    python "$jarvisHome/tools/schnitt/autoedit.py" --thema "$Thema" --stil "$Stil" --laenge $Laenge
}

function jcar {
    python "$jarvisHome/tools/schnitt/car_edit.py" --thema "$Thema" --stil "$Stil" --laenge $Laenge
}

function jpc {
    python "$jarvisHome/tools/pc/steuerung.py" --mode "status"
}

function jlernen {
    python "$jarvisHome/tools/lernen/lernmodul.py" --mode "hilfe"
}

function jgeld {
    python "$jarvisHome/tools/geld/system.py" --mode "status"
}

function jziel {
    python "$jarvisHome/tools/geld/system.py" --mode "ziel"
}

function jreparatur {
    Write-Host "Reparaturmodus: prüfe Dateistruktur und installierte Pakete."
    python -m pip install -r "$jarvisHome/requirements.txt"
    python "$jarvisHome/check.py"
}

Install-All
