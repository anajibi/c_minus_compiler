from typing import List

from declarations import Semantic_Error


class SemanticAnalyzer:
    semantic_errors: List[Semantic_Error]
    is_break_inside_loop: bool

    def __init__(self):
        self.semantic_errors = []
        self.is_break_inside_loop = False

    def break_is_inside(self):
        self.is_break_inside_loop = True

    def break_is_outside(self):
        self.is_break_inside_loop = False

    def check_void_type(self, type_val, curr_token):
        if SemanticAnalyzer.is_void_type(type_val.lexeme):
            self.make_void_type_error(curr_token)

    def check_break(self, curr_token):
        if not self.is_break_inside_loop:
            self.make_break_error(curr_token)

    @staticmethod
    def is_void_type(type_val: str) -> bool:
        if type_val == 'void':
            return True
        return False

    def make_void_type_error(self, curr_token):
        self.semantic_errors.append(
            Semantic_Error(curr_token.line_num, f"Illegal type of void for {curr_token.lexeme}."))

    def make_break_error(self, curr_token):
        self.semantic_errors.append(
            Semantic_Error(curr_token.line_num, f"No 'repeat ... until' found for 'break'."))

    def make_scoping_error(self, curr_token):
        self.semantic_errors.append(
            Semantic_Error(curr_token.line_num, f"'{curr_token.lexeme}' is not defined."))

    def make_args_num_error(self, line_num, lexeme):
        self.semantic_errors.append(
            Semantic_Error(line_num, f"Mismatch in numbers of arguments of '{lexeme}'."))

    def check_is_defined(self, curr_token, symbol_table):
        id_val = curr_token.lexeme
        if (id_val, 1) in symbol_table or (id_val, 0) in symbol_table:
            return True
        self.make_scoping_error(curr_token)

    def check_args_num(self, ptr_table, symbol_table, called_args_num, func_ptr, curr_token):
        lexeme = ptr_table[func_ptr]
        attr = symbol_table[(lexeme, 0)]
        if attr.arg_cell_num != called_args_num:
            self.make_args_num_error(curr_token.line_num, lexeme)
