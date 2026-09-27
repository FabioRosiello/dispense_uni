# ============================================================
#  Script di compilazione della Dispensa di Tecnologie Web
#  Richiede LuaLaTeX (MiKTeX oppure TeX Live).
#  Uso:  powershell -ExecutionPolicy Bypass -File build.ps1
# ============================================================

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

# Se lualatex non e' nel PATH, prova le posizioni tipiche di MiKTeX
if (-not (Get-Command lualatex -ErrorAction SilentlyContinue)) {
    $candidati = @(
        "$env:LOCALAPPDATA\Programs\MiKTeX\miktex\bin\x64",
        "C:\Program Files\MiKTeX\miktex\bin\x64",
        "C:\texlive\2025\bin\windows",
        "C:\texlive\2024\bin\windows"
    )
    foreach ($c in $candidati) {
        if (Test-Path "$c\lualatex.exe") { $env:PATH = "$c;$env:PATH"; break }
    }
}

if (-not (Get-Command lualatex -ErrorAction SilentlyContinue)) {
    Write-Host "ERRORE: lualatex non trovato. Installa MiKTeX o TeX Live." -ForegroundColor Red
    exit 1
}

# Tre passate: contenuto -> indice -> riferimenti incrociati
foreach ($passata in 1..3) {
    Write-Host "--- Passata $passata di 3 ---" -ForegroundColor Cyan
    lualatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Compilazione fallita alla passata $passata. Vedi main.log" -ForegroundColor Red
        exit 1
    }
}

Write-Host "OK: main.pdf generato." -ForegroundColor Green
