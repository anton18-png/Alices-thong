SC STOP YandexBrowserService
SC CONFIG YandexBrowserService start= disabled
SC DELETE YandexBrowserService

browser\browser.exe --user-data-dir="%~dp0%\USER_DATA" --allow-outdated-plugins --disable-logging --disable-breakpad --disable-encryption --disable-machine-id --disable-usage-statistics --disable-crash-reporter --disable-metrics --disable-metrics-reporting --disable-sync --disable-sync-telemetry --disable-rlz --disable-client-side-prediction anton18-png.github.io/Alices-thong/start