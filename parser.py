#Andrew Stephens
#Project 2: Parser
#Dr. Ranjidha Rajan 
#Principles of Programming Languages
#Date: 04/5/2026

import re

#Create TOCKENS list
#????? Modify to your own token list
RR_INT  = 'RR_INTEGER_VAL'
RR_FLOAT = 'RR_FLOAT_VAL'
RR_PLUS  = 'RR_PLUS_OPERATOR'
RR_MINUS = 'RR_MINUS_OPERATOR'
RR_SPACE = 'RR_SPACE_OPERATOR'
RR_MULTIPLY = 'RR_MULTIPLY_OPERATOR'
RR_DIVIDE = 'RR_DIVIDE_OPERATOR'
RR_EQUALS = 'RR_EQUALS_OPERATOR'
RR_PARENTHESIS_OPEN = 'RR_PARENTHESIS_OPEN'
RR_PARENTHESIS_CLOSE = 'RR_PARENTHESIS_CLOSE'
RR_ILLEGAL_CHAR = 'ILLEGAL_Character'
RR_COMMENT = 'RR_COMMENT_Character'

#Create number list 0 to 5
#Added 6789
DIGITS = '0123456789'
OPERATORS = '+-*/=()'


#Token Class from the last project
class Token:
    def __init__(self, type_, value=None, index=None, line=None, column=None):
        self.type = type_
        self.value = value
        self.index = index
        self.line = line
        self.column = column

    def __repr__(self):
        # Formatting value for output
        if self.value is None:
            val = "' '"
        else:
            val = self.value
        return f"Output[{self.type}: {val}, Character Values = Line#: {self.line}, Column#: {self.column}, Index: {self.index}]"


#Lexar Class from the last project
#Create a lexer class constructor as below 
class Lexer:   
    def __init__(self, text):
        self.text = text
        self.pos = -1 
        self.current_char = None
        self.line = 1
        self.column = 0
        self.advance()

    # The advance function to move thru characters
    def advance(self):
        self.pos+=1  
        self.column+=1

        if self.pos < len(self.text):
            self.current_char=self.text[self.pos]
            if self.current_char == '\n':
                self.line+=1
                self.column=0
        else:
            self.current_char=None   
       
    #Tokens placement/Tokens appending with consideration to Index/Column/Line #
    def make_tokens(self):
            tokens = []
            
            while self.current_char is not None:
                self.start_index = self.pos
                self.start_line = self.line
                self.start_column = self.column

                # Handle Comments within input
                if self.current_char == '|':
                    tokens.append(Token(RR_COMMENT, ' | ', self.start_index, self.start_line, self.start_column))
                    while self.current_char is not None and self.current_char != '\n':
                        self.advance()
                    if self.current_char == '\n':
                        self.advance()
                    continue
                #Handles Specific characters
                elif self.current_char == '+':
                    tokens.append(Token(RR_PLUS, '+', self.start_index, self.start_line, self.start_column))
                    self.advance()
                elif self.current_char == '-':
                    tokens.append(Token(RR_MINUS, '-', self.start_index, self.start_line, self.start_column))
                    self.advance()
                elif self.current_char == '*':
                    tokens.append(Token(RR_MULTIPLY, '*', self.start_index, self.start_line, self.start_column))
                    self.advance()
                elif self.current_char == '/':
                    tokens.append(Token(RR_DIVIDE, '/', self.start_index, self.start_line, self.start_column))
                    self.advance()
                elif self.current_char == '=':
                    tokens.append(Token(RR_EQUALS, '=', self.start_index, self.start_line, self.start_column))
                    self.advance()
                elif self.current_char == '(':
                    tokens.append(Token(RR_PARENTHESIS_OPEN, ' " ( " ', self.start_index, self.start_line, self.start_column))
                    self.advance()
                elif self.current_char == ')':
                    tokens.append(Token(RR_PARENTHESIS_CLOSE, ' " ) " ', self.start_index, self.start_line, self.start_column))
                    self.advance()
                elif self.current_char == ' ':
                    tokens.append(Token(RR_SPACE, "' '", self.start_index, self.start_line, self.start_column))
                    self.advance()
                # Handles the numbers with the regex method
                elif self.current_char in DIGITS or self.current_char == '.':
                    # Check for standalone dot (illegal) vs decimal number
                    if self.current_char == '.' and (self.pos + 1 >= len(self.text) or self.text[self.pos + 1] not in DIGITS):
                        tokens.append(self.makeIllegal())
                    else:
                        tokens.append(self.regex_match())
                
                # Handles Illegal Characters
                else: 
                    tokens.append(self.makeIllegal())
        
            return tokens

    #Aligning the regex matching process with the token process
    def regex_match(self):
            self.start_index = self.pos
            self.start_line = self.line
            self.start_column = self.column

            # regex_match Breakdown: 
            # \d* (zero or more digits) 
            # \.? (optional decimal point) 
            # \d+ (one or more digits)
            
            pattern = re.compile(r'\d*\.?\d+') 
            match = pattern.match(self.text[self.pos:])
            if not match:
                return self.makeIllegal()
            num_str = match.group(0)

            #Ciphers between Float and Int Values
            for _ in range(len(num_str)):
                self.advance()
            if '.' in num_str:
                return Token(RR_FLOAT, float(num_str), self.start_index, self.start_line, self.start_column)
            else:
                return Token(RR_INT, int(num_str), self.start_index, self.start_line, self.start_column)

    #The makeIllegal function covers illegal values within the input while also incorporating the comment value.
    def makeIllegal(self):
            illegal_chars = ""
            start_index = self.pos
            start_line = self.line
            start_column = self.column
    #Advances through the character values 
            while self.current_char is not None and self.current_char not in DIGITS + OPERATORS + ' |.':
                illegal_chars += self.current_char
                self.advance()   
    #Advances through the list and then outputs the illegal characters as well as the start colomn of occurance
            print(f"Illegal Character: '{illegal_chars}'")
            print(f"File <stdin>, line {start_line}")
            print(f"Column:{start_column}")
    #Returns the characters with the start index/line/coloumn
            return Token(RR_ILLEGAL_CHAR, f" '{illegal_chars}'", start_index, start_line, start_column)

    # Executing function
    def run(text):
        lexer = Lexer(text)
        tokens = lexer.make_tokens() 
        
        return tokens


