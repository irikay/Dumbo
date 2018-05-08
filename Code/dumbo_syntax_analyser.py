import ply.yacc as yac

from Code.dumbo_lexical_analyser import tokens

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '=': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '>': lambda x, y: x > y,
    '>=': lambda x, y: x >= y,
    '<': lambda x, y: x < y,
    '<=': lambda x, y: x <= y
}

precedence = (
    ('left', "BOOL_OP"),
    ("left", "ADD_OP"),
    ("left", "MUL_OP"),
)

def p_expression_op(p):
    ''' expression : expression ADD_OP expression
                   : expression MULT_OP expression
                   : expression BOOL_OP expression'''
    p[0] = operations[p[2]](p[1], p[3])






