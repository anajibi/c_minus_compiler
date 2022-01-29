from enum import Enum
from typing import Dict, List

from declarations import Token

DATA_SEGMENT = 808
STACK_SEGMENT = 5000
BLOCK_SIZE = 4

PRINT_VARIABLE = 800
TOP_SP = 804
MAIN_STARTING_POINT = None


class AttributeOutType(Enum):
    INT = "int",
    VOID = "void"


class AttributeType(Enum):
    FUNC = "funciton",
    ARR = "array",
    VAR = "var",
    PAR = "param"


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
    ptr: int
    scope: int
    out_type: AttributeOutType
    arg_cell_num: int
    type: AttributeType
    func_starting_point: int

    def __init__(self, ptr, scope):
        self.ptr = ptr
        self.scope = scope
        self.out_type = None
        self.arg_cell_num = None
        self.type = None
        self.func_starting_point = None


class InterCodeGen:
    symbol_table: Dict[str, Attribute]
    ptr_table: Dict[int, str]
    code: List
    stack: List
    scope: int
    data_seg_ptr: int

    def __init__(self):
        self.symbol_table = {}
        self.code = []
        self.stack = []
        self.initiate_code()
        self.scope = 0
        self.data_seg_ptr = DATA_SEGMENT
        self.ptr_table = {}

    def initiate_code(self):
        self.code += [assign([number(0), PRINT_VARIABLE]), assign([number(0), TOP_SP])]

    def generate(self, action, curr_token):
        pass

    def get_temp(self):
        temp = self.data_seg_ptr
        self.data_seg_ptr += BLOCK_SIZE
        return temp

    def pid(self, curr_token: Token):
        if self.scope == 1:
            pass
        else:
            temp = self.get_temp()
            attr = Attribute(ptr=temp, scope=self.scope)
            self.symbol_table[curr_token.lexeme] = attr
            self.ptr_table = attr
            self.stack.append(temp)

    def ptoken(self, curr_token: Token):
        self.stack.append(curr_token.lexeme)

    def stvar(self):
        addr = self.stack.pop()
        type = self.stack.pop()
        attribute = self.findID(addr)

        attribute.type = AttributeType.VAR
        if type == "int":
            attribute.out_type = AttributeOutType.INT
        else:
            attribute.out_type = AttributeOutType.VOID

    def findID(self, addr):
        return self.symbol_table[self.ptr_table[addr]]


def assign(operands):
    return ThreeStateCode(TSCType.ASSIGN, operands)


def number(num):
    return f"#{num}"
