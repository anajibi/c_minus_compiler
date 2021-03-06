from enum import Enum
from typing import Dict, List, Tuple, Union

from constants import OUTPUT_FILE_NAME
from declarations import Token, ActionSymbol
from semantic_analyzer import SemanticAnalyzer


def assign(operands):
    return ThreeStateCode(TSCType.ASSIGN, operands)


def number(num):
    return f"#{num}"


def indirect(addr: int):
    return f"@{addr}"


def direct(addr):
    return int(addr[1:])


def jp(operand):
    return ThreeStateCode(TSCType.JP, [operand])


def jpf(operands):
    return ThreeStateCode(TSCType.JPF, operands)


def add(operands):
    return ThreeStateCode(TSCType.ADD, operands)


def sub(operands):
    return ThreeStateCode(TSCType.SUB, operands)


def mult(operands):
    return ThreeStateCode(TSCType.MULT, operands)


def equal(operands):
    return ThreeStateCode(TSCType.EQ, operands)


def less_than(operands):
    return ThreeStateCode(TSCType.LT, operands)


DATA_SEGMENT = 816
STACK_SEGMENT = 5000
BLOCK_SIZE = 4

PRINT_VARIABLE = 800
TOP_SP = 804
RETURN_VARIABLE = 808
RETURN_ADDRESS = 812

OUTPUT_PTR = -100

MAIN_STARTING_POINT = None
START_ARGS_SYMBOL = "START_ARGS_SYMBOL"
REPEAT_STARTING_POINT = "REPEAT_STARTING_POINT"


def push_to_stack(addr):
    return [assign([addr, indirect(TOP_SP)]),
            add([TOP_SP, number(BLOCK_SIZE), TOP_SP])]


def pop_from_stack(addr):
    return [sub([TOP_SP, number(BLOCK_SIZE), TOP_SP]),
            assign([indirect(TOP_SP), addr])]


class AttributeOutType(Enum):
    INT = "int",
    VOID = "void"


class AttributeType(Enum):
    FUNC = "function",
    ARR = "array",
    VAR = "var",
    PAR_VAR = "param_var",
    PAR_ARR = "param_arr",
    LOCAL_VAR = "local_var",
    LOCAL_ARR = "local_arr"


class TSCType(Enum):
    ADD = "ADD",
    MULT = "MULT",
    SUB = "SUB",
    EQ = "EQ",
    LT = "LT",
    ASSIGN = "ASSIGN",
    JPF = "JPF",
    JP = "JP",
    PRINT = "PRINT"

    # enum to string
    def enum_to_str(self):
        if isinstance(self.value, Tuple):
            return self.value[0]
        return self.value


class ThreeStateCode:
    op: TSCType
    operands: List

    def __init__(self, op, operands):
        self.op = op
        self.operands = operands

    def __str__(self):
        return f"({self.op.enum_to_str()}, {', '.join(map(lambda x: str(x), self.operands))})"


class Attribute:
    ptr: int  # int i-> 400; int a[5] 400 -> 404, 408, ... 420; int a[] -> 400 -> 500
    scope: int
    out_type: AttributeOutType or None
    arg_cell_num: int or None
    type: AttributeType or None

    def __init__(self, ptr, scope):
        self.ptr = ptr
        self.scope = scope
        self.out_type = None
        self.arg_cell_num = None
        self.type = None


class FunctionInfo:
    params: List[Tuple[int, Attribute]]
    local_vars: List[int]
    temps: List[int]

    def __init__(self, params):
        self.params = params
        self.local_vars = []
        self.temps = []


