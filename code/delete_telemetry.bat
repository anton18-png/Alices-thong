@echo off
chcp 65001
color f0
setlocal enabledelayedexpansion

:: Удаляем все ключи телеметрии Яндекс Браузера
echo Удаляем все ключи телеметрии Яндекс Браузера...
reg delete "HKLM\SOFTWARE\Policies\Yandex\Browser" /f
reg delete "HKLM\SOFTWARE\Yandex\Browser" /f
reg delete "HKCU\SOFTWARE\Yandex\Browser" /f
reg delete "HKLM\SOFTWARE\Yandex\Telemetry" /f
reg delete "HKLM\SOFTWARE\Yandex\UsageStatistics" /f
reg delete "HKLM\SOFTWARE\Yandex\CrashReports" /f
reg delete "HKLM\SOFTWARE\Yandex\RLZ" /f
reg delete "HKLM\SOFTWARE\Yandex\SearchSuggest" /f
reg delete "HKLM\SOFTWARE\Yandex\SafeBrowsing" /f
reg delete "HKLM\SOFTWARE\Yandex\BrowserUsageTracking" /f
reg delete "HKLM\SOFTWARE\Yandex\ExtensionUsageTracking" /f
reg delete "HKLM\SOFTWARE\Yandex\ExtensionInstallTracking" /f
reg delete "HKLM\SOFTWARE\Yandex\ExtensionUpdateTracking" /f
reg delete "HKLM\SOFTWARE\Yandex\Extension::ovalTracking" /f
reg delete "HKLM\SOFTWARE\Yandex\ExtensionCrashReporting" /f

:: Удаляем все записи телеметрии
reg delete "HKCU\Software\Yandex\YandexBrowser\Telemetry" /f

:: Удаляем все службы Яндекса
echo Удаляем все службы Яндекса...

:: Останавливаем службу Яндекс Браузера
SC STOP YandexBrowserService
SC CONFIG YandexBrowserService start= disabled
SC DELETE YandexBrowserService

sc stop YandexUpdaterService
sc delete YandexUpdaterService
sc stop YaTransmgr
sc delete YaTransmgr
sc stop YandexProtectService
sc delete YandexProtectService
sc stop YandexDiskSync
sc delete YandexDiskSync
sc stop YandexBrowserUpdater
sc delete YandexBrowserUpdater
sc stop YandexBrowserCrashHandler
sc delete YandexBrowserCrashHandler
sc stop YandexBrowserExtensionUpdater
sc delete YandexBrowserExtensionUpdater

:: Удаляем все задания планировщика задач, связанные с Яндексом
echo Удаляем все задания планировщика задач, связанные с Яндексом...
schtasks /delete /tn "YandexUpdaterTask" /f
schtasks /delete /tn "YandexProtectTask" /f
schtasks /delete /tn "YandexDiskSyncTask" /f
schtasks /delete /tn "YandexBrowserUpdaterTask" /f
schtasks /delete /tn "YandexBrowserCrashHandlerTask" /f
schtasks /delete /tn "YandexBrowserExtensionUpdaterTask" /f

:: Удаляем все расширения
:: for /f "tokens=*" %%a in ('reg query "HKCU\Software\Yandex\YandexBrowser\Extensions" /s /v') do (
::   reg delete "HKCU\Software\Yandex\YandexBrowser\Extensions\%%a" /f
:: )

:: Восстанавливаем необходимые расширения
reg add "HKCU\Software\Yandex\YandexBrowser\Extensions" /v "Yandex Browser Helper" /t REG_SZ /d "obkmjpcfjnhmkgpjikgklnjnmhphgknb" /f
reg add "HKCU\Software\Yandex\YandexBrowser\Extensions" /v "Yandex Browser Updater" /t REG_SZ /d "kmendfapggjehodndflmmgagdbamhnob" /f
reg add "HKCU\Software\Yandex\YandexBrowser\Extensions" /v "Yandex Browser Crash Handler" /t REG_SZ /d "igikjgjehlmljgjgjgjgjgjgjgjgjgj" /f

