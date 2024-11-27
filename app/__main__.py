from . import db, gui, setup_logger

logger = setup_logger(__name__)

if __name__ == "__main__":
    db.database.close()
    root = gui.tk.Tk()
    gui.MainApplication(root)
    root.mainloop()
