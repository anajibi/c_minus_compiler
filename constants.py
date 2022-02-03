from typing import Dict, List

from declarations import Nonterminal as NT, NTerminalInfo, Transition, TokenType, T_ID, ActionSymbol

INPUT_FILE_NAME = "input.txt"
OUTPUT_FILE_NAME = "output.txt"
SYMBOL_TABLE_FILE_NAME = "symbol_table.txt"
TOKENS_FILE_NAME = "tokens.txt"
LEXICAL_ERRORS_FILE_NAME = "lexical_errors.txt"
PARSE_TREE_FILE_NAME = "parse_tree.txt"
SYNTAX_ERRORS_FILE_NAME = "syntax_errors.txt"
KEYWORDS = ['if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return', 'endif']
EPSILON = "epsilon"

N_TERMINALS_INFO: Dict[NT, NTerminalInfo] = {
    NT.PROGRAM: NTerminalInfo(
        [
            T_ID(TokenType.EOF, "$"), T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ],
        [
            T_ID(TokenType.EOF, "$")
        ]),
    NT.DECLARATION_LIST: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void"), EPSILON
        ],
        [
            T_ID(TokenType.EOF, "$"), TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return")
        ]
    ),
    NT.DECLARATION: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ],
        [
            T_ID(TokenType.EOF, "$"), TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ]
    ),
    NT.DECLARATION_INITIAL: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "["), T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, ")"), T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.DECLARATION_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "["), T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.EOF, "$"), TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ]
    ),
    NT.VAR_DECLARATION_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "[")
        ],
        [
            T_ID(TokenType.EOF, "$"), TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ]
    ),
    NT.FUN_DECLARATION_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.EOF, "$"), TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ]
    ),
    NT.TYPE_SPECIFIER: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ],
        [
            TokenType.ID
        ]
    ),
    NT.PARAMS: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ],
        [
            T_ID(TokenType.SYMBOL, ")")
        ]
    ),
    NT.PARAM_LIST: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, ","), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ")")
        ]
    ),
    NT.PARAM: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void")
        ],
        [
            T_ID(TokenType.SYMBOL, ")"), T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.PARAM_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "["), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ")"), T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.COMPOUND_STMT: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "{")
        ],
        [
            T_ID(TokenType.EOF, "$"), TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "int"), T_ID(TokenType.KEYWORD, "void"),
            T_ID(TokenType.KEYWORD, "endif"), T_ID(TokenType.KEYWORD, "else"), T_ID(TokenType.KEYWORD, "until")
        ]
    ),
    NT.STATEMENT_LIST: NTerminalInfo(
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM, T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.KEYWORD, "break"), T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, "}")
        ]
    ),
    NT.STATEMENT: NTerminalInfo(
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM, T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.KEYWORD, "break"), T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return")
        ],
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "endif"), T_ID(TokenType.KEYWORD, "else"), T_ID(TokenType.KEYWORD, "until")
        ]
    ),
    NT.EXPRESSION_STMT: NTerminalInfo(
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM, T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.KEYWORD, "break")
        ],
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "endif"), T_ID(TokenType.KEYWORD, "else"), T_ID(TokenType.KEYWORD, "until")
        ]
    ),
    NT.SELECTION_STMT: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "if")
        ],
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "endif"), T_ID(TokenType.KEYWORD, "else"), T_ID(TokenType.KEYWORD, "until")
        ]
    ),
    NT.ELSE_STMT: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "endif"), T_ID(TokenType.KEYWORD, "else")
        ],
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "endif"), T_ID(TokenType.KEYWORD, "else"), T_ID(TokenType.KEYWORD, "until")
        ]
    ),
    NT.ITERATION_STMT: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "repeat")
        ],
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "endif"), T_ID(TokenType.KEYWORD, "else"), T_ID(TokenType.KEYWORD, "until")
        ]
    ),
    NT.RETURN_STMT: NTerminalInfo(
        [
            T_ID(TokenType.KEYWORD, "return")
        ],
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "endif"), T_ID(TokenType.KEYWORD, "else"), T_ID(TokenType.KEYWORD, "until")
        ]
    ),
    NT.RETURN_STMT_PRIME: NTerminalInfo(
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            TokenType.ID, T_ID(TokenType.SYMBOL, ";"), TokenType.NUM,
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "{"), T_ID(TokenType.SYMBOL, "}"), T_ID(TokenType.KEYWORD, "break"),
            T_ID(TokenType.KEYWORD, "if"),
            T_ID(TokenType.KEYWORD, "repeat"), T_ID(TokenType.KEYWORD, "return"),
            T_ID(TokenType.KEYWORD, "endif"), T_ID(TokenType.KEYWORD, "else"), T_ID(TokenType.KEYWORD, "until")
        ]
    ),
    NT.EXPRESSION: NTerminalInfo(
        [
            TokenType.ID, TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.B: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "["), T_ID(TokenType.SYMBOL, "("), T_ID(TokenType.SYMBOL, "="),
            T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="), T_ID(TokenType.SYMBOL, "+"),
            T_ID(TokenType.SYMBOL, "-"), T_ID(TokenType.SYMBOL, "*"), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.H: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "="),
            T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="), T_ID(TokenType.SYMBOL, "+"),
            T_ID(TokenType.SYMBOL, "-"), T_ID(TokenType.SYMBOL, "*"), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.SIMPLE_EXPRESSION_ZEGOND: NTerminalInfo(
        [
            TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.SIMPLE_EXPRESSION_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "("),
            T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="), T_ID(TokenType.SYMBOL, "+"),
            T_ID(TokenType.SYMBOL, "-"), T_ID(TokenType.SYMBOL, "*"), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.C: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.RELOP: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "==")
        ],
        [
            TokenType.ID, TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ]
    ),
    NT.ADDITIVE_EXPRESSION: NTerminalInfo(
        [
            TokenType.ID, TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ",")
        ]
    ),
    NT.ADDITIVE_EXPRESSION_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "("), T_ID(TokenType.SYMBOL, "+"),
            T_ID(TokenType.SYMBOL, "-"), T_ID(TokenType.SYMBOL, "*"), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "==")
        ]
    ),
    NT.ADDITIVE_EXPRESSION_ZEGOND: NTerminalInfo(
        [
            TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "==")
        ]
    ),
    NT.D: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-"), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "==")
        ]
    ),
    NT.ADDOP: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-")
        ],
        [
            TokenType.ID, TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ]
    ),
    NT.TERM: NTerminalInfo(
        [
            TokenType.ID, TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="),
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-")
        ]
    ),
    NT.TERM_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "("), T_ID(TokenType.SYMBOL, "*"), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="),
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-")
        ]
    ),
    NT.TERM_ZEGOND: NTerminalInfo(
        [
            TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="),
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-")
        ]
    ),
    NT.G: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "*"), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="),
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-")
        ]
    ),
    NT.FACTOR: NTerminalInfo(
        [
            TokenType.ID, TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="),
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-"), T_ID(TokenType.SYMBOL, "*")
        ]
    ),
    NT.VAR_CALL_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "["), T_ID(TokenType.SYMBOL, "("), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="),
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-"), T_ID(TokenType.SYMBOL, "*")
        ]
    ),
    NT.VAR_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "["), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="),
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-"), T_ID(TokenType.SYMBOL, "*")
        ]
    ),
    NT.FACTOR_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, "("), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="),
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-"), T_ID(TokenType.SYMBOL, "*")
        ]
    ),
    NT.FACTOR_ZEGOND: NTerminalInfo(
        [
            TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.SYMBOL, ";"), T_ID(TokenType.SYMBOL, "]"), T_ID(TokenType.SYMBOL, ")"),
            T_ID(TokenType.SYMBOL, ","), T_ID(TokenType.SYMBOL, "<"), T_ID(TokenType.SYMBOL, "=="),
            T_ID(TokenType.SYMBOL, "+"), T_ID(TokenType.SYMBOL, "-"), T_ID(TokenType.SYMBOL, "*")
        ]
    ),
    NT.ARGS: NTerminalInfo(
        [
            TokenType.ID, TokenType.NUM, T_ID(TokenType.SYMBOL, "("), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ")")
        ]
    ),
    NT.ARG_LIST: NTerminalInfo(
        [
            TokenType.ID, TokenType.NUM, T_ID(TokenType.SYMBOL, "(")
        ],
        [
            T_ID(TokenType.SYMBOL, ")")
        ]
    ),
    NT.ARG_LIST_PRIME: NTerminalInfo(
        [
            T_ID(TokenType.SYMBOL, ","), EPSILON
        ],
        [
            T_ID(TokenType.SYMBOL, ")")
        ]
    )
}

