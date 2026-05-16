import os
import subprocess
import shutil
from pathlib import Path

HOSTS_PATH = os.environ.get(
    "SystemRoot", "C:\\Windows"
) + "\\System32\\drivers\\etc\\hosts"

HOSTS_BACKUP = HOSTS_PATH + ".backup_alices"

MARKER_START = "### ALICES BLOCK START"
MARKER_END = "### ALICES BLOCK END"


def _hosts_backup_exists():
    return os.path.exists(HOSTS_BACKUP)


def create_backup():
    if not _hosts_backup_exists():
        shutil.copy2(HOSTS_PATH, HOSTS_BACKUP)
        return True
    return False


def restore_from_backup():
    if _hosts_backup_exists():
        shutil.copy2(HOSTS_BACKUP, HOSTS_PATH)
        return True
    return False


def remove_old_blocks():
    if not os.path.exists(HOSTS_PATH):
        return False
    with open(HOSTS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    inside_block = False
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if MARKER_START in stripped or stripped.startswith("### ALICES BLOCK START"):
            inside_block = True
            continue
        if MARKER_END in stripped or stripped.startswith("### ALICES BLOCK END"):
            inside_block = False
            continue
        if not inside_block:
            new_lines.append(line)
    with open(HOSTS_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    return True


def get_current_blocks():
    if not os.path.exists(HOSTS_PATH):
        return []
    with open(HOSTS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    inside = False
    blocks = []
    for line in lines:
        stripped = line.strip()
        if MARKER_START in stripped:
            inside = True
            continue
        if MARKER_END in stripped:
            break
        if inside and stripped and not stripped.startswith("#"):
            parts = stripped.split()
            if len(parts) >= 2:
                blocks.append(parts[1])
    return blocks


def is_blocked():
    if not os.path.exists(HOSTS_PATH):
        return False
    with open(HOSTS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    return MARKER_START in content


def add_blocks(host_entries, label="Блокировка"):
    create_backup()
    remove_old_blocks()
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HOSTS_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n{MARKER_START} - {now}\n")
        f.write(f"# {label}\n")
        for entry in host_entries:
            f.write(entry + "\n")
        f.write(f"{MARKER_END}\n")
    flush_dns()


def remove_all_blocks():
    remove_old_blocks()
    flush_dns()


def flush_dns():
    subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
