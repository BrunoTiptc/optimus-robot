@echo off
REM Start script para backend Optimus Robot (Windows)
REM Este arquivo roda no diretório brain-core.
setlocal enabledelayedexpansion

REM Navega para o diretório do script
cd /d "%~dp0"

REM Cria ambiente virtual se ainda não existir
if not exist ".venv\Scripts\activate.bat" (
    python -m venv .venv
)

:MENU
cls
echo ================================================
echo Optimus Robot Launcher - brain-core
echo ================================================
echo.
echo 1) Iniciar servidor backend
echo 2) Rodar testes (pytest)
echo 3) Abrir frontend (index.html)
echo 4) Instalar / atualizar dependencias
echo 5) Sair
echo.
set /p choice=Escolha uma opcao [1-5]: 

if "%choice%"=="1" goto START_SERVER
if "%choice%"=="2" goto RUN_TESTS
if "%choice%"=="3" goto OPEN_FRONTEND
if "%choice%"=="4" goto INSTALL_DEPS
if "%choice%"=="5" goto END

echo Opcao invalida. Tente novamente.
pause
goto MENU

:ACTIVATE
call .venv\Scripts\activate.bat
goto :eof

:INSTALL_DEPS
call :ACTIVATE
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Dependencias instaladas/atualizadas.
pause
goto MENU

:START_SERVER
set REDIS_URL=redis://localhost:6379

REM Define automaticamente o caminho do service account key se existir.
set "KEY_PATH=%~dp0optimus-key.json"
if exist "%KEY_PATH%" (
    set "GOOGLE_APPLICATION_CREDENTIALS=%KEY_PATH%"
    echo GOOGLE_APPLICATION_CREDENTIALS definido para %KEY_PATH%
) else (
    echo AVISO: optimus-key.json nao encontrado em %~dp0
    echo Defina GOOGLE_APPLICATION_CREDENTIALS manualmente se quiser usar o Firestore remoto.
)

echo Iniciando servidor backend em nova janela...
start "Optimus Backend" cmd /k "cd /d "%~dp0" && call ".venv\Scripts\activate.bat" && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

goto MENU

:RUN_TESTS
call :ACTIVATE
echo.
echo [SISTEMA] Injetando PYTHONPATH para o ambiente Windows...
echo.
REM Configura o caminho absoluto da pasta raiz + brain-core para o Python achar a pasta 'app'
set "PYTHONPATH=%~dp0;%~dp0brain-core"
pytest "%~dp0..\tests"
pause
goto MENU

:OPEN_FRONTEND
REM Força o prompt de comando a usar a codificação UTF-8 (Page Code 65001) para aceitar o emoji
chcp 65001 >nul

REM Define os caminhos sem aspas internas para não quebrar o interpretador do Windows
set "FRONTEND_DIR=%~dp0..\..\HologramOptimus"
set "FRONTEND_HTML=%~dp0..\..\HologramOptimus\index.html"

REM Se não achar na pasta de trás, tenta na raiz do projeto atual
if not exist "%FRONTEND_HTML%" (
    set "FRONTEND_DIR=%~dp0.."
    set "FRONTEND_HTML=%~dp0..\index.html"
)

if exist "%FRONTEND_HTML%" (
    echo.
    echo [SISTEMA] Frontend encontrado! Iniciando servidor HTTP...
    echo Abrindo em: http://127.0.0.1:5500/index.html
    echo.
    REM Rodamos o comando limpando as aspas problemáticas do CD
    start "Optimus Frontend" cmd /k "chcp 65001 >nul && cd /d %FRONTEND_DIR% && python -m http.server 5500"
    timeout /t 2 >nul
    start "" "http://127.0.0.1:5500/index.html"
) else (
    echo =======================================================
    echo AVISO: Nao foi possivel encontrar o arquivo index.html
    echo Verifique o caminho da pasta: %FRONTEND_HTML%
    echo =======================================================
)
REM Restaura o padrão do terminal após rodar
chcp 850 >nul
pause
goto MENU

:END
endlocal
exit /b