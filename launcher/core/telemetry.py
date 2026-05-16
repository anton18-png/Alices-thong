import os
import subprocess
import shutil
from pathlib import Path

YANDEX_TELEMETRY = [
    "debug.log",
    "eventlog_provider.dll",
    "service_update.exe",
    "browser_wer.dll",
    "MEIPreload",
    "PrivacySandboxAttestationsPreloaded",
]

YANDEX_OPTIONAL = {
    "notifications": ["notification_helper.exe"],
    "sync": ["IwaKeyDistribution"],
    "alice": ["alice_solver", "voiceactivation", "cspeechkit.dll", "speechkit_action_lib64.dll"],
    "neuro": ["neuroedit", "readability_ml", "text_detector_data", "video_translation", "dssm.dll", "textclassifier.dll"],
    "widgets": ["widgets"],
    "visual": ["VisualElements", "browser.VisualElementsManifest.xml"],
    "sig": ["*.sig"],
    "easylist": ["resources/easylist"],
    "dxvk": ["d3dcompiler_47.dll", "dxcompiler.dll", "dxil.dll", "libEGL.dll", "libGLESv2.dll", "vk_swiftshader.dll", "vk_swiftshader_icd.json", "vulkan-1.dll"],
    "service_bins": ["browser_proxy.exe", "clidmgr.exe", "browser_elf.dll", "offline_spellchecker.dll", "winrt_helper.dll", "unpacki.dll", "7z.dll", "brodef.dll", "abt-bindings.dll", "modules"],
    "brand_config": ["brand_config", "partner_config"],
    "wallpapers": ["resources/wallpapers"],
    "morphology": ["resources/morphology"],
    "safebrowsing": ["resources/safebrowsing"],
    "ui_config": ["ui_config"],
    "web_app_config": ["web_app_config"],
    "ntp_cache": ["ntp/NativeCacheStorage"],
    "browser_paks": ["browser_100_percent.pak", "browser_200_percent.pak"],
    "v8_snapshot": ["v8_context_snapshot.bin"],
    "logos": ["resources/about_logo_en.png", "resources/about_logo_en_2x.png", "resources/about_logo_ru.png", "resources/about_logo_ru_2x.png", "resources/cloud_notes.ico", "resources/messenger.ico", "resources/sxs.ico", "resources/tablo"],
    "extensions_data": ["resources/extension"],
    "locales_extra": ["Locales/en-US_FEMININE.pak", "Locales/en-US_MASCULINE.pak", "Locales/en-US_NEUTER.pak", "Locales/ru_FEMININE.pak", "Locales/ru_MASCULINE.pak", "Locales/ru_NEUTER.pak"],
}

GOOGLE_CHROME_TELEMETRY = [
    "kss.dll", "chrome_wer.dll", "elevation_service.exe",
    "software_reporter_tool.exe", "swiftshader",
]

OPERA_TELEMETRY = [
    "opera_autoupdate.exe", "opera_crashreporter.exe",
    "browser_wer.dll", "operalog.log",
]

YANDEX_SERVICES = [
    "YandexBrowserService", "YandexUpdaterService", "YaTransmgr",
    "YandexProtectService", "YandexDiskSync", "YandexBrowserUpdater",
    "YandexBrowserCrashHandler", "YandexBrowserExtensionUpdater",
]

YANDEX_SCHTASKS = [
    "YandexUpdaterTask", "YandexProtectTask", "YandexDiskSyncTask",
    "YandexBrowserUpdaterTask", "YandexBrowserCrashHandlerTask",
    "YandexBrowserExtensionUpdaterTask", "YandexBrowserUpdateTask",
    "YandexUpdateTaskMachineCore", "YandexUpdateTaskMachineUA",
    "Восстановление сервиса обновлений Яндекс Браузер",
    "Обновление Браузера Яндекс", "Системное обновление Браузера Яндекс",
]

YANDEX_REGISTRY_PATHS = [
    r"HKLM\SOFTWARE\Yandex",
    r"HKLM\SOFTWARE\Wow6432Node\Yandex",
    r"HKCU\SOFTWARE\Yandex",
    r"HKCU\SOFTWARE\AppDataLow\Yandex",
    r"HKLM\SOFTWARE\Policies\Yandex",
    r"HKCU\SOFTWARE\Policies\Yandex",
]

# Все хосты используют 127.0.0.1 для единообразия

