import pandas as pd
from pathlib import Path
import os

def delete_file(filepath, filename):
    if os.path.exists(filepath):
        if Path(filepath).is_file:
            os.remove(filepath)
            print("File deleted:", filename)
        else:
            print("Path is actually a directory. Not deleting.", filename)
    else:
        print("The file does not exist:", filename)

FILE_LIST = Path(r"file_list.xlsx")

df = pd.read_excel(FILE_LIST)

for i, row in df.iterrows():
    filepath = row["Filepath"]
    filename = row["Filename"]
    translatable = row["Translatable"]
    if translatable == "No":
        delete_file(filepath, filename)
