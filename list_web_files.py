from pathlib import Path
import pandas as pd


def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

WEBSITE_FOLDER = Path(r"C:\My Web Sites\Havasu Falls\www.havasu-falls.com")

file_list = []

for filepath in WEBSITE_FOLDER.rglob("*.*"):
    filename = filepath.name
    extension = filepath.suffix
    bytes = filepath.stat().st_size
    filesize = convert_bytes(bytes)
    file_list.append([filepath, filename, extension, filesize])

df = pd.DataFrame(file_list, columns=["Filepath", "Filename", "Extension", "Filesize"])
df.to_excel('file_list.xlsx')
