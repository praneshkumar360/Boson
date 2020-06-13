from token import Token
from token_types import *
from position import *
from error import *
import string

######################
##### CONSTANTS ######
######################

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

######################
#####   LEXER   ######
######################

class Lexer:

    def __init__(self, fn, text):
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.curr_char = None
        self.increment()
        
    def increment(self):
        self.pos.increment(self.curr_char)
        if self.pos.index < len(self.text):
            self.curr_char = self.text[self.pos.index]
        else:
            self.curr_char = None

    def create_tokens(self):
        tokens = []

        while self.curr_char != None:
            if self.curr_char in ' \t':
                self.increment()
            elif self.curr_char in '#':
                self.skip_comment()
            elif self.curr_char in ';\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.increment()
            elif self.curr_char in DIGITS:
                tokens.append(self.make_num())
            elif self.curr_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.curr_char == '"':
                tokens.append(self.make_string())
            elif self.curr_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '-':
                tokens.append(self.make_minus_or_arrow())
            elif self.curr_char == '*':
                tokens.append(self.make_mul_or_pow())
                self.increment()
            elif self.curr_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '%':
                tokens.append(Token(TT_MOD, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '&':
                tokens.append(Token(TT_AND, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '|':
                tokens.append(Token(TT_OR, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '~':
                tokens.append(Token(TT_NOT, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '^':
                tokens.append(Token(TT_XOR, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.increment()
            elif self.curr_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '$':
                tokens.append(Token(TT_DOL, pos_start=self.pos))
                self.increment()
            elif self.curr_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '!':
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)
            elif self.curr_char == '=':
                tokens.append(self.make_equals())
            elif self.curr_char == '<':
                tokens.append(self.make_less_than())
            elif self.curr_char == '>':
                tokens.append(self.make_greater_than())
            elif self.curr_char == '[':
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
                self.increment()
            elif self.curr_char == ']':
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                self.increment()
            elif self.curr_char == '@':
                tokens.append(Token(TT_AT, pos_start=self.pos))
                self.increment()
            else:
                pos_start = self.pos.copy()
                
                return [], IllegalCharError(pos_start, self.pos,"'"+self.curr_char+"'")
        
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_num(self):
            num_str = ''
            dot = 0
            pos_start = self.pos.copy()
            while self.curr_char != None and self.curr_char in DIGITS + '.':
                if self.curr_char == '.':
                    if dot == 1: break
                    dot += 1
                    num_str += '.'
                else:
                    num_str += self.curr_char
                self.increment()
            if dot == 0:
                return Token(TT_INT, int(num_str), pos_start, self.pos)
            else:
                return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()
        while self.curr_char != None and self.curr_char in LETTERS_DIGITS + '_':
            id_str += self.curr_char
            self.increment()
        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        self.increment()
        while self.curr_char != None and (self.curr_char != '"'):
            string += self.curr_char
            self.increment()
        self.increment()
        return Token(TT_STRING, string, pos_start, self.pos)

    
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.increment()
		
        if self.curr_char == '=':
            self.increment()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.increment()

        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_equals(self):
        tok_type = TT_EQUAL
        pos_start = self.pos.copy()
        self.increment()

        if self.curr_char == '=':
            self.increment()
            tok_type = TT_EE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.increment()

        if self.curr_char == '=':
            self.increment()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.increment()

        if self.curr_char == '=':
            self.increment()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_minus_or_arrow(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.increment()

        if self.curr_char == '>':
            self.increment()
            tok_type = TT_ARROW

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_mul_or_pow(self):
        tok_type = TT_MUL
        pos_start = self.pos.copy()
        self.increment()
        if self.curr_char == '*':
            self.increment()
            tok_type = TT_POW
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def skip_comment(self):
        self.increment()
        while self.curr_char != '\n':
            self.increment()
        self.increment()