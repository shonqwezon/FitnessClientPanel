from app.gui.mainApplication import MainApplication
from . import db, gui, setup_logger


logger = setup_logger(__name__)


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
    db.database.close()
