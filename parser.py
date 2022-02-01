from anytree import Node, RenderTree
from constants import T_DIAGRAMS, N_TERMINALS_INFO, EPSILON, PARSE_TREE_FILE_NAME, SYNTAX_ERRORS_FILE_NAME
from declarations import Nonterminal as NT, Token, State, TokenType, T_ID, Syntax_Error, ActionSymbol

prev_token = None


class Parser:

    def __init__(self, scanner, inter_code_gen):
        self.scanner = scanner
        self.inter_code_gen = inter_code_gen

    @staticmethod
    def is_in_follow(identifier, curr_token):
        return curr_token.type in N_TERMINALS_INFO[identifier].follow \
               or T_ID(curr_token.type, curr_token.lexeme) in N_TERMINALS_INFO[identifier].follow

    @staticmethod
    def is_in_first(identifier, curr_token):
        return curr_token.type in N_TERMINALS_INFO[identifier].first \
               or T_ID(curr_token.type, curr_token.lexeme) in N_TERMINALS_INFO[identifier].first

    @staticmethod
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
            return Parser.is_in_first(identifier, curr_token) or cond
        else:
            return False

    @staticmethod
    def find_matching_transition(transitions, curr_token, curr_state_nt):
        for transition in transitions:
            identifier = transition.identifier
            if isinstance(identifier, ActionSymbol):
                identifier = T_DIAGRAMS[curr_state_nt][transition.dest_state][0].identifier
            if Parser.match(identifier, curr_token):
                return transition
        return None

    @staticmethod
    def save_tree(head):
        f = open(PARSE_TREE_FILE_NAME, "wb")
        for pre, fill, node in RenderTree(head):
            test = (pre + node.name + "\n").encode("UTF-8")
            f.write(test)
        f.close()

    @staticmethod
    def save_syntax_errors(syntax_errors):
        f = open(SYNTAX_ERRORS_FILE_NAME, "+w")
        if len(syntax_errors) == 0:
            f.write("There is no syntax error.")
        else:
            for error in syntax_errors:
                f.write(str(error) + "\n")
        f.close()

    @staticmethod
    def all_terminals(state_transitions):
        for transition in state_transitions:
            if (isinstance(transition.identifier, NT) or transition.identifier == EPSILON) or (
                    isinstance(transition.identifier, T_ID) and transition.identifier.type == TokenType.EOF):
                return False
        return True

    @staticmethod
    def extract_token(identifier):
        if isinstance(identifier, T_ID):
            return identifier.lexeme
        else:
            return identifier.value

    def check_follows(self, nt_transitions, curr_token, syntax_errors):
        global prev_token
        for transition in nt_transitions:
            if Parser.is_in_follow(transition.identifier, curr_token):
                syntax_errors.append(
                    Syntax_Error(curr_token.line_num,
                                 f'missing {transition.identifier.value}'))
                return transition.dest_state

        syntax_errors.append(
            Syntax_Error(curr_token.line_num,
                         f'illegal {curr_token.type.value if curr_token.type == TokenType.NUM or curr_token.type == TokenType.ID else curr_token.lexeme}'))
        prev_token = curr_token
        return self.scanner.get_next_token()

    def parse(self):
        global prev_token
        syntax_errors: list[Syntax_Error] = []
        accepted = False
        head = Node(NT.PROGRAM.value)
        stack = []
        curr_state = State(NT.PROGRAM, 0)
        curr_token = self.scanner.get_next_token()
        while not accepted:
            if len(T_DIAGRAMS[curr_state.nonterminal]) == curr_state.state:
                if len(stack) == 0:
                    accepted = True
                else:
                    curr_state = stack.pop()
                    head = head.parent
            else:
                state_transitions = T_DIAGRAMS[curr_state.nonterminal][curr_state.state]
                if isinstance(state_transitions[0].identifier, ActionSymbol):
                    self.inter_code_gen.generate(state_transitions[0].identifier, prev_token)
                    curr_state.state = state_transitions[0].dest_state
                    continue
                transition = Parser.find_matching_transition(state_transitions, curr_token, curr_state.nonterminal)

                if transition is not None:
                    identifier = transition.identifier
                    if isinstance(identifier, ActionSymbol):
                        self.inter_code_gen.generate(identifier, prev_token)
                        curr_state.state = transition.dest_state
                        continue
                    if isinstance(identifier, TokenType) or isinstance(identifier, T_ID):
                        curr_state.state = transition.dest_state
                        Node(str(curr_token), parent=head)
                        prev_token = curr_token
                        curr_token = self.scanner.get_next_token()
                    elif isinstance(identifier, NT):
                        stack.append(State(curr_state.nonterminal, transition.dest_state))
                        curr_state = State(identifier, 0)
                        head = Node(identifier.value, head)
                    else:
                        Node(EPSILON, parent=head)
                        curr_state.state = transition.dest_state
                else:
                    if curr_token.type == TokenType.EOF:
                        syntax_errors.append(
                            Syntax_Error(curr_token.line_num, f'Unexpected EOF'))
                        while head.parent is not None:
                            head = head.parent
                        break
                    if Parser.all_terminals(state_transitions):
                        syntax_errors.append(
                            Syntax_Error(curr_token.line_num,
                                         f'missing {Parser.extract_token(state_transitions[0].identifier)}'))
                        curr_state.state = state_transitions[0].dest_state
                    else:
                        nt_transitions = filter(lambda tr: isinstance(tr.identifier, NT), state_transitions)
                        token_or_state = self.check_follows(nt_transitions, curr_token, syntax_errors)
                        if isinstance(token_or_state, Token):
                            curr_token = token_or_state
                        else:
                            curr_state.state = token_or_state

        Parser.save_tree(head)
        Parser.save_syntax_errors(syntax_errors)
        return head
