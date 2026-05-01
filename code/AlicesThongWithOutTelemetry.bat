@echo off
chcp 65001 >nul
title Alices Thong - Yandex Browser Portable
setlocal enablededelayedexpansion

:: Получаем SID
for /f "usebackq tokens=2" %%a in (`whoami /user /nh 2^>nul`) do set "SID=%%a"

:: Определяем пути
set "BROWSER_EXE=AlicesThong.exe"
set "DATA_DIR=data"
set "DEFAULT_DIR=%DATA_DIR%\Default"
set "PREFS_FILE=%DEFAULT_DIR%\Preferences"
set "SESSIONS_DIR=%DEFAULT_DIR%\Sessions"
set "SESSION_STORAGE=%DEFAULT_DIR%\Session Storage"

echo ===================================================
echo Alices Thong - Yandex Browser Portable
echo ===================================================
echo.

:: --- СОЗДАНИЕ ПАПОК, ЕСЛИ НЕТ ---
if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"
if not exist "%DEFAULT_DIR%" mkdir "%DEFAULT_DIR%"

:: --- БЛОКИРОВКА СЛУЖБ ---
echo [0] Блокировка служб и обновлений...

sc stop YandexBrowserService >nul 2>&1
sc config YandexBrowserService start= disabled >nul 2>&1
sc delete YandexBrowserService >nul 2>&1

sc stop YandexUpdaterService >nul 2>&1
sc config YandexUpdaterService start= disabled >nul 2>&1
sc delete YandexUpdaterService >nul 2>&1

sc stop YaTransmgr >nul 2>&1
sc delete YaTransmgr >nul 2>&1

sc stop YandexProtectService >nul 2>&1
sc delete YandexProtectService >nul 2>&1

schtasks /delete /tn "YandexUpdaterTask" /f >nul 2>&1
schtasks /delete /tn "YandexProtectTask" /f >nul 2>&1
schtasks /delete /tn "YandexBrowserUpdaterTask" /f >nul 2>&1
schtasks /delete /tn "YandexUpdateTaskMachineCore" /f >nul 2>&1
schtasks /delete /tn "YandexUpdateTaskMachineUA" /f >nul 2>&1

:: --- ПРИМЕНЕНИЕ НАСТРОЕК ЧЕРЕЗ РЕЕСТР (политики) ---
echo [1] Применение политик через реестр...

reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser" /v "BackgroundModeEnabled" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser" /v "ScreenshotsEnabled" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser" /v "RestoreOnStartup" /t REG_DWORD /d 4 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser" /v "UpdateDefault" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser" /v "MetricsReportingEnabled" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser" /v "SessionRestoreAutoRestore" /t REG_DWORD /d 0 /f >nul 2>&1

:: Альтернативные пути для политик (с пробелом)
reg add "HKLM\SOFTWARE\Policies\Yandex\Yandex Browser" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\Yandex Browser" /v "BackgroundModeEnabled" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\Yandex Browser" /v "ScreenshotsEnabled" /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\Yandex Browser" /v "RestoreOnStartup" /t REG_DWORD /d 4 /f >nul 2>&1

reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "YandexBrowser" /f >nul 2>&1
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "YandexBrowser" /f >nul 2>&1
echo     [+] Политики применены


:: --- УДАЛЕНИЕ ФАЙЛОВ СЕССИЙ ---
echo [3] Очистка файлов сессий...

if exist "%SESSIONS_DIR%" (
    del /f /q "%SESSIONS_DIR%\*.*" >nul 2>&1
    echo     [+] Очищена папка Sessions
)

if exist "%SESSION_STORAGE%" (
    del /f /q "%SESSION_STORAGE%\*.*" >nul 2>&1
    echo     [+] Очищена папка Session Storage
)

:: --- УДАЛЕНИЕ ФАЙЛА СКРИНШОТЕРА (если есть) ---
echo [4] Удаление скриншотера...

