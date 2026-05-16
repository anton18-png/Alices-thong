import os
import subprocess
import winreg
from pathlib import Path

SETUP_EXE_NAME = "setup.exe"

YANDEX_BROWSER_PATHS = [
    os.path.expandvars(r"%USERPROFILE%\AppData\Local\Yandex\YandexBrowser\Application"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Yandex\YandexBrowser\Application"),
    os.path.expandvars(r"%ProgramFiles%\Yandex\YandexBrowser\Application"),
]

YANDEX_PROCESSES = ["yandex.exe", "browser.exe", "YandexWorking.exe", "service_update.exe", "setup.exe"]

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

YANDEX_UNINSTALL_KEYS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\YandexBrowser"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\YandexBrowser"),
    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\YandexBrowser"),
]


def find_setup_exe():
    root = Path(os.getcwd())
    candidates = [
        root / SETUP_EXE_NAME,
        root / "setup" / SETUP_EXE_NAME,
        root / "installer" / SETUP_EXE_NAME,
    ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None


def run_setup_exe(path):
    subprocess.Popen([path], shell=True)


def find_official_uninstaller():
    for hkey, key_path in YANDEX_UNINSTALL_KEYS:
        try:
            with winreg.OpenKey(hkey, key_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY) as k:
                uninstall_str, _ = winreg.QueryValueEx(k, "UninstallString")
                if uninstall_str:
                    return uninstall_str.replace('"', '')
        except:
            pass
    return None


def run_official_uninstaller():
    path = find_official_uninstaller()
    if path and os.path.exists(path.replace("\\", "").split()[0] if " " in path else path):
        try:
            subprocess.run(f'"{path}" /S', shell=True, capture_output=True, timeout=60)
            return True
        except:
            pass
    return False


def find_yandex_browser():
    for p in YANDEX_BROWSER_PATHS:
        if os.path.exists(p):
            browser_exe = os.path.join(p, "browser.exe")
            if os.path.exists(browser_exe):
                return p
    return None


def get_yandex_version():
    base = find_yandex_browser()
    if not base:
        return None
    for item in os.listdir(base):
        item_path = os.path.join(base, item)
        if os.path.isdir(item_path) and item[0].isdigit():
            return item
    return None


def kill_browser_processes():
    results = []
    for proc in YANDEX_PROCESSES:
        subprocess.run(f"taskkill /F /IM {proc} /T", shell=True, capture_output=True)
        results.append(f"Процесс {proc} остановлен")
    return results


def delete_services():
    results = []
    for svc in YANDEX_SERVICES:
        subprocess.run(f"sc stop {svc}", shell=True, capture_output=True)
        subprocess.run(f"sc delete {svc}", shell=True, capture_output=True)
        results.append(f"Служба {svc} удалена")
    return results


def delete_schtasks():
    results = []
    for task in YANDEX_SCHTASKS:
        subprocess.run(f'schtasks /delete /tn "{task}" /f', shell=True, capture_output=True)
        results.append(f"Задача {task} удалена")
    return results


def delete_registry():
    results = []
    reg_paths = [
        r"HKLM\SOFTWARE\Yandex",
        r"HKLM\SOFTWARE\Wow6432Node\Yandex",
        r"HKCU\SOFTWARE\Yandex",
        r"HKCU\SOFTWARE\AppDataLow\Yandex",
        r"HKLM\SOFTWARE\Policies\Yandex",
        r"HKCU\SOFTWARE\Policies\Yandex",
        r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\YandexBrowser",
        r"HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\YandexBrowser",
        r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\YandexBrowser",
        r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\browser.exe",
        r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\browser.exe",
    ]
    for path in reg_paths:
        subprocess.run(f'reg delete "{path}" /f', shell=True, capture_output=True)
        results.append(f"Ветка {path} удалена")
    rundel = [
        (r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "YandexBrowser"),
        (r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "YandexBrowser"),
    ]
    for hive, val in rundel:
        subprocess.run(f'reg delete "{hive}" /v "{val}" /f', shell=True, capture_output=True)
        results.append(f"Автозагрузка {val} удалена")
    return results


def delete_files_and_folders():
    results = []
    paths_to_delete = [
        os.path.expandvars(r"C:\Program Files (x86)\Yandex"),
        os.path.expandvars(r"C:\Program Files\Yandex"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Yandex"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\Yandex"),
        os.path.expandvars(r"%LocalAppData%\Yandex\YaPin"),
    ]
    for p in paths_to_delete:
        if os.path.exists(p):
            try:
                subprocess.run(f'takeown /f "{p}" /r /d y 2>nul', shell=True, capture_output=True)
                subprocess.run(f'icacls "{p}" /grant administrators:F /T 2>nul', shell=True, capture_output=True)
                subprocess.run(f'rmdir /s /q "{p}"', shell=True, capture_output=True)
                results.append(f"Папка {p} удалена")
            except Exception:
                pass

    shortcuts_to_del = [
        os.path.expandvars(r"%USERPROFILE%\Desktop\Yandex.lnk"),
        os.path.expandvars(r"%Public%\Desktop\Yandex.lnk"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Yandex.lnk"),
        os.path.expandvars(r"%ProgramData%\Microsoft\Windows\Start Menu\Programs\Yandex.lnk"),
        os.path.expandvars(r"%APPDATA%\Microsoft\Internet Explorer\Quick Launch\Yandex.lnk"),
    ]
    for s in shortcuts_to_del:
        p = os.path.expandvars(s)
        if os.path.exists(p):
            try:
                os.remove(p)
                results.append(f"Ярлык удалён")
            except Exception:
                pass
    return results


def fully_remove_browser():
    results = []

    results.append("Шаг 1: Запуск официального деинсталлятора...")
    try:
        if run_official_uninstaller():
            results.append("  Официальный деинсталлятор выполнен")
        else:
            results.append("  Официальный деинсталлятор не найден, продолжаем принудительно")
    except Exception as e:
        results.append(f"  Ошибка деинсталлятора: {e}")

    results.append("Шаг 2: Остановка процессов...")
    results.extend(kill_browser_processes())

    results.append("Шаг 3: Удаление служб...")
    results.extend(delete_services())

    results.append("Шаг 4: Удаление заданий планировщика...")
    results.extend(delete_schtasks())

    results.append("Шаг 5: Очистка реестра...")
    results.extend(delete_registry())

    results.append("Шаг 6: Удаление файлов и папок...")
    results.extend(delete_files_and_folders())

    return results
