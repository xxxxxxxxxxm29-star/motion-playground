$Root = $PSScriptRoot
Set-Location $Root

if (-not (Test-Path "$Root\.venv")) {
    Write-Host "Создаю виртуальное окружение..." -ForegroundColor Yellow
    python -m venv .venv
    & "$Root\.venv\Scripts\python.exe" -m pip install --upgrade pip
    & "$Root\.venv\Scripts\pip.exe" install -r requirements.txt
}

Write-Host "Запускаю auth-сервис на http://127.0.0.1:5000/login" -ForegroundColor Green
Start-Process -FilePath "$Root\.venv\Scripts\python.exe" `
              -ArgumentList "auth_app.py" -WorkingDirectory $Root

if (Test-Path "$Root\room_server.py") {
    Write-Host "Запускаю room-сервис на http://127.0.0.1:8080" -ForegroundColor Green
    Start-Process -FilePath "$Root\.venv\Scripts\python.exe" `
                  -ArgumentList "room_server.py" -WorkingDirectory $Root
} else {
    Write-Host "room_server.py не найден — скопируйте его в $Root" -ForegroundColor Yellow
}