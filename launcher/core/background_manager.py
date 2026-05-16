import os
import random
from pathlib import Path
from PIL import Image
import customtkinter as ctk

BACKGROUNDS_DIR = Path(__file__).resolve().parent.parent.parent / "backgrounds"


class BackgroundManager:
    def __init__(self):
        self._cache = {}

    def get_dark_wallpapers(self):
        path = BACKGROUNDS_DIR / "dark"
        if not path.exists():
            return []
        return sorted(
            [f for f in os.listdir(path)
             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        )

    def get_light_wallpapers(self):
        path = BACKGROUNDS_DIR / "light"
        if not path.exists():
            return []
        return sorted(
            [f for f in os.listdir(path)
             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        )

    def get_random_dark(self):
        files = self.get_dark_wallpapers()
        return random.choice(files) if files else None

    def get_random_light(self):
        files = self.get_light_wallpapers()
        return random.choice(files) if files else None

    def get_ctk_image(self, theme, filename, size=(240, 140)):
        key = (theme, filename, size)
        if key in self._cache:
            return self._cache[key]
        path = BACKGROUNDS_DIR / theme / filename
        if not path.exists():
            return None
        img = Image.open(path)
        img.thumbnail(size, Image.LANCZOS)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        self._cache[key] = ctk_img
        return ctk_img

    def get_full_ctk_image(self, theme, filename, display_size=(800, 450)):
        path = BACKGROUNDS_DIR / theme / filename
        if not path.exists():
            return None
        img = Image.open(path)
        img.thumbnail(display_size, Image.LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
