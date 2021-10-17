from constants import LEXICAL_ERRORS_FILE_NAME, INPUT_FILE_NAME

symbol_table = set()
lexical_error_log = open(LEXICAL_ERRORS_FILE_NAME, "a")
input_file = open(INPUT_FILE_NAME, "r", encoding="UTF-8")
current_lexeme = ""
current_buffer = ""
line_number = 0


def get_next_token():
    global current_buffer
    global line_number
    if current_buffer == "":
        current_buffer = input_file.readline()
        line_number += 1
    if current_buffer == "":
        return None
    pass;


def report_lexical_error(dumped_lexeme, error_type):
    lexical_error_log.write(f"({dumped_lexeme}, {error_type}) ")