class InterCodeGen:
    function_info: Dict[int, FunctionInfo]
    symbol_table: Dict[Tuple[str, int], Attribute]
    ptr_table: Dict[Union[str, int], str]
    code: List
    stack: List
    scope: int
    data_seg_ptr: int
    param_list: List[Tuple[int, Attribute]]
    current_scope_func: str or None
    function_temps: List[int]
    break_list: List[int]
    semantic_analyzer: SemanticAnalyzer

    def __init__(self):
        self.symbol_table = {}
        self.code = []
        self.stack = []
        self.initiate_code()
        self.scope = 0
        self.data_seg_ptr = DATA_SEGMENT
        self.ptr_table = {}
        self.current_scope_func = "GLOBAL"
        self.function_info = {}
        self.function_temps = []
        self.ptr_table[OUTPUT_PTR] = "output"
        attr = Attribute(ptr=OUTPUT_PTR, scope=0)
        attr.type = AttributeType.FUNC
        attr.arg_cell_num = 1
        self.symbol_table[("output", 0)] = attr
        self.break_list = []
        self.semantic_analyzer = SemanticAnalyzer()

    def initiate_code(self):
        self.code += [assign([number(0), PRINT_VARIABLE]), assign([number(STACK_SEGMENT), TOP_SP]),
                      assign([number(0), RETURN_VARIABLE]),
                      assign([number(0), RETURN_ADDRESS])]

    def generate(self, action: ActionSymbol, curr_token):
        if action == ActionSymbol.ptoken:
            self.ptoken(curr_token)
        elif action == ActionSymbol.pid:
            self.pid(curr_token)
            self.semantic_analyzer.push_type(curr_token, AttributeType.VAR, self.current_scope_func)
        elif action == ActionSymbol.starr:
            type_val, curr_token = self.starr()
            self.semantic_analyzer.check_void_type(type_val, curr_token)
        elif action == ActionSymbol.stvar:
            type_val, curr_token = self.stvar()
            self.semantic_analyzer.check_void_type(type_val, curr_token)
        elif action == ActionSymbol.stfunc:
            self.stfunc()
        elif action == ActionSymbol.st_param_arr:
            type_val, curr_token = self.st_param(is_arr=True)
            self.semantic_analyzer.check_void_type(type_val, curr_token)
        elif action == ActionSymbol.st_param_var:
            type_val, curr_token = self.st_param(is_arr=False)
            self.semantic_analyzer.check_void_type(type_val, curr_token)
        elif action == ActionSymbol.pop_exp:
            self.pop_exp()
            self.semantic_analyzer.empty_type_stack()
        elif action == ActionSymbol.break_val:
            self.break_val()
            self.semantic_analyzer.check_break(curr_token)
        elif action == ActionSymbol.save:
            self.save()
        elif action == ActionSymbol.jpf_save:
            self.jpf_save()
        elif action == ActionSymbol.jpf_save_i:
            self.jpf_save_i()
            self.semantic_analyzer.break_is_outside()
        elif action == ActionSymbol.jp:
            self.jp()
        elif action == ActionSymbol.save_i:
            self.save_i()
            self.semantic_analyzer.break_is_inside()
        elif action == ActionSymbol.determine_arr:
            self.determine_arr()
            self.semantic_analyzer.type_arr_is_int(curr_token)
        elif action == ActionSymbol.return_result:
            self.return_result()
        elif action == ActionSymbol.assign:
            self.assign()
        elif action == ActionSymbol.compare:
            right_hand_side, left_hand_side = self.compare()
            self.semantic_analyzer.check_op(right_hand_side, left_hand_side, curr_token)
        elif action == ActionSymbol.addop:
            right_hand_side, left_hand_side = self.addop()
            self.semantic_analyzer.check_op(right_hand_side, left_hand_side, curr_token)
        elif action == ActionSymbol.mult:
            right_hand_side, left_hand_side = self.mult()
            self.semantic_analyzer.check_op(right_hand_side, left_hand_side, curr_token)
        elif action == ActionSymbol.start_args:
            self.start_args()
        elif action == ActionSymbol.start_func:
            self.start_func(curr_token)
        elif action == ActionSymbol.call_func:
            args, func_ptr = self.call_func()
            if self.semantic_analyzer.check_is_args_num_ok(self.ptr_table, self.symbol_table, len(args), func_ptr,
                                                           curr_token):
                if func_ptr != OUTPUT_PTR:
                    self.semantic_analyzer.check_is_args_type_ok(self.ptr_table, self.symbol_table,
                                                                 self.function_info[func_ptr].params, args, func_ptr,
                                                                 curr_token)  # self.param_list might be empty
                    self.semantic_analyzer.type_func_is_int_void(len(args), func_ptr, self.symbol_table, self.ptr_table)

        elif action == ActionSymbol.init_program:
            self.init_program()
        elif action == ActionSymbol.end_func:
            self.end_func()
        elif action == ActionSymbol.return_from_func:
            self.return_from_func()
        elif action == ActionSymbol.determine_id:
            if self.semantic_analyzer.check_is_defined(curr_token, self.symbol_table):
                variable = self.determine_id(curr_token, is_determined=True)
                self.semantic_analyzer.push_type(curr_token, variable.type, self.current_scope_func)
            else:
                self.determine_id(curr_token, is_determined=False)
        elif action == ActionSymbol.pnum:
            self.pnum(curr_token)
            self.semantic_analyzer.push_type(curr_token, AttributeType.VAR, self.current_scope_func)
        else:
            raise Exception("Invalid action symbol")

    def get_temp(self, num_cells=1) -> int:
        temp = self.data_seg_ptr
        self.data_seg_ptr += BLOCK_SIZE * num_cells
        if self.scope == 1:
            self.function_info[self.symbol_table[(self.current_scope_func, 0)].ptr].temps.append(temp)
        return temp

    def pid(self, curr_token: Token):
        self.stack.append(curr_token)

    def stvar(self):
        curr_token = self.stack.pop()
        type_val = self.stack.pop()
        addr = self.get_temp()
        attr = Attribute(ptr=addr, scope=self.scope)
        self.symbol_table[(curr_token.lexeme, self.scope)] = attr
        self.ptr_table[addr] = curr_token.lexeme
        attr = self.find_id(addr, self.scope)
        self.assign_type(attr, type_val)
        if self.scope == 0:
            attr.type = AttributeType.VAR
            self.code.append(assign([number(0), addr]))
        else:
            attr.type = AttributeType.LOCAL_VAR
            self.function_info[self.symbol_table[(self.current_scope_func, 0)].ptr].local_vars.append(addr)
            self.code += push_to_stack(addr)
            self.code.append(assign([number(0), addr]))

        return type_val, curr_token

    def starr(self):
        num_cells = int(self.stack.pop().lexeme)
        curr_token = self.stack.pop()
        type_val = self.stack.pop()
        addr = self.get_temp()
        starting_point = self.get_temp(num_cells)
        attr = Attribute(ptr=addr, scope=self.scope)
        self.symbol_table[(curr_token.lexeme, self.scope)] = attr
        self.ptr_table[addr] = curr_token.lexeme
        self.assign_type(attr, type_val)
        attr.arg_cell_num = int(num_cells)
        if self.scope == 0:
            attr.type = AttributeType.ARR
            self.code.append(assign([number(starting_point), addr]))
            for i in range(num_cells):
                self.code.append(assign([number(0), starting_point + i * 4]))
        else:
            attr.type = AttributeType.LOCAL_ARR
            self.function_info[self.symbol_table[(self.current_scope_func, 0)].ptr].local_vars.append(addr)
            self.code.append(assign([number(starting_point), addr]))
            for i in range(num_cells):
                temp_addr = starting_point + i * 4
                self.code += push_to_stack(temp_addr)
                self.code += [assign([number(0), temp_addr])]

        return type_val, curr_token

    def st_param(self, is_arr: bool):
        curr_token = self.stack.pop()
        type_val = self.stack.pop()
        temp = self.get_temp()
        attr = Attribute(ptr=temp, scope=self.scope)
        self.symbol_table[(curr_token.lexeme, self.scope)] = attr
        self.ptr_table[temp] = curr_token.lexeme
        attr.out_type = AttributeOutType.INT
        if is_arr:
            attr.type = AttributeType.PAR_ARR
        else:
            attr.type = AttributeType.PAR_VAR
        self.param_list.append((temp, attr))
        return type_val, curr_token

    def ptoken(self, curr_token: Token):
        self.stack.append(curr_token)

    def start_func(self, curr_token: Token):
        type_val = self.stack.pop()
        ptr = len(self.code) + 1
        self.current_scope_func = curr_token.lexeme
        self.code.append("")
        attr = Attribute(ptr=ptr, scope=self.scope)
        self.symbol_table[(curr_token.lexeme, self.scope)] = attr
        self.ptr_table[ptr] = curr_token.lexeme
        self.scope = 1
        self.function_info[ptr] = FunctionInfo([])
        self.assign_type(attr, type_val)
        self.stack.append(ptr)
        self.param_list = []

    def stfunc(self):
        number_of_args = len(self.param_list)
        addr = self.stack.pop()
        attribute = self.find_id(addr, 0)
        attribute.arg_cell_num = number_of_args
        attribute.type = AttributeType.FUNC
        self.function_info[addr].params = self.param_list
        if self.ptr_table[addr] == "main":
            global MAIN_STARTING_POINT
            MAIN_STARTING_POINT = addr

    def end_func(self):
        func_name = self.current_scope_func
        func = self.symbol_table[(func_name, 0)]
        self.param_list = []
        self.delete_scope_one()
        self.scope = 0
        if func_name != "main":
            self.return_from_func()
        if func_name == "main":
            self.code[func.ptr - 1] = jp(len(self.code) + 1)
        else:
            self.code[func.ptr - 1] = jp(len(self.code))
        self.current_scope_func = None

    def pop_exp(self):
        self.stack.pop()

    def break_val(self):
        self.break_list.append(len(self.code))
        self.code.append("")

    def save(self):
        i = len(self.code)
        self.code.append("")
        self.stack.append(i)

    def jpf_save(self):
        addr = self.stack.pop()
        cond = self.stack.pop()
        self.code[addr] = jpf([cond, len(self.code) + 1])
        i = len(self.code)
        self.code.append("")
        self.stack.append(i)

    def jp(self):
        addr = self.stack.pop()
        self.code[addr] = jp(len(self.code))

    def save_i(self):
        self.stack.append(REPEAT_STARTING_POINT)
        i = len(self.code)
        self.stack.append(i)

    def jpf_save_i(self):
        cond = self.stack.pop()
        addr = self.stack.pop()
        self.code.append(jpf([cond, addr]))
        for break_point in self.break_list:
            self.code[break_point] = jp(len(self.code))
        self.break_list = []
        self.stack.pop()

    def assign(self):
        right_side = self.stack.pop()
        left_side = self.stack.pop()
        self.code.append(assign([right_side, left_side]))
        self.stack.append(left_side)

    def determine_arr(self):
        index = self.stack.pop()
        array = self.stack.pop()
        temp = self.get_temp()
        self.code.append(add([direct(array), index, temp]))
        self.stack.append(indirect(temp))

    def pnum(self, current_token: Token):
        self.stack.append(number(int(current_token.lexeme)))

    def compare(self):
        right_hand_side = self.stack.pop()
        operator = self.stack.pop().lexeme
        left_hand_side = self.stack.pop()
        temp = self.get_temp()
        if operator == '<':
            self.code.append(less_than([left_hand_side, right_hand_side, temp]))
        elif operator == '==':
            self.code.append(equal([left_hand_side, right_hand_side, temp]))
        else:
            print("ERROR")
        self.stack.append(temp)

        return right_hand_side, left_hand_side

    def addop(self):
        right_hand_side = self.stack.pop()
        operator = self.stack.pop().lexeme
        left_hand_side = self.stack.pop()
        temp = self.get_temp()
        if operator == '+':
            self.code.append(add([left_hand_side, right_hand_side, temp]))
        elif operator == '-':
            self.code.append(sub([left_hand_side, right_hand_side, temp]))
        else:
            print("ERROR")
        self.stack.append(temp)

        return right_hand_side, left_hand_side

    def mult(self):
        right_hand_side = self.stack.pop()
        left_hand_side = self.stack.pop()
        temp = self.get_temp()
        self.code.append(mult([left_hand_side, right_hand_side, temp]))
        self.stack.append(temp)

        return right_hand_side, left_hand_side

    def start_args(self):
        self.stack.append(START_ARGS_SYMBOL)

    def call_func(self):
        args = self.get_args()
        func_ptr = self.stack.pop()
        if func_ptr == -1:
            self.stack.append(PRINT_VARIABLE)  # For undefined ID
        elif self.ptr_table[func_ptr] == "output":
            self.code.append(assign([args[0], PRINT_VARIABLE]))
            self.code.append(ThreeStateCode(TSCType.PRINT, [PRINT_VARIABLE]))
            self.stack.append(PRINT_VARIABLE)
        else:
            self.code += push_to_stack(RETURN_ADDRESS)
            self.save_and_copy_args(args, func_ptr)
            self.push_temps(func_ptr)  # this line is not needed for not-recursive functions
            self.code.append(assign([number(len(self.code) + 2), RETURN_ADDRESS]))
            self.code.append(jp(func_ptr))
            self.pop_temps(func_ptr)  # this line is not needed for not-recursive functions
            for param in reversed(self.function_info[func_ptr].params):
                self.code += pop_from_stack(param[0])
            self.code += pop_from_stack(RETURN_ADDRESS)
            temp = self.get_temp()
            self.code.append(assign([RETURN_VARIABLE, temp]))
            self.stack.append(temp)

        return args, func_ptr

    def return_result(self):
        self.code.append(assign([self.stack.pop(), RETURN_VARIABLE]))
        self.return_from_func()

    def return_from_func(self):
        for local_var in reversed(self.function_info[self.symbol_table[(self.current_scope_func, 0)].ptr].local_vars):
            self.code += pop_from_stack(local_var)
        self.code.append(jp(indirect(RETURN_ADDRESS)))

    def init_program(self):
        self.init_all_temps()
        self.jump_to_main()

    @staticmethod
    def assign_type(attribute, type_val):
        if type_val.lexeme == "int":
            attribute.out_type = AttributeOutType.INT
        else:
            attribute.out_type = AttributeOutType.VOID

    def find_id(self, addr, scope):
        return self.symbol_table[(self.ptr_table[addr], scope)]

    def determine_id(self, current_token: Token, is_determined: bool):
        if is_determined:
            id_val = current_token.lexeme
            if (id_val, self.scope) in self.symbol_table:
                variable = self.symbol_table[(id_val, self.scope)]
            else:
                variable = self.symbol_table[(id_val, 0)]
            if variable.type == AttributeType.VAR \
                    or variable.type == AttributeType.LOCAL_VAR \
                    or variable.type == AttributeType.PAR_VAR:
                self.stack.append(variable.ptr)
            elif variable.type == AttributeType.FUNC:
                self.stack.append(variable.ptr)
            elif variable.type == AttributeType.ARR \
                    or variable.type == AttributeType.PAR_ARR \
                    or variable.type == AttributeType.LOCAL_ARR:
                self.stack.append(indirect(variable.ptr))

            return variable
        else:
            self.stack.append(-1)

    def delete_scope_one(self):
        scope_one = [key for key in self.symbol_table.keys() if key[1] == 1]
        for key in scope_one:
            del self.ptr_table[self.symbol_table[key].ptr]
            del self.symbol_table[key]

    def get_args(self):
        args = []
        arg = self.stack.pop()
        while arg != START_ARGS_SYMBOL:
            args.append(arg)
            arg = self.stack.pop()
        return list(reversed(args))

    def save_and_copy_args(self, args, func_ptr):
        for arg, param in zip(args, self.function_info[func_ptr].params):
            # a function to check if param is array, then use direct(arg) instead of arg in two lines below
            self.code += push_to_stack(param[0])
            if param[1].type == AttributeType.PAR_ARR:
                self.code.append(assign([direct(arg), param[0]]))
            else:
                self.code.append(assign([arg, param[0]]))

    def push_temps(self, func_ptr):
        for temp in self.function_info[func_ptr].temps:
            self.code += push_to_stack(temp)

    def pop_temps(self, func_ptr):
        for temp in reversed(self.function_info[func_ptr].temps):
            self.code += pop_from_stack(temp)

    def init_all_temps(self):
        self.stack.append(len(self.code))
        self.code.append("")
        for i in range(DATA_SEGMENT, self.data_seg_ptr, 4):
            if i in self.ptr_table and (self.ptr_table[i], 0) in self.symbol_table:
                continue
            self.code.append(assign([number(0), i]))

    def jump_to_main(self):
        self.code.append(jp(MAIN_STARTING_POINT))
        self.code[self.stack.pop()] = jp(len(self.code))

    def save_inter_code(self, has_semantic_error: bool):
        f = open(OUTPUT_FILE_NAME, "wb")
        if has_semantic_error:
            f.write('The code has not been generated.'.encode())
        else:
            for index, inter_code in enumerate(self.code):
                f.write(f'{index}\t{str(inter_code)}\n'.encode())
        f.close()
