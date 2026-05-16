import os
import sys
import shutil
import subprocess
from pathlib import Path

YANDEX_SOURCE = os.path.expandvars(
    r"%USERPROFILE%\AppData\Local\Yandex\YandexBrowser\Application"
)

if getattr(sys, 'frozen', False):
    LAUNCHER_ROOT = Path(sys.executable).parent
else:
    LAUNCHER_ROOT = Path(__file__).resolve().parent.parent.parent


def _copy_launcher_files(dest_root):
    return None
    # dest = Path(dest_root)
    # for name in ["AlicesThong.exe", "portapp.json"]:
    #     src = LAUNCHER_ROOT / name
    #     if src.exists():
    #         shutil.copy2(str(src), str(dest / name))


def _rename_browser_exe(app_dir):
    browser_exe = Path(app_dir) / "browser.exe"
    chrome_exe = Path(app_dir) / "chrome.exe"
    if browser_exe.exists() and not chrome_exe.exists():
        browser_exe.rename(chrome_exe)


def find_source_browser():
    if os.path.exists(YANDEX_SOURCE):
        browser_exe = os.path.join(YANDEX_SOURCE, "browser.exe")
        if os.path.exists(browser_exe):
            return YANDEX_SOURCE
    return None


def install_portable(source_path, dest_path, progress_callback=None):
    dest = Path(dest_path)
    app_dir = dest / "app"
    data_dir = dest / "data"

    app_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    total_files = 0
    for root, dirs, files in os.walk(source_path):
        for f in files:
            total_files += 1

    copied = 0
    for root, dirs, files in os.walk(source_path):
        rel = Path(root).relative_to(source_path)
        target = app_dir / rel
        target.mkdir(parents=True, exist_ok=True)
        for f in files:
            src_file = Path(root) / f
            dst_file = target / f
            try:
                shutil.copy2(str(src_file), str(dst_file))
            except:
                pass
            copied += 1
            if progress_callback and total_files > 0:
                progress_callback(int(copied * 100 / total_files))

    _rename_browser_exe(app_dir)
    _copy_launcher_files(dest)

    return str(app_dir)


def install_to_existing(source_path, browser_path, progress_callback=None):
    dest = Path(browser_path)
    app_dir = dest / "app"

    app_dir.mkdir(parents=True, exist_ok=True)

    total_files = 0
    for root, dirs, files in os.walk(source_path):
        for f in files:
            total_files += 1

    copied = 0
    for root, dirs, files in os.walk(source_path):
        rel = Path(root).relative_to(source_path)
        target = app_dir / rel
        target.mkdir(parents=True, exist_ok=True)
        for f in files:
            src_file = Path(root) / f
            dst_file = target / f
            try:
                shutil.copy2(str(src_file), str(dst_file))
            except:
                pass
            copied += 1
            if progress_callback and total_files > 0:
                progress_callback(int(copied * 100 / total_files))

    _rename_browser_exe(app_dir)
    _copy_launcher_files(dest)

    return str(app_dir)


def install_strings_to_browser(source_path, target_browser_dir, progress_callback=None):
    app_dir = Path(target_browser_dir) / "app"
    app_dir.mkdir(parents=True, exist_ok=True)

    total = sum(len(files) for _, _, files in os.walk(source_path))
    copied = 0

    for root, dirs, files in os.walk(source_path):
        rel = Path(root).relative_to(source_path)
        target = app_dir / rel
        target.mkdir(parents=True, exist_ok=True)
        for f in files:
            src = Path(root) / f
            dst = target / f
            try:
                shutil.copy2(str(src), str(dst))
            except:
                pass
            copied += 1
            if progress_callback and total > 0:
                progress_callback(int(copied * 100 / total))

    _rename_browser_exe(app_dir)
    _copy_launcher_files(Path(target_browser_dir))

    return str(app_dir)
