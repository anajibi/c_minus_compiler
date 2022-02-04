from enum import Enum
from typing import List, Dict, Tuple

from declarations import Semantic_Error


class CheckingType(Enum):
    FUNC = "function",
    ARR = "array",
    INT = "int",
    VOID = "void"


class SemanticAnalyzer:
    semantic_errors: List[Semantic_Error]
    is_break_inside_loop: bool
    type_stack: List[CheckingType]
    type_dict: Dict[str, Dict[str, CheckingType]]  # type_dict['func1'][c] = INT
    lines_with_type_mismatch: List[int]

    def __init__(self):
        self.semantic_errors = []
        self.is_break_inside_loop = False
        self.line_had_type_mismatch = []
        self.type_stack = []
        self.type_dict = {}

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
            Semantic_Error(curr_token.line_num, f"Illegal type of void for '{curr_token.lexeme}'."))

    def make_break_error(self, curr_token):
        self.semantic_errors.append(
            Semantic_Error(curr_token.line_num, f"No 'repeat ... until' found for 'break'."))

    def make_scoping_error(self, curr_token):
        self.semantic_errors.append(
            Semantic_Error(curr_token.line_num, f"'{curr_token.lexeme}' is not defined."))

    def make_args_num_error(self, line_num, lexeme):
        self.semantic_errors.append(
            Semantic_Error(line_num, f"Mismatch in numbers of arguments of '{lexeme}'."))

    def make_args_type_error(self, line_num, arg_num, func_lexeme, expected_type, got_type):
        self.semantic_errors.append(
            Semantic_Error(line_num,
                           f"Mismatch in type of argument {arg_num} of '{func_lexeme}'. "
                           f"Expected '{expected_type}' but got '{got_type}' instead."))

    def make_op_type_error(self, line_num, got_type, expected_type):
        if line_num not in self.line_had_type_mismatch:
            self.semantic_errors.append(
                Semantic_Error(line_num, f"Type mismatch in operands, Got {got_type} instead of {expected_type}."))
            self.line_had_type_mismatch.append(line_num)

    def check_is_defined(self, curr_token, symbol_table):
        id_val = curr_token.lexeme
        if (id_val, 1) in symbol_table or (id_val, 0) in symbol_table:
            return True
        self.make_scoping_error(curr_token)

    def check_is_args_num_ok(self, ptr_table, symbol_table, called_args_num, func_ptr, curr_token):
        lexeme = ptr_table[func_ptr]
        attr = symbol_table[(lexeme, 0)]
        if attr.arg_cell_num != called_args_num:
            self.make_args_num_error(curr_token.line_num, lexeme)
            return False
        return True

    def check_is_args_type_ok(self, ptr_table, symbol_table, param_list, called_args, func_ptr, curr_token):
        # We must know called_args num is equal to defined_args num by now
        func_lexeme = ptr_table[func_ptr]
        attr = symbol_table[(func_lexeme, 0)]
        got_types = []
        for _ in called_args:
            got_types.append(self.type_stack.pop())  # Pops the last evaluated arguments of func
        got_types = list(reversed(got_types))
        for index, arg_ptr in enumerate(called_args):
            param_type: str = param_list[index][1].type.value[0]
            got_type: str = got_types[index].value[0]
            if 'var' in param_type:
                param_type = 'int'
            elif 'arr' in param_type:
                param_type = 'array'
            if got_type != param_type:
                # We can also get required by type_dict[func_lexeme][index] because it is ordered
                self.make_args_type_error(curr_token.line_num, index + 1, func_lexeme, param_type, got_type)
                return False
        return True

    def check_is_op_var_type_ok(self, curr_token):
        right_hand_type = self.type_stack.pop()
        left_hand_type = self.type_stack.pop()

        if right_hand_type != left_hand_type:
            self.make_op_type_error(curr_token.line_num, right_hand_type.value[0], left_hand_type.value[0])

        self.type_stack.append(right_hand_type)  # Imagine they're the same, push 1 of them now

    def check_op(self, right_hand_side, left_hand_side, curr_token):
        if right_hand_side != -1 and left_hand_side != -1:  # If False, already have another semantic error
            self.check_is_op_var_type_ok(curr_token)

    def type_arr_is_int(self, curr_token):
        self.type_stack.pop()  # Pops the last evaluated argument of array
        self.type_stack.pop()  # Pops for array itself
        self.type_stack.append(CheckingType.INT)

    def type_func_is_int_void(self, args_num, func_ptr, symbol_table, ptr_table):
        # Last evaluated args have been popped in check_is_args_type_ok
        self.type_stack.pop()  # Pops for array itself

        func_lexeme = ptr_table[func_ptr]
        func_type = symbol_table[(func_lexeme, 0)].out_type.value[0]  # Can be int or void
        if 'int' in func_type:
            self.type_stack.append(CheckingType.INT)
        else:
            self.type_stack.append(CheckingType.VOID)

    def insert_in_type_dict(self, current_scope_func, lexeme, type_val: CheckingType):
        if current_scope_func not in self.type_dict:
            self.type_dict[current_scope_func] = {}
        self.type_dict[current_scope_func][lexeme] = type_val

    def push_type(self, curr_token, type_val, current_scope_func):
        from inter_code_gen import AttributeType
        if type_val == AttributeType.VAR \
                or type_val == AttributeType.LOCAL_VAR \
                or type_val == AttributeType.PAR_VAR:
            self.type_stack.append(CheckingType.INT)
            self.insert_in_type_dict(current_scope_func, curr_token.lexeme, CheckingType.INT)
        elif type_val == AttributeType.FUNC:
            self.type_stack.append(CheckingType.FUNC)
            self.type_dict[current_scope_func][curr_token.lexeme] = CheckingType.FUNC
        elif type_val == AttributeType.ARR \
                or type_val == AttributeType.PAR_ARR \
                or type_val == AttributeType.LOCAL_ARR:
            self.type_stack.append(CheckingType.ARR)
            self.type_dict[current_scope_func][curr_token.lexeme] = CheckingType.ARR

    def empty_type_stack(self):
        self.type_stack = []
