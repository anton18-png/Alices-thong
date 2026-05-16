@echo off
chcp 65001 >nul
title Стринги Алисы — Компиляция

echo ===================================================
echo   Компиляция лаунчера Стрингов Алисы
echo ===================================================
echo.

:: Проверка наличия Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ОШИБКА] Python не найден! Установите Python 3.10+
    pause
    exit /b 1
)

:: Проверка наличия PyInstaller
where pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Установка PyInstaller...
    pip install pyinstaller
)

:: Установка зависимостей
echo [*] Установка зависимостей...
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

:: Очистка старых сборок
if exist "dist\Launcher.exe" del /f /q "dist\Launcher.exe"
if exist "build" rd /s /q "build"
if exist "*.spec" del /f /q "*.spec"

:: Поиск иконки
set "ICON_FILE="
if exist "icon.ico" set "ICON_FILE=icon.ico"
@REM if exist "launcher.ico" set "ICON_FILE=launcher.ico"
@REM if exist "app.ico" set "ICON_FILE=app.ico"

set "ICON_ARG="
if defined ICON_FILE set "ICON_ARG=--icon %ICON_FILE%"

:: Компиляция
echo [*] Компиляция...
echo.
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "Launcher" ^
    %ICON_ARG% ^
    --add-data "launcher;launcher" ^
    --hidden-import "PIL._tkinter_finder" ^
    --collect-all customtkinter ^
    --clean ^
    --noconfirm ^
    main.pyw

:: Копирование portapp.json рядом с exe
if exist "portapp.json" (
    copy /y "portapp.json" "dist\portapp.json" >nul
    echo [+] portapp.json скопирован в dist\
)

:: Копирование AlicesThong.exe рядом с exe
if exist "AlicesThong.exe" (
    copy /y "AlicesThong.exe" "dist\AlicesThong.exe" >nul
    echo [+] AlicesThong.exe скопирован в dist\
)

if %errorlevel% equ 0 (
    echo.
    echo ===================================================
    echo   Компиляция завершена!
    echo   Файл: dist\Launcher.exe
    echo   Размер:
    for %%f in ("dist\Launcher.exe") do echo   %%~zf байт
    echo ===================================================
) else (
    echo.
    echo [ОШИБКА] Компиляция не удалась!
)

pause
