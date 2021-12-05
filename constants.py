from enum import Enum
from typing import Callable, Union

from nonterminals import Nonterminal as NT

INPUT_FILE_NAME = "input.txt"
SYMBOL_TABLE_FILE_NAME = "symbol_table.txt"
TOKENS_FILE_NAME = "tokens.txt"
LEXICAL_ERRORS_FILE_NAME = "lexical_errors.txt"
PARSE_TREE_FILE_NAME = "parse_tree.txt"
SYNTAX_ERRORS_FILE_NAME = "syntax_errors.txt"
KEYWORDS = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return', 'endif']
EPSILON = "EPSILON"


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
        return f"({self.type.value}, {self.lexeme})"


class T_ID:
    type: TokenType
    lexeme: str

    def __init__(self, type: TokenType, lexeme):
        self.type = type
        self.lexeme = lexeme


class State:
    nonterminal: NT
    state: int

    def __init__(self, nonterminal, state):
        self.nonterminal = nonterminal
        self.state = state


class Transition:
    dest_state: int
    identifier: Union[str, NT, TokenType, T_ID]

    def __init__(self, dest_state: int, identifier):
        self.dest_state = dest_state
        self.identifier = identifier


class NTerminalInfo:
    first: list[str]
    follow: list[str]

    def __init__(self, first, follow):
        self.first = first
        self.follow = follow


N_TERMINALS_INFO: dict[NT, NTerminalInfo] = {
    NT.PROGRAM: NTerminalInfo([], [])
}