YANDEX_HOSTS = [
    "127.0.0.1 yandex.com",
    "127.0.0.1 passport.yandex.ru",
    "127.0.0.1 avatars.yandex.net",
    "127.0.0.1 yandex.ru",
    "127.0.0.1 ya.ru",
    "127.0.0.1 yandex.net",
    "127.0.0.1 yastatic.net",
    "127.0.0.1 yandex.org",
    "127.0.0.1 yandex.com.ru",
    "127.0.0.1 yandex.net.ru",
    "127.0.0.1 yandex.by",
    "127.0.0.1 yandex.kz",
    "127.0.0.1 yandex.uz",
    "127.0.0.1 yandex.md",
    "127.0.0.1 yandex.fr",
    "127.0.0.1 yandex.az",
    "127.0.0.1 yandex.com.tr",
    "127.0.0.1 yandex.ro",
    "127.0.0.1 yandex.asia",
    "127.0.0.1 yandex.mobi",
    "127.0.0.1 yandex.ua",
    "127.0.0.1 www.yandex.ru",
    "127.0.0.1 www.yandex.com",
    "127.0.0.1 mc.yandex.ru",
    "127.0.0.1 metrika.yandex.ru",
    "127.0.0.1 metrika.yandex.net",
    "127.0.0.1 audience.yandex.ru",
    "127.0.0.1 direct.yandex.ru",
    "127.0.0.1 money.yandex.ru",
    "127.0.0.1 market.yandex.ru",
    "127.0.0.1 afisha.yandex.ru",
    "127.0.0.1 news.yandex.ru",
    "127.0.0.1 pogoda.yandex.ru",
    "127.0.0.1 tv.yandex.ru",
    "127.0.0.1 translate.yandex.ru",
    "127.0.0.1 browser.yandex.ru",
    "127.0.0.1 dzen.ru",
    "127.0.0.1 zen.yandex.ru",
    "127.0.0.1 kinopoisk.ru",
    "127.0.0.1 auto.ru",
    "127.0.0.1 rabota.ru",
    "127.0.0.1 cloud.yandex.ru",
    "127.0.0.1 storage.yandexcloud.net",
    "127.0.0.1 api.browser.yandex.ru",
    "127.0.0.1 update.browser.yandex.net",
    "127.0.0.1 station.yandex",
    "127.0.0.1 metrica.yandex",
    "127.0.0.1 docs.yandex",
    "127.0.0.1 rentaxi.yandex",
    "127.0.0.1 translate-image.yandex",
    "127.0.0.1 music.yandex.ru",
    "127.0.0.1 disk.yandex.ru",
    "127.0.0.1 taxi.yandex.ru",
    "127.0.0.1 eda.yandex.ru",
    "127.0.0.1 maps.yandex.ru",
    "127.0.0.1 mail.yandex.ru",
    "127.0.0.1 browser-update.yandex.ru",
    "127.0.0.1 updater.yandex.ru",
    "127.0.0.1 update.yandex.ru",
    "127.0.0.1 autoupdate.yandex.ru",
    "127.0.0.1 autoupdate.yandex.net",
    "127.0.0.1 stat.yandex.ru",
    "127.0.0.1 stats.yandex.ru",
    "127.0.0.1 counter.yandex.ru",
    "127.0.0.1 clickhouse.yandex.ru",
    "127.0.0.1 analytics.yandex.ru",
    "127.0.0.1 report.yandex.ru",
    "127.0.0.1 reports.yandex.ru",
    "127.0.0.1 api.yandex.ru",
    "127.0.0.1 api.yandex.com",
    "127.0.0.1 backend.yandex.ru",
    "127.0.0.1 ssp.yandex.ru",
    "127.0.0.1 rtb.yandex.ru",
    "127.0.0.1 adfox.yandex.ru",
    "127.0.0.1 ads.yandex.ru",
    "127.0.0.1 browser.yandex.net",
    "127.0.0.1 ya-browser.yandex.ru",
    "127.0.0.1 protect.yandex.ru",
    "127.0.0.1 protect.yandex.net",
    "127.0.0.1 yandexprotect.ru",
    "127.0.0.1 yandexprotect.net",
    "127.0.0.1 passport.yandex.com",
    "127.0.0.1 id.yandex.ru",
    "127.0.0.1 login.yandex.ru",
    "127.0.0.1 sync.yandex.ru",
    "127.0.0.1 sync.yandex.net",
    "127.0.0.1 disk.yandex.net",
    "127.0.0.1 storage.yandex.net",
    "127.0.0.1 radio.yandex.ru",
    "127.0.0.1 video.yandex.ru",
    "127.0.0.1 yandex-news.ru",
    "127.0.0.1 navigator.yandex.ru",
    "127.0.0.1 delivery.yandex.ru",
    "127.0.0.1 food.yandex.ru",
    "127.0.0.1 alice.yandex.ru",
    "127.0.0.1 voice.yandex.ru",
    "127.0.0.1 speech.yandex.ru",
    "127.0.0.1 events.yandex.net",
    "127.0.0.1 metrics.yandex.com",
    "127.0.0.1 api-metrics.yandex.net",
    "127.0.0.1 update.api.yandex.net",
    "127.0.0.1 yandexad.com",
    "127.0.0.1 yandexads.com",
    "127.0.0.1 yandex-adfox.ru",
    "127.0.0.1 market.yandex.com",
    "127.0.0.1 avito.yandex.ru",
    "127.0.0.1 realty.yandex.ru",
    "127.0.0.1 auto.yandex.ru",
    "127.0.0.1 health.yandex.ru",
    "127.0.0.1 weather.yandex.ru",
    "127.0.0.1 horoscope.yandex.ru",
    "127.0.0.1 kinopoisk.yandex.ru",
    "127.0.0.1 games.yandex.ru",
    "127.0.0.1 launcher.yandex.ru",
    "127.0.0.1 disc.yandex.ru",
    "127.0.0.1 mail.yandex.com",
    "127.0.0.1 connect.yandex.ru",
    "127.0.0.1 oauth.yandex.ru",
    "127.0.0.1 social.yandex.ru",
    "127.0.0.1 cpm.yandex.ru",
    "127.0.0.1 offer.yandex.ru",
    "127.0.0.1 target.yandex.ru",
    "127.0.0.1 adsrv.yandex.ru",
    "127.0.0.1 an.yandex.ru",
    "127.0.0.1 webmaster.yandex.ru",
    "127.0.0.1 webvisor.yandex.ru",
    "127.0.0.1 appmetrica.yandex.ru",
    "127.0.0.1 appmetrica.yandex.net",
    "127.0.0.1 push.yandex.ru",
    "127.0.0.1 yabs.yandex.ru",
    "127.0.0.1 wap.yandex.ru",
    "127.0.0.1 m.yandex.ru",
    "127.0.0.1 yandex.st",
    "127.0.0.1 yandexadexchange.net",
    "127.0.0.1 yandex-video.net",
    "127.0.0.1 yandex.download",
    "127.0.0.1 yandex.video",
    "127.0.0.1 yandex.maps",
    "127.0.0.1 yandex.music",
    "127.0.0.1 yandex.taxi",
    "127.0.0.1 yandex.market",
    "127.0.0.1 yandex.mail",
    "127.0.0.1 yandex.news",
    "127.0.0.1 yandex.zen",
    "127.0.0.1 yandex.alice",
    "127.0.0.1 yandex.translate",
    "127.0.0.1 yandex.weather",
    "127.0.0.1 yandex.images",
    "127.0.0.1 yandex.pogoda",
    "127.0.0.1 yandex.rasp",
    "127.0.0.1 yandex.health",
    "127.0.0.1 yandex.autoru",
    "127.0.0.1 yandex.realty",
    "127.0.0.1 yandex.jobs",
    "127.0.0.1 yandex.collections",
    "127.0.0.1 yandex.poster",
    "127.0.0.1 yandex.plus",
    "127.0.0.1 yandex.pay",
    "127.0.0.1 yandex.eda",
    "127.0.0.1 yandex.lavka",
    "127.0.0.1 yandex.drive",
    "127.0.0.1 yandex.go",
    "127.0.0.1 yandex.sports",
    "127.0.0.1 yandex.finance",
]

