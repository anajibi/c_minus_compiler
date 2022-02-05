import os
from time import sleep

from constants import PARSE_TREE_FILE_NAME, \
    SYNTAX_ERRORS_FILE_NAME, OUTPUT_FILE_NAME, SEMANTIC_ERRORS_FILE_NAME


def compare():
    root_dir = r"C:\Users\njibi\Desktop\TestCases"
    index = 0
    correct_count = 0
    for subdir, dirs, files in os.walk(root_dir):
        for _dir in dirs:
            test_case_id = root_dir + "\\" + _dir + "\\"
            input_txt = open(test_case_id + "input.txt", "r").read()
            open("input.txt", "w").write(input_txt)
            os.system('C:\Python310\python.exe compiler.py')

            se = open(test_case_id + SEMANTIC_ERRORS_FILE_NAME, "r").read().strip()
            se_m = open(SEMANTIC_ERRORS_FILE_NAME, "r").read().strip()

            if _dir.__contains__("S"):
                pt = open(test_case_id + OUTPUT_FILE_NAME, "r").read().strip()
                pt_m = open(OUTPUT_FILE_NAME, "r").read().strip()

                print(f"{_dir}:")
                if pt == pt_m:
                    print("output matched for semantic error test")
                else:
                    print("FUK")
            else:
                os.system("tester_Windows.exe > expected.txt")
                print(f"{_dir}:")
                e = open(test_case_id + "expected.txt", "r").read().strip()
                e_m = open("expected.txt", "r").read().strip()
                if e == e_m and se == se_m:
                    correct_count += 1
                print(e == e_m, "expected")
                print(se == se_m, "semantic errors")

                print("=========================================")
            index += 1
    print(f"{correct_count}/{index}")

compare()
