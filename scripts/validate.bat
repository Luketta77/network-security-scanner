@echo off
setlocal

cd /d "%~dp0\.."

if not exist ".env" (
    echo [!] Arquivo .env nao encontrado.
    echo [!] Copie .env.example para .env e ajuste as configuracoes.
    pause
    exit /b 1
)

if "%~1"=="" (
    echo.
    set /p TARGET=Digite a rede autorizada [ex: 192.168.1.0/24]:
) else (
    set TARGET=%~1
)

echo.
echo ============================================
echo     CYBERSECURITY EXPOSURE PLATFORM
echo ============================================
echo.
echo [+] Starting Security Validation...
echo [+] Discovering assets...
echo [+] Checking exposed ports...
echo [+] Evaluating risk...
echo [+] Validating security baseline...
echo.

set TARGET_CIDR=%TARGET%

python src\main.py

if errorlevel 1 (
    echo.
    echo [!] Validation failed.
    pause
    exit /b 1
)

endlocal
