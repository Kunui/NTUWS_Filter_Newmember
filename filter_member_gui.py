import os
os.chdir(os.path.dirname(__file__))
import tkinter as tk
from tkinter import filedialog as fdl
from filter_member import admember as adm

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
        self.welcome_questionaire_list_entry = tk.Entry(width = 40)
        self.total_member_list_label_enrty = tk.Entry(width = 40)
        self.quarantine_list_label_entry = tk.Entry(width = 40)
        self.win.mainloop()

    def select_file(self, filetype: str):
        if filetype == "welcome_questionaire_list":
            self.welcome_questionaire_list_filepath = fdl.askopenfilename()
            self.welcome_questionaire_list_entry.delete(0, tk.END)
            self.welcome_questionaire_list_entry.insert(0, self.welcome_questionaire_list_filepath)
        if filetype == "total_member_list":

        if filetype == "quarantine_list":

filmem_gui()