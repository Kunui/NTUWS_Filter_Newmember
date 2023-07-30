import tkinter as tk
import pandas as pd
from tkinter import filedialog as fdl
from filtmem.filter_member import admember as adm
#from filter_member import admember as adm

class filmem_gui(tk.Tk):
    def __init__(self) -> None:
        
        super().__init__()
        self.geometry("550x500")
        self.title("選擇開啟的檔案")

        #Lables
        self.welcome_questionaire_list_label = tk.Label(text = "歡迎問卷名單")
        self.total_member_list_label = tk.Label(text = "一般會員名單")
        self.quarantine_list_label = tk.Label(text = "隔離區名單")
        self.samples_date_label = tk.Label(text = "樣本日期")
        
        #Entries
        self.welcome_questionaire_list_entry = tk.Entry(width = 40)
        self.total_member_list_enrty = tk.Entry(width = 40)
        self.quarantine_list_entry = tk.Entry(width = 40)
        self.samples_date_entry = tk.Entry(width = 5)

        #Buttons
        self.welcome_questionaire_list_button = tk.Button(
            self,
            text = "選擇檔案",
            height = 1,
            command = lambda: self.select_file(filetype = "welcome_questionaire_list")
        )
        self.total_member_list_button = tk.Button(
            self,
            text = "選擇檔案",
            height = 1,
            command = lambda: self.select_file(filetype = "total_member_list")
        )
        self.quarantine_list_button = tk.Button(
            self,
            text = "選擇檔案",
            height = 1,
            command = lambda: self.select_file(filetype = "quarantine_list")
        )
        
        self.duplicate_samples_var = tk.IntVar(self, value = 0)
        self.duplicate_samples_button = tk.Checkbutton(
            self,
            text = "重複樣本",
            height = 1,
            variable = self.duplicate_samples_var,
            onvalue = 1,
            offvalue = 0,
            command = self.duplicate_samples_examination
        )
        self.problematic_samples_var =  tk.IntVar(self, value =0)
        self.problematic_samples_button = tk.Checkbutton(
            self,
            text = "問題樣本",
            height = 1,
            variable = self.problematic_samples_var,
            onvalue = 1,
            offvalue = 0,
            command = self.problematic_samples_examination
        )
        self.successful_samples_var = tk.IntVar(self, value = 0)
        self.successful_samples_button = tk.Checkbutton(
            self,
            text = "成功樣本",
            height = 1,
            variable = self.successful_samples_var,
            onvalue = 1,
            offvalue = 0,
            command = self.successful_samples_examination
        )
        
        self.execute_button = tk.Button(
            self,
            text = "OK",
            height = 1,
            command = self.execute
        )
        
        #gridding
        self.welcome_questionaire_list_label.grid(
            row = 0, column = 0, columnspan = 5,padx=10, ipadx=5, sticky = "w"
        )
        self.welcome_questionaire_list_entry.grid(
            row = 1, column = 0, columnspan = 4, padx=10, ipadx=5
        )
        self.welcome_questionaire_list_button.grid(
            row = 1, column = 4, padx=10, ipadx=5
        )
        self.total_member_list_label.grid(
            row = 2, column = 0, columnspan = 5,padx=10, ipadx=5, sticky = "w"
        )
        self.total_member_list_enrty.grid(
            row = 3, column = 0, columnspan = 4, padx=10, ipadx=5
        )
        self.total_member_list_button.grid(
            row = 3, column = 4, padx=10, ipadx=5
        )
        self.quarantine_list_label.grid(
            row = 4, column = 0, columnspan = 5,padx=10, ipadx=5, sticky = "w"
        )
        self.quarantine_list_entry.grid(
            row = 5, column = 0, columnspan = 4, padx=10, ipadx=5
        )
        self.quarantine_list_button.grid(
            row = 5, column = 4, padx=10, ipadx=5
        )
        self.duplicate_samples_button.grid(
            row = 6, column = 0, padx=10, ipadx=5
        )
        self.problematic_samples_button.grid(
            row = 6, column = 1, padx=10, ipadx=5
        )
        self.successful_samples_button.grid(
            row = 6, column = 2, padx=10, ipadx=5
        )
        self.samples_date_label.grid(
            row = 7, column = 0,padx=10, ipadx=5, sticky = "E"
        )
        self.samples_date_entry.grid(
            row = 7, column = 1, padx=10, ipadx=5, sticky = "w"
        )
        self.execute_button.grid(
            row = 8, column = 3,  padx=10, ipadx=5
        )

    def select_file(self, filetype: str):
        if filetype == "welcome_questionaire_list":
            self.welcome_questionaire_list_filepath = fdl.askopenfilename()
            self.welcome_questionaire_list_entry.delete(0, tk.END)
            self.welcome_questionaire_list_entry.insert(0, self.welcome_questionaire_list_filepath)
        if filetype == "total_member_list":
            self.total_member_list_filepath = fdl.askopenfilename()
            self.total_member_list_enrty.delete(0, tk.END)
            self.total_member_list_enrty.insert(0, self.total_member_list_filepath)
        if filetype == "quarantine_list":
            self.quarantine_list_filepath = fdl.askopenfilename()
            self.quarantine_list_entry.delete(0, tk.END)
            self.quarantine_list_entry.insert(0, self.quarantine_list_filepath)

    def samples_date(self):
        samples_date_numbers = self.samples_date_entry.get()
        return samples_date_numbers

    def added_members(self):
        samples = adm(
            welqmlist = self.welcome_questionaire_list_filepath,
            ttmlist = self.total_member_list_filepath,
            qtlist = self.quarantine_list_filepath
        )
        self.welcome_questionaire_samples,  self.total_member_samples = samples.get_filter()
        return samples
    
    def duplicate_samples_examination(self):
        self.duplicate_samples_var.set(self.duplicate_samples_var.get())

    def problematic_samples_examination(self):
        self.problematic_samples_var.set(self.problematic_samples_var.get())

    def successful_samples_examination(self):
        self.successful_samples_var.set(self.successful_samples_var.get())
    
    def export_examination(self, outputname: str):
        return f'{self.samples_date()}{outputname}.xlsx'
        
    
    def execute(self):
        samples = self.added_members()
        
        if self.duplicate_samples_var.get() == 1:
            duplicate_samples_path = self.export_examination(
                outputname = "重複樣本"
            )
            self.duplicate_samples = samples.duplicate_number(
                wqs = self.welcome_questionaire_samples
            )
            self.duplicate_samples.to_excel(duplicate_samples_path, index = False, encoding = 'utf_8_sig')
        
        if self.problematic_samples_var.get() == 1:
            problematic_samples_path = self.export_examination(
                outputname = "問題樣本"
            )
            self.problematic_samples = samples.get_problem(
                wqs = self.welcome_questionaire_samples,
                tts = self.total_member_samples
            )
            self.problematic_samples.to_excel(
                problematic_samples_path,
                index = False,
                encoding = "utf_8_sig"
            )
        
        if self.successful_samples_var.get() == 1:
            successful_samples_path = self.export_examination(
                outputname = "成功樣本"
            )
            self.successful_samples = samples.sample_merge(
                wqs = self.welcome_questionaire_samples,
                tts = self.total_member_samples
            )
            self.successful_samples.to_excel(
                successful_samples_path,
                index = False,
                encoding = "utf_8_sig"
            )
        
        samples.export_result(
            wqs = self.welcome_questionaire_samples,
            tts = self.total_member_samples,
            output = self.samples_date()
        )
        self.destroy()
        self.quit()

#filmem_gui().mainloop()