from scanner import get_next_token, init_keywords, print_symbol_table, print_lexical_errors
from constants import TOKENS_FILE_NAME


def main():
    tokens_list = dict()

    def print_tokens():

        tokens_file = open(TOKENS_FILE_NAME, "w")
        for index, token_line in tokens_list.items():
            tokens_file.write(f"{index + 1}.\t")
            for token in token_line:
                tokens_file.write(f"({token.type}, {token.lexeme}) ")
            tokens_file.write("\n")

    init_keywords()

    while (token := get_next_token()) is not None:
        if tokens_list.get(token.line_num - 1) is None:
            tokens_list[token.line_num - 1] = [token]
        else:
            tokens_list[token.line_num - 1].append(token)

    print_tokens()
    print_symbol_table()
    print_lexical_errors()


if __name__ == '__main__':
    main()
