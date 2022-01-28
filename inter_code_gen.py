from enum import Enum
from typing import Dict, List

DATA_SEGMENT = 508
STACK_SEGMENT = 5000

PRINT_VARIABLE = 500
TOP_SP = 504


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
    scope: int
    out_type: AttributeType
    arg_cell_num: int
    type: AttributeType

    def __init__(self, scope, out_type, arg_cell_num, type):
        self.scope = scope
        self.out_type = out_type
        self.arg_cell_num = arg_cell_num
        self.type = type


class InterCodeGen:
    symbol_table: Dict[str, Attribute]
    code: List
    stack: List

    def __init__(self):
        self.symbol_table = {}
        self.code = []
        self.stack = []
        self.initiate_code()

    def initiate_code(self):
        self.code += [assign([number(0), PRINT_VARIABLE]), assign([number(0), TOP_SP])]

    def generate(self, action, head):
        pass


def assign(operands):
    return ThreeStateCode(TSCType.ASSIGN, operands)


def number(num):
    return f"#{num}"
