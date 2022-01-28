from typing import Dict

from constants import LEXICAL_ERRORS_FILE_NAME, INPUT_FILE_NAME, KEYWORDS, SYMBOL_TABLE_FILE_NAME
import re

from declarations import Token, TokenType

lexical_error_log = open(LEXICAL_ERRORS_FILE_NAME, "w")
symbol_table_log = open(SYMBOL_TABLE_FILE_NAME, "w")
input_file = open(INPUT_FILE_NAME, "r", encoding="UTF-8")


def is_digit(char):
    return re.fullmatch(r"\d", char) is not None


def is_letter(char):
    return re.fullmatch(r"[A-Za-z]", char) is not None


def is_white_space(char):
    return re.fullmatch(r"\s", char) is not None


def is_symbol(char):
    return re.fullmatch(r"[;:,\[\](){}+\-*=<]", char) is not None


def is_starting_comment(char):
    return re.fullmatch(r"/", char) is not None


def shorten(lexeme):
    return f"{lexeme[:7]}{'...' if len(lexeme) > 7 else ''}"


class Scanner:
    symbol_table: Dict
    current_lexeme: str
    buffer: str
    line_number: int
    lexical_errors: Dict
    read_token: Token or None

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

    def read_new_line(self):
        self.buffer = input_file.readline()
        self.line_number += 1

    def append_to_current_lexeme(self):
        self.current_lexeme = self.current_lexeme + self.buffer[0]
        self.buffer = self.buffer[1:]

    def get_next_token(self):
        token: str
        if self.buffer == "":
            self.read_new_line()
        if self.buffer == "":
            return Token(TokenType.EOF, "$", self.line_number)
        if is_digit(self.buffer[0]):
            self.append_to_current_lexeme()
            self.read_number()
            self.read_token = Token(TokenType.NUM, self.current_lexeme, self.line_number)
        elif is_white_space(self.buffer[0]):
            self.buffer = self.buffer[1:]
            test = self.get_next_token()
            return test
        elif is_letter(self.buffer[0]):  # For Keywords & IDs
            self.append_to_current_lexeme()
            self.read_keyword_or_id()
            if self.current_lexeme in KEYWORDS:
                self.read_token = Token(TokenType.KEYWORD,
                                        self.current_lexeme, self.line_number)
            else:
                if self.current_lexeme:
                    self.symbol_table[self.current_lexeme] = "ID"
                self.read_token = Token(TokenType.ID, self.current_lexeme, self.line_number)
        elif is_starting_comment(self.buffer[0]):
            self.append_to_current_lexeme()
            self.read_comment()
            self.current_lexeme = ""
            return self.get_next_token()
        elif is_symbol(self.buffer[0]):
            self.append_to_current_lexeme()
            self.read_symbol()
            self.read_token = Token(TokenType.SYMBOL, self.current_lexeme, self.line_number)
        else:
            self.append_to_current_lexeme()
            self.report_error("Invalid input")
            return self.get_next_token()
        self.current_lexeme = ""
        if self.read_token.lexeme != "":
            return self.read_token
        else:
            return self.get_next_token()

    def read_number(self):
        while self.buffer != "" and is_digit(self.buffer[0]):
            self.append_to_current_lexeme()
        if self.buffer != '' and (not (
                is_symbol(self.buffer[0]) | is_white_space(self.buffer[0]) | is_starting_comment(
                self.buffer[0]))):
            self.append_to_current_lexeme()
            self.report_error("Invalid number")

    def read_keyword_or_id(self):
        while self.buffer != "" and (is_digit(self.buffer[0]) or is_letter(self.buffer[0])):
            self.append_to_current_lexeme()
        if self.buffer != '' and (
                not (is_symbol(self.buffer[0]) | is_white_space(self.buffer[0]) | is_starting_comment(
                    self.buffer[0]))):
            self.append_to_current_lexeme()
            self.report_error("Invalid input")

    def read_and_dump_comment(self, stop_char):
        while self.buffer != "" and self.buffer[0] != stop_char:
            self.append_to_current_lexeme()

    def read_comment(self):
        starting_line = self.line_number
        if self.buffer != "" and is_starting_comment(self.buffer[0]):
            self.append_to_current_lexeme()
            while self.buffer != "" and self.buffer[0] != "\n":
                self.append_to_current_lexeme()
        elif self.buffer != "" and re.fullmatch("[*]", self.buffer[0]) is not None:
            self.append_to_current_lexeme()
            while True:
                self.read_and_dump_comment("*")
                if self.buffer == "":
                    self.read_new_line()
                    if self.buffer == "":
                        self.current_lexeme = shorten(self.current_lexeme)
                        self.report_error("Unclosed comment", starting_line)
                        self.current_lexeme = ""
                        return
                else:
                    self.append_to_current_lexeme()
                    if self.buffer != "" and self.buffer[0] == "/":
                        self.append_to_current_lexeme()
                        return
        else:
            self.report_error("Invalid input")

    def read_symbol(self):
        if self.current_lexeme == "=":
            if self.buffer != "" and self.buffer[0] == "=":
                self.append_to_current_lexeme()
            self.handle_invalid_input()
        elif self.current_lexeme == "*":
            if self.buffer != "" and self.buffer[0] == "/":
                self.append_to_current_lexeme()
                self.report_error("Unmatched comment")
            self.handle_invalid_input()

    def handle_invalid_input(self):
        if self.buffer != "" and not (
                is_white_space(self.buffer[0]) | is_starting_comment(self.buffer[0]) | is_digit(
                self.buffer[0]) |
                is_letter(self.buffer[0]) | is_symbol(self.buffer[0])):
            self.append_to_current_lexeme()
            self.report_error("Invalid input")

    def report_error(self, error_type, line_num=-1):
        if line_num == -1:
            line_num = self.line_number
        if self.lexical_errors.get(line_num) is None:
            self.lexical_errors[line_num] = [
                LexicalError(self.current_lexeme, error_type)]
        else:
            self.lexical_errors[line_num].append(
                LexicalError(self.current_lexeme, error_type))
        self.current_lexeme = ""

    def write_lexical_errors(self):
        if len(self.lexical_errors) != 0:
            lexical_error_log.write(f"{self.line_number - 1}.\t")
            error: LexicalError
            for error in self.lexical_errors:
                lexical_error_log.write(
                    f"({error.dumped_lexeme}, {error.error_type}) ")
            lexical_error_log.write("\n")
        self.lexical_errors = {}

    def print_symbol_table(self):
        index = 0
        for symbol in self.symbol_table:
            index += 1
            symbol_table_log.write(f"{index}.\t{symbol}\n")

    def print_lexical_errors(self):
        if len(self.lexical_errors) != 0:
            for key in sorted(self.lexical_errors.keys()):
                lexical_error_log.write(f"{key}.\t")
                for error in self.lexical_errors[key]:
                    lexical_error_log.write(
                        f"({error.dumped_lexeme}, {error.error_type}) ")
                lexical_error_log.write("\n")
        else:
            lexical_error_log.write("There is no lexical error.")


class LexicalError:
    dumped_lexeme: str
    error_type: str

    def __init__(self, dumped_lexeme, error_type):
        self.dumped_lexeme = dumped_lexeme
        self.error_type = error_type
