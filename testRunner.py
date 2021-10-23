import os

from constants import LEXICAL_ERRORS_FILE_NAME, SYMBOL_TABLE_FILE_NAME, TOKENS_FILE_NAME


def compare():
    index = 1
    while index < 11:
        test_case_id = f"C:\\Users\\Ali Najibi\\Desktop\\PA1_testcases1.3\\T{'0' if index < 10 else ''}{index}\\"
        input_txt = open(test_case_id + "input.txt", "r").read()
        open("input.txt", "w").write(input_txt)
        os.system('python compiler.py')
        le = open(test_case_id + "lexical_errors.txt", "r").read()
        st = open(test_case_id + "symbol_table.txt", "r").read()
        t = open(test_case_id + "tokens.txt", "r").read()
        le_m = open(LEXICAL_ERRORS_FILE_NAME, "r").read()
        st_m = open(SYMBOL_TABLE_FILE_NAME, "r").read()
        t_m = open(TOKENS_FILE_NAME, "r").read()

        print(le == le_m, "lexical_errors")
        print(st == st_m, "Symbol Table")
        print(t == t_m, "Tokens")
        print("=========================================")
        index += 1


compare()
