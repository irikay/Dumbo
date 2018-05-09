import ply.yacc as yacc

from Code.dumbo_lexical_analyser import tokens
from Code.dumbo_lexical_analyser import get_variables

output = 0
data = 0
template = 0
datas = {}

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
    ("left", "MULT_OP")
)

# Programme

def p_programme_htlm(p):
    '''programme : HTLM'''
    p[0] = p[1]

def p_programme_programme(p):
    '''programme : HTLM programme'''
    p[0] = p[1] + ''.join(str(e) for e in p[2])

def p_programme_dumbloc(p):
    '''programme : dumbloc
                  | dumbloc programme'''
    if len(p) == 3:
        print(p[1])
        p[0] = ''.join(str(e) for e in p[1]) + p[2]
    else:
        p[0] = p[1]

# Dumbloc

def p_dumbloc_bloc(p):
    '''dumbloc : START expressionslist STOP'''
    p[0] = p[2]

# Expressions List

def p_expressionslist_expr(p):
    '''expressionslist : expression SEMICOLON'''
    p[0] = p[1]

def p_expressionslist_exprs(p):
    ''' expressionslist : expression SEMICOLON expressionslist'''
    p[0] = p[1] + p[3]

# Expression

def p_expression_print(p):
    '''expression : PRINT stringexpression'''
    p[0] = p[2]

def p_expression_variable(p):
    '''expression : VARIABLE ASSIGN values'''
    p[0] = p[3]

# String Expression

def p_stringexpression_var(p):
    '''stringexpression : VARIABLE'''
    p[0] = datas.get(p[1])

def p_stringexpression_apostrophe_var(p):
    '''stringexpression : APOSTROPHE VALUE APOSTROPHE'''
    p[0] = p[2]

# Values

def p_values_val(p):
    '''values : APOSTROPHE VALUE APOSTROPHE'''
    p[0] = p[2]

def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc(outputdir='generated')

def interpreter(data0, template0, output0):
    global output, data, template
    output = output0
    d =  parser.parse(data0.read())
    #Datas contient les variables a mette dans les templates, c'est un dictionnaire
    global datas
    datas = get_variables(data0)

    template = parser.parse(template0.read())
    print(template)
    if template is not None:
        output0.write(template)


