@echo off
chcp 65001 >nul
title Clean Yandex Browser - Final Version
echo ===================================================
echo Очистка Яндекс Браузера (минимальная)
echo ===================================================
echo.

cd /d "%~dp0"

:: Удаление .sig файлов (везде)
echo [1] Удаление файлов подписей (.sig)...
del /f /q /s *.sig 2>nul
echo     [+] Все .sig файлы удалены

:: Удаление файлов в корне
echo [2] Удаление лишних файлов в корне...
del /f /q browser.VisualElementsManifest.xml 2>nul
del /f /q browser_proxy.exe 2>nul
del /f /q clidmgr.exe 2>nul
del /f /q debug.log 2>nul
echo     [+] Готово

:: Переход в папку с версией
if exist "26.4.0.2116" (
    cd "26.4.0.2116"
) else (
    echo Папка 26.4.0.2116 не найдена!
    pause
    exit /b 1
)

:: Удаление телеметрии и мусора (НЕ трогаем notification_helper)
echo [3] Удаление телеметрии и мусорных файлов...
del /f /q eventlog_provider.dll 2>nul
del /f /q partner_config 2>nul
del /f /q brand_config 2>nul
echo     [+] Готово
echo     [+] notification_helper.exe и YandexDictionaries оставлены

:: Удаление ненужных папок
echo [4] Удаление ненужных папок...

for %%d in (
    "IwaKeyDistribution"
    "MEIPreload"
    "PrivacySandboxAttestationsPreloaded"
) do (
    if exist "%%d" (
        rmdir /s /q "%%d" 2>nul
        echo     Удалено: %%d
    )
)

:: Удаление стандартных фильтров рекламы (опционально)
echo.
choice /c YN /n /m "Удалить стандартные фильтры рекламы easylist? (Y/N) "
if not errorlevel 2 (
    if exist "resources\easylist" rmdir /s /q "resources\easylist" 2>nul
    echo     [+] Easylist удалён
) else (
    echo     [-] Easylist оставлен
)

echo.
echo ===================================================
echo Очистка завершена!
echo.
echo УДАЛЕНО:
echo - .sig файлы
echo - browser_proxy.exe, clidmgr.exe
echo - eventlog_provider.dll
echo - IwaKeyDistribution, MEIPreload, PrivacySandboxAttestationsPreloaded
echo.
echo ОСТАВЛЕНО:
echo - notification_helper.exe
echo - YandexDictionaries
echo - ntp, text_detector_data, vk_swiftshader.dll
echo - resources/wallpapers, resources/safebrowsing
echo - ui_config, widgets, web_app_config
echo - Все нейросети (Алиса, Нейроредактор, Перевод видео)
echo ===================================================
pause