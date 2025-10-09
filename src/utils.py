# Aqui se pondran las funciones de utilidad
from pandasql import sqldf
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# aqui agregar load csv
def select_file():
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path: 
            print("Selected file:", file_path)
            data = pd.read_csv(file_path, header = 0)

root = tk.Tk()
root.title("File Upload Example")

upload_button = tk.Button(root, text="Select File", command=select_file)
upload_button.pack(pady=20)

root.mainloop()
