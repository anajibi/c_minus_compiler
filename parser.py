from anytree import Node, RenderTree
from constants import TokenType, State, T_DIAGRAMS, Token, Transition, N_TERMINALS_INFO, TokenIdentifier, EPSILON
from scanner import get_next_token


def match(identifier: Transition.identifier, curr_token: Token):
    if isinstance(identifier, TokenType):
        return curr_token.type == identifier
    elif isinstance(identifier, TokenIdentifier):
        return curr_token.type == identifier.type and curr_token.lexeme == identifier.lexeme
    elif identifier == EPSILON:
        return curr_token.type in N_TERMINALS_INFO[identifier].follow \
               or curr_token.lexeme in N_TERMINALS_INFO[identifier].follow
    else:
        return curr_token.type in N_TERMINALS_INFO[identifier].first \
               or curr_token.lexeme in N_TERMINALS_INFO[identifier].first


def find_matching_transition(transitions, curr_token):
    for transition in transitions:
        if match(transition.identifier, curr_token):
            return transition
    return None


def parse():
    accepted = False
    head = Node("Program")
    stack = []
    curr_state = State("Program", 0)
    curr_token = get_next_token()
    while not accepted:
        state_transitions = T_DIAGRAMS[curr_state.nonterminal][curr_state.state]
        if len(state_transitions) == 0:
            if len(stack) == 0:
                accepted = True
            else:
                curr_state = stack.pop()
                head = head.parent
        else:
            transition = find_matching_transition(state_transitions, curr_token)
            if transition is not None:
                identifier = transition.identifier
                if isinstance(identifier, TokenType) or isinstance(identifier, TokenIdentifier):
                    curr_state.state = transition.dest_state
                    Node(str(curr_token), parent=head)
                    curr_token = get_next_token()
                elif identifier == EPSILON:
                    curr_state.state = transition.dest_state
                else:
                    stack.append(State(curr_state.nonterminal, transition.dest_state))
                    curr_state = State(identifier, 0)
                    head = Node(identifier, head)
            else:
                while curr_token.type in N_TERMINALS_INFO[curr_state.nonterminal].follow \
                        or curr_token.lexeme in N_TERMINALS_INFO[curr_state.nonterminal].follow:
                    curr_token = get_next_token()
                head = head.parent
    print("Done")
