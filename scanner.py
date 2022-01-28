from typing import Dict

from constants import LEXICAL_ERRORS_FILE_NAME, INPUT_FILE_NAME, KEYWORDS, SYMBOL_TABLE_FILE_NAME
import re

from declarations import Token, TokenType

lexical_error_log = open(LEXICAL_ERRORS_FILE_NAME, "w")
symbol_table_log = open(SYMBOL_TABLE_FILE_NAME, "w")
input_file = open(INPUT_FILE_NAME, "r", encoding="UTF-8")



class Scanner:
    symbol_table: Dict
    current_lexeme: str
    buffer: str
    line_number: int
    lexical_errors: Dict
    read_token: str

    def __init__(self):
        self.symbol_table = {}
        self.current_lexeme = ""
        self.buffer = ""
        self.line_number = 0
        self.lexical_errors = {}
        self.read_token = None


    def init_keywords(self):
        for keyword in KEYWORDS:
            self.symbol_table[keyword] = "KEYWORD"


    def read_new_line():
        global buffer
        global line_number
        buffer = input_file.readline()
        line_number += 1


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
            return Token(TokenType.EOF, "$", line_number)
        if is_digit(buffer[0]):
            append_to_current_lexeme()
            read_number()
            read_token = Token(TokenType.NUM, current_lexeme, line_number)
        elif is_white_space(buffer[0]):
            buffer = buffer[1:]
            test = get_next_token()
            return test
        elif is_letter(buffer[0]):  # For Keywords & IDs
            append_to_current_lexeme()
            read_keyword_or_id()
            if current_lexeme in KEYWORDS:
                read_token = Token(TokenType.KEYWORD, current_lexeme, line_number)
            else:
                if current_lexeme:
                    symbol_table[current_lexeme] = "ID"
                read_token = Token(TokenType.ID, current_lexeme, line_number)
        elif is_starting_comment(buffer[0]):
            append_to_current_lexeme()
            read_comment()
            current_lexeme = ""
            return get_next_token()
        elif is_symbol(buffer[0]):
            append_to_current_lexeme()
            read_symbol()
            read_token = Token(TokenType.SYMBOL, current_lexeme, line_number)
        else:
            append_to_current_lexeme()
            report_error("Invalid input")
            return get_next_token()
        current_lexeme = ""
        if read_token.lexeme != "":
            return read_token
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
        if buffer != '' and (not (is_symbol(buffer[0]) | is_white_space(buffer[0]) | is_starting_comment(buffer[0]))):
            append_to_current_lexeme()
            report_error("Invalid number")


    def read_keyword_or_id():
        while buffer != "" and (is_digit(buffer[0]) or is_letter(buffer[0])):
            append_to_current_lexeme()
        if buffer != '' and (not (is_symbol(buffer[0]) | is_white_space(buffer[0]) | is_starting_comment(
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
                        current_lexeme = shorten(current_lexeme)
                        report_error("Unclosed comment", starting_line)
                        current_lexeme = ""
                        return
                else:
                    append_to_current_lexeme()
                    if buffer != "" and buffer[0] == "/":
                        append_to_current_lexeme()
                        return
        else:
            report_error("Invalid input")


    def read_symbol():
        if current_lexeme == "=":
            if buffer != "" and buffer[0] == "=":
                append_to_current_lexeme()
            if buffer != "" and not (
                    is_white_space(buffer[0]) | is_starting_comment(buffer[0]) | is_digit(buffer[0]) |
                    is_letter(buffer[0]) | is_symbol(buffer[0])):
                append_to_current_lexeme()
                report_error("Invalid input")
        elif current_lexeme == "*":
            if buffer != "" and buffer[0] == "/":
                append_to_current_lexeme()
                report_error("Unmatched comment")
            if buffer != "" and not (
                    is_white_space(buffer[0]) | is_starting_comment(buffer[0]) | is_digit(buffer[0]) |
                    is_letter(buffer[0]) | is_symbol(buffer[0])):
                append_to_current_lexeme()
                report_error("Invalid input")


    def report_error(error_type, line_num=-1):
        global current_lexeme
        if line_num == -1:
            line_num = line_number
        if lexical_errors.get(line_num) is None:
            lexical_errors[line_num] = [LexicalError(current_lexeme, error_type)]
        else:
            lexical_errors[line_num].append(LexicalError(current_lexeme, error_type))
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


    def print_symbol_table():
        index = 0
        for symbol in symbol_table:
            index += 1
            symbol_table_log.write(f"{index}.\t{symbol}\n")


    def print_lexical_errors():
        if len(lexical_errors) != 0:
            for key in sorted(lexical_errors.keys()):
                lexical_error_log.write(f"{key}.\t")
                for error in lexical_errors[key]:
                    lexical_error_log.write(f"({error.dumped_lexeme}, {error.error_type}) ")
                lexical_error_log.write("\n")
        else:
            lexical_error_log.write("There is no lexical error.")


class LexicalError:
    dumped_lexeme: str
    error_type: str

    def __init__(self, dumped_lexeme, error_type):
        self.dumped_lexeme = dumped_lexeme
        self.error_type = error_type
