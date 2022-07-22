import enum
import sys


class Lexer:

    def __init__(self, input):
        self.code = input + '\n'             # a line of code for the lexer
        self.current_char = ''               # that lexer check
        self.current_position = -1           # position in line
        self.get_next_character()


    # process with the following symbol
    def get_next_character(self):
        self.current_position += 1
        if self.current_position >= len(self.code):
            self.current_char = '\0'
        else:
            self.current_char = self.code[self.current_position]


    # check next character
    def check_next(self):
        if self.current_position + 1  >= len(self.code):
            return '\0'
        return self.code[self.current_position + 1]


    # error
    def abort(self, message):        
        sys.exit('Lexing error. ' + message)
		

    # skipping spaces
    def skip_shift(self):
        
        while self.current_char == ' ' or self.current_char == '\t' or self.current_char == '\r':
            self.get_next_character()
		

    # skipping comments
    def skip_comment(self):
        
        if self.current_char == '#':
            # пока не начнется новая строка
            while self.current_char != '\n':
                self.get_next_character()


    # function for getting the appropriate token
    def get_token(self):

        self.skip_shift()
        self.skip_comment()

        if self.current_char == '+':
            token = Token(self.current_char, TokenType.PLUS)	# Plus token.

        elif self.current_char == '-':
            token = Token(self.current_char, TokenType.MINUS)	# Minus token.

        elif self.current_char == '*':
            token = Token(self.current_char, TokenType.ASTERISK)	# Asterisk token.

        elif self.current_char == '/':
            token = Token(self.current_char, TokenType.SLASH)	# Slash token.

        elif self.current_char == '\n':
            token = Token(self.current_char, TokenType.NEWLINE)	# Newline token.

        elif self.current_char == '\0':
            token = Token(self.current_char, TokenType.EOF)	# EOF token.

        elif self.current_char == '=':
            # check = or ==
            if self.check_next() == '=':
                last_char = self.current_char    # '='
                self.get_next_character()
                token = Token(last_char + self.current_char, TokenType.EQEQ)
            else:
                token = Token(self.current_char, TokenType.EQ)
        
        elif self.current_char == '>':
            # check > or >=
            if self.check_next() == '=':
                last_char = self.current_char
                self.get_next_character()
                token = Token(last_char + self.current_char, TokenType.GTEQ)
            else:
                token = Token(self.current_char, TokenType.GT)

        elif self.current_char == '<':
            # check < or <=
            if self.check_next() == '=':
                last_char = self.current_char
                self.get_next_character()
                token = Token(last_char + self.current_char, TokenType.LTEQ)
            else:
                token = Token(self.current_char, TokenType.LT)

        elif self.current_char == '!':
            # check ! or ! =
            if self.check_next() == '=':
                last_char = self.current_char
                self.get_next_character()
                print(last_char)    
                print(self.current_char)    # =
                token = Token(last_char + self.current_char, TokenType.NOTEQ)
            else:
                self.abort('Expected !=, got !' + self.check_next())

        elif self.current_char == '\"':
            # get symbols between quotation marks
            self.get_next_character()
            startPos = self.current_position

            while self.current_char != '\"':
                if self.current_char == '\r' or self.current_char == '\n'or self.current_char == '\t' or self.current_char == '\\' or self.current_char == '\%':
                    self.abort('Illegal character in string')
                self.get_next_character()
            # get substring
            tokText = self.code[startPos : self.current_position]
            token = Token(tokText, TokenType.STRING)

        elif self.current_char.isdigit():
            startPos = self.current_position

            while self.check_next().isdigit():
                self.get_next_character()
            if self.check_next() == '.':
                self.get_next_character()

                if not self.check_next().isdigit():
                    self.abort('Illigal character in number')

                while self.check_next().isdigit():
                    self.get_next_character()
                
            tokText = self.code[startPos : self.current_position + 1]
            token = Token(tokText, TokenType.NUMBER)

        elif self.current_char.isalpha():
            startPos = self.current_position

            while self.check_next().isalnum():
                self.get_next_character()
            
            tokText = self.code[startPos : self.current_position + 1]
            keyword = Token.check_if_keyword(tokText)

            if keyword == None:
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)

        else:
            self.abort('Unknowen token: ' + self.current_char)
			
        self.get_next_character()
        return token


class Token:

    def __init__(self, tokenText, tokenKind):

        self.text = tokenText   
        self.kind = tokenKind

    # method for determining the token for a keyword
    @staticmethod
    def check_if_keyword(tokenText):

        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


# class with tokens
class TokenType(enum.Enum):

	EOF = -1
	NEWLINE = 0
	NUMBER = 1
	IDENT = 2
	STRING = 3

	# Keywords.
	LABEL = 101
	GOTO = 102
	PRINT = 103
	INPUT = 104
	LET = 105
	IF = 106
	THEN = 107
	ENDIF = 108
	WHILE = 109
	REPEAT = 110
	ENDWHILE = 111

	# Operators.
	EQ = 201  
	PLUS = 202
	MINUS = 203
	ASTERISK = 204
	SLASH = 205
	EQEQ = 206
	NOTEQ = 207
	LT = 208
	LTEQ = 209
	GT = 210
	GTEQ = 211