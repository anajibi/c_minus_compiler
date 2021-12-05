from anytree import Node
from constants import T_DIAGRAMS, N_TERMINALS_INFO, EPSILON
from scanner import get_next_token
from declarations import Nonterminal as NT, Token, State, Transition, TokenType, T_ID


def match(identifier: Transition.identifier, curr_token: Token):
    if isinstance(identifier, TokenType):
        return curr_token.type == identifier
    elif isinstance(identifier, T_ID):
        return curr_token.type == identifier.type and curr_token.lexeme == identifier.lexeme
    elif identifier == EPSILON:
        return curr_token.type in N_TERMINALS_INFO[identifier].follow \
               or curr_token.lexeme in N_TERMINALS_INFO[identifier].follow
    elif isinstance(identifier, NT):
        return curr_token.type in N_TERMINALS_INFO[identifier].first \
               or curr_token.lexeme in N_TERMINALS_INFO[identifier].first
    else:
        return False


def find_matching_transition(transitions, curr_token):
    for transition in transitions:
        if match(transition.identifier, curr_token):
            return transition
    return None


def parse():
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
                    curr_state.state = transition.dest_state
            else:
                while curr_token.type in N_TERMINALS_INFO[curr_state.nonterminal].follow \
                        or curr_token.lexeme in N_TERMINALS_INFO[curr_state.nonterminal].follow:
                    curr_token = get_next_token()
                head = head.parent
    print("Done")
