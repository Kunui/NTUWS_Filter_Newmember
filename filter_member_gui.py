import os
os.chdir(os.path.dirname(__file__))
import tkinter as tk
from tkinter import filedialog as fdl
import filter_member as fm

class filmem_gui():
    def __init__(self) -> None:
        self.win = tk.Tk()
        self.win.geometry("550x500")
        self.win.title("選擇開啟檔案")

        #Lables
        self.welcome_questionaire_list_label = tk.Label(text = "歡迎問卷名單")
        self.total_member_list_label = tk.Label(text = "一般會員名單")
        self.quarantine_list_label = tk.Label(text = "隔離區名單")
        
        #Entries
        self.welcome_questionaire_list_entry = tk.Entry()
        self.total_member_list_label_enrty = tk.Entry()
        self.quarantine_list_label_entry = tk.Entry()
        self.win.mainloop()

    '''def select_file(self, filetype: str):
        if filetype == "welcome_questionaire_list":

        if filetype == "total_member_list":

        if filetype == "quarantine_list":'''

filmem_gui()