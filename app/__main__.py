from . import setup_logger
from app.gui.MainApplication import MainApplication


logger = setup_logger(__name__)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
