from anytree import Node, RenderTree
from constants import T_DIAGRAMS, N_TERMINALS_INFO, EPSILON, PARSE_TREE_FILE_NAME, SYNTAX_ERRORS_FILE_NAME
from scanner import get_next_token
from declarations import Nonterminal as NT, Token, State, Transition, TokenType, T_ID, Syntax_Error


def is_in_follow(identifier, curr_token):
    return curr_token.type in N_TERMINALS_INFO[identifier].follow \
           or T_ID(curr_token.type, curr_token.lexeme) in N_TERMINALS_INFO[identifier].follow


def is_in_first(identifier, curr_token):
    return curr_token.type in N_TERMINALS_INFO[identifier].first \
           or T_ID(curr_token.type, curr_token.lexeme) in N_TERMINALS_INFO[identifier].first


def match(identifier, curr_token: Token):
    if isinstance(identifier, TokenType):
        return curr_token.type == identifier
    elif isinstance(identifier, T_ID):
        return curr_token.type == identifier.type and curr_token.lexeme == identifier.lexeme
    elif identifier == EPSILON:
        return True
    elif isinstance(identifier, NT):
        cond = False
        if EPSILON in N_TERMINALS_INFO[identifier].first:
            cond = curr_token.type in N_TERMINALS_INFO[identifier].follow \
                   or T_ID(curr_token.type, curr_token.lexeme) in N_TERMINALS_INFO[identifier].follow
        return is_in_first(identifier, curr_token) or cond
    else:
        return False


def find_matching_transition(transitions, curr_token):
    for transition in transitions:
        if match(transition.identifier, curr_token):
            return transition
    return None


def save_tree(head):
    f = open(PARSE_TREE_FILE_NAME, "+w")
    for pre, fill, node in RenderTree(head):
        f.write("%s%s" % (pre, node.name))


def save_syntax_errors(syntax_errors):
    with open(SYNTAX_ERRORS_FILE_NAME, "+w") as f:
        if len(syntax_errors) == 0:
            f.write("There is no syntax error.")
        else:
            for error in syntax_errors:
                f.write(error)


def parse():
    syntax_errors: list[Syntax_Error] = []
    accepted = False
    head = Node(NT.PROGRAM.value)
    stack = []
    curr_state = State(NT.PROGRAM, 0)
    curr_token = get_next_token()
    while not accepted:
        if len(T_DIAGRAMS[curr_state.nonterminal]) == curr_state.state:
            if len(stack) == 0:
                accepted = True
            else:
                curr_state = stack.pop()
                head = head.parent
        else:
            state_transitions = T_DIAGRAMS[curr_state.nonterminal][curr_state.state]
            transition = find_matching_transition(state_transitions, curr_token)
            if transition is not None:
                identifier = transition.identifier
                if isinstance(identifier, TokenType) or isinstance(identifier, T_ID):
                    curr_state.state = transition.dest_state
                    Node(str(curr_token), parent=head)
                    curr_token = get_next_token()
                elif isinstance(identifier, NT):
                    stack.append(State(curr_state.nonterminal, transition.dest_state))
                    curr_state = State(identifier, 0)
                    head = Node(identifier.value, head)
                else:
                    Node(EPSILON, parent=head)
                    curr_state.state = transition.dest_state
            else:
                while curr_token.type in N_TERMINALS_INFO[curr_state.nonterminal].follow \
                        or curr_token.lexeme in N_TERMINALS_INFO[curr_state.nonterminal].follow:
                    curr_token = get_next_token()
                head = head.parent
    save_tree(head)
    save_syntax_errors(syntax_errors)
    return head
