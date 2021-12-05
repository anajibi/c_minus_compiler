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
        []
    ],
    NT.DECLARATION_LIST: [
        [Transition(1, NT.DECLARATION), Transition(2, EPSILON)],
        [Transition(2, NT.DECLARATION_LIST)],
        []
    ],
    NT.DECLARATION: [
        [Transition(1, NT.DECLARATION_INITIAL)],
        [Transition(2, NT.DECLARATION_PRIME)],
        []
    ],
    NT.DECLARATION_INITIAL: [
        [Transition(1, NT.TYPE_SPECIFIER)],
        [Transition(2, TokenType.ID)],
        []
    ],
    NT.DECLARATION_PRIME: [
        [Transition(1, NT.FUN_DECLARATION_PRIME), Transition(1, NT.VAR_DECLARATION_PRIME)],
        []
    ],
    NT.VAR_DECLARATION_PRIME: [
        [Transition(4, T_ID(TokenType.SYMBOL, ";")), Transition(1, T_ID(TokenType.SYMBOL, "["))],
        [Transition(2, TokenType.NUM)],
        [Transition(3, T_ID(TokenType.SYMBOL, "]"))],
        [Transition(4, T_ID(TokenType.SYMBOL, ";"))],
        []
    ],
    NT.FUN_DECLARATION_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "("))],
        [Transition(2, NT.PARAMS)],
        [Transition(3, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(4, NT.COMPOUND_STMT)],
        []
    ],
    NT.TYPE_SPECIFIER: [
        [Transition(1, T_ID(TokenType.KEYWORD, "int")), Transition(1, T_ID(TokenType.KEYWORD, "void"))],
        []
    ],
    NT.PARAMS: [
        [Transition(1, T_ID(TokenType.KEYWORD, "int")), Transition(4, T_ID(TokenType.KEYWORD, "void"))],
        [Transition(2, TokenType.ID)],
        [Transition(3, NT.PARAM_PRIME)],
        [Transition(4, NT.PARAM_LIST)],
        []
    ]

}
