from enum import Enum
from typing import Dict, List, Tuple, Union

from declarations import Token


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


def add(operands):
    return ThreeStateCode(TSCType.ADD, operands)


def sub(operands):
    return ThreeStateCode(TSCType.SUB, operands)


DATA_SEGMENT = 816
STACK_SEGMENT = 5000
BLOCK_SIZE = 4

PRINT_VARIABLE = 800
TOP_SP = 804
RETURN_VARIABLE = 808
RETURN_ADDRESS = 812

MAIN_STARTING_POINT = None
START_ARGS_SYMBOL = "START_ARGS_SYMBOL"


def push_to_stack(addr):
    return [assign([addr, indirect(TOP_SP)]), add([TOP_SP, number(BLOCK_SIZE), TOP_SP])]


def pop_from_stack(addr):
    return [sub([TOP_SP, number(BLOCK_SIZE), TOP_SP]), assign([indirect(TOP_SP), addr])]


class AttributeOutType(Enum):
    INT = "int",
    VOID = "void"


class AttributeType(Enum):
    FUNC = "funciton",
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


class ThreeStateCode:
    OP: TSCType
    operands: List

    def __init__(self, OP, operands):
        self.OP = OP
        self.operands = operands


class Attribute:
    ptr: int  # int i-> 400; int a[5] 400 -> 404, 408, ... 420; int a[] -> 400 -> 500
    scope: int
    out_type: AttributeOutType
    arg_cell_num: int
    type: AttributeType

    def __init__(self, ptr, scope):
        self.ptr = ptr
        self.scope = scope
        self.out_type = None
        self.arg_cell_num = None
        self.type = None


