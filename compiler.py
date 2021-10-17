from scanner import get_next_token
from constants import TOKENS_FILE_NAME

tokens_file = open(TOKENS_FILE_NAME, "a")

tokens_list = []
while (token := get_next_token()) is not None:
    if tokens_list[token[1]]:
        tokens_list[token[1]].append(token[0])
    else:
        tokens_list[token[1]] = token[0]
index = 0
for token_line, in tokens_list:
    global index
    index += 1
    tokens_file.write(f"{index}.\t")
    for token in token_line:
        tokens_file.write(f"{token} ")

    tokens_file.write("\n")
