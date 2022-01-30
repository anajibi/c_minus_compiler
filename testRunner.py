import os

from constants import PARSE_TREE_FILE_NAME, \
    SYNTAX_ERRORS_FILE_NAME


def compare():
    root_dir = r"C:\Users\njibi\Desktop\PA1_extra_samples"
    index = 1
    for subdir, dirs, files in os.walk(root_dir):
        for _dir in dirs:
            test_case_id = root_dir + "\\" + _dir + "\\"
            input_txt = open(test_case_id + "input.txt", "r").read()
            open("input.txt", "w").write(input_txt)
            os.system('python compiler.py')
            pt = open(test_case_id + PARSE_TREE_FILE_NAME, "r").read().strip()
            se = open(test_case_id + SYNTAX_ERRORS_FILE_NAME, "r").read().strip()

            pt_m = open(PARSE_TREE_FILE_NAME, "r").read().strip()
            se_m = open(SYNTAX_ERRORS_FILE_NAME, "r").read().strip()
            print(f"{index}:")
            if pt == pt_m and se == se_m:
                print("All True")
            else:
                print(pt == pt_m, "parse tree")
                print(se == se_m, "Syntax Errors")
                print("=========================================")
            index += 1


compare()
