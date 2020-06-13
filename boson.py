######################
###### IMPORTS #######
######################

from lexer import *
from parse import *
from interpreter import *
from context import *
from builtin import *

######################
######   RUN   #######
######################

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.create_tokens()
    if error: return None, error
    
    # Generate AST
    parser_ = Parser(tokens)
    ast = parser_.parse()
    if ast.error: return None, ast.error

    # Run Program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)
    return result.value, result.error