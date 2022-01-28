from enum import Enum
from typing import Union


class ActionSymbol(Enum):
    ptoken = "ptoken"


class Nonterminal(Enum):
    PROGRAM = "Program"
    DECLARATION_LIST = "Declaration-list"
    DECLARATION = "Declaration"
    DECLARATION_INITIAL = "Declaration-initial"
    DECLARATION_PRIME = "Declaration-prime"
    VAR_DECLARATION_PRIME = "Var-declaration-prime"
    FUN_DECLARATION_PRIME = "Fun-declaration-prime"
    TYPE_SPECIFIER = "Type-specifier"
    PARAMS = "Params"
    PARAM_LIST = "Param-list"
    PARAM = "Param"
    PARAM_PRIME = "Param-prime"
    COMPOUND_STMT = "Compound-stmt"
    STATEMENT_LIST = "Statement-list"
    STATEMENT = "Statement"
    EXPRESSION_STMT = "Expression-stmt"
    SELECTION_STMT = "Selection-stmt"
    ELSE_STMT = "Else-stmt"
    ITERATION_STMT = "Iteration-stmt"
    RETURN_STMT = "Return-stmt"
    RETURN_STMT_PRIME = "Return-stmt-prime"
    EXPRESSION = "Expression"
    B = "B"
    H = "H"
    SIMPLE_EXPRESSION_ZEGOND = "Simple-expression-zegond"
    SIMPLE_EXPRESSION_PRIME = "Simple-expression-prime"
    C = "C"
    RELOP = "Relop"
    ADDITIVE_EXPRESSION = "Additive-expression"
    ADDITIVE_EXPRESSION_PRIME = "Additive-expression-prime"
    ADDITIVE_EXPRESSION_ZEGOND = "Additive-expression-zegond"
    D = "D"
    ADDOP = "Addop"
    TERM = "Term"
    TERM_PRIME = "Term-prime"
    TERM_ZEGOND = "Term-zegond"
    G = "G"
    FACTOR = "Factor"
    VAR_CALL_PRIME = "Var-call-prime"
    VAR_PRIME = "Var-prime"
    FACTOR_PRIME = "Factor-prime"
    FACTOR_ZEGOND = "Factor-zegond"
    ARGS = "Args"
    ARG_LIST = "Arg-list"
    ARG_LIST_PRIME = "Arg-list-prime"


class TokenType(Enum):
    NUM = "NUM"
    KEYWORD = "KEYWORD"
    ID = "ID"
    SYMBOL = "SYMBOL"
    EOF = "EOF"


class TransitionType(Enum):
    T = "TERMINAL"
    NT = "NON-TERMINAL"


class Token:
    type: TokenType
    lexeme: str
    line_num: int

    def __init__(self, type: TokenType, lexeme, line_num):
        self.type = type
        self.lexeme = lexeme
        self.line_num = line_num

    def __str__(self):
        if self.lexeme == "$":
            return self.lexeme
        return f"({self.type.value}, {self.lexeme})"


class T_ID:
    type: TokenType
    lexeme: str

    def __init__(self, type: TokenType, lexeme):
        self.type = type
        self.lexeme = lexeme

    def __eq__(self, other):
        return isinstance(other, T_ID) and self.type == other.type and self.lexeme == other.lexeme


class State:
    nonterminal: Nonterminal
    state: int

    def __init__(self, nonterminal, state):
        self.nonterminal = nonterminal
        self.state = state


class Transition:
    dest_state: int
    identifier: Union[str, Nonterminal, TokenType, T_ID, ActionSymbol]

    def __init__(self, dest_state: int, identifier):
        self.dest_state = dest_state
        self.identifier = identifier


class NTerminalInfo:
    first: list[str]
    follow: list[str]

    def __init__(self, first, follow):
        self.first = first
        self.follow = follow


class Syntax_Error:
    line_num: int
    text: str

    def __init__(self, line_num, text):
        self.text = text
        self.line_num = line_num

    def __str__(self):
        return f'#{self.line_num} : syntax error, {self.text}'
