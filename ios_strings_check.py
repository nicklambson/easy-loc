from nslocalized import StringTable
from pathlib import Path
import collections
import re


def check_placeholders(source, target, index):
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
        print("Line", index, "has mismatched placeholders.")
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


def check_wrapper(text, index):
    if text[0] != '\"':
        print("\n")
        print("Line", index, "is missing an opening double quote around the text:", text)
    elif text[-1] != '\"':
        print("\n")
        print("Line", index, "is missing a closing double quote around the text:", text)
    elif text[-2:] == '\\\"':
        print("\n")
        print("Line", index, "the closing double quote is escaped, please unescape:", text)


def check_escapes(text, index):
    if text[0] == "\"" and text[-1] == "\"" and text[-2] != "\\":
        text = text[1:-1]
        unescaped_backslashes = [hit for hit in UNESCAPED_BACKSLASH.findall(text)]
        if unescaped_backslashes:
            print("\n")
            print("Line", index, "has an unescaped backslash. Please escape/remove/fix:", text)
            print("Backslash is only necessary before \\\" \\\' \\r \\n and the backslash character itself.")
            print("Examples: \\\" \\' \\r \\n \\\\")
            print("Backslash is also necessary before variable names wrapped in parentheses.")
            print("Example: \\(authenticationCode)")
        unescaped_quotes = [hit for hit in UNESCAPED_QUOTE.findall(text)]
        if unescaped_quotes:
            print("\n")
            print("Line", index, "has unescaped quotes. Please escape:", text)
    else:
        print("\n")
        print("Cannot check escapes due to unexpected text wrapper.")


def comment_check(text, index):
    if text[:2] != "/*":
        print("\n")
        print("Line", index, "is missing a /* at the beginning of the comment line:", text)
    if text[-2:] != "*/":
        print("\n")
        print("Line", index, "is missing a */ at the end of the comment line:", text)


def semicolon_check(text, index):
    if text[-1] != ';':
        print("\n")
        print("Line", index, "is missing a semicolon at the end of the text:", text)


FOLDER = Path(r"folder_path_here")
UNESCAPED_QUOTE = re.compile(r"(?<!\\)\"")
UNESCAPED_BACKSLASH = re.compile(r"(?<!\\)(?:\\)(?![nr\"\'\\(])")
REGEX1 = re.compile(r'\{\d+\}')      #checks for things like {0} and {12}
REGEX2 = re.compile(r'\%\d+\$[ds]')  #checks for things like %1$d and %2$s
REGEX3 = re.compile(r'<.*?>')        #checks for things like <anything_in_between>
REGEX4 = re.compile(r'\%[ds@]')      #checks for things like %s and %d and %@
REGEX_LIST = [REGEX1, REGEX2, REGEX3, REGEX4]

for filepath in FOLDER.rglob("*.strings"):
    print("\n")
    print("Checking File:", filepath.parent.name, filepath.name)
    with filepath.open(encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()
        string_table = collections.defaultdict(dict)
        for line_num, line in enumerate(lines, start=1):
            if line == '':
                pass
            elif line[:2] == "/*":
                comment_check(line, line_num)
            elif "=" in line:
                semicolon_check(line, line_num)
                line = line.strip(";")
                groups = line.split(" = ")
                half = len(groups) / 2
                src = "".join(groups[:int(half)])
                tgt = "".join(groups[int(half):])
                check_wrapper(src, line_num)
                check_escapes(src, line_num)
                check_wrapper(tgt, line_num)
                check_escapes(tgt, line_num)
                check_placeholders(src, tgt, line_num)
            else:
                print("\n")
                print("Line", line_num, "does not have an equals sign or is an invalid comment", line)
    try:
        st = StringTable.read(str(filepath))
        print("File is valid .strings file.")
    except Exception as e:
        print("\n")
        print("******WARNING!******")
        print("File is not valid .strings")
        print(e)