T_DIAGRAMS: dict[NT, list[list[Transition]]] = {
    NT.PROGRAM: [
        [Transition(1, NT.DECLARATION_LIST)],
        [Transition(2, T_ID(TokenType.EOF, "$"))],
    ],
    NT.DECLARATION_LIST: [
        [Transition(1, NT.DECLARATION), Transition(2, EPSILON)],
        [Transition(2, NT.DECLARATION_LIST)],
    ],
    NT.DECLARATION: [
        [Transition(1, NT.DECLARATION_INITIAL)],
        [Transition(2, NT.DECLARATION_PRIME)],
    ],
    NT.DECLARATION_INITIAL: [
        [Transition(1, NT.TYPE_SPECIFIER)],
        [Transition(2, TokenType.ID)],
    ],
    NT.DECLARATION_PRIME: [
        [Transition(1, NT.FUN_DECLARATION_PRIME), Transition(1, NT.VAR_DECLARATION_PRIME)],
    ],
    NT.VAR_DECLARATION_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "[")), Transition(4, T_ID(TokenType.SYMBOL, ";"))],
        [Transition(2, TokenType.NUM)],
        [Transition(3, T_ID(TokenType.SYMBOL, "]"))],
        [Transition(4, T_ID(TokenType.SYMBOL, ";"))],
    ],
    NT.FUN_DECLARATION_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "("))],
        [Transition(2, NT.PARAMS)],
        [Transition(3, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(4, NT.COMPOUND_STMT)],
    ],
    NT.TYPE_SPECIFIER: [
        [Transition(1, T_ID(TokenType.KEYWORD, "int")), Transition(1, T_ID(TokenType.KEYWORD, "void"))],
    ],
    NT.PARAMS: [
        [Transition(1, T_ID(TokenType.KEYWORD, "int")), Transition(4, T_ID(TokenType.KEYWORD, "void"))],
        [Transition(2, TokenType.ID)],
        [Transition(3, NT.PARAM_PRIME)],
        [Transition(4, NT.PARAM_LIST)],
    ],
    NT.PARAM_LIST: [
        [Transition(1, T_ID(TokenType.SYMBOL, ",")), Transition(3, EPSILON)],
        [Transition(2, NT.PARAM)],
        [Transition(3, NT.PARAM_LIST)],
    ],
    NT.PARAM: [
        [Transition(1, NT.DECLARATION_INITIAL)],
        [Transition(2, NT.PARAM_PRIME)],
    ],
    NT.PARAM_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "[")), Transition(2, EPSILON)],
        [Transition(2, T_ID(TokenType.SYMBOL, "]"))],
    ],
    NT.COMPOUND_STMT: [
        [Transition(1, T_ID(TokenType.SYMBOL, "{"))],
        [Transition(2, NT.DECLARATION_LIST)],
        [Transition(3, NT.STATEMENT_LIST)],
    ],
    NT.STATEMENT_LIST: [
        [Transition(1, NT.STATEMENT), Transition(2, EPSILON)],
        [Transition(2, NT.STATEMENT_LIST)]
    ],
    NT.STATEMENT: [
        [
            Transition(1, NT.EXPRESSION_STMT),
            Transition(1, NT.COMPOUND_STMT),
            Transition(1, NT.SELECTION_STMT),
            Transition(1, NT.ITERATION_STMT),
            Transition(1, NT.RETURN_STMT),
        ]
    ],
    NT.EXPRESSION_STMT: [
        [Transition(1, NT.EXPRESSION), Transition(1, T_ID(TokenType.KEYWORD, "break")),
         Transition(2, T_ID(TokenType.SYMBOL, ";"))],
        [Transition(2, T_ID(TokenType.SYMBOL, ";"))]
    ],
    NT.SELECTION_STMT: [
        [Transition(1, T_ID(TokenType.KEYWORD, "if"))],
        [Transition(2, T_ID(TokenType.SYMBOL, "("))],
        [Transition(3, NT.EXPRESSION)],
        [Transition(4, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(5, NT.STATEMENT)],
        [Transition(6, NT.ELSE_STMT)],
    ],
    NT.ELSE_STMT: [
        [Transition(1, T_ID(TokenType.KEYWORD, "else")), Transition(3, T_ID(TokenType.KEYWORD, "endif"))],
        [Transition(2, NT.STATEMENT)],
        [Transition(3, T_ID(TokenType.KEYWORD, "endif"))]
    ],
    NT.ITERATION_STMT: [
        [Transition(1, T_ID(TokenType.KEYWORD, "repeat"))],
        [Transition(2, NT.STATEMENT)],
        [Transition(3, T_ID(TokenType.KEYWORD, "until"))],
        [Transition(4, T_ID(TokenType.SYMBOL, "("))],
        [Transition(5, NT.EXPRESSION)],
        [Transition(6, T_ID(TokenType.SYMBOL, ")"))],
    ],
    NT.RETURN_STMT: [
        [Transition(1, T_ID(TokenType.KEYWORD, "return"))],
        [Transition(2, NT.RETURN_STMT_PRIME)]
    ],
    NT.RETURN_STMT_PRIME: [
        [Transition(1, NT.EXPRESSION), Transition(2, T_ID(TokenType.SYMBOL, ";"))],
        [Transition(2, T_ID(TokenType.SYMBOL, ";"))]
    ],
    NT.EXPRESSION: [
        [Transition(1, TokenType.ID), Transition(2, NT.SIMPLE_EXPRESSION_ZEGOND)],
        [Transition(2, NT.B)]
    ],
    NT.B: [
        [Transition(1, T_ID(TokenType.SYMBOL, "=")), Transition(2, T_ID(TokenType.SYMBOL, "[")),
         Transition(5, NT.SIMPLE_EXPRESSION_PRIME)],
        [Transition(5, NT.EXPRESSION)],
        [Transition(3, NT.EXPRESSION)],
        [Transition(4, T_ID(TokenType.SYMBOL, "]"))],
        [Transition(5, NT.H)],
    ],
    NT.H: [
        [Transition(1, NT.G), Transition(3, NT.EXPRESSION)],
        [Transition(2, NT.D)],
        [Transition(3, NT.C)],
    ],
    NT.SIMPLE_EXPRESSION_ZEGOND: [
        [Transition(1, NT.ADDITIVE_EXPRESSION_ZEGOND)],
        [Transition(2, NT.C)]
    ],
    NT.SIMPLE_EXPRESSION_PRIME: [
        [Transition(1, NT.ADDITIVE_EXPRESSION_PRIME)],
        [Transition(2, NT.C)]
    ],
    NT.C: [
        [Transition(1, NT.RELOP), Transition(2, EPSILON)],
        [Transition(2, NT.ADDITIVE_EXPRESSION)]
    ],
    NT.RELOP: [
        [Transition(1, T_ID(TokenType.SYMBOL, "<")), Transition(1, T_ID(TokenType.SYMBOL, "=="))]
    ],
    NT.ADDITIVE_EXPRESSION: [
        [Transition(1, NT.TERM)],
        [Transition(2, NT.D)]
    ],
    NT.ADDITIVE_EXPRESSION_PRIME: [
        [Transition(1, NT.TERM_PRIME)],
        [Transition(2, NT.D)]
    ],
    NT.ADDITIVE_EXPRESSION_ZEGOND: [
        [Transition(1, NT.TERM_ZEGOND)],
        [Transition(2, NT.D)]
    ],
    NT.D: [
        [Transition(1, NT.ADDOP), Transition(3, EPSILON)],
        [Transition(2, NT.TERM)],
        [Transition(3, NT.D)],
    ],
    NT.ADDOP: [
        [Transition(1, T_ID(TokenType.SYMBOL, "+")), Transition(1, T_ID(TokenType.SYMBOL, "-"))]
    ],
    NT.TERM: [
        [Transition(1, NT.FACTOR)],
        [Transition(2, NT.G)]
    ],
    NT.TERM_PRIME: [
        [Transition(1, NT.FACTOR_PRIME)],
        [Transition(2, NT.G)]
    ],
    NT.TERM_ZEGOND: [
        [Transition(1, NT.FACTOR_ZEGOND)],
        [Transition(2, NT.G)]
    ],
    NT.G: [
        [Transition(1, T_ID(TokenType.SYMBOL, "*")), Transition(3, EPSILON)],
        [Transition(2, NT.FACTOR)],
        [Transition(3, NT.G)],
    ],
    NT.FACTOR: [
        [Transition(1, T_ID(TokenType.SYMBOL, "(")), Transition(3, TokenType.ID), Transition(4, TokenType.NUM)],
        [Transition(2, NT.EXPRESSION)],
        [Transition(4, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(4, NT.VAR_CALL_PRIME)]
    ],
    NT.VAR_CALL_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "(")), Transition(3, NT.VAR_PRIME)],
        [Transition(2, NT.ARGS)],
        [Transition(3, T_ID(TokenType.SYMBOL, ")"))]
    ],
    NT.VAR_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "[")), Transition(3, EPSILON)],
        [Transition(2, NT.EXPRESSION)],
        [Transition(3, T_ID(TokenType.SYMBOL, "]"))]
    ],
    NT.FACTOR_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "(")), Transition(3, EPSILON)],
        [Transition(2, NT.ARGS)],
        [Transition(3, T_ID(TokenType.SYMBOL, ")"))]
    ],
    NT.FACTOR_ZEGOND: [
        [Transition(1, T_ID(TokenType.SYMBOL, "(")), Transition(3, TokenType.NUM)],
        [Transition(2, NT.EXPRESSION)],
        [Transition(3, T_ID(TokenType.SYMBOL, ")"))]
    ],
    NT.ARGS: [
        [Transition(1, NT.ARG_LIST), Transition(1, EPSILON)]
    ],
    NT.ARG_LIST: [
        [Transition(1, NT.EXPRESSION)],
        [Transition(2, NT.ARG_LIST_PRIME)]
    ],
    NT.ARG_LIST_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, ",")), Transition(3, EPSILON)],
        [Transition(2, NT.EXPRESSION)],
        [Transition(3, NT.ARG_LIST_PRIME)],
    ]
}
