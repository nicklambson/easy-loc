import json
from pathlib import Path
import re

# Update path to point to location of folders with JSON files
WORKING_FILES = Path(r'path_to_translated_files')
SOURCE_FILE = Path(r'path_to_source_files')


# Function to Check JSON
def check_json(filepath):
    global SOURCE_JSON
    try:  # tries to load the file into a JSON parser
        target_content = open(filepath, 'r', encoding="utf-8")
        target_json = json.load(target_content)
        print("File is valid JSON:", filepath.parent.name, filepath.name)
        iterate_recursively(SOURCE_JSON, target_json)
    except ValueError as e:
        # if there is an error it will show the first error
        # in that file (others might exist!!)
        print(e)
        print('in: ' + str(filepath))
        print('\n')


def iterate_recursively(src_json, tgt_json):
    for key, value in tgt_json.items():
        if isinstance(value, dict):
            iterate_recursively(src_json[key], value)
        else:
            check_placeholders(src_json[key], value, key)


def check_placeholders(source, target, key_text):
    global REGEX_LIST
    source_hits = []
    target_hits = []
    for regex in REGEX_LIST:
        for match in regex.findall(source):
            source_hits.append(match)

    for regex in REGEX_LIST:
        for match in regex.findall(target):
            target_hits.append(match)

    # compare the two lists and print error if necessary
    if sorted(source_hits) != sorted(target_hits):
        print("\n")
        print("Key", key_text, "has mismatched placeholders.")
        print("Source:", source)
        print("Target:", target)

        # print a message if a placeholder detected in the source isn't in the target
        for hit in sorted(source_hits):
            if hit not in sorted(target_hits):
                print("Placeholder missing or misspelled in target: " + str(hit))
        # print a message if a placeholder detected in the target isn't in the source
        for hit in sorted(target_hits):
            if hit not in sorted(source_hits):
                print("Placeholder added or misspelled in target: " + str(hit))


SOURCE_CONTENT = open(SOURCE_FILE, 'r', encoding="utf-8")
SOURCE_JSON = json.load(SOURCE_CONTENT)
REGEX1 = re.compile(r'\{\d+\}')      #checks for things like {0} and {12}
REGEX2 = re.compile(r'\%\d+\$[ds]')  #checks for things like %1$d and %2$s
REGEX3 = re.compile(r'<.*?>')        #checks for things like <anything_in_between>
REGEX4 = re.compile(r'\%[ds@]')      #checks for things like %s and %d and %@
REGEX_LIST = [REGEX1, REGEX2, REGEX3, REGEX4]

print("IMPORTANT: placeholder check can only be done once all files pass the validity check.")

# Search all directories and subdirectories for the files
for filepath in WORKING_FILES.rglob("*.json"):
    check_json(filepath)  # check the file
