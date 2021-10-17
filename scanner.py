from constants import LEXICAL_ERRORS_FILE_NAME, INPUT_FILE_NAME

symbol_table = set()
lexical_error_log = open(LEXICAL_ERRORS_FILE_NAME, "a")
input_file = open(INPUT_FILE_NAME, "r", encoding="UTF-8")
current_lexeme = ""
buffer = ""
line_number = 0
lexical_errors = []


def read_new_line():
    global buffer
    global line_number
    buffer = input_file.readline()
    line_number += 1
    write_lexical_errors()


def get_next_token():
    global buffer
    global line_number
    if buffer == "":
        read_new_line()

    if buffer == "":
        return None
    pass;


def write_lexical_errors():
    global lexical_errors
    if len(lexical_errors) != 0:
        lexical_error_log.write(f"{line_number}.\t")
        error: LexicalError
        for error in lexical_errors:
            lexical_error_log.write(f"({error.dumped_lexeme}, {error.error_type}) ")
        lexical_error_log.write("\n")
    lexical_errors = []


class LexicalError:
    dumped_lexeme: str
    error_type: str

    def __init__(self, dumped_lexeme, error_type):
        self.dumped_lexeme = dumped_lexeme
        self.error_type = error_type
