@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ============================================
echo   量子学技术  -  一键生成 PDF
echo ============================================
echo.

set "NODE_EXE="
for /f "delims=" %%i in ('where node 2^>nul') do (
    if not defined NODE_EXE set "NODE_EXE=%%i"
)
if not defined NODE_EXE (
    if exist "%ProgramFiles%\nodejs\node.exe" set "NODE_EXE=%ProgramFiles%\nodejs\node.exe"
)
if not defined NODE_EXE (
    echo [错误] 没有找到 Node.js，请先安装 Node.js 后重试。
    pause
    exit /b 1
)

set "NPM_EXE=%~dp0book\build\npm.cmd"
if not exist "%NPM_EXE%" (
    for %%i in ("%NODE_EXE%") do set "NODE_DIR=%%~dpi"
    set "NPM_EXE=!NODE_DIR!npm.cmd"
)

if not exist "book\build\node_modules\katex" (
    echo [1/3] 首次运行，正在安装构建依赖……
    pushd book\build
    call "!NPM_EXE!" install --no-audit --no-fund
    if errorlevel 1 (
        echo [错误] 依赖安装失败，请检查网络后重试。
        popd
        pause
        exit /b 1
    )
    popd
) else (
    echo [1/3] 构建依赖已就绪。
)

echo [2/3] 正在渲染 HTML 并排版 PDF……
"%NODE_EXE%" "book\build\build.js"
if errorlevel 1 (
    echo.
    echo [错误] 构建失败，请查看上面的提示。
    pause
    exit /b 1
)

echo [3/3] 完成。输出文件在 output 目录。
echo.
pause
