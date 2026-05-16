import os
import subprocess
import json
import time
from pathlib import Path

BROWSER_FLAGS_SYNC = [
    "--no-default-browser-check",
    "--no-first-run",
    "--no-pings",
    "--no-report-upload",
    "--no-crash-upload",
    "--disable-background-mode",
    "--disable-background-networking",
    "--disable-background-timer-throttling",
    "--disable-breakpad",
    "--disable-crash-reporter",
    "--disable-dev-shm-usage",
    "--disable-features=Screenshots,AutomaticTabDiscarding,BackgroundModeEnabled,SessionRestoreAutoRestore",
    "--disable-logging",
    "--disable-metrics",
    "--disable-metrics-reporting",
    "--disable-session-crashed-bubble",
    "--disable-usage-statistics",
    "--no-sandbox",
    "--restore-on-startup=0",
    "--silent-debugger-extension-api",
    "--test-type",
    "--ignore-certificate-errors",
    "--force-dark-mode",
]

BROWSER_FLAGS_NOSYNC = BROWSER_FLAGS_SYNC + [
    "--disable-sync",
    "--disable-sync-types=ALL",
]

REG_POLICIES = [
    ("BackgroundModeEnabled", "0"),
    ("ScreenshotsEnabled", "0"),
    ("RestoreOnStartup", "4"),
    ("UpdateDefault", "0"),
    ("MetricsReportingEnabled", "0"),
    ("SessionRestoreAutoRestore", "0"),
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


def run_as_admin():
    import ctypes, sys
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)


def find_browser_exe(base_dir):
    for name in ["browser.exe", "chrome.exe", "AlicesThong.exe"]:
        p = Path(base_dir) / name
        if p.exists():
            return str(p)
    app_dir = Path(base_dir) / "app"
    if app_dir.exists():
        for name in ["browser.exe", "chrome.exe", "AlicesThong.exe"]:
            p = app_dir / name
            if p.exists():
                return str(p)
        for d in app_dir.iterdir():
            if d.is_dir() and d.name[0].isdigit():
                for name in ["browser.exe", "chrome.exe"]:
                    p = d / name
                    if p.exists():
                        return str(p)
    return None


def find_data_dir(base_dir):
    d = Path(base_dir) / "data"
    d.mkdir(parents=True, exist_ok=True)
    (d / "Default").mkdir(parents=True, exist_ok=True)
    return str(d)


def apply_registry_policies(disable_sync=False):
    results = []
    base = r"HKLM\SOFTWARE\Policies\Yandex\YandexBrowser"
    subprocess.run(f'reg add "{base}" /f', shell=True, capture_output=True)
    for key, val in REG_POLICIES:
        subprocess.run(f'reg add "{base}" /v "{key}" /t REG_DWORD /d {val} /f', shell=True, capture_output=True)
        results.append(f"Политика {key} = {val}")
    if disable_sync:
        subprocess.run(f'reg add "{base}" /v "SyncDisabled" /t REG_DWORD /d 1 /f', shell=True, capture_output=True)
        results.append("Синхронизация отключена через реестр")
    alt = r"HKLM\SOFTWARE\Policies\Yandex\Yandex Browser"
    subprocess.run(f'reg add "{alt}" /f', shell=True, capture_output=True)
    for key, val in REG_POLICIES[:4]:
        subprocess.run(f'reg add "{alt}" /v "{key}" /t REG_DWORD /d {val} /f', shell=True, capture_output=True)
    return results


def stop_services():
    results = []
    for svc in YANDEX_SERVICES:
        subprocess.run(f"sc stop {svc}", shell=True, capture_output=True)
        subprocess.run(f"sc config {svc} start= disabled", shell=True, capture_output=True)
        subprocess.run(f"sc delete {svc}", shell=True, capture_output=True)
        results.append(f"Служба {svc} заблокирована")
    return results


def delete_schtasks():
    results = []
    for task in YANDEX_SCHTASKS:
        subprocess.run(f'schtasks /delete /tn "{task}" /f', shell=True, capture_output=True)
        results.append(f"Задача {task} удалена")
    return results


def create_preferences(data_dir):
    prefs_file = Path(data_dir) / "Default" / "Preferences"
    if prefs_file.exists():
        try:
            with open(prefs_file, "r", encoding="utf-8") as f:
                prefs = json.load(f)
        except:
            prefs = {}
    else:
        prefs = {}

    prefs["browser"]["metrics_id"] = ""
    prefs["browser"]["metrics_last_report"] = ""
    prefs["browser"]["last_metrics_id"] = ""
    prefs["browser"]["first_day_of_month_metrics"] = ""
    prefs["browser"]["disable_telemetry"] = True
    prefs["browser"]["disable_background_networking"] = True
    prefs["browser"]["disable_logging"] = True
    prefs["background_mode"]["enabled"] = False
    prefs["session"]["restore_on_startup"] = 0
    prefs["session"]["max_recently_selected"] = 0
    prefs["safebrowsing"]["enabled"] = False
    prefs["download"]["prompt_for_download"] = True

    prefs_file.parent.mkdir(parents=True, exist_ok=True)
    with open(prefs_file, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2)
    return str(prefs_file)


def clear_sessions(data_dir):
    results = []
    sessions = Path(data_dir) / "Default" / "Sessions"
    session_storage = Path(data_dir) / "Default" / "Session Storage"
    for p in [sessions, session_storage]:
        if p.exists():
            for f in p.glob("*"):
                f.unlink(missing_ok=True)
            results.append(f"Очищена папка {p.name}")
    return results


def remove_screenshots(browser_exe_dir):
    results = []
    for f in Path(browser_exe_dir).glob("YandexDiskScreenshotEditor.exe"):
        f.unlink(missing_ok=True)
        results.append("Удалён YandexDiskScreenshotEditor.exe")
    return results


def export_registry():
    results = []
    sid = ""
    try:
        out = subprocess.run("whoami /user /nh", shell=True, capture_output=True, text=True)
        sid = out.stdout.strip().split()[-1]
    except:
        pass
    r1 = subprocess.run('reg export "HKCU\\Software\\Yandex\\YandexBrowser" "AlicesThong.reg" /y',
                        shell=True, capture_output=True)
    results.append(f"Экспорт HKCU: {r1.returncode}")
    if sid:
        r2 = subprocess.run(f'reg export "HKU\\{sid}\\Software\\Yandex\\YandexBrowser" "AlicesThong_HKU.reg" /y',
                            shell=True, capture_output=True)
        results.append(f"Экспорт HKU: {r2.returncode}")
    return results


def cleanup_registry():
    results = []
    subprocess.run('reg delete "HKCU\\Software\\Yandex" /f', shell=True, capture_output=True)
    results.append("Реестр HKCU очищен")
    try:
        out = subprocess.run("whoami /user /nh", shell=True, capture_output=True, text=True)
        sid = out.stdout.strip().split()[-1]
        subprocess.run(f'reg delete "HKU\\{sid}\\Software\\Yandex" /f', shell=True, capture_output=True)
        results.append("Реестр HKU очищен")
    except:
        pass
    return results


def run_pre_launch(delay_ms=0):
    import time
    if delay_ms > 0:
        time.sleep(delay_ms / 1000)
    results = []
    results.extend(stop_services())
    results.extend(delete_schtasks())
    return results


def run_browser(browser_exe, flags, start_url="anton18-png.github.io/Alices-thong/start"):
    cmd = [browser_exe] + flags
    if start_url:
        cmd.append(start_url)
    subprocess.Popen(cmd, shell=True)
