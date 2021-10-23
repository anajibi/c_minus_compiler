import os

from constants import LEXICAL_ERRORS_FILE_NAME, SYMBOL_TABLE_FILE_NAME, TOKENS_FILE_NAME


def compare():
    root_dir = "C:\\Users\\Ali Najibi\\Desktop\\PA1_testcases1.3\\PA1_extra_samples\\"
    index = 1
    for subdir, dirs, files in os.walk(root_dir):
        for _dir in dirs:
            test_case_id = root_dir + "\\" + _dir + "\\"
            input_txt = open(test_case_id + "input.txt", "r").read()
            open("input.txt", "w").write(input_txt)
            os.system('python3 compiler.py')
            le = open(test_case_id + "lexical_errors.txt", "r").read()
            st = open(test_case_id + "symbol_table.txt", "r").read()
            t = open(test_case_id + "tokens.txt", "r").read()
            le_m = open(LEXICAL_ERRORS_FILE_NAME, "r").read()
            st_m = open(SYMBOL_TABLE_FILE_NAME, "r").read()
            t_m = open(TOKENS_FILE_NAME, "r").read()
            print(f"{index}:")
            if le == le_m and st == st_m and t == t_m:
                print("All True")
            else:
                print(le == le_m, "lexical_errors")
                print(st == st_m, "Symbol Table")
                print(t == t_m, "Tokens")
                print("=========================================")
            index += 1


compare()
