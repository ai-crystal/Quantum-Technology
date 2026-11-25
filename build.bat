@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "NODE_EXE="
for /f "delims=" %%i in ('where node 2^>nul') do if not defined NODE_EXE set "NODE_EXE=%%i"
if not defined NODE_EXE if exist "%ProgramFiles%\nodejs\node.exe" set "NODE_EXE=%ProgramFiles%\nodejs\node.exe"
if not defined NODE_EXE (
    echo [ERROR] Node.js not found. Please install Node.js first.
    pause
    exit /b 1
)

if not exist "books\build\node_modules\katex" (
    echo [1/3] Installing build dependencies ...
    pushd books\build
    call npm install --no-audit --no-fund
    if errorlevel 1 (
        popd
        echo [ERROR] Dependency installation failed.
        pause
        exit /b 1
    )
    popd
) else (
    echo [1/3] Dependencies ready.
)

echo [2/3] Rendering PDF ...
if "%~1"=="" (
    "%NODE_EXE%" "books\build\build.js"
) else (
    "%NODE_EXE%" "books\build\build.js" --book %~1
)
if errorlevel 1 (
    echo [ERROR] Build failed. See messages above.
    pause
    exit /b 1
)

echo [3/3] Updating site files ...
"%NODE_EXE%" "books\build\site.js"

echo.
echo Done. PDFs are in the output folder.
pause
