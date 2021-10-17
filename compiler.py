from scanner import get_next_token, init_keywords
from constants import TOKENS_FILE_NAME


def main():
    tokens_file = open(TOKENS_FILE_NAME, "w")
    index = 0
    tokens_list = dict()

    init_keywords()

    while (token := get_next_token()) is not None:
        if tokens_list.get(token[1] - 1) is None:
            tokens_list[token[1] - 1] = [token[0]]
        else:
            tokens_list[token[1] - 1].append(token[0])
    for _, token_line in tokens_list.items():
        index += 1
        tokens_file.write(f"{index}.\t")
        for token in token_line:
            tokens_file.write(f"({token.type}, {token.lexeme}) ")

        tokens_file.write("\n")


if __name__ == '__main__':
    main()
