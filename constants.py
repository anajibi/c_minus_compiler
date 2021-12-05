from enum import Enum
from typing import Callable, Union

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


class TokenIdentifier:
    type: TokenType
    lexeme: str

    def __init__(self, type: TokenType, lexeme):
        self.type = type
        self.lexeme = lexeme


class State:
    nonterminal: str
    state: int

    def __init__(self, nonterminal, state):
        self.nonterminal = nonterminal
        self.state = state


class Transition:
    dest_state: int
    identifier: Union[str, TokenType, TokenIdentifier]

    def __init__(self, dest_state: int, identifier):
        self.dest_state = dest_state
        self.identifier = identifier


class NTerminalInfo:
    first: list[str]
    follow: list[str]

    def __init__(self, first, follow):
        self.first = first
        self.follow = follow


N_TERMINALS_INFO: dict[str, NTerminalInfo] = {
    "Program": NTerminalInfo([], [])
}

T_DIAGRAMS: dict[str, list[list[Transition]]] = {
    "Program": [
        [Transition(1, "Declaration-list")],
        [Transition(2, TokenIdentifier(TokenType.EOF, "$"))],
        []
    ],
    "Declaration-list": [
        [Transition(1, "Declaration"), Transition(2, EPSILON)],
        [Transition(2, "Declaration-list")],
        []
    ],
    "Declaration": [
        [Transition(1, "Declaration-initial")],
        [Transition(2, "Declaration-prime")],
        []
    ],
    "Declaration-initial": [
        [Transition(1, "Type-specifier")],
        [Transition(2, TokenType.ID)],
        []
    ],
    "Declaration-prime": [
        [Transition(1, "Fun-declaration-prime"), Transition(1, "Var-declaration-prime")],
        []
    ],
    "Var-declaration-prime": [
        [Transition(4, TokenIdentifier(TokenType.SYMBOL, ";")), Transition(1, TokenIdentifier(TokenType.SYMBOL, "["))],
        [Transition(2, TokenType.NUM)],
        [Transition(3, TokenIdentifier(TokenType.SYMBOL, "]"))],
        [Transition(4, TokenIdentifier(TokenType.SYMBOL, ";"))],
        []
    ]

}
