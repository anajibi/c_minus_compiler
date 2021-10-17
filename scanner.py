from constants import LEXICAL_ERRORS_FILE_NAME, INPUT_FILE_NAME, KEYWORDS
import re

symbol_table = {}
lexical_error_log = open(LEXICAL_ERRORS_FILE_NAME, "w")
input_file = open(INPUT_FILE_NAME, "r", encoding="UTF-8")
current_lexeme = ""
buffer = ""
line_number = 0
lexical_errors = []
read_token = None


def init_keywords():
    for keyword in KEYWORDS:
        symbol_table[keyword] = "KEYWORD"


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
    elif is_letter(buffer[0]):  # For Keywords & IDs
        append_to_current_lexeme()
        read_keyword_or_id()
        if current_lexeme in dict(list(symbol_table.items())[:8]):
            read_token = Token("KEYWORD", current_lexeme)
        else:
            read_token = Token("ID", current_lexeme)
    elif is_starting_comment(buffer[0]):
        append_to_current_lexeme()
        read_comment()
        current_lexeme = ""
        return get_next_token()
    elif is_symbol(buffer[0]):
        append_to_current_lexeme()
        read_symbol()
        read_token = Token("SYMBOL", current_lexeme)
    else:
        append_to_current_lexeme()
        report_error("Invalid input")
        return get_next_token()
    current_lexeme = ""
    if read_token.lexeme != "":
        return [read_token, line_number]
    else:
        return get_next_token()


def is_digit(char):
    return re.fullmatch("\d", char) is not None


def is_letter(char):
    return re.fullmatch("[A-Za-z]", char) is not None  # Todo: Shouldn't it be \w?


def is_white_space(char):
    return re.fullmatch("\s", char) is not None


def is_symbol(char):
    return re.fullmatch("[;:,\[\](){}+\-*=<]", char) is not None


def is_starting_comment(char):
    return re.fullmatch("/", char) is not None


def read_number():
    while buffer != "" and is_digit(buffer[0]):
        append_to_current_lexeme()
    if buffer[0] and (not (is_symbol(buffer[0]) | is_white_space(buffer[0]) | is_starting_comment(buffer[0]))):
        append_to_current_lexeme()
        report_error("Invalid number")


def read_keyword_or_id():
    while buffer != "" and (is_digit(buffer[0]) or is_letter(buffer[0])):
        append_to_current_lexeme()
    if buffer[0] and (not (is_symbol(buffer[0]) | is_white_space(buffer[0]) | is_starting_comment(
            buffer[0]))):
        append_to_current_lexeme()
        report_error("Invalid input")


def read_and_dump_comment(stop_char):
    while buffer != "" and buffer[0] != stop_char:
        append_to_current_lexeme()


def shorten(lexeme):
    return f"{lexeme[:7]}{'...' if len(lexeme) > 7 else ''}"


def read_comment():
    starting_line = line_number
    global current_lexeme
    if buffer != "" and is_starting_comment(buffer[0]):
        append_to_current_lexeme()
        while buffer != "" and buffer[0] != "\n":
            append_to_current_lexeme()
    elif buffer != "" and re.fullmatch("[*]", buffer[0]) is not None:
        append_to_current_lexeme()
        while True:
            read_and_dump_comment("*")
            if buffer == "":
                read_new_line()
                if buffer == "":
                    lexical_error_log.write(f"{starting_line}.\t({shorten(current_lexeme)}, Unclosed comment) ")
                    current_lexeme = ""
                    return
            else:
                append_to_current_lexeme()
                if buffer != "" and buffer[0] == "/":
                    append_to_current_lexeme()
                    return
    else:
        if buffer != "":
            append_to_current_lexeme()
        report_error("Invalid input")


def read_symbol():
    if current_lexeme == "=":
        if buffer != "" and buffer[0] == "=":
            append_to_current_lexeme()
    elif current_lexeme == "*":
        if buffer != "" and buffer[0] == "/":
            append_to_current_lexeme()
            report_error("Unmatched comment")


def report_error(typ):
    global current_lexeme
    lexical_errors.append(LexicalError(current_lexeme, typ))
    current_lexeme = ""


def write_lexical_errors():
    global lexical_errors
    if len(lexical_errors) != 0:
        lexical_error_log.write(f"{line_number - 1}.\t")
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