class NumberNode:
    def __init__(self, toks):
        self.tok = toks


#Incorporates the BinOp requirement
class BinOpNode:
    def __init__(self, left, op_toks, right):
        self.left = left
        self.op_tok = op_toks
        self.right = right


#Incorporates the UnaryOp requirement
class UnaryOpNode:
    def __init__(self, op_toks, node):
        self.op_tok = op_toks
        self.node = node


#Parser class goes through each value within the input
class Parser:
    def __init__(self, tokens):
        # Removing the space tokens
        self.tokens = [t for t in tokens if t.type != RR_SPACE]
        self.pos = -1
        self.current_tok = None
        self.advance()

    #Advances character index
    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_tok = self.tokens[self.pos]
        else:
            self.current_tok = None
    
    #Covers the empty input and unexpected values
    def parse(self):
        if not self.tokens:
            raise Exception("Empty input")
        result = self.expr()

        if self.current_tok is not None:
            raise Exception(f"Unexpected token: {self.current_tok}")
        return result

    #Encompasses values within expressions, equations
    def expr(self):
        node = self.term()
        while self.current_tok is not None and self.current_tok.type in (RR_PLUS, RR_MINUS):
            op_tok = self.current_tok
            self.advance()
            if self.current_tok is None:
                raise Exception("Missing operand value after operator")

            right = self.term()
            node = BinOpNode(node, op_tok, right)

        return node

    #Encompasses values within expressions, equations
    def term(self):
        node = self.factor()

        while self.current_tok is not None and self.current_tok.type in (RR_MULTIPLY, RR_DIVIDE):
            op_tok = self.current_tok
            self.advance()
            if self.current_tok is None:
                raise Exception("Missing operand after operator")

            right = self.factor()
            node = BinOpNode(node, op_tok, right)

        return node

    def factor(self):
        tok = self.current_tok
        if tok is None:
            raise Exception("Unexpected end of input")

        # Unary operators (+, -)
        if tok.type in (RR_PLUS, RR_MINUS):
            self.advance()
            return UnaryOpNode(tok, self.factor())

        # Numbers with int and float values
        elif tok.type in (RR_INT, RR_FLOAT):
            self.advance()
            return NumberNode(tok)

        # Parentheses values
        elif tok.type == RR_PARENTHESIS_OPEN:
            self.advance()
            node = self.expr()

            if self.current_tok is None or self.current_tok.type != RR_PARENTHESIS_CLOSE:
                raise Exception("Unmatched parenthesis")

            self.advance()
            return node

        raise Exception(f"Unexpected token: {tok}")


#I did use Google Gemini for parts of this print function mainly because I 
# was curious how to format the left and right aspect of the output.
def print_AST(node, indent=0):
    space = "  " * indent
    #Encompasses the number input values
    if isinstance(node, NumberNode):
        print(space + f"Number(' {node.tok.value} ')")
    #Incorporates Unary Operators
    elif isinstance(node, UnaryOpNode):
        print(space + f"Unary Operator(' {node.op_tok.value.strip()} ')")
        print_AST(node.node, indent + 2)
    #Creates division between left and right for output
    elif isinstance(node, BinOpNode):
        print(space + f"BinOp(' {node.op_tok.value.strip()} ')")
        print(space + " Left:")
        print_AST(node.left, indent + 2)
        print(space + " Right:")
        print_AST(node.right, indent + 2)


#Test Cases:

#Submission Page Example
#Input: 1+2*3
#Output: 
'''
TOKENS:
Output[RR_INTEGER_VAL:1, Input = Line#: 1, Column#: 1, Index: 0]
Output[RR_PLUS_OPERATOR: +, Input = Line#: 1, Column#: 2, Index: 1]
Output[RR_INTEGER_VAL:2, Input = Line#: 1, Column#: 3, Index: 2]
Output[RR_MULTIPLY_OPERATOR: *, Input = Line#: 1, Column#: 4, Index: 3]
Output[RR_INTEGER_VAL:3, Input = Line#: 1, Column#: 5, Index: 4]

ABSTRACT SYNTAX TREE (AST):
BinOp(' + ')
 Left:
    Number(' 1 ')
 Right:
    BinOp(' * ')
     Left:
        Number(' 2 ')
     Right:
        Number(' 3 ')
'''

#Submission Page Example
#Input: (1+4)*5+1 
#Output:
'''
TOKENS:
Output[RR_PARENTHESIS_OPEN: (, Input = Line#: 1, Column#: 1, Index: 0]
Output[RR_INTEGER_VAL:1, Input = Line#: 1, Column#: 2, Index: 1]
Output[RR_PLUS_OPERATOR: +, Input = Line#: 1, Column#: 3, Index: 2]
Output[RR_INTEGER_VAL:4, Input = Line#: 1, Column#: 4, Index: 3]
Output[RR_PARENTHESIS_CLOSE: ), Input = Line#: 1, Column#: 5, Index: 4]
Output[RR_MULTIPLY_OPERATOR: *, Input = Line#: 1, Column#: 6, Index: 5]
Output[RR_INTEGER_VAL:5, Input = Line#: 1, Column#: 7, Index: 6]
Output[RR_PLUS_OPERATOR: +, Input = Line#: 1, Column#: 8, Index: 7]
Output[RR_INTEGER_VAL:1, Input = Line#: 1, Column#: 9, Index: 8]

ABSTRACT SYNTAX TREE (AST):
BinOp(' + ')
 Left:
    BinOp(' * ')
     Left:
        BinOp(' + ')
         Left:
            Number(' 1 ')
         Right:
            Number(' 4 ')
     Right:
        Number(' 5 ')
 Right:
    Number(' 1 ')

'''

#Submission Page Example
#Input: 3+)
#Output:
'''
TOKENS:
Output[RR_INTEGER_VAL:3, Character Values = Line#: 1, Column#: 1, Index: 0]
Output[RR_PLUS_OPERATOR: +, Character Values = Line#: 1, Column#: 2, Index: 1]
Output[RR_PARENTHESIS_CLOSE: " ) " , Character Values = Line#: 1, Column#: 3, Index: 2]

PARSING ERROR: Unexpected token: Output[RR_PARENTHESIS_CLOSE: " ) " , Character Values = Line#: 1, Column#: 3, Index: 2]

'''

#Input: |3+3
#Output:
'''
TOKENS:
Output[RR_COMMENT_Character: | , Character Values = Line#: 1, Column#: 1, Index: 0]

PARSING ERROR: Unexpected token: Output[RR_COMMENT_Character: | , Character Values = Line#: 1, Column#: 1, Index: 0]

'''

#Input: 9 - (-5)
#Output:
'''
TOKENS:
Output[RR_INTEGER_VAL:9, Character Values = Line#: 1, Column#: 1, Index: 0]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 2, Index: 1]
Output[RR_MINUS_OPERATOR: -, Character Values = Line#: 1, Column#: 3, Index: 2]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 4, Index: 3]
Output[RR_PARENTHESIS_OPEN: " ( " , Character Values = Line#: 1, Column#: 5, Index: 4]
Output[RR_MINUS_OPERATOR: -, Character Values = Line#: 1, Column#: 6, Index: 5]
Output[RR_INTEGER_VAL:5, Character Values = Line#: 1, Column#: 7, Index: 6]
Output[RR_PARENTHESIS_CLOSE: " ) " , Character Values = Line#: 1, Column#: 8, Index: 7]

ABSTRACT SYNTAX TREE (AST):
BinOp(' - ')
 Left:
    Number(' 9 ')
 Right:
    Unary Operator(' - ')
        Number(' 5 ')

'''

#Input: 10 + (-5)
#Output:
'''
TOKENS:
Output[RR_INTEGER_VAL:10, Character Values = Line#: 1, Column#: 1, Index: 0]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 3, Index: 2]
Output[RR_PLUS_OPERATOR: +, Character Values = Line#: 1, Column#: 4, Index: 3]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 5, Index: 4]
Output[RR_PARENTHESIS_OPEN: " ( " , Character Values = Line#: 1, Column#: 6, Index: 5]
Output[RR_MINUS_OPERATOR: -, Character Values = Line#: 1, Column#: 7, Index: 6]
Output[RR_INTEGER_VAL:5, Character Values = Line#: 1, Column#: 8, Index: 7]
Output[RR_PARENTHESIS_CLOSE: " ) " , Character Values = Line#: 1, Column#: 9, Index: 8]

ABSTRACT SYNTAX TREE (AST):
BinOp(' + ')
 Left:
    Number(' 10 ')
 Right:
    Unary Operator(' - ')
        Number(' 5 ')

'''

#Input: 12 - (10*2) + 5
#Output:
'''
TOKENS:
Output[RR_INTEGER_VAL:12, Character Values = Line#: 1, Column#: 1, Index: 0]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 3, Index: 2]
Output[RR_MINUS_OPERATOR: -, Character Values = Line#: 1, Column#: 4, Index: 3]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 5, Index: 4]
Output[RR_PARENTHESIS_OPEN: " ( " , Character Values = Line#: 1, Column#: 6, Index: 5]
Output[RR_INTEGER_VAL:10, Character Values = Line#: 1, Column#: 7, Index: 6]
Output[RR_MULTIPLY_OPERATOR: *, Character Values = Line#: 1, Column#: 9, Index: 8]
Output[RR_INTEGER_VAL:2, Character Values = Line#: 1, Column#: 10, Index: 9]
Output[RR_PARENTHESIS_CLOSE: " ) " , Character Values = Line#: 1, Column#: 11, Index: 10]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 12, Index: 11]
Output[RR_PLUS_OPERATOR: +, Character Values = Line#: 1, Column#: 13, Index: 12]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 14, Index: 13]
Output[RR_INTEGER_VAL:5, Character Values = Line#: 1, Column#: 15, Index: 14]

ABSTRACT SYNTAX TREE (AST):
BinOp(' + ')
 Left:
    BinOp(' - ')
     Left:
        Number(' 12 ')
     Right:
        BinOp(' * ')
         Left:
            Number(' 10 ')
         Right:
            Number(' 2 ')
 Right:
    Number(' 5 ')

'''

#Input: 8 * (9 - 2)
#Output:
'''
TOKENS:
Output[RR_INTEGER_VAL:8, Character Values = Line#: 1, Column#: 1, Index: 0]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 2, Index: 1]
Output[RR_MULTIPLY_OPERATOR: *, Character Values = Line#: 1, Column#: 3, Index: 2]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 4, Index: 3]
Output[RR_PARENTHESIS_OPEN: " ( " , Character Values = Line#: 1, Column#: 5, Index: 4]
Output[RR_INTEGER_VAL:9, Character Values = Line#: 1, Column#: 6, Index: 5]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 7, Index: 6]
Output[RR_MINUS_OPERATOR: -, Character Values = Line#: 1, Column#: 8, Index: 7]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 9, Index: 8]
Output[RR_INTEGER_VAL:2, Character Values = Line#: 1, Column#: 10, Index: 9]
Output[RR_PARENTHESIS_CLOSE: " ) " , Character Values = Line#: 1, Column#: 11, Index: 10]

ABSTRACT SYNTAX TREE (AST):
BinOp(' * ')
 Left:
    Number(' 8 ')
 Right:
    BinOp(' - ')
     Left:
        Number(' 9 ')
     Right:
        Number(' 2 ')

'''

