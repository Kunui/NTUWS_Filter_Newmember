import os
os.chdir(os.path.dirname(__file__))
import tkinter as tk
from tkinter import filedialog as fdl
import filter_member as fm

class filmem_gui():
    def __init__(self) -> None:
        self.win = tk.Tk()
        self.win.geometry("550x500")