GOOGLE_CHROME_HOSTS = [
    "127.0.0.1 ssl.google-analytics.com",
    "127.0.0.1 www.google-analytics.com",
    "127.0.0.1 google-analytics.com",
    "127.0.0.1 stats.g.doubleclick.net",
    "127.0.0.1 www.googletagmanager.com",
    "127.0.0.1 googletagmanager.com",
    "127.0.0.1 googleads.g.doubleclick.net",
    "127.0.0.1 pagead2.googlesyndication.com",
    "127.0.0.1 cm.g.doubleclick.net",
    "127.0.0.1 securepubads.g.doubleclick.net",
    "127.0.0.1 tpc.googlesyndication.com",
    "127.0.0.1 metrics.gstatic.com",
    "127.0.0.1 csi.gstatic.com",
    "127.0.0.1 crashlytics.google.com",
    "127.0.0.1 android.googleapis.com",
    "127.0.0.1 safebrowsing.googleapis.com",
    "127.0.0.1 safebrowsing.google.com",
    "127.0.0.1 dl.google.com",
    "127.0.0.1 update.googleapis.com",
]

OPERA_HOSTS = [
    "127.0.0.1 opera.com",
    "127.0.0.1 www.opera.com",
    "127.0.0.1 telemetry.opera.com",
    "127.0.0.1 telemetry-data.opera.com",
    "127.0.0.1 analytics.opera.com",
    "127.0.0.1 stats.opera.com",
    "127.0.0.1 usage.opera.com",
    "127.0.0.1 metrics.opera.com",
    "127.0.0.1 api.opera.com",
    "127.0.0.1 autoupdate.opera.com",
    "127.0.0.1 autoupdate-geo.opera.com",
    "127.0.0.1 update.opera.com",
    "127.0.0.1 updates.opera.com",
    "127.0.0.1 desktop-update.opera.com",
    "127.0.0.1 sync.opera.com",
    "127.0.0.1 auth.opera.com",
    "127.0.0.1 account.opera.com",
    "127.0.0.1 addons.opera.com",
    "127.0.0.1 extensions.opera.com",
    "127.0.0.1 logs.opera.com",
    "127.0.0.1 crashlogs.opera.com",
    "127.0.0.1 crash-reports.opera.com",
    "127.0.0.1 geo.opera.com",
    "127.0.0.1 vpn.opera.com",
    "127.0.0.1 cdn.opera.com",
    "127.0.0.1 browser.opera.com",
    "127.0.0.1 news.opera.com",
    "127.0.0.1 newsfeed.opera.com",
    "127.0.0.1 content.opera.com",
    "127.0.0.1 crypto.opera.com",
    "127.0.0.1 wallet.opera.com",
    "127.0.0.1 proxy.opera.com",
    "127.0.0.1 desktop.opera.com",
    "127.0.0.1 desktop-api.opera.com",
    "127.0.0.1 opera-api.com",
    "127.0.0.1 opera-api2.com",
    "127.0.0.1 operabrowser.com",
    "127.0.0.1 static.opera.com",
    "127.0.0.1 img.opera.com",
    "127.0.0.1 images.opera.com",
    "127.0.0.1 region.opera.com",
    "127.0.0.1 location.opera.com",
    "127.0.0.1 geolocation.opera.com",
    "127.0.0.1 tunnel.opera.com",
]

