from typing import List

from declarations import Semantic_Error


class SemanticAnalyzer:
    semantic_errors: List[Semantic_Error]
    is_break_inside_loop: bool

    def __init__(self):
        self.semantic_errors = []
        self.is_break_inside_loop = False

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
