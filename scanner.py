from constants import LEXICAL_ERRORS_FILE_NAME, INPUT_FILE_NAME
import re

symbol_table = set()
lexical_error_log = open(LEXICAL_ERRORS_FILE_NAME, "a")
input_file = open(INPUT_FILE_NAME, "r", encoding="UTF-8")
current_lexeme = ""
buffer = ""
line_number = 0
lexical_errors = []
read_token = None


def read_new_line():
    global buffer
    global line_number
    buffer = input_file.readline()
    line_number += 1
    write_lexical_errors()


def append_to_current_lexeme():
    global current_lexeme
    global buffer
    current_lexeme = current_lexeme + buffer[0]
    buffer = buffer[1:]


def get_next_token():
    global buffer
    global line_number
    global current_lexeme
    global read_token
    token: str

    if buffer == "":
        read_new_line()
    if buffer == "":
        return None
    if is_digit(buffer[0]):
        append_to_current_lexeme()
        read_number()
        read_token = Token("NUM", current_lexeme)
    elif is_white_space(buffer[0]):
        buffer = buffer[1:]
        return get_next_token()

    current_lexeme = ""
    if read_token.lexeme != "":
        return [read_token, line_number]
    else:
        return get_next_token()


def is_digit(char):
    return re.fullmatch("\d", char) is not None


def is_white_space(char):
    return re.fullmatch("\s", char) is not None


def read_number():
    while buffer != "" and is_digit(buffer[0]):
        append_to_current_lexeme()


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


class Token:
    type: str
    lexeme: str

    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme
