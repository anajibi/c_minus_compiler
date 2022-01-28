from parser import Parser
from scanner import Scanner
from inter_code_gen import InterCodeGen

# Ali Najibi 98106123
# Alireza Honarvar 98102551
if __name__ == '__main__':
    scanner = Scanner()
    inter_code_gen = InterCodeGen()
    parser = Parser(scanner, inter_code_gen)
    parser.parse()

