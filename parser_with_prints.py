import sys
from token import NEWLINE
from lex import *


# класс будет отслеживать токены и проверять соответсвие гармматика
class Parser:

    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()
        self.declared_labels = set()
        self.labels_gotoed = set()

        self.current_token = None
        self.peek_token = None
        # инициализация текущего токена и послудующего
        self.next_token()
        self.next_token()

    # будет возврашать True, если токен соответствует
    def check_token(self, kind):
        return kind == self.current_token.kind

    # будет возврашать True, если следующий токен соответствует
    def check_peek(self, kind):
        return kind == self.peek_token.kind

    # прверяет на соответсвие текущий токен, если нет, то ошибка, продвигает текущий токен
    def match(self, kind):
        if not self.check_token(kind):      # если будет возвращен False
            self.abort('Expected ' + kind.name + ' got ' + self.current_token.kind.name)
        self.next_token()

    # продвигает текущий токен
    def next_token(self):
        self.current_token = self.peek_token        # делаем из текущего токена следующий
        self.peek_token = self.lexer.get_token()     # получаем токен

    # эта функция возвращает True, если текущий токен относится к оператору сравнения
    def is_comparison_operator(self):
        return self.check_token(TokenType.GT) or self.check_token(TokenType.GTEQ) or self.check_token(TokenType.LT) or self.check_token(TokenType.LTEQ) or self.check_token(TokenType.EQEQ) or self.check_token(TokenType.NOTEQ)

    def abort(self, message):
        sys.exit('Error' + message)


    # Правила 

    # program ::= {statement}
    def program(self):
        print('PROGRAM')

        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

        for label in self.labels_gotoed:
            if label not in self.declared_labels:
                self.abort('Attempting to GOTO to underclared label: ' + label)

    
    # statement ::= "PRINT" (expression | string) nl
    def statement(self):

        if self.check_token(TokenType.PRINT):
            print('STATEMENT-PRINT')
            self.next_token()

            if self.check_token(TokenType.STRING):
                self.next_token()

            else:
                self.expression()
            
        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.check_token(TokenType.IF):
            print('STATEMNT-IF')
            self.next_token()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            while not self.check_token(TokenType.ENDIF):
                self.statement()
            
            self.match(TokenType.ENDIF)

        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.check_token(TokenType.WHILE):
            print('STETEMNT-WHILE')
            self.next_token()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)

        # "LABEL" ident
        elif self.check_token(TokenType.LABEL):

            print('STATEMENT-LABEL')
            self.next_token()

            # если текущий текст токена в множестве объявленных переменных, то будет ошибка
            # если нету, то добавляется в множество
            if self.current_token.text in self.declared_labels:
                self.abort('Label already exists: ' + self.current_token.text)
            self.declared_labels.add(self.current_token.text)

            self.match(TokenType.IDENT)

        # "GOTO" ident
        elif self.check_token(TokenType.GOTO):
            print(TokenType.IDENT)
            self.next_token()
            self.labels_gotoed.add(self.current_token.text)
            self.match(TokenType.IDENT)
        
        # "LET" ident "=" expression
        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")
            self.next_token()

            if self.current_token.text not in self.symbols:
                self.symbols.add(self.current_token.text)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            self.expression()

        # "INPUT" ident
        elif self.check_token(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.next_token()

            if self.current_token.text not in self.symbols:
                self.symbols.add(self.current_token.text)

            self.match(TokenType.IDENT)

        # если стейтмент не соответствует ни одному из 7 типов, то ошибка
        else:
            self.abort("Invalid statement at " + self.current_token.text + " (" + self.current_token.kind.name + ")")

        # новая линия
        self.nl()


    # comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
    def comparison(self):
        print('COMPARISON')

        self.expression()

        if self.is_comparison_operator():
            self.next_token()
            self.expression()
        
        else:
            self.abort('Expected comparison operator at: ' + self.current_token.text)

        while self.is_comparison_operator():
            self.next_token()
            self.expression()

        
    def expression(self):
        print('EXPRESSION')
        
        self.term()

        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
            self.term()

    
    def term(self):
        print('TERM')

        self.unary()

        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            self.next_token()
            self.unary()

    
    def unary(self):
        print('UNARY')

        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
        self.primary()

    
    def primary(self):
        print('PRIMARY (' + self.current_token.text + ')')

        if self.check_token(TokenType.NUMBER):
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            if self.current_token.text not in self.symbols:
                self.abort('Referencing variable before assignment: ' + self.check_token.text)
            self.next_token()
        else:
            self.abort('Unexpected token at ' + self.current_token.text)

    
    # функция, которая обрабатывает новую линию программы
    # # nl ::= '\n'+
    def nl(self):

        print('NEW-LINE')

        self.match(TokenType.NEWLINE)

        while self.check_token(TokenType.NEWLINE):
            self.next_token()


    

    




