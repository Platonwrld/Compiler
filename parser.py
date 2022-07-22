import sys
from lex import *


# class will keep track of tokens and check the consistency of garmmatics
class Parser:

    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()
        self.declared_labels = set()
        self.labels_gotoed = set()

        self.current_token = None
        self.peek_token = None
        # initialization of the current token and the next token
        self.next_token()
        self.next_token()

    # will return True if the token matches 
    def check_token(self, kind):
        return kind == self.current_token.kind

    # will return True if the next token matches
    def check_peek(self, kind):
        return kind == self.peek_token.kind

    # checks the current token for a match, if not, it is an error, moves the current token
    def match(self, kind):
        if not self.check_token(kind):      # if returned False
            self.abort('Expected ' + kind.name + ' got ' + self.current_token.kind.name)
        self.next_token()

    # moves current token
    def next_token(self):
        self.current_token = self.peek_token        
        self.peek_token = self.lexer.get_token()    

    # return True if current token relate to the comparison operator
    def is_comparison_operator(self):
        return self.check_token(TokenType.GT) or self.check_token(TokenType.GTEQ) or self.check_token(TokenType.LT) or self.check_token(TokenType.LTEQ) or self.check_token(TokenType.EQEQ) or self.check_token(TokenType.NOTEQ)

    def abort(self, message):
        sys.exit('Error' + message)


    # Statements rules 

    # 
    def program(self):
        
        # template code for translating an empty program
        self.emitter.header_line('#include <stdio.h>')
        self.emitter.header_line('int main(void){')

        ### Go through all the expressions

        # Skip new lines
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        # Parse expressions
        while not self.check_token(TokenType.EOF):
            self.statement()

        # Close sunction
        self.emitter.emit_line('return 0;')
        self.emitter.emit_line('}')

        for label in self.labels_gotoed:
            if label not in self.declared_labels:
                self.abort('Attempting to GOTO to underclared label: ' + label)

    
    def statement(self):

        if self.check_token(TokenType.PRINT):
            self.next_token()

            # emit simple string print
            if self.check_token(TokenType.STRING):
                self.emitter.emit_line("printf(\"" + self.current_token.text + "\\n\");")
                self.next_token()

            else:
                self.emitter.emit("printf(\"%" + ".2f\\n\", (float)(")
                self.expression()
                self.emitter.emit_line("));")
            
        # "IF" "THEN" {statement} "ENDIF"
        elif self.check_token(TokenType.IF):
            self.next_token()
            self.emitter.emit("if(")
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emit_line("){")

            while not self.check_token(TokenType.ENDIF):
                self.statement()
            
            self.match(TokenType.ENDIF)
            self.emitter.emit_line("}")

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.check_token(TokenType.WHILE):
            self.next_token()
            self.emitter.emit("while(")
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emit_line("){")

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emit_line("}")

        # "LABEL" ident
        elif self.check_token(TokenType.LABEL):

            self.next_token()

            # if the current token text is in a set of declared variables, then there will be an error
            # if not, it is added to the set
            if self.current_token.text in self.declared_labels:
                self.abort('Label already exists: ' + self.current_token.text)
            self.declared_labels.add(self.current_token.text)

            self.emitter.emit_line(self.current_token.text + ":")
            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.check_token(TokenType.GOTO):
            self.next_token()
            self.labels_gotoed.add(self.current_token.text)
            self.emitter.emit_line("goto " + self.check_token.text + ";")
            self.match(TokenType.IDENT)
        
        # "LET" ident "=" expression
        elif self.check_token(TokenType.LET):
            self.next_token()

            if self.current_token.text not in self.symbols:
                self.symbols.add(self.current_token.text)
                self.emitter.header_line("float " + self.current_token.text + ";")

            self.emitter.emit(self.current_token.text + " = ")
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            self.expression()
            self.emitter.emit_line(";")
        

        # "INPUT" ident
        elif self.check_token(TokenType.INPUT):
            self.next_token()

            if self.current_token.text not in self.symbols:
                self.symbols.add(self.current_token.text)
                self.emitter.header_line("float " + self.current_token.text + ";")

            self.emitter.emit_line("if(0 == scanf(\"%" + "f\", &" + self.current_token.text + ")) {")
            self.emitter.emit_line(self.current_token.text + " = 0;")
            self.emitter.emit("scanf(\"%")
            self.emitter.emit_line("*s\");")
            self.emitter.emit_line("}")
            self.match(TokenType.IDENT)

        # if the statement does not match any of the 7 types, then the error
        else:
            self.abort("Invalid statement at " + self.current_token.text + " (" + self.current_token.kind.name + ")")

        # new line
        self.nl()


    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):

        self.expression()

        if self.is_comparison_operator():
            self.emitter.emit(self.current_token.text)
            self.next_token()
            self.expression()
        
        while self.is_comparison_operator():
            self.emitter.emit(self.current_token.text)
            self.next_token()
            self.expression()

        
    def expression(self):
        
        self.term()

        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.current_token.text)
            self.next_token()
            self.term()

    
    def term(self):

        self.unary()

        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            self.emitter.emit(self.current_token.text)
            self.next_token()
            self.unary()

    
    def unary(self):

        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.emitter.emit(self.current_token.text)
            self.next_token()
        self.primary()

    
    def primary(self):

        if self.check_token(TokenType.NUMBER):
            self.emitter.emit(self.current_token.text)
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            if self.current_token.text not in self.symbols:
                self.abort('Referencing variable before assignment: ' + self.current_token.text)
            self.emitter.emit(self.current_token.text)
            self.next_token()
        else:
            self.abort('Unexpected token at ' + self.current_token.text)

    
    # a function that processes a new program line
    # # nl ::= '\n'+
    def nl(self):

        self.match(TokenType.NEWLINE)

        while self.check_token(TokenType.NEWLINE):
            self.next_token()


    

    




