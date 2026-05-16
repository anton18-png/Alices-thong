import os
import sys
import threading
import subprocess
import random
from pathlib import Path

import customtkinter as ctk
from launcher.core import telemetry
from launcher.core import hosts_blocker
from launcher.core import browser_manager
from launcher.core import installer as inst
from launcher.core import launcher_engine

if getattr(sys, 'frozen', False):
    LAUNCHER_DIR = Path(sys.executable).parent
else:
    LAUNCHER_DIR = Path(__file__).resolve().parent.parent

ACCENT = "#f85149"
ACCENT_HOVER = "#da3633"
BG_DARK = "#0d1117"
CARD_BG = "#161b22"
BORDER = "#30363d"
TEXT_PRIMARY = "#f0f6fc"
TEXT_SECONDARY = "#8b949e"

ctk.set_appearance_mode("dark")


class LogRedirect:
    def __init__(self, text_widget):
        self.text = text_widget
    def write(self, message):
        self.text.configure(state="normal")
        self.text.insert("end", message)
        self.text.see("end")
        self.text.configure(state="disabled")
    def flush(self):
        pass


def _make_card(parent, **kwargs):
    return ctk.CTkFrame(parent, fg_color=CARD_BG, border_color=BORDER, border_width=1, corner_radius=12, **kwargs)


def _section_title(parent, text):
    lbl = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=16, weight="bold"), text_color=ACCENT)
    lbl.pack(anchor="w", pady=(10, 5))
    return lbl