class FunctionInfo:
    params: List[(int, Attribute)]
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
    param_list: List[(int, Attribute)]
    current_scope_func: str
    local_var_list: List[int]
    function_temps: List[int]

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

    def initiate_code(self):
        self.code += [assign([number(0), PRINT_VARIABLE]), assign([number(0), RETURN_VARIABLE]),
                      assign([number(0), RETURN_ADDRESS]), assign([number(STACK_SEGMENT), TOP_SP]), ]

    def generate(self, action, curr_token):
        pass

    def get_temp(self, num_cells=1) -> number:
        temp = self.data_seg_ptr
        self.data_seg_ptr += BLOCK_SIZE * num_cells
        if self.scope == 1:
            self.function_info[self.symbol_table[(self.current_scope_func, 0)].ptr].temps.append(temp)
        return temp

    def pid(self, curr_token: Token):
        self.stack.append(curr_token)

    def stvar(self):
        curr_token = self.stack.pop()
        type = self.stack.pop()
        addr = self.get_temp()
        attr = Attribute(ptr=addr, scope=self.scope)
        self.symbol_table[(curr_token.lexeme, self.scope)] = attr
        self.ptr_table[addr] = curr_token.lexeme
        attr = self.find_id(addr)
        self.assign_type(attr, type)
        if self.scope == 0:
            attr.type = AttributeType.VAR
            self.code.append(assign([number(0), addr]))
        else:
            attr.type = AttributeType.LOCAL_VAR
            self.local_var_list.append(addr)
            self.code += push_to_stack(addr)
            self.code.append(assign([number(0), addr]))

    def starr(self):
        num_cells = int(self.stack.pop().lexeme)
        curr_token = self.stack.pop()
        type = self.stack.pop()
        addr = self.get_temp()
        starting_point = self.get_temp(num_cells)
        attr = Attribute(ptr=addr, scope=self.scope)
        self.symbol_table[(curr_token.lexeme, self.scope)] = attr
        self.ptr_table[addr] = curr_token.lexeme
        self.assign_type(attr, type)
        attr.arg_cell_num = int(num_cells)
        if self.scope == 0:
            attr.type = AttributeType.ARR
            self.code.append(assign([number(starting_point), addr]))
            for i in range(num_cells):
                self.code.append(assign([number(0), starting_point + i * 4]))
        else:
            attr.type = AttributeType.LOCAL_ARR
            self.local_var_list.append(addr)
            self.code.append(assign([number(starting_point), addr]))
            for i in range(num_cells):
                temp_addr = starting_point + i * 4
                self.code += push_to_stack(temp_addr)
                self.code += [assign([number(0), temp_addr])]

    def st_param_var(self):
        curr_token = self.stack.pop()
        temp = self.get_temp()
        attr = Attribute(ptr=temp, scope=self.scope)
        self.symbol_table[(curr_token.lexeme, self.scope)] = attr
        self.ptr_table[temp] = curr_token.lexeme
        attr.out_type = AttributeOutType.INT
        attr.type = AttributeType.PAR_VAR
        self.param_list.append((temp, attr))

    def st_param_arr(self):
        curr_token = self.stack.pop()
        temp = self.get_temp()
        attr = Attribute(ptr=temp, scope=self.scope)
        self.symbol_table[(curr_token.lexeme, self.scope)] = attr
        self.ptr_table[temp] = curr_token.lexeme
        attr.out_type = AttributeOutType.INT
        attr.type = AttributeType.PAR_ARR
        self.param_list.append((temp, attr))

    def ptoken(self, curr_token: Token):
        self.stack.append(curr_token)

    def start_func(self, curr_token: Token):
        type = self.stack.pop()
        ptr = len(self.code) + 1
        self.current_scope_func = curr_token.lexeme
        self.code.append("")
        attr = Attribute(ptr=ptr, scope=self.scope)
        self.symbol_table[(curr_token.lexeme, self.scope)] = attr
        self.ptr_table[ptr] = curr_token.lexeme
        self.scope = 1
        self.assign_type(attr, type)
        self.stack.append(ptr)

    def stfunc(self):
        number_of_args = len(self.param_list)
        addr = self.stack.pop()
        attribute = self.find_id(addr)
        attribute.arg_cell_num = number_of_args
        attribute.type = AttributeType.FUNC
        self.function_info[addr] = FunctionInfo(self.param_list)
        if self.ptr_table[addr] == "main":
            MAIN_STARTING_POINT = addr

    def end_func(self):
        func_name = self.current_scope_func
        func = self.symbol_table[(func_name, 0)]
        self.function_info[func.ptr].local_vars = self.local_var_list
        self.param_list, self.local_var_list = [], []
        self.delete_scope_one()
        self.scope = 0
        self.code[func.ptr - 1] = len(self.code)

    def pop_exp(self):
        self.stack.pop()

    def break_val(self):
        pass

    def save(self):
        i = len(self.code)
        self.code.append("")
        self.stack.append(i)

    def jpf_save(self):
        pass

    def jp(self):
        pass

    def save_i(self):
        self.stack.append(len(self.code))

    def jpf_save_i(self):
        pass

    def assign(self):
        pass

    def determine_arr(self):
        index = self.stack.pop()
        array = self.stack.pop()
        temp = self.get_temp()
        self.stack.append(add([direct(array), index, temp]))

    def pnum(self, current_token: Token):
        self.stack.append(number(int(current_token.lexeme)))

    def compare(self):
        pass

    def addop(self):
        pass

    def mult(self):
        pass

    def start_args(self):
        self.stack.append(START_ARGS_SYMBOL)

    def call_func(self):
        func_ptr = self.stack.pop()
        if self.ptr_table[func_ptr] == "output":
            self.code.append(assign([self.stack.pop(), PRINT_VARIABLE]))
            self.code.append(ThreeStateCode(TSCType.PRINT, PRINT_VARIABLE))
        else:
            self.code += push_to_stack(RETURN_ADDRESS)
            args = self.get_args()
            self.save_and_copy_args(args, func_ptr)
            self.push_temps(func_ptr)
            self.code.append(assign([number(len(self.code) + 1), RETURN_ADDRESS]))
            for param in reversed(self.function_info[func_ptr].params):
                self.code += pop_from_stack(param[0])
            self.code += pop_from_stack(RETURN_ADDRESS)
            self.pop_temps(func_ptr)
            temp = self.get_temp()
            self.code.append(assign([RETURN_VARIABLE, temp]))
            self.stack.append(temp)

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
    def assign_type(attribute, type):
        if type.lexeme == "int":
            attribute.out_type = AttributeOutType.INT
        else:
            attribute.out_type = AttributeOutType.VOID

    def find_id(self, addr):
        return self.symbol_table[(self.ptr_table[addr], self.scope)]
        # if (self.ptr_table[addr], self.scope) in self.symbol_table:
        #     return self.symbol_table[(self.ptr_table[addr], self.scope)]
        # else:
        #     return self.symbol_table[(self.ptr_table[addr], 0)]

    def determine_id(self, current_lexeme: Token):
        id = current_lexeme.lexeme
        variable = self.symbol_table[(id, self.scope)]
        if variable.type == AttributeType.VAR or variable.type == AttributeType.LOCAL_VAR or variable.type == AttributeType.PAR_VAR:
            self.stack.append(variable.ptr)
        elif variable.type == AttributeType.FUNC:
            self.stack.append(variable.ptr)
        elif variable.type == AttributeType.ARR or variable.type == AttributeType.PAR_ARR or variable.type == AttributeType.LOCAL_ARR:
            self.stack.append(indirect(variable.ptr))

    def delete_scope_one(self):
        pass

    def get_local_vars_num(self):
        pass

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
            self.code += push_to_stack(param)
            if param[1].type == AttributeType.PAR_VAR:
                self.code.append(assign([direct(arg), param]))
            else:
                self.code.append(assign([arg, param]))

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
            self.code.append(assign([number(0), i]))

    def jump_to_main(self):
        self.code.append(jp(MAIN_STARTING_POINT))
        self.code[self.stack.pop()] = jp(len(self.code))