#Input: 9-(
#Output:
'''
TOKENS:
Output[RR_INTEGER_VAL:9, Character Values = Line#: 1, Column#: 1, Index: 0]
Output[RR_MINUS_OPERATOR: -, Character Values = Line#: 1, Column#: 2, Index: 1]
Output[RR_PARENTHESIS_OPEN: " ( " , Character Values = Line#: 1, Column#: 3, Index: 2]

PARSING ERROR: Unexpected end of input

'''

#Input: 3 + 7 * (2.5)
#Output:
'''
TOKENS:
Output[RR_INTEGER_VAL:3, Character Values = Line#: 1, Column#: 1, Index: 0]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 2, Index: 1]
Output[RR_PLUS_OPERATOR: +, Character Values = Line#: 1, Column#: 3, Index: 2]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 4, Index: 3]
Output[RR_INTEGER_VAL:7, Character Values = Line#: 1, Column#: 5, Index: 4]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 6, Index: 5]
Output[RR_MULTIPLY_OPERATOR: *, Character Values = Line#: 1, Column#: 7, Index: 6]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 8, Index: 7]
Output[RR_PARENTHESIS_OPEN: " ( " , Character Values = Line#: 1, Column#: 9, Index: 8]
Output[RR_FLOAT_VAL:2.5, Character Values = Line#: 1, Column#: 10, Index: 9]
Output[RR_PARENTHESIS_CLOSE: " ) " , Character Values = Line#: 1, Column#: 13, Index: 12]

ABSTRACT SYNTAX TREE (AST):
BinOp(' + ')
 Left:
    Number(' 3 ')
 Right:
    BinOp(' * ')
     Left:
        Number(' 7 ')
     Right:
        Number(' 2.5 ')

'''

#Input: 4 - (2+2.2) * -3
#Output:
'''
TOKENS:
Output[RR_INTEGER_VAL:4, Character Values = Line#: 1, Column#: 1, Index: 0]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 2, Index: 1]
Output[RR_MINUS_OPERATOR: -, Character Values = Line#: 1, Column#: 3, Index: 2]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 4, Index: 3]
Output[RR_PARENTHESIS_OPEN: " ( " , Character Values = Line#: 1, Column#: 5, Index: 4]
Output[RR_INTEGER_VAL:2, Character Values = Line#: 1, Column#: 6, Index: 5]
Output[RR_PLUS_OPERATOR: +, Character Values = Line#: 1, Column#: 7, Index: 6]
Output[RR_FLOAT_VAL:2.2, Character Values = Line#: 1, Column#: 8, Index: 7]
Output[RR_PARENTHESIS_CLOSE: " ) " , Character Values = Line#: 1, Column#: 11, Index: 10]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 12, Index: 11]
Output[RR_MULTIPLY_OPERATOR: *, Character Values = Line#: 1, Column#: 13, Index: 12]
Output[RR_SPACE_OPERATOR:' ', Character Values = Line#: 1, Column#: 14, Index: 13]
Output[RR_MINUS_OPERATOR: -, Character Values = Line#: 1, Column#: 15, Index: 14]
Output[RR_INTEGER_VAL:3, Character Values = Line#: 1, Column#: 16, Index: 15]

ABSTRACT SYNTAX TREE (AST):
BinOp(' - ')
 Left:
    Number(' 4 ')
 Right:
    BinOp(' * ')
     Left:
        BinOp(' + ')
         Left:
            Number(' 2 ')
         Right:
            Number(' 2.2 ')
     Right:
        Unary Operator(' - ')
            Number(' 3 ')

'''



#References:

#https://tomassetti.me/parsing-in-python/

#Google. (2026). Gemini (March 15 version) [Large language model]. 
#https://gemini.google.com/

#Principles of Programming Course