def _launch_card(parent, title, desc, color, btn_text, command):
    card = _make_card(parent)
    card.pack(fill="x", pady=(0, 12))
    top = ctk.CTkFrame(card, fg_color="transparent")
    top.pack(fill="x", padx=16, pady=(12, 0))
    dot = ctk.CTkLabel(top, text="●", font=ctk.CTkFont(size=20), text_color=color)
    dot.pack(side="left", padx=(0, 8))
    lbl = ctk.CTkLabel(top, text=title, font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT_PRIMARY)
    lbl.pack(side="left")
    if desc:
        ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY,
                      wraplength=900).pack(anchor="w", padx=42, pady=(4, 8))
    btn_frame = ctk.CTkFrame(card, fg_color="transparent")
    btn_frame.pack(fill="x", padx=16, pady=(0, 12))
    ctk.CTkButton(btn_frame, text=btn_text, command=command,
                  fg_color=color, hover_color=color,
                  corner_radius=8, height=38,
                  font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")


class AlicesThongLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Стринги Алисы — Лаунчер")
        self.geometry("1150x780")
        self.minsize(1000, 700)
        self.configure(fg_color=BG_DARK)

        self._log = None

        self._build_top_bar()
        self._build_nav()
        self._build_content_area()
        self._build_status_bar()

    # ─── TOP BAR ─────────────────────────────────────
    def _build_top_bar(self):
        self.top_bar_frame = ctk.CTkFrame(self, fg_color="#161b22", height=56, corner_radius=0)
        self.top_bar_frame.pack(fill="x")
        self.top_bar_frame.pack_propagate(False)
        c = ctk.CTkFrame(self.top_bar_frame, fg_color="transparent")
        c.pack(fill="both", padx=24, pady=8)
        ctk.CTkLabel(c, text="  Стринги Алисы",
                      font=ctk.CTkFont(size=20, weight="bold"), text_color=TEXT_PRIMARY).pack(side="left")
        ctk.CTkLabel(c, text="v1.0  Лаунчер",
                      font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(side="left", padx=(8, 0))
        self.top_bar_frame.lift()

    # ─── NAV ─────────────────────────────────────────
    def _build_nav(self):
        self.nav_frame = ctk.CTkFrame(self, fg_color="#161b22", height=48, corner_radius=0)
        self.nav_frame.pack(fill="x")
        self.nav_frame.pack_propagate(False)
        c = ctk.CTkFrame(self.nav_frame, fg_color="transparent")
        c.pack(fill="both", padx=24)
        self.nav_btns = {}
        # tabs = [("launch","Запуск"),("install","Установка"),
        #         ("telemetry","Телеметрия"),("hosts","Блокировка"),
        #         ("browser","Браузер")]
        tabs = [("launch","Запуск"),("install","Установка"),("hosts","Блокировка"),("browser","Браузер")]
        for key, label in tabs:
            btn = ctk.CTkButton(c, text=label, font=ctk.CTkFont(size=13, weight="bold"),
                                fg_color="transparent" if key != "launch" else ACCENT,
                                hover_color="#1c2333", text_color=TEXT_PRIMARY,
                                corner_radius=8, height=32,
                                command=lambda k=key: self._switch_tab(k))
            btn.pack(side="left", padx=(0, 6))
            self.nav_btns[key] = btn
        self._active_tab = "launch"

    def _switch_tab(self, key):
        if self._active_tab == key:
            return
        self.nav_btns[self._active_tab].configure(fg_color="transparent")
        self.nav_btns[key].configure(fg_color=ACCENT)
        self._active_tab = key
        for name in ["launch","install","telemetry","hosts","browser"]:
            getattr(self, f"page_{name}", None) and getattr(self, f"page_{name}").pack_forget()
        getattr(self, f"page_{key}").pack(fill="both", expand=True, padx=24, pady=16)
        getattr(self, f"page_{key}").lift()

    # ─── CONTENT ─────────────────────────────────────
    def _build_content_area(self):
        self.content = ctk.CTkFrame(self, fg_color=BG_DARK)
        self.content.pack(fill="both", expand=True)
        pages = ["launch","install","telemetry","hosts","browser"]
        for p in pages:
            setattr(self, f"page_{p}", ctk.CTkFrame(self.content, fg_color="transparent"))
        self._build_launch_page()
        self._build_install_page()
        # self._build_telemetry_page()
        self._build_hosts_page()
        self._build_browser_page()
        self.page_launch.pack(fill="both", expand=True, padx=24, pady=16)

    def _build_status_bar(self):
        self.status_bar_frame = ctk.CTkFrame(self, fg_color="#161b22", height=28, corner_radius=0)
        self.status_bar_frame.pack(fill="x", side="bottom")
        self.status_bar_frame.pack_propagate(False)
        self.status_label = ctk.CTkLabel(self.status_bar_frame, text="Готов к работе",
                                          font=ctk.CTkFont(size=11), text_color=TEXT_SECONDARY)
        self.status_label.pack(side="left", padx=16)
    def set_status(self, msg, color=TEXT_SECONDARY):
        self.status_label.configure(text=msg, text_color=color)

    def log(self, msg):
        if self._log:
            self._log.write(msg + "\n")

    # ═══════════════════════════════════════════════════
    # TAB: LAUNCH
    # ═══════════════════════════════════════════════════
    def _build_launch_page(self):
        p = self.page_launch
        scroll = ctk.CTkScrollableFrame(p, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        hero = _make_card(scroll)
        hero.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(hero, text="✨ Стринги Алисы ✨",
                      font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_PRIMARY).pack(pady=(16, 4))
        ctk.CTkLabel(hero, text="Выберите режим запуска",
                      font=ctk.CTkFont(size=13), text_color=TEXT_SECONDARY).pack(pady=(0, 16))
        self.launch_browser_path = ctk.StringVar(value=str(LAUNCHER_DIR))

        _launch_card(scroll,"Режим 1 — Без телеметрии, с синхронизацией","Службы блокируются, синхронизация работает.","#3fb950","Запустить (телеметрия выкл, синх вкл)",lambda: self._launch("sync"))
        _launch_card(scroll,"Режим 2 — Без телеметрии, без синхронизации","То же + полное отключение синхронизации.","#d29922","Запустить (телеметрия выкл, синх выкл)",lambda: self._launch("nosync"))
        _launch_card(scroll,"Режим 3 — Полная блокировка","Режим 2 + блокировка 250+ доменов в hosts.","#f85149","Запустить (полная блокировка)",lambda: self._launch("full"))
        _launch_card(scroll,"Режим 4 — Полная блокировка + инкогнито","Режим 3 + режим инкогнито.","#f85149","Запустить (полная блокировка + инкогнито)",lambda: self._launch("full_incognito"))
        _launch_card(scroll,"Режим 5 — Как Яндекс Браузер (без изменений)","Минимальные флаги, снимает блокировку hosts.","#8b949e","Запустить (без изменений)",lambda: self._launch("vanilla"))

        self.launch_log = ctk.CTkTextbox(scroll, height=100, fg_color=BG_DARK, border_color=BORDER, border_width=1,
                                          corner_radius=8, text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=12))
        self.launch_log.pack(fill="x", pady=(0, 16))

    def _browse_launch_path(self):
        path = ctk.filedialog.askdirectory(title="Папка с портативным браузером")
        if path:
            self.launch_browser_path.set(path)

    def _launch(self, mode):
        t = threading.Thread(target=self._do_launch, args=(mode,), daemon=True)
        t.start()

    def _do_launch(self, mode):
        base = self.launch_browser_path.get()
        browser_exe = launcher_engine.find_browser_exe(base)
        if not browser_exe:
            self.launch_log.insert("end", f"Не найден browser.exe в {base}\nСначала установите через вкладку Установка\n")
            return
        self.launch_log.delete("1.0", "end")
        self._log = LogRedirect(self.launch_log)
        data_dir = launcher_engine.find_data_dir(base)

        if mode == "sync":
            self.log("=== Режим 1: без телеметрии, с синхронизацией ===")
            self.log("[0] Экспорт реестра...")
            for r in launcher_engine.export_registry(): self.log(f"  {r}")
            self.log("[0b] Очистка реестра...")
            for r in launcher_engine.cleanup_registry(): self.log(f"  {r}")
            self.log("[1] Блокировка служб...")
            for r in launcher_engine.run_pre_launch(): self.log(f"  {r}")
            self.log("[2] Политики реестра...")
            for r in launcher_engine.apply_registry_policies(False): self.log(f"  {r}")
            self.log("[3] Очистка сессий...")
            for r in launcher_engine.clear_sessions(data_dir): self.log(f"  {r}")
            launcher_engine.run_browser(browser_exe, launcher_engine.BROWSER_FLAGS_SYNC)
            self.log("Браузер запущен.")
        elif mode == "nosync":
            self.log("=== Режим 2: без телеметрии, без синхронизации ===")
            self.log("[0] Экспорт реестра...")
            for r in launcher_engine.export_registry(): self.log(f"  {r}")
            self.log("[0b] Очистка реестра...")
            for r in launcher_engine.cleanup_registry(): self.log(f"  {r}")
            for r in launcher_engine.run_pre_launch(): self.log(f"  {r}")
            for r in launcher_engine.apply_registry_policies(True): self.log(f"  {r}")
            for r in launcher_engine.clear_sessions(data_dir): self.log(f"  {r}")
            launcher_engine.run_browser(browser_exe, launcher_engine.BROWSER_FLAGS_NOSYNC)
            self.log("Браузер запущен.")
        elif mode == "full":
            self.log("=== Режим 3: полная блокировка ===")
            self.log("[0] Экспорт реестра...")
            for r in launcher_engine.export_registry(): self.log(f"  {r}")
            self.log("[0b] Очистка реестра...")
            for r in launcher_engine.cleanup_registry(): self.log(f"  {r}")
            for r in launcher_engine.run_pre_launch(): self.log(f"  {r}")
            for r in launcher_engine.apply_registry_policies(True): self.log(f"  {r}")
            for r in launcher_engine.clear_sessions(data_dir): self.log(f"  {r}")
            self.log("[4] Блокировка hosts...")
            all_h = []; all_h.extend(telemetry.YANDEX_HOSTS); all_h.extend(telemetry.GOOGLE_CHROME_HOSTS); all_h.extend(telemetry.OPERA_HOSTS); all_h.extend(telemetry.MAX_HOSTS); all_h.extend(telemetry.GOSUSLUGI_HOSTS); all_h.extend(telemetry.MAILRU_HOSTS)
            try:
                hosts_blocker.add_blocks(all_h, "Полная")
                self.log(f"  Добавлено {len(all_h)} доменов")
            except Exception as e: self.log(f"  Ошибка: {e}")
            flags = launcher_engine.BROWSER_FLAGS_NOSYNC + ["--disable-features=Screenshots,AutomaticTabDiscarding,BackgroundModeEnabled,SessionRestoreAutoRestore,YandexAliceAssistant,YandexVoiceAssistant,VoiceActivation,AliceAssistant"]
            launcher_engine.run_browser(browser_exe, flags)
            self.log("Браузер запущен.")
        elif mode == "full_incognito":
            self.log("=== Режим 4: полная блокировка + инкогнито ===")
            self.log("[0] Экспорт реестра...")
            for r in launcher_engine.export_registry(): self.log(f"  {r}")
            self.log("[0b] Очистка реестра...")
            for r in launcher_engine.cleanup_registry(): self.log(f"  {r}")
            for r in launcher_engine.run_pre_launch(): self.log(f"  {r}")
            for r in launcher_engine.apply_registry_policies(True): self.log(f"  {r}")
            for r in launcher_engine.clear_sessions(data_dir): self.log(f"  {r}")
            self.log("[4] Блокировка hosts...")
            all_h = []; all_h.extend(telemetry.YANDEX_HOSTS); all_h.extend(telemetry.GOOGLE_CHROME_HOSTS); all_h.extend(telemetry.OPERA_HOSTS); all_h.extend(telemetry.MAX_HOSTS); all_h.extend(telemetry.GOSUSLUGI_HOSTS); all_h.extend(telemetry.MAILRU_HOSTS)
            try:
                hosts_blocker.add_blocks(all_h, "Полная")
                self.log(f"  Добавлено {len(all_h)} доменов")
            except Exception as e: self.log(f"  Ошибка: {e}")
            flags = launcher_engine.BROWSER_FLAGS_NOSYNC + ["--incognito", "--disable-features=Screenshots,AutomaticTabDiscarding,BackgroundModeEnabled,SessionRestoreAutoRestore,YandexAliceAssistant,YandexVoiceAssistant,VoiceActivation,AliceAssistant"]
            launcher_engine.run_browser(browser_exe, flags)
            self.log("Браузер запущен в инкогнито.")
        elif mode == "vanilla":
            self.log("=== Режим 5: как Яндекс Браузер ===")
            self.log("[1] Разблокировка hosts...")
            try:
                hosts_blocker.remove_all_blocks()
                self.log("  Блокировка снята")
            except Exception as e: self.log(f"  Ошибка: {e}")
            self.log("[2] Запуск с минимальными флагами...")
            flags = ["--disable-features=Screenshots,AutomaticTabDiscarding,BackgroundModeEnabled,SessionRestoreAutoRestore","--no-sandbox","--restore-on-startup=0"]
            launcher_engine.run_browser(browser_exe, flags)
            self.log("Браузер запущен.")

    # ═══════════════════════════════════════════════════
    # TAB: INSTALL
    # ═══════════════════════════════════════════════════
    def _build_install_page(self):
        p = self.page_install
        scroll = ctk.CTkScrollableFrame(p, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        hero = _make_card(scroll)
        hero.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(hero, text="Установка Стрингов Алисы",
                      font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_PRIMARY).pack(pady=(16, 4))
        card = _make_card(scroll)
        card.pack(fill="x", pady=(0, 12))
        _section_title(card, "Способ установки")
        bf = ctk.CTkFrame(card, fg_color="transparent")
        bf.pack(fill="x", padx=16, pady=8)
        # self.install_to_browser_btn = ctk.CTkButton(bf, text="Установить в существующий", command=self._install_to_browser, fg_color=ACCENT, hover_color=ACCENT_HOVER, corner_radius=8, height=40, width=220, font=ctk.CTkFont(size=13, weight="bold"))
        # self.install_to_browser_btn.pack(side="left", padx=(0, 10))
        self.install_portable_btn = ctk.CTkButton(bf, text="Портативная установка", command=self._install_portable, fg_color="#1f6feb", hover_color="#388bfd", corner_radius=8, height=40, width=220, font=ctk.CTkFont(size=13, weight="bold"))
        self.install_portable_btn.pack(side="left")
        self.install_path_var = ctk.StringVar(value=str(LAUNCHER_DIR))
        card3 = _make_card(scroll)
        card3.pack(fill="x")
        _section_title(card3, "Прогресс")
        self.install_progress = ctk.CTkProgressBar(card3, mode="determinate", fg_color=BG_DARK, progress_color=ACCENT, corner_radius=4)
        self.install_progress.pack(fill="x", padx=16, pady=(8, 4))
        self.install_progress.set(0)
        self.install_status = ctk.CTkLabel(card3, text="Ожидание...", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY)
        self.install_status.pack(pady=(0, 12))

    def _browse_install_path(self):
        path = ctk.filedialog.askdirectory(title="Выберите папку для установки")
        if path: self.install_path_var.set(path)

    def _install_to_browser(self):
        s = inst.find_source_browser()
        if not s: self.install_status.configure(text="Яндекс Браузер не найден!", text_color="#f85149"); return
        t = threading.Thread(target=self._do_install_to_browser, args=(s, self.install_path_var.get()), daemon=True); t.start()

    def _do_install_to_browser(self, source, dest):
        self.install_status.configure(text="Установка...", text_color="#d29922")
        def p(v): self.after(0, self.install_progress.set, v/100)
        try:
            inst.install_to_existing(source, dest, p)
            self.after(0, lambda: self.install_status.configure(text="Готово!", text_color="#3fb950"))
            self.after(0, lambda: self.install_progress.set(1))
            self.after(0, lambda d=dest: self.launch_browser_path.set(d))
        except Exception as e: self.after(0, lambda: self.install_status.configure(text=f"Ошибка: {e}", text_color="#f85149"))

    def _install_portable(self):
        s = inst.find_source_browser()
        if not s: self.install_status.configure(text="Яндекс Браузер не найден!", text_color="#f85149"); return
        t = threading.Thread(target=self._do_install_portable, args=(s, self.install_path_var.get()), daemon=True); t.start()

    def _do_install_portable(self, source, dest):
        self.install_status.configure(text="Портативная установка...", text_color="#d29922")
        def p(v): self.after(0, self.install_progress.set, v/100)
        try:
            inst.install_portable(source, dest, p)
            self.after(0, lambda: self.install_status.configure(text="Готово!", text_color="#3fb950"))
            self.after(0, lambda: self.install_progress.set(1))
            self.after(0, lambda d=dest: self.launch_browser_path.set(d))
        except Exception as e: self.after(0, lambda: self.install_status.configure(text=f"Ошибка: {e}", text_color="#f85149"))

    # ═══════════════════════════════════════════════════
    # TAB: TELEMETRY
    # ═══════════════════════════════════════════════════
    # def _build_telemetry_page(self):
    #     p = self.page_telemetry
    #     scroll = ctk.CTkScrollableFrame(p, fg_color="transparent")
    #     scroll.pack(fill="both", expand=True)
    #     hero = _make_card(scroll)
    #     hero.pack(fill="x", pady=(0, 16))
    #     ctk.CTkLabel(hero, text="Очистка телеметрии",
    #                   font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_PRIMARY).pack(pady=(16, 4))
    #     path_card = _make_card(scroll)
    #     path_card.pack(fill="x", pady=(0, 12))
    #     _section_title(path_card, "Путь к браузеру")
    #     pf = ctk.CTkFrame(path_card, fg_color="transparent")
    #     pf.pack(fill="x", padx=16, pady=8)
    #     self.telemetry_browser_path = ctk.StringVar(value=os.path.join(os.getcwd()))
    #     ctk.CTkEntry(pf, textvariable=self.telemetry_browser_path, fg_color=BG_DARK, border_color=BORDER, corner_radius=6).pack(side="left", fill="x", expand=True, padx=(0, 8))
    #     ctk.CTkButton(pf, text="Обзор", command=lambda: self._browse_telemetry_path(), fg_color="#1c2333", hover_color=BORDER, corner_radius=6, width=80).pack(side="right")

    #     self.telemetry_yandex_checkboxes = {}
    #     self.telemetry_chrome_checkboxes = {}
    #     self.telemetry_opera_checkboxes = {}

    #     y_card = _make_card(scroll)
    #     y_card.pack(fill="x", pady=(0, 12))
    #     _section_title(y_card, "Яндекс Браузер")
    #     yandex_items = [
    #         ("telemetry","Телеметрия (всегда)",True),
    #         ("notifications","Уведомления",False),
    #         ("sync","Синхронизация",False),
    #         ("alice","Алиса",False),
    #         ("neuro","Нейросети",False),
    #         ("widgets","Виджеты",False),
    #         ("visual","Иконки пуска",False),
    #         ("sig","Подписи .sig",False),
    #         ("easylist","EasyList",False),
    #         # ("dxvk","DirectX/Vulkan",False),
    #         # ("service_bins","Служебные .exe/.dll",False),
    #         # ("brand_config","Бренд-конфиги",False),
    #         # ("browser_paks","100/200% паки",False),
    #         # ("v8_snapshot","V8 снепшот",False),
    #         ("wallpapers","Обои браузера",False),
    #         # ("morphology","Морфология",False),
    #         # ("safebrowsing","Safe Browsing",False),
    #         # ("logos","Логотипы/иконки",False),
    #         # ("ui_config","UI конфиги",False),
    #         # ("web_app_config","Конфиги веб-приложений",False),
    #         # ("ntp_cache","Кэш новой вкладки",False),
    #         # ("extensions_data","Данные расширений",False),
    #         # ("locales_extra","Доп. языковые паки",False),
    #     ]
    #     g = ctk.CTkFrame(y_card, fg_color="transparent")
    #     g.pack(fill="x", padx=16, pady=8)
    #     for i,(key,label,default) in enumerate(yandex_items):
    #         var = ctk.BooleanVar(value=default)
    #         cb = ctk.CTkCheckBox(g, text=label, variable=var, text_color=TEXT_PRIMARY, corner_radius=4, fg_color=ACCENT, hover_color=ACCENT_HOVER)
    #         cb.grid(row=i//2, column=i%2, sticky="w", padx=4, pady=3)
    #         if key=="telemetry": cb.configure(state="disabled")
    #         self.telemetry_yandex_checkboxes[key]=var

    #     c_card = _make_card(scroll)
    #     c_card.pack(fill="x", pady=(0, 12))
    #     _section_title(c_card, "Google Chrome")
    #     g2 = ctk.CTkFrame(c_card, fg_color="transparent")
    #     g2.pack(fill="x", padx=16, pady=8)
    #     for i,(key,label) in enumerate([("kss","KSS"),("chrome_wer","Chrome WER"),("elevation","Elevation"),("software_reporter","Software Reporter"),("swiftshader","SwiftShader")]):
    #         var = ctk.BooleanVar(value=True)
    #         ctk.CTkCheckBox(g2, text=label, variable=var, text_color=TEXT_PRIMARY, corner_radius=4, fg_color="#e2b714", hover_color="#d4a50d").grid(row=0, column=i, sticky="w", padx=4, pady=3)
    #         self.telemetry_chrome_checkboxes[key]=var

    #     o_card = _make_card(scroll)
    #     o_card.pack(fill="x", pady=(0, 12))
    #     _section_title(o_card, "Opera")
    #     g3 = ctk.CTkFrame(o_card, fg_color="transparent")
    #     g3.pack(fill="x", padx=16, pady=8)
    #     for i,(key,label) in enumerate([("autoupdate","Автообновление"),("crashreporter","Crash Reporter"),("browser_wer","Browser WER"),("logs","Opera Logs")]):
    #         var = ctk.BooleanVar(value=True)
    #         ctk.CTkCheckBox(g3, text=label, variable=var, text_color=TEXT_PRIMARY, corner_radius=4, fg_color="#cc0000", hover_color="#990000").grid(row=0, column=i, sticky="w", padx=4, pady=3)
    #         self.telemetry_opera_checkboxes[key]=var

    #     s_card = _make_card(scroll)
    #     s_card.pack(fill="x", pady=(0, 12))
    #     _section_title(s_card, "Системные")
    #     g4 = ctk.CTkFrame(s_card, fg_color="transparent")
    #     g4.pack(fill="x", padx=16, pady=8)
    #     self.telemetry_services_var=ctk.BooleanVar(value=True); self.telemetry_schtasks_var=ctk.BooleanVar(value=True); self.telemetry_registry_var=ctk.BooleanVar(value=True)
    #     ctk.CTkCheckBox(g4, text="Службы", variable=self.telemetry_services_var, text_color=TEXT_PRIMARY, corner_radius=4, fg_color=ACCENT, hover_color=ACCENT_HOVER).grid(row=0,column=0,sticky="w",padx=4,pady=3)
    #     ctk.CTkCheckBox(g4, text="Планировщик", variable=self.telemetry_schtasks_var, text_color=TEXT_PRIMARY, corner_radius=4, fg_color=ACCENT, hover_color=ACCENT_HOVER).grid(row=0,column=1,sticky="w",padx=4,pady=3)
    #     ctk.CTkCheckBox(g4, text="Политики реестра", variable=self.telemetry_registry_var, text_color=TEXT_PRIMARY, corner_radius=4, fg_color=ACCENT, hover_color=ACCENT_HOVER).grid(row=0,column=2,sticky="w",padx=4,pady=3)

    #     btn_card = _make_card(scroll)
    #     btn_card.pack(fill="x")
    #     ctk.CTkButton(btn_card, text="Запустить очистку", command=self._run_telemetry_cleanup, fg_color=ACCENT, hover_color=ACCENT_HOVER, corner_radius=8, height=42, font=ctk.CTkFont(size=14,weight="bold")).pack(pady=16)
    #     self.telemetry_progress = ctk.CTkProgressBar(btn_card, mode="determinate", fg_color=BG_DARK, progress_color=ACCENT, corner_radius=4)
    #     self.telemetry_progress.pack(fill="x", padx=16, pady=(0, 8))
    #     self.telemetry_progress.set(0)
    #     self.telemetry_result = ctk.CTkTextbox(btn_card, height=100, fg_color=BG_DARK, border_color=BORDER, border_width=1, corner_radius=8, text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=12))
    #     self.telemetry_result.pack(fill="x", padx=16, pady=(0, 16))

    # def _browse_telemetry_path(self):
    #     path = ctk.filedialog.askdirectory(title="Выберите папку браузера")
    #     if path: self.telemetry_browser_path.set(path)

    # def _run_telemetry_cleanup(self):
    #     t = threading.Thread(target=self._do_telemetry_cleanup, daemon=True); t.start()

    # def _do_telemetry_cleanup(self):
    #     base = self.telemetry_browser_path.get()
    #     bdir = telemetry.find_browser_version_dir(base)
    #     if not bdir:
    #         self.after(0, lambda: self.telemetry_result.insert("end", f"Не найдено в {base}\n")); return
    #     self.after(0, lambda: self.telemetry_result.delete("1.0","end"))
    #     self._log = LogRedirect(self.telemetry_result)
    #     bdir = str(bdir)
    #     for r in telemetry.remove_yandex_telemetry(bdir): self.log(f"  [Y] {r}")
    #     ym = {k: telemetry.YANDEX_OPTIONAL[k] for k in telemetry.YANDEX_OPTIONAL}
    #     for k in [k for k,v in self.telemetry_yandex_checkboxes.items() if v.get()]:
    #         if k in ym:
    #             for m in telemetry.remove_yandex_optional(bdir, ym[k]): self.log(f"  [Y] {m}")
    #     if any(v.get() for v in self.telemetry_chrome_checkboxes.values()):
    #         self.log("--- Chrome ---")
    #         for m in telemetry.remove_google_chrome_telemetry(bdir): self.log(f"  [C] {m}")
    #     if any(v.get() for v in self.telemetry_opera_checkboxes.values()):
    #         self.log("--- Opera ---")
    #         for m in telemetry.remove_opera_telemetry(bdir): self.log(f"  [O] {m}")
    #     for m in telemetry.cleanup_yandex_backups(bdir): self.log(f"  [*] {m}")
    #     if self.telemetry_services_var.get():
    #         self.log("--- Службы ---")
    #         for m in telemetry.stop_and_delete_services(): self.log(f"  [S] {m}")
    #     if self.telemetry_schtasks_var.get():
    #         self.log("--- Планировщик ---")
    #         for m in telemetry.delete_schtasks(): self.log(f"  [T] {m}")
    #     if self.telemetry_registry_var.get():
    #         self.log("--- Политики ---")
    #         for m in telemetry.apply_registry_policies(): self.log(f"  [R] {m}")
    #     self.log("Очистка завершена!")

    # ═══════════════════════════════════════════════════
    # TAB: HOSTS
    # ═══════════════════════════════════════════════════
    def _build_hosts_page(self):
        p = self.page_hosts
        scroll = ctk.CTkScrollableFrame(p, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        hero = _make_card(scroll)
        hero.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(hero, text="Блокировка через hosts",
                      font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_PRIMARY).pack(pady=(16, 4))
        card = _make_card(scroll)
        card.pack(fill="x", pady=(0, 12))
        _section_title(card, "Выберите")
        g = ctk.CTkFrame(card, fg_color="transparent")
        g.pack(fill="x", padx=16, pady=8)
        self.hosts_yandex_var=ctk.BooleanVar(value=True); self.hosts_chrome_var=ctk.BooleanVar(value=False); self.hosts_opera_var=ctk.BooleanVar(value=True); self.hosts_max_var=ctk.BooleanVar(value=True); self.hosts_gosuslugi_var=ctk.BooleanVar(value=True); self.hosts_mailru_var=ctk.BooleanVar(value=False)
        for i,(t,v) in enumerate([("Яндекс",self.hosts_yandex_var),("Google",self.hosts_chrome_var),("Opera",self.hosts_opera_var),("MAX",self.hosts_max_var),("Госуслуги",self.hosts_gosuslugi_var),("Mail.ru",self.hosts_mailru_var)]):
            ctk.CTkCheckBox(g,text=t,variable=v,text_color=TEXT_PRIMARY,corner_radius=4,fg_color=ACCENT,hover_color=ACCENT_HOVER).grid(row=i,column=0,sticky="w",padx=4,pady=4)
        btn_card = _make_card(scroll)
        btn_card.pack(fill="x")
        bf = ctk.CTkFrame(btn_card, fg_color="transparent")
        bf.pack(pady=16)
        ctk.CTkButton(bf,text="Применить",command=self._apply_hosts_block,fg_color=ACCENT,hover_color=ACCENT_HOVER,corner_radius=8,height=38,font=ctk.CTkFont(size=13,weight="bold")).pack(side="left",padx=4)
        ctk.CTkButton(bf,text="Снять",command=self._remove_hosts_block,fg_color="#da3633",hover_color="#f85149",corner_radius=8,height=38,font=ctk.CTkFont(size=13,weight="bold")).pack(side="left",padx=4)
        ctk.CTkButton(bf,text="Восстановить hosts",command=self._restore_hosts,fg_color="#1c2333",hover_color=BORDER,corner_radius=8,height=38,font=ctk.CTkFont(size=13)).pack(side="left",padx=4)
        self.hosts_status = ctk.CTkLabel(btn_card, text="", font=ctk.CTkFont(size=12))
        self.hosts_status.pack(pady=(0, 4))

    def _get_selected_hosts(self):
        e,l=[],[]
        if self.hosts_yandex_var.get(): e.extend(telemetry.YANDEX_HOSTS);l.append("Ya")
        if self.hosts_chrome_var.get(): e.extend(telemetry.GOOGLE_CHROME_HOSTS);l.append("Ch")
        if self.hosts_opera_var.get(): e.extend(telemetry.OPERA_HOSTS);l.append("Op")
        if self.hosts_max_var.get(): e.extend(telemetry.MAX_HOSTS);l.append("M")
        if self.hosts_gosuslugi_var.get(): e.extend(telemetry.GOSUSLUGI_HOSTS);l.append("G")
        if self.hosts_mailru_var.get(): e.extend(telemetry.MAILRU_HOSTS);l.append("Mr")
        return e,",".join(l)

    def _apply_hosts_block(self):
        t = threading.Thread(target=self._do_apply_hosts,daemon=True); t.start()
    def _do_apply_hosts(self):
        e,l=self._get_selected_hosts()
        if not e: self.after(0,lambda:self.hosts_status.configure(text="Ничего не выбрано!",text_color="#f85149")); return
        try:
            hosts_blocker.add_blocks(e,l)
            self.after(0,lambda:self.hosts_status.configure(text=f"Блокировка ({len(e)} доменов)",text_color="#3fb950"))
        except Exception as ex: self.after(0,lambda:self.hosts_status.configure(text=f"Ошибка: {ex}",text_color="#f85149"))
    def _remove_hosts_block(self):
        try: hosts_blocker.remove_all_blocks(); self.hosts_status.configure(text="Блокировка снята",text_color="#3fb950")
        except Exception as ex: self.hosts_status.configure(text=f"Ошибка: {ex}",text_color="#f85149")
    def _restore_hosts(self):
        try:
            if hosts_blocker.restore_from_backup(): self.hosts_status.configure(text="hosts восстановлен",text_color="#3fb950")
            else: self.hosts_status.configure(text="Бекап не найден",text_color="#d29922")
        except Exception as ex: self.hosts_status.configure(text=f"Ошибка: {ex}",text_color="#f85149")

    # ═══════════════════════════════════════════════════
    # TAB: BROWSER
    # ═══════════════════════════════════════════════════
    def _build_browser_page(self):
        p = self.page_browser
        scroll = ctk.CTkScrollableFrame(p, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        hero = _make_card(scroll)
        hero.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(hero, text="Управление браузером",
                      font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_PRIMARY).pack(pady=(16, 4))
        info_card = _make_card(scroll)
        info_card.pack(fill="x", pady=(0, 12))
        self.browser_info = ctk.CTkLabel(info_card, text="", font=ctk.CTkFont(size=13), text_color=TEXT_PRIMARY)
        self.browser_info.pack(padx=16, pady=16)
        self._update_browser_info()
        setup_card = _make_card(scroll)
        setup_card.pack(fill="x", pady=(0, 12))
        _section_title(setup_card, "Установка")
        bf = ctk.CTkFrame(setup_card, fg_color="transparent")
        bf.pack(padx=16, pady=12)
        # self.setup_btn = ctk.CTkButton(bf, text="Запустить setup.exe", command=self._run_setup, fg_color=ACCENT, hover_color=ACCENT_HOVER, corner_radius=8, height=40, width=200, font=ctk.CTkFont(size=13, weight="bold"))
        # self.setup_btn.pack(side="left", padx=(0, 10))
        self.download_btn = ctk.CTkButton(bf, text="Скачать с browser.yandex.ru", command=self._open_download_page, fg_color="#1f6feb", hover_color="#388bfd", corner_radius=8, height=40, width=220, font=ctk.CTkFont(size=13, weight="bold"))
        self.download_btn.pack(side="left")
        del_card = _make_card(scroll)
        del_card.pack(fill="x", pady=(0, 12))
        _section_title(del_card, "Удаление")
        ctk.CTkLabel(del_card, text="Сначала официальный деинсталлятор, затем принудительно.", font=ctk.CTkFont(size=12), text_color=TEXT_SECONDARY).pack(anchor="w", padx=16, pady=(0, 8))
        self.delete_btn = ctk.CTkButton(del_card, text="Удалить Яндекс Браузер", command=self._delete_browser, fg_color="#da3633", hover_color="#f85149", corner_radius=8, height=40, font=ctk.CTkFont(size=13, weight="bold"))
        self.delete_btn.pack(padx=16, pady=(0, 12))
        log_card = _make_card(scroll)
        log_card.pack(fill="x")
        _section_title(log_card, "Лог")
        self.browser_progress = ctk.CTkProgressBar(log_card, mode="determinate", fg_color=BG_DARK, progress_color=ACCENT, corner_radius=4)
        self.browser_progress.pack(fill="x", padx=16, pady=(8, 4))
        self.browser_progress.set(0)
        self.browser_status = ctk.CTkLabel(log_card, text="", font=ctk.CTkFont(size=12))
        self.browser_status.pack()
        self.browser_log = ctk.CTkTextbox(log_card, height=100, fg_color=BG_DARK, border_color=BORDER, border_width=1, corner_radius=8, text_color=TEXT_PRIMARY, font=ctk.CTkFont(size=12))
        self.browser_log.pack(fill="x", padx=16, pady=(0, 16))

    def _update_browser_info(self):
        base = browser_manager.find_yandex_browser()
        if base:
            ver = browser_manager.get_yandex_version()
            self.browser_info.configure(text=f"Яндекс Браузер найден: {base}" + (f"\n   Версия: {ver}" if ver else ""), text_color="#3fb950")
        else:
            self.browser_info.configure(text="Яндекс Браузер не установлен", text_color="#d29922")

    def _run_setup(self):
        p = browser_manager.find_setup_exe()
        if not p: self.browser_status.configure(text="setup.exe не найден", text_color="#f85149"); return
        self.browser_status.configure(text=f"Запуск...", text_color="#3fb950"); browser_manager.run_setup_exe(p)

    def _open_download_page(self):
        import webbrowser; webbrowser.open("https://browser.yandex.ru/")

    def _delete_browser(self):
        t = threading.Thread(target=self._do_delete, daemon=True); t.start()

    def _do_delete(self):
        self.delete_btn.configure(state="disabled")
        self.browser_status.configure(text="Удаление...", text_color="#d29922")
        self._log = LogRedirect(self.browser_log)
        self.browser_log.delete("1.0","end")
        try:
            for r in browser_manager.fully_remove_browser(): self.log(r)
            self.after(0, lambda: self.browser_status.configure(text="Удалён!", text_color="#3fb950"))
            self.after(0, self._update_browser_info)
        except Exception as ex: self.after(0, lambda: self.browser_status.configure(text=f"Ошибка: {ex}", text_color="#f85149"))
        finally: self.after(0, lambda: self.delete_btn.configure(state="normal"))