:: Устанавливаем расширения для приватности
reg add "HKCU\Software\Yandex\YandexBrowser\Extensions" /v "uBlock Origin" /t REG_SZ /d "cjpalhdlnbpafiamejdnhcphjbkeiagm" /f
reg add "HKCU\Software\Yandex\YandexBrowser\Extensions" /v "HTTPS Everywhere" /t REG_SZ /d "gcbommkclmclpchllfjekcdonpmejbdp" /f
reg add "HKCU\Software\Yandex\YandexBrowser\Extensions" /v "Privacy Badger" /t REG_SZ /d "pkehgijcmpdhfbdbbnkijodmdjhbjlgp" /f

:: Добавляем записи в hosts для блокировки обновлений и телеметрии
echo 127.0.0.1 update.api.yandex.net >> "%windir%\System32\drivers\etc\hosts"
echo 127.0.0.1 events.yandex.net >> "%windir%\System32\drivers\etc\hosts"
echo 127.0.0.1 metrics.yandex.com >> "%windir%\System32\drivers\etc\hosts"
echo 127.0.0.1 api-metrics.yandex.net >> "%windir%\System32\drivers\etc\hosts"

:: Отключаем телеметрию
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "send_usage_stats" /t REG_DWORD /d 0 /f
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "send_crash_reports" /t REG_DWORD /d 0 /f
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "send_error_reports" /t REG_DWORD /d 0 /f

:: Включаем режим инкогнито по умолчанию
:: reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "default_browser_mode" /t REG_DWORD /d 1 /f

:: Удаляем историю посещений после закрытия браузера
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "delete_history_after_close" /t REG_DWORD /d 1 /f

:: Удаляем куки после закрытия браузера
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "delete_cookies_after_close" /t REG_DWORD /d 1 /f

:: Удаляем локальное хранилище после закрытия браузера
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "delete_local_storage_after_close" /t REG_DWORD /d 1 /f

:: Включаем шифрование данных при передаче
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "encryption" /t REG_DWORD /d 1 /f

:: Включаем проверку сертификатов
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "certificate_check" /t REG_DWORD /d 1 /f

:: Включаем блокировку вредоносных сайтов
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "malware_protection" /t REG_DWORD /d 1 /f

:: Устанавливаем сторонний DNS-сервис
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "dns_provider" /t REG_SZ /d "cloudflare" /f

:: Устанавливаем сторонний proxy-сервис
reg add "HKCU\Software\Yandex\YandexBrowser\Settings" /v "proxy_provider" /t REG_SZ /d "tor" /f

:: Настройка GoodbyeDPI для работы с Яндекс Браузером
Reg.exe add "HKCU\Software\Policies\Yandex\YandexBrowser" /v "QuicEnabled" /t REG_DWORD /d "0" /f
Reg.exe add "HKCU\Software\Policies\Yandex\YandexBrowser" /v "TLS13HybridKyberEnabled" /t REG_DWORD /d "0" /f
Reg.exe add "HKLM\Software\Policies\Yandex\YandexBrowser" /v "QuicEnabled" /t REG_DWORD /d "0" /f
Reg.exe add "HKLM\Software\Policies\Yandex\YandexBrowser" /v "TLS13HybridKyberEnabled" /t REG_DWORD /d "0" /f

:: Сообщаем об успешном завершении
echo Телеметрия и службы Яндекс Браузера отключены. Настройки изменены на полную приватность и анонимность.
echo Настройки Яндекс Браузера изменены.

:: start "" "%USERPROFILE%\AppData\Local\Yandex\YandexBrowser\Application\browser.exe" --disable-usage-stats --disable-crash-reporter --disable-error-reporter --disable-telemetry --disable-sync --disable-background-apps --enable-features=IncognitoModeAvailability,IncognitoModeAvailability:enabled_by_default

pause

SC STOP YandexBrowserService
SC CONFIG YandexBrowserService start= disabled
SC DELETE YandexBrowserService

browser\browser.exe --user-data-dir="%~dp0%\USER_DATA" --allow-outdated-plugins --disable-logging --disable-breakpad --disable-encryption --disable-machine-id --disable-usage-statistics --disable-crash-reporter --disable-metrics --disable-metrics-reporting --disable-sync --disable-sync-telemetry --disable-rlz --disable-client-side-prediction anton18-png.github.io/Alices-thong/start