MAX_HOSTS = [
    "127.0.0.1 max.ru",
    "127.0.0.1 legal.max.ru",
    "127.0.0.1 download.max.ru",
]

MAILRU_HOSTS = [
    "127.0.0.1 mail.ru",
    "127.0.0.1 e.mail.ru",
    "127.0.0.1 m.mail.ru",
    "127.0.0.1 touch.mail.ru",
    "127.0.0.1 my.mail.ru",
    "127.0.0.1 agent.mail.ru",
    "127.0.0.1 cloud.mail.ru",
    "127.0.0.1 calendar.mail.ru",
    "127.0.0.1 todo.mail.ru",
    "127.0.0.1 files.mail.ru",
    "127.0.0.1 video.mail.ru",
    "127.0.0.1 audio.mail.ru",
    "127.0.0.1 foto.mail.ru",
    "127.0.0.1 games.mail.ru",
    "127.0.0.1 health.mail.ru",
    "127.0.0.1 lady.mail.ru",
    "127.0.0.1 hitech.mail.ru",
    "127.0.0.1 auto.mail.ru",
    "127.0.0.1 sport.mail.ru",
    "127.0.0.1 news.mail.ru",
    "127.0.0.1 realty.mail.ru",
    "127.0.0.1 ping.mail.ru",
    "127.0.0.1 api.mail.ru",
    "127.0.0.1 oauth.mail.ru",
    "127.0.0.1 connect.mail.ru",
    "127.0.0.1 target.mail.ru",
    "127.0.0.1 ads.mail.ru",
    "127.0.0.1 ad.mail.ru",
    "127.0.0.1 id.mail.ru",
    "127.0.0.1 login.mail.ru",
    "127.0.0.1 account.mail.ru",
    "127.0.0.1 help.mail.ru",
    "127.0.0.1 corp.mail.ru",
    "127.0.0.1 support.mail.ru",
    "127.0.0.1 delivery.mail.ru",
    "127.0.0.1 payment.mail.ru",
    "127.0.0.1 pay.mail.ru",
    "127.0.0.1 money.mail.ru",
    "127.0.0.1 biz.mail.ru",
    "127.0.0.1 job.mail.ru",
    "127.0.0.1 reg.mail.ru",
    "127.0.0.1 ld.mail.ru",
    "127.0.0.1 lists.mail.ru",
    "127.0.0.1 imgsmail.ru",
    "127.0.0.1 smtp.mail.ru",
    "127.0.0.1 imap.mail.ru",
    "127.0.0.1 pop.mail.ru",
    "127.0.0.1 r.mail.ru",
    "127.0.0.1 s.mail.ru",
    "127.0.0.1 static.mail.ru",
    "127.0.0.1 img.mail.ru",
    "127.0.0.1 cdn.mail.ru",
    "127.0.0.1 counters.mail.ru",
    "127.0.0.1 top.mail.ru",
    "127.0.0.1 tracker.mail.ru",
    "127.0.0.1 analytics.mail.ru",
    "127.0.0.1 stat.mail.ru",
    "127.0.0.1 logs.mail.ru",
    "127.0.0.1 push.mail.ru",
    "127.0.0.1 notify.mail.ru",
    "127.0.0.1 mradx.net",
    "127.0.0.1 mbx.mail.ru",
    "127.0.0.1 vk.com",
    "127.0.0.1 vk.ru",
    "127.0.0.1 vk.me",
    "127.0.0.1 userapi.com",
    "127.0.0.1 m.vk.com",
    "127.0.0.1 api.vk.com",
    "127.0.0.1 im.vk.com",
    "127.0.0.1 pu.vk.com",
    "127.0.0.1 ps.vk.com",
    "127.0.0.1 pv.vk.com",
    "127.0.0.1 pho.vk.com",
    "127.0.0.1 cdn.vk.com",
    "127.0.0.1 js.vk.com",
    "127.0.0.1 css.vk.com",
    "127.0.0.1 ads.vk.com",
    "127.0.0.1 target.vk.com",
    "127.0.0.1 ad.vk.com",
    "127.0.0.1 login.vk.com",
    "127.0.0.1 id.vk.com",
    "127.0.0.1 push.vk.com",
    "127.0.0.1 stats.vk.com",
    "127.0.0.1 files.vk.com",
    "127.0.0.1 music.vk.com",
    "127.0.0.1 video.vk.com",
    "127.0.0.1 live.vk.com",
    "127.0.0.1 mycdn.me",
    "127.0.0.1 ok.ru",
    "127.0.0.1 odnoklassniki.ru",
    "127.0.0.1 m.ok.ru",
    "127.0.0.1 api.ok.ru",
    "127.0.0.1 connect.ok.ru",
    "127.0.0.1 i.ok.ru",
    "127.0.0.1 im.ok.ru",
    "127.0.0.1 cfm.ok.ru",
    "127.0.0.1 groups.ok.ru",
    "127.0.0.1 upload.ok.ru",
    "127.0.0.1 apps.ok.ru",
    "127.0.0.1 log.ok.ru",
    "127.0.0.1 stats.ok.ru",
    "127.0.0.1 target.ok.ru",
    "127.0.0.1 ads.ok.ru",
    "127.0.0.1 ad.ok.ru",
    "127.0.0.1 my.games",
    "127.0.0.1 mygames.com",
]

