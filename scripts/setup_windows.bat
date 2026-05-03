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

set PYTHON_EXE=

for %%p in (python python3 py) do (
    for /f "delims=" %%i in ('where %%p 2^>nul') do (
        echo %%i | findstr /i "msys mingw" >nul
        if errorlevel 1 (
            set PYTHON_EXE=%%i
            goto :python_found
        )
    )
)

:python_found
if "%PYTHON_EXE%"=="" (
    echo  [ERRO] Python valido nao encontrado!
    echo  Evita versoes MSYS2. Instala Python oficial.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('"%PYTHON_EXE%" --version') do set PYVER=%%i
echo  [OK] %PYVER%
echo  [OK] Usando: %PYTHON_EXE%
echo.

:: -----------------------------------------------
:: 2. Criar/reutilizar ambiente virtual
:: -----------------------------------------------
echo [2/3] A criar ambiente virtual...

if exist venv (
    echo  A remover venv antigo...
    rmdir /s /q venv
)

"%PYTHON_EXE%" -m venv venv
if errorlevel 1 (
    echo  [ERRO] Falha ao criar venv.
    pause
    exit /b 1
)

echo  [OK] venv criado.

call "venv\Scripts\activate.bat"
python -m pip install --upgrade pip --quiet
echo  [OK] pip atualizado.
echo.

:: -----------------------------------------------
:: 3. Instalar dependencias
:: -----------------------------------------------
echo [3/3] A instalar dependencias...
echo.

if not exist requirements.txt (
    echo  [ERRO] requirements.txt nao encontrado na raiz do projeto!
    echo  Certifica-te que está ao lado do main.py
    pause
    exit /b 1
)

echo   - A instalar a partir de requirements.txt...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo  [ERRO] Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo  [OK] Dependencias instaladas com sucesso.
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
cmd /k
pause