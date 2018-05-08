import ply.yacc as yacc

from Code.dumbo_lexical_analyser import tokens
from Code.dumbo_lexical_analyser import get_variables

output = 0
data = 0
template = 0

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


def p_expr_htlm(p):
    ''' expr : HTLM'''
    p[0] = p[1]

#def p_programme_dumbloc(p):
#    ''' programme : START expressions_liste STOP'''
#    p[0] = p[2]



def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc(outputdir='generated')

def interpreter(data0, template0, output0):
    global output, data, template
    output = output0
    output.write('a')
    d =  parser.parse(data0.read())

    #Datas contient les variables a mette dans les templates, c'est un dictionnaire
    datas = get_variables(data0)
    print(datas)

    template = parser.parse(template0.read())
    output0.write(template)