GOSUSLUGI_HOSTS = [
    "127.0.0.1 gosuslugi.ru",
    "127.0.0.1 www.gosuslugi.ru",
    "127.0.0.1 lk.gosuslugi.ru",
    "127.0.0.1 esia.gosuslugi.ru",
    "127.0.0.1 passport.gosuslugi.ru",
    "127.0.0.1 login.gosuslugi.ru",
    "127.0.0.1 beta.gosuslugi.ru",
    "127.0.0.1 gosuslugi41.ru",
    "127.0.0.1 gosuslugi.tech",
    "127.0.0.1 gu.spb.ru",
    "127.0.0.1 mos.ru",
    "127.0.0.1 www.mos.ru",
    "127.0.0.1 mfc.ru",
    "127.0.0.1 gosuslugi74.ru",
    "127.0.0.1 gosuslugi.am",
    "127.0.0.1 gosuslugi.by",
    "127.0.0.1 gosuslugi.kz",
    "127.0.0.1 gosuslugi96.ru",
]


def find_browser_version_dir(base_path):
    app_path = Path(base_path) / "app"
    if not app_path.exists():
        return None
    for d in app_path.iterdir():
        if d.is_dir() and d.name[0].isdigit():
            return d
    return None


def remove_yandex_telemetry(browser_dir):
    results = []
    for item in YANDEX_TELEMETRY:
        path = Path(browser_dir) / item
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
            results.append(f"Удалена папка: {item}")
        elif path.exists():
            path.unlink(missing_ok=True)
            results.append(f"Удалён файл: {item}")
    return results


