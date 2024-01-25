# coding=utf-8
# @Version: python3.10
# @Time: 2024/1/25 17:06
# @Author: PlutoCtx
# @Email: ctx195467@163.com
# @File: demo01.py
# @Software: PyCharm
# @User: chent

import tkinter as tk
from tkinter import filedialog
from pandastable import Table
import pandas as pd
import pyperclip

class ExcelEditor(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.open_btn = tk.Button(self, text="Open Excel", command=self.open_excel)
        self.open_btn.grid(row=0, column=0, padx=10, pady=10)

        self.copy_btn = tk.Button(self, text="Copy Cell", command=self.copy_cell)
        self.copy_btn.grid(row=0, column=1, padx=10, pady=10)

        self.table_frame = tk.Frame(self)
        self.table_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    def open_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls"), ("Excel files", "*.xlsx")])
        if file_path:
            self.load_excel(file_path)

    def load_excel(self, file_path):
        self.df = pd.read_excel(file_path)
        self.table = Table(self.table_frame, dataframe=self.df, showtoolbar=True, showstatusbar=True)
        self.table.show()

    def copy_cell(self):
        if hasattr(self, 'df'):
            cell_value = self.df.iloc[0, 4]  # 第一行第五列的数据（索引从0开始）
            pyperclip.copy(str(cell_value))  # 将数据复制到剪切板
        else:
            print("No DataFrame loaded.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Excel Editor")
    ExcelEditor(root)
    root.mainloop()
