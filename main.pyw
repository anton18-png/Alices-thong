import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from launcher.ui import AlicesThongLauncher


def main():
    app = AlicesThongLauncher()
    app.mainloop()


if __name__ == "__main__":
    main()
