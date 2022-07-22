from lex import *
from parser import *
from emit import *
import sys



def main():

    print('Simple compiler')

    # so that after the call main.py there was a file ['main.py ', 'code.simp']
    if len(sys.argv) != 2:
        sys.exit('Error: Compiler needs source file as argument.')

    # open the file with a code
    with open(sys.argv[1], 'r') as input_file:
        input = input_file.read()

    # we pass a file to the lexer, the lexer will assign tokens to characters line by line
    lexer = Lexer(input)
    # we pass to emitter the name of the file with the result of the code
    emitter = Emitter('out.c')
    # we pass tokens to the parser and emitter, the parser will build a tree
    parser = Parser(lexer, emitter)

    parser.program()    # start parse
    emitter.write_file()
    print('Compiling completed!')

main()