T_DIAGRAMS: Dict[NT, List[List[Transition]]] = {
    NT.PROGRAM: [
        [Transition(1, NT.DECLARATION_LIST)],
        [Transition(2, ActionSymbol.init_program)],
        [Transition(3, T_ID(TokenType.EOF, "$"))],
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
        [Transition(2, NT.FUN_DECLARATION_PRIME), Transition(1, ActionSymbol.pid)],
        [Transition(2, NT.VAR_DECLARATION_PRIME)]
    ],
    NT.VAR_DECLARATION_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "[")), Transition(6, ActionSymbol.stvar)],
        [Transition(2, TokenType.NUM), ],
        [Transition(3, ActionSymbol.ptoken)],
        [Transition(4, T_ID(TokenType.SYMBOL, "]"))],
        [Transition(5, ActionSymbol.starr)],
        [Transition(7, T_ID(TokenType.SYMBOL, ";"))],
        [Transition(7, T_ID(TokenType.SYMBOL, ";"))],

    ],
    NT.FUN_DECLARATION_PRIME: [
        [Transition(1, ActionSymbol.start_func)],
        [Transition(2, T_ID(TokenType.SYMBOL, "("))],
        [Transition(3, NT.PARAMS)],
        [Transition(4, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(5, ActionSymbol.stfunc)],
        [Transition(6, NT.COMPOUND_STMT)],
        [Transition(7, ActionSymbol.end_func)],
    ],
    NT.TYPE_SPECIFIER: [
        [Transition(1, T_ID(TokenType.KEYWORD, "int")), Transition(1, T_ID(TokenType.KEYWORD, "void"))],
        [Transition(2, ActionSymbol.ptoken)],
    ],
    NT.PARAMS: [
        [Transition(1, T_ID(TokenType.KEYWORD, "int")), Transition(6, T_ID(TokenType.KEYWORD, "void"))],
        [Transition(2, ActionSymbol.ptoken)],
        [Transition(3, TokenType.ID)],
        [Transition(4, ActionSymbol.pid)],
        [Transition(5, NT.PARAM_PRIME)],
        [Transition(6, NT.PARAM_LIST)],
    ],
    NT.PARAM_LIST: [
        [Transition(1, T_ID(TokenType.SYMBOL, ",")), Transition(3, EPSILON)],
        [Transition(2, NT.PARAM)],
        [Transition(3, NT.PARAM_LIST)],
    ],
    NT.PARAM: [
        [Transition(1, NT.DECLARATION_INITIAL)],
        [Transition(2, ActionSymbol.pid)],
        [Transition(3, NT.PARAM_PRIME)],
    ],
    NT.PARAM_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "[")), Transition(3, ActionSymbol.st_param_var)],
        [Transition(2, T_ID(TokenType.SYMBOL, "]"))],
        [Transition(4, ActionSymbol.st_param_arr)],
        [Transition(4, EPSILON)],
    ],
    NT.COMPOUND_STMT: [
        [Transition(1, T_ID(TokenType.SYMBOL, "{"))],
        [Transition(2, NT.DECLARATION_LIST)],
        [Transition(3, NT.STATEMENT_LIST)],
        [Transition(4, T_ID(TokenType.SYMBOL, "}"))],
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
        [Transition(1, NT.EXPRESSION), Transition(3, T_ID(TokenType.KEYWORD, "break")),
         Transition(2, T_ID(TokenType.SYMBOL, ";"))],
        [Transition(2, T_ID(TokenType.SYMBOL, ";"))],
        [Transition(5, ActionSymbol.pop_exp)],
        [Transition(4, T_ID(TokenType.SYMBOL, ";"))],
        [Transition(5, ActionSymbol.break_val)]
    ],
    NT.SELECTION_STMT: [
        [Transition(1, T_ID(TokenType.KEYWORD, "if"))],
        [Transition(2, T_ID(TokenType.SYMBOL, "("))],
        [Transition(3, NT.EXPRESSION)],
        [Transition(4, ActionSymbol.save)],
        [Transition(5, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(6, NT.STATEMENT)],
        [Transition(7, ActionSymbol.jpf_save)],
        [Transition(8, NT.ELSE_STMT)],
        [Transition(9, ActionSymbol.jp)]
    ],
    NT.ELSE_STMT: [
        [Transition(1, T_ID(TokenType.KEYWORD, "else")), Transition(3, T_ID(TokenType.KEYWORD, "endif"))],
        [Transition(2, NT.STATEMENT)],
        [Transition(3, T_ID(TokenType.KEYWORD, "endif"))]
    ],
    NT.ITERATION_STMT: [
        [Transition(1, T_ID(TokenType.KEYWORD, "repeat"))],
        [Transition(2, ActionSymbol.save_i)],
        [Transition(3, NT.STATEMENT)],
        [Transition(4, T_ID(TokenType.KEYWORD, "until"))],
        [Transition(5, T_ID(TokenType.SYMBOL, "("))],
        [Transition(6, NT.EXPRESSION)],
        [Transition(7, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(8, ActionSymbol.jpf_save_i)]
    ],
    NT.RETURN_STMT: [
        [Transition(1, T_ID(TokenType.KEYWORD, "return"))],
        [Transition(2, NT.RETURN_STMT_PRIME)]
    ],
    NT.RETURN_STMT_PRIME: [
        [Transition(1, NT.EXPRESSION), Transition(3, T_ID(TokenType.SYMBOL, ";"))],
        [Transition(2, T_ID(TokenType.SYMBOL, ";"))],
        [Transition(4, ActionSymbol.return_result)],
        [Transition(4, ActionSymbol.return_from_func)]
    ],
    NT.EXPRESSION: [
        [Transition(1, TokenType.ID), Transition(3, NT.SIMPLE_EXPRESSION_ZEGOND)],
        [Transition(2, ActionSymbol.determine_id)],
        [Transition(3, NT.B)]
    ],
    NT.B: [
        [Transition(1, T_ID(TokenType.SYMBOL, "=")), Transition(2, T_ID(TokenType.SYMBOL, "[")),
         Transition(7, NT.SIMPLE_EXPRESSION_PRIME)],
        [Transition(6, NT.EXPRESSION)],
        [Transition(3, NT.EXPRESSION)],
        [Transition(4, T_ID(TokenType.SYMBOL, "]"))],
        [Transition(5, ActionSymbol.determine_arr)],
        [Transition(7, NT.H)],
        [Transition(7, ActionSymbol.assign)]
    ],
    NT.H: [
        [Transition(1, NT.G), Transition(3, T_ID(TokenType.SYMBOL, "="))],
        [Transition(2, NT.D)],
        [Transition(5, NT.C)],
        [Transition(4, NT.EXPRESSION)],
        [Transition(5, ActionSymbol.assign)]
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
        [Transition(1, NT.RELOP), Transition(3, EPSILON)],
        [Transition(2, NT.ADDITIVE_EXPRESSION)],
        [Transition(3, ActionSymbol.compare)]
    ],
    NT.RELOP: [
        [Transition(1, T_ID(TokenType.SYMBOL, "<")), Transition(1, T_ID(TokenType.SYMBOL, "=="))],
        [Transition(2, ActionSymbol.ptoken)]
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
        [Transition(1, NT.ADDOP), Transition(4, EPSILON)],
        [Transition(2, NT.TERM)],
        [Transition(3, ActionSymbol.addop)],
        [Transition(4, NT.D)],
    ],
    NT.ADDOP: [
        [Transition(1, T_ID(TokenType.SYMBOL, "+")), Transition(1, T_ID(TokenType.SYMBOL, "-"))],
        [Transition(2, ActionSymbol.ptoken)]
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
        [Transition(1, T_ID(TokenType.SYMBOL, "*")), Transition(4, EPSILON)],
        [Transition(2, NT.FACTOR)],
        [Transition(3, ActionSymbol.mult)],
        [Transition(4, NT.G)],
    ],
    NT.FACTOR: [
        [Transition(1, T_ID(TokenType.SYMBOL, "(")), Transition(3, TokenType.ID), Transition(4, TokenType.NUM)],
        [Transition(2, NT.EXPRESSION)],
        [Transition(6, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(5, ActionSymbol.determine_id)],
        [Transition(6, ActionSymbol.pnum)],
        [Transition(6, NT.VAR_CALL_PRIME)]
    ],
    NT.VAR_CALL_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "(")), Transition(5, NT.VAR_PRIME)],
        [Transition(2, ActionSymbol.start_args)],
        [Transition(3, NT.ARGS)],
        [Transition(4, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(5, ActionSymbol.call_func)],
    ],
    NT.VAR_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "[")), Transition(4, EPSILON)],
        [Transition(2, NT.EXPRESSION)],
        [Transition(3, T_ID(TokenType.SYMBOL, "]"))],
        [Transition(4, ActionSymbol.determine_arr)]
    ],
    NT.FACTOR_PRIME: [
        [Transition(1, T_ID(TokenType.SYMBOL, "(")), Transition(5, EPSILON)],
        [Transition(2, ActionSymbol.start_args)],
        [Transition(3, NT.ARGS)],
        [Transition(4, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(5, ActionSymbol.call_func)]
    ],
    NT.FACTOR_ZEGOND: [
        [Transition(1, T_ID(TokenType.SYMBOL, "(")), Transition(3, TokenType.NUM)],
        [Transition(2, NT.EXPRESSION)],
        [Transition(4, T_ID(TokenType.SYMBOL, ")"))],
        [Transition(4, ActionSymbol.pnum)]
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

# ITSELF
# Program Declaration-list $
# Declaration-list Declaration Declaration-list | EPSILON
# Declaration Declaration-initial Declaration-prime
# Declaration-initial Type-specifier ID
# Declaration-prime Fun-declaration-prime | Var-declaration-prime
# Var-declaration-prime ; | [ NUM ] ;
# Fun-declaration-prime ( Params ) Compound-stmt
# Type-specifier int | void
# Params int ID Param-prime Param-list | void
# Param-list , Param Param-list | EPSILON
# Param Declaration-initial Param-prime
# Param-prime [ ] | EPSILON
# Compound-stmt { Declaration-list Statement-list }
# Statement-list Statement Statement-list | EPSILON
# Statement Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt
# Expression-stmt Expression ; | break ; | ;
# Selection-stmt if ( Expression ) Statement Else-stmt
# Else-stmt endif | else Statement endif
# Iteration-stmt repeat Statement until ( Expression )
# Return-stmt return Return-stmt-prime
# Return-stmt-prime ; | Expression ;
# Expression Simple-expression-zegond | ID B
# B = Expression | [ Expression ] H | Simple-expression-prime
# H = Expression | G D C
# Simple-expression-zegond Additive-expression-zegond C
# Simple-expression-prime Additive-expression-prime C
# C Relop Additive-expression | EPSILON
# Relop < | ==
# Additive-expression Term D
# Additive-expression-prime Term-prime D
# Additive-expression-zegond Term-zegond D
# D Addop Term D | EPSILON
# Addop + | -
# Term Factor G
# Term-prime Factor-prime G
# Term-zegond Factor-zegond G
# G * Factor G | EPSILON
# Factor ( Expression ) | ID Var-call-prime | NUM
# Var-call-prime ( Args ) | Var-prime
# Var-prime [ Expression ] | EPSILON
# Factor-prime ( Args ) | EPSILON
# Factor-zegond ( Expression ) | NUM
# Args Arg-list | EPSILON
# Arg-list Expression Arg-list-prime
# Arg-list-prime , Expression Arg-list-prime | EPSILON


# WEBSITE COPY AND PASTE
# Program⟶Declarationlist $
# Declarationlist⟶Declaration Declarationlist
# Declarationlist⟶
# Declaration⟶Declarationinitial Declarationprime
# Declarationinitial⟶Typespecifier ID
# Declarationprime⟶Fundeclarationprime
# Declarationprime⟶Vardeclarationprime
# Vardeclarationprime⟶;
# Vardeclarationprime⟶[ NUM ] ;
# Fundeclarationprime⟶( Params ) Compoundstmt
# Typespecifier⟶int
# Typespecifier⟶void
# Params⟶int ID Paramprime Paramlist
# Params⟶void
# Paramlist⟶, Param Paramlist
# Paramlist⟶
# Param⟶Declarationinitial Paramprime
# Paramprime⟶[ ]
# Paramprime⟶
# Compoundstmt⟶{ Declarationlist Statementlist }
# Statementlist⟶Statement Statementlist
# Statementlist⟶
# Statement⟶Expressionstmt
# Statement⟶Compoundstmt
# Statement⟶Selectionstmt
# Statement⟶Iterationstmt
# Statement⟶Returnstmt
# Expressionstmt⟶Expression ;
# Expressionstmt⟶break ;
# Expressionstmt⟶;
# Selectionstmt⟶if ( Expression ) Statement Elsestmt
# Elsestmt⟶endif
# Elsestmt⟶else Statement endif
# Iterationstmt⟶repeat Statement until ( Expression )
# Returnstmt⟶return Returnstmtprime
# Returnstmtprime⟶;
# Returnstmtprime⟶Expression ;
# Expression⟶Simpleexpressionzegond
# Expression⟶ID B
# B⟶= Expression
# B⟶[ Expression ] H
# B⟶Simpleexpressionprime
# H⟶= Expression
# H⟶G D C
# Simpleexpressionzegond⟶Additiveexpressionzegond C
# Simpleexpressionprime⟶Additiveexpressionprime C
# C⟶Relop Additiveexpression
# C⟶
# Relop⟶<
# Relop⟶==
# Additiveexpression⟶Term D
# Additiveexpressionprime⟶Termprime D
# Additiveexpressionzegond⟶Termzegond D
# D⟶Addop Term D
# D⟶
# Addop⟶+
# Addop⟶-
# Term⟶Factor G
# Termprime⟶Factorprime G
# Termzegond⟶Factorzegond G
# G⟶* Factor G
# G⟶
# Factor⟶( Expression )
# Factor⟶ID Varcallprime
# Factor⟶NUM
# Varcallprime⟶( Args )
# Varcallprime⟶Varprime
# Varprime⟶[ Expression ]
# Varprime⟶
# Factorprime⟶( Args )
# Factorprime⟶
# Factorzegond⟶( Expression )
# Factorzegond⟶NUM
# Args⟶Arglist
# Args⟶
# Arglist⟶Expression Arglistprime
# Arglistprime⟶, Expression Arglistprime
# Arglistprime⟶
