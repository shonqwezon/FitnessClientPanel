from . import gui, setup_logger

logger = setup_logger(__name__)

if __name__ == "__main__":
    root = gui.tk.Tk()
    gui.MainApplication(root)
    root.mainloop()
