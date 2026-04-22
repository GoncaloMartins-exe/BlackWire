@echo off
chcp 65001 >nul
title Blackwire - Setup

echo.
echo  ██████╗ ██╗      █████╗  ██████╗██╗  ██╗██╗    ██╗██╗██████╗ ███████╗
echo  ██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝██║    ██║██║██╔══██╗██╔════╝
echo  ██████╔╝██║     ███████║██║     █████╔╝ ██║ █╗ ██║██║██████╔╝█████╗
echo  ██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██║███╗██║██║██╔══██╗██╔══╝
echo  ██████╔╝███████╗██║  ██║╚██████╗██║  ██╗╚███╔███╔╝██║██║  ██║███████╗
echo  ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚══════╝
echo.
echo  Setup do ambiente de desenvolvimento
echo  -----------------------------------------------
echo.

:: Navegar para a raiz do projeto
cd /d "%~dp0.."
echo  [INFO] A trabalhar em: %CD%
echo.

:: -----------------------------------------------
:: 1. Verificar Python
:: -----------------------------------------------
echo [1/3] A verificar Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  [ERRO] Python nao encontrado!
    echo  Instala em: https://www.python.org/downloads/
    echo  Nao te esquecas de marcar "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYVER=%%i
echo  [OK] %PYVER% encontrado.
echo.

:: -----------------------------------------------
:: 2. Criar/reutilizar ambiente virtual
:: -----------------------------------------------
echo [2/3] A verificar ambiente virtual (venv)...
if exist venv (
    echo  [SKIP] venv ja existe, a reutilizar.
) else (
    echo  A criar venv...
    python -m venv venv
    if errorlevel 1 (
        echo  [ERRO] Falha ao criar venv.
        pause
        exit /b 1
    )
    echo  [OK] venv criado.
)

call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
echo  [OK] pip atualizado.
echo.

:: -----------------------------------------------
:: 3. Instalar dependencias
:: -----------------------------------------------
echo [3/3] A instalar dependencias...
echo.

echo   - PySide6 (interface grafica Qt6)...
pip install PySide6 --quiet
if errorlevel 1 ( echo  [ERRO] Falha ao instalar PySide6. && pause && exit /b 1 )

echo   - paramiko (SSH / SFTP)...
pip install paramiko --quiet
if errorlevel 1 ( echo  [ERRO] Falha ao instalar paramiko. && pause && exit /b 1 )

echo   - pyqtgraph (graficos de monitorizacao)...
pip install pyqtgraph --quiet
if errorlevel 1 ( echo  [ERRO] Falha ao instalar pyqtgraph. && pause && exit /b 1 )

echo   - cryptography (dependencia do paramiko)...
pip install cryptography --quiet
if errorlevel 1 ( echo  [ERRO] Falha ao instalar cryptography. && pause && exit /b 1 )

echo   - pyinstaller (empacotar em .exe mais tarde)...
pip install pyinstaller --quiet
if errorlevel 1 ( echo  [ERRO] Falha ao instalar pyinstaller. && pause && exit /b 1 )

:: Guardar versoes no requirements.txt
pip freeze > requirements.txt
echo.
echo  [OK] Todas as dependencias instaladas.
echo  [OK] requirements.txt atualizado com versoes exatas.
echo.

:: -----------------------------------------------
:: Concluido
:: -----------------------------------------------
echo  -----------------------------------------------
echo  Setup concluido com sucesso!
echo.
echo  Para comecar a desenvolver:
echo    1. Ativa o venv:   venv\Scripts\activate
echo    2. Corre a app:    python main.py
echo  -----------------------------------------------
echo.
pause