def remove_yandex_optional(browser_dir, items):
    results = []
    for item in items:
        path = Path(browser_dir) / item
        if "*" in item:
            for f in Path(browser_dir).glob(item):
                f.unlink(missing_ok=True)
                results.append(f"Удалён {f.name}")
            continue
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
            results.append(f"Удалена папка: {item}")
        elif path.exists():
            path.unlink(missing_ok=True)
            results.append(f"Удалён файл: {item}")
    return results


def remove_google_chrome_telemetry(browser_dir):
    results = []
    for item in GOOGLE_CHROME_TELEMETRY:
        path = Path(browser_dir) / item
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
            results.append(f"Удалена папка: {item}")
        elif path.exists():
            path.unlink(missing_ok=True)
            results.append(f"Удалён файл: {item}")
    return results


def remove_opera_telemetry(browser_dir):
    results = []
    for item in OPERA_TELEMETRY:
        path = Path(browser_dir) / item
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
            results.append(f"Удалена папка: {item}")
        elif path.exists():
            path.unlink(missing_ok=True)
            results.append(f"Удалён файл: {item}")
    return results


def cleanup_yandex_backups(browser_dir):
    results = []
    for f in Path(browser_dir).glob("*.backup"):
        f.unlink(missing_ok=True)
        results.append(f"Удалён {f.name}")
    return results


def stop_and_delete_services():
    results = []
    for svc in YANDEX_SERVICES:
        subprocess.run(f"sc stop {svc}", shell=True, capture_output=True)
        subprocess.run(f"sc delete {svc}", shell=True, capture_output=True)
        results.append(f"Служба {svc} остановлена и удалена")
    return results


def delete_schtasks():
    results = []
    for task in YANDEX_SCHTASKS:
        subprocess.run(f'schtasks /delete /tn "{task}" /f', shell=True, capture_output=True)
        results.append(f"Задача {task} удалена")
    return results


def apply_registry_policies():
    results = []
    policies = [
        ("BackgroundModeEnabled", "0"),
        ("ScreenshotsEnabled", "0"),
        ("RestoreOnStartup", "4"),
        ("UpdateDefault", "0"),
        ("MetricsReportingEnabled", "0"),
        ("SessionRestoreAutoRestore", "0"),
    ]
    base = r"HKLM\SOFTWARE\Policies\Yandex\YandexBrowser"
    subprocess.run(f'reg add "{base}" /f', shell=True, capture_output=True)
    for key, val in policies:
        subprocess.run(f'reg add "{base}" /v "{key}" /t REG_DWORD /d {val} /f', shell=True, capture_output=True)
        results.append(f"Политика {key} = {val}")

    alt = r"HKLM\SOFTWARE\Policies\Yandex\Yandex Browser"
    subprocess.run(f'reg add "{alt}" /f', shell=True, capture_output=True)
    for key, val in policies[:4]:
        subprocess.run(f'reg add "{alt}" /v "{key}" /t REG_DWORD /d {val} /f', shell=True, capture_output=True)
    return results


def delete_registry_keys():
    results = []
    for path in YANDEX_REGISTRY_PATHS:
        subprocess.run(f'reg delete "{path}" /f', shell=True, capture_output=True)
        results.append(f"Ветка {path} удалена")
    return results
