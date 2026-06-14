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
call ".venv\Scripts\activate.bat"
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
call :ACTIVATE
REM Ajuste estas variaveis conforme seu ambiente real.
set REDIS_URL=redis://localhost:6379
REM Defina OPENAI_API_KEY no seu ambiente ou no arquivo .env.
REM OPENAI_API_KEY também pode ser configurado em optimus-robot\.env.

REM Define automaticamente o caminho do service account key se existir.
set "KEY_PATH=%~dp0optimus-key.json"
if exist "%KEY_PATH%" (
    set "GOOGLE_APPLICATION_CREDENTIALS=%KEY_PATH%"
    echo GOOGLE_APPLICATION_CREDENTIALS definido para %GOOGLE_APPLICATION_CREDENTIALS%
) else (
    echo AVISO: optimus-key.json nao encontrado em %~dp0
    echo Defina GOOGLE_APPLICATION_CREDENTIALS manualmente se quiser usar o Firestore remoto.
)

echo Iniciando servidor backend...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
if %ERRORLEVEL% neq 0 (
    echo.
    echo Erro ao iniciar o servidor. Veja as mensagens acima.
    pause
)

goto END

:RUN_TESTS
call :ACTIVATE
pytest
pause
goto MENU

:OPEN_FRONTEND
set "FRONTEND=%~dp0..\..\HologramOptimus\index.html"
if exist "%FRONTEND%" (
    start "" "%FRONTEND%"
) else (
    echo Nao foi possivel encontrar o frontend em:
    echo %FRONTEND%
    echo Ajuste o caminho no start.bat se necessario.
)
pause
goto MENU

:END
endlocal
exit /b