import ply.yacc as yacc

from Code.dumbo_lexical_analyser import tokens
from Code.dumbo_lexical_analyser import variables

output = 0
datas = 0
template = 0
datas = {}
tmp = {}

tmp_str = ""
tmp_var = []

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
        p[0] = ''.join(str(e) for e in p[1]) + p[2]
    else:
        p[0] = p[1]

# Dumbloc

def p_dumbloc_bloc(p):
    '''dumbloc : START expressionslist STOP'''
    p[0] = p[2]

# Expressions List

def p_expressionslist_expression(p):
    '''expressionslist : expression SEMICOLON
                       | expression SEMICOLON expressionslist'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

# Expression

def p_expression_print(p):
    '''expression : PRINT stringexpression'''
    p[0] = p[2]

def p_expression_for_strlist(p):
    '''expression : FOR VARIABLE IN stringlist DO expressionslist ENDFOR'''
    global tmp_str, tmp_var
    tmp_str = ""
    for i in range(0, len(p[4])):
        tmp_str += p_expressionslist_expression(p[4][i])
    p[0] = tmp_str

def p_expression_for_var(p):
    '''expression : FOR varinvar DO expressionslist ENDFOR'''
    global tmp_str
    tmp_str = ""
    for i in range(0,  len(p[2])):
        tmp_str += ''.join(str(e) for e in p[4])
    p[0] = tmp_str

def p_varinvar_vars(p):
    '''varinvar : VARIABLE IN VARIABLE'''
    global tmp
    tmp[p[1]] = datas[p[3]]
    t = list(tmp[p[1]])
    p[0] = t

def p_expression_strexpr(p):
    '''expression : VARIABLE ASSIGN stringexpression'''
    global datas
    datas[p[1]] = p[3]
    p[0] = p[3]

def p_expression_strlist(p):
    '''expression : VARIABLE ASSIGN stringlist'''
    global datas
    l_tmp = p[3]
    datas[p[1]] = l_tmp
    p[0] = p[3]

# String Expression

def p_stringexpression_var(p):
    '''stringexpression : VARIABLE'''
    if p[1] in tmp:
        t = tmp[p[1]]
        t2 = t.pop(0)
        tmp[p[1]] = t
        #if len(tmp[p[1]]) == 0:
            #
        p[0] = t2
    elif p[1] in datas:
        p[0] = datas[p[1]]
    else:
        p[0] = p[1]

def p_stringexpression_string(p):
    '''stringexpression : string'''
    p[0] = p[1]

def p_stringexpression_string_concat(p):
    '''stringexpression : stringexpression DOT stringexpression'''
    p[0] = p[1] + p[3]

# String List

def p_stringlist_list(p):
    '''stringlist : OPEN_PAR stringlistinterior CLOSE_PAR'''
    p[0] = p[2]

# String List Interior

def p_stringlistinterior_list(p):
    '''stringlistinterior : string
                          | string COMMA stringlistinterior'''
    if len(p) == 4:
        p[0] = [p[1]] + (p[3])
    else:
        p[0] = [p[1]]


# Values

def p_string_str(p):
    '''string : APOSTROPHE VALUE APOSTROPHE'''
    p[0] = p[2]

def p_error(p):
    print("Syntax error in input!")


parser = yacc.yacc(outputdir='generated')

def interpreter(data0, template0, output0):
    global output, datas, template
    output = output0
    d =  parser.parse(data0.read())

    template = parser.parse(template0.read(), debug = False)
    print(template)
    if template is not None:
        output0.write(template)


