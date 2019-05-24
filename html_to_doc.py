from pathlib import Path
import pandas as pd
import shutil
import os

WORKING_FILES = Path(r"working_files")
HTML_1 = r'<html><body>'
HTML_2 = r'</body></html>'

PARENT = WORKING_FILES.parent
RESULT = PARENT / 'result'

if RESULT.exists():
    shutil.rmtree(RESULT)
os.mkdir(RESULT)

for filepath in WORKING_FILES.rglob("*.xlsx"):
    sub_folder_name = filepath.stem
    sub_folder_path = RESULT / sub_folder_name
    if not sub_folder_path.exists():
        os.mkdir(sub_folder_path)
    df = pd.read_excel(filepath, dtype=object, use_default_na=False)
    for index, row in df.iterrows():
        new_name = 'new_name'
        suffix = 'suffix'
        english_html = row['HTML']
        file_num = index + 2
        filename = "_".join([str(file_num), new_name, suffix]) + '.doc'
        filepath = sub_folder_path / filename
        with open(filepath, 'w', encoding="utf-8") as f:
            f.write(HTML_1)
            f.write(english_html)
            f.write(HTML_2)