for /d %%d in ("26.4.0.2116") do (
    if exist "%%d\YandexDiskScreenshotEditor.exe" (
        del /f /q "%%d\YandexDiskScreenshotEditor.exe" >nul 2>&1
        echo     [+] Удалён YandexDiskScreenshotEditor.exe
    )
)

:: --- УСТАНОВКА РАСШИРЕНИЙ ---
echo [5] Установка расширений...

reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser\ExtensionInstallForcelist" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser\ExtensionInstallForcelist" /v "1" /t REG_SZ /d "cjpalhdlnbpafiamejdnhcphjbkeiagm;https://clients2.google.com/service/update2/crx" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser\ExtensionInstallForcelist" /v "2" /t REG_SZ /d "pkehgijcmpdhfbdbbnkijodmdjhbjlgp;https://clients2.google.com/service/update2/crx" /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Yandex\YandexBrowser\ExtensionInstallForcelist" /v "3" /t REG_SZ /d "gcbommkclmclpchllfjekcdonpmejbdp;https://clients2.google.com/service/update2/crx" /f >nul 2>&1
echo     [+] Расширения добавлены

:: --- ИМПОРТ ПОЛЬЗОВАТЕЛЬСКИХ НАСТРОЕК ---
if exist "AlicesThong.reg" (
    echo [6] Импорт настроек...
    reg import "AlicesThong.reg" >nul 2>&1
    echo     [+] Импорт выполнен
)

:: --- ЗАПУСК БРАУЗЕРА С ФЛАГАМИ ---
echo.
echo [7] Запуск Яндекс Браузера...

:: Все возможные флаги для отключения нежелательных функций
"%BROWSER_EXE%" ^
    --no-default-browser-check ^
    --no-first-run ^
    --no-pings ^
    --no-report-upload ^
    --no-crash-upload ^
    --disable-background-mode ^
    --disable-background-networking ^
    --disable-background-timer-throttling ^
    --disable-breakpad ^
    --disable-crash-reporter ^
    --disable-dev-shm-usage ^
    --disable-extensions-except="cjpalhdlnbpafiamejdnhcphjbkeiagm,pkehgijcmpdhfbdbbnkijodmdjhbjlgp,gcbommkclmclpchllfjekcdonpmejbdp" ^
    --disable-features=Screenshots,AutomaticTabDiscarding,BackgroundModeEnabled,SessionRestoreAutoRestore ^
    --disable-logging ^
    --disable-metrics ^
    --disable-metrics-reporting ^
    --disable-session-crashed-bubble ^
    --disable-sync ^
    --disable-sync-telemetry ^
    --disable-usage-statistics ^
    --no-sandbox ^
    --restore-on-startup=0 ^
    --silent-debugger-extension-api ^
    --test-type --ignore-certificate--errors ^
    anton18-png.github.io/Alices-thong/start

:: Браузер работает в обычном режиме без wait (иначе скрипт зависнет)

:: --- ЭКСПОРТ НАСТРОЕК (перед очисткой) ---
echo.
echo [8] Ожидание закрытия браузера...
tasklist /fi "imagename eq %BROWSER_EXE%" | findstr /i "%BROWSER_EXE%" >nul
:wait
timeout /t 2 /nobreak >nul
tasklist /fi "imagename eq %BROWSER_EXE%" | findstr /i "%BROWSER_EXE%" >nul
if not errorlevel 1 goto wait
echo     [+] Браузер закрыт

:: --- ЭКСПОРТ НАСТРОЕК В REG ФАЙЛ ---
echo.
echo [9] Экспорт настроек...

reg export "HKCU\Software\Yandex\YandexBrowser" "AlicesThong.reg" /y >nul 2>&1

if exist "AlicesThong.reg" (
    for %%A in ("AlicesThong.reg") do (
        echo     [+] Настройки сохранены в AlicesThong.reg (%%~zA байт)
    )
)

:: --- ОЧИСТКА РЕЕСТРА ---
echo.
echo [10] Очистка реестра...
reg delete "HKCU\Software\Yandex" /f >nul 2>&1
echo     [+] Ветка HKCU\Software\Yandex удалена