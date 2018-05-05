import ply.lex as lex

states = (
    ('inCode', 'exclusive'),
    ('inValue', 'exclusive')
)

tokens = ('START', 'STOP',
          'BOOL_OP',
          'INTEGER', 'ADD_OP', 'MULT_OP',
          'NAME', 'ASSIGN', 'VALUE', 'APOSTROPHE', 'OPEN_PAR', 'CLOSE_PAR',
          'COMMA', 'SEMICOLON', 'DOT'
          )
# Pour ici? 'FOR', 'IN', 'PRINT', 'ENDFOR', 'DO', 'AND', 'OR','BOOLEAN', 'VALUE','TEXT', 'NAME',

#Explication

#START et STOP : "{{", "}}"
#BOOL_OP: les opérations booléennes
#INTEGER, ADD_OP, MULT_OP: un int, opérations + et -, opérations * et /
#NAME: une variable/constante à laquelle on attribue une valeur
#ASSIGN: l'opérateur assignetion ":="
#VALUE: le(s) valeur(s) d'une variable/constante
#APOSTROPHE: "'", début d'une VALUE
#OPEN_PAR, CLOSE_PAR: "(", ")", début d'une liste de VALUE
#COMMA, SEMICOLON, DOT: ",", ";", "."

##########INITIAL##########

def t_START(t):
    r'{{'
    lexer.begin('inCode')
    return t

t_ignore  = ' \t \n'

def t_error(t):
    print(t)
    print(t.value[0])
    print("Character Illegal '%s'" %t.value[0])
    return t

##########IN CODE##########

def t_inCode_STOP(t):
    r'}}'
    t.lexer.begin('INITIAL')
    return t

def t_inCode_NAME(t):
    r'\w+'
    return t

def t_inCode_ASSIGN(t):
    r':='
    return t

def t_inCode_APOSTROPHE(t):
    r'\''
    lexer.begin('inValue')
    return t

def t_inCode_OPEN_PAR(t):
    r'\('
    return t

def t_inCode_CLOSE_PAR(t):
    r'\)'
    return t

def t_inCode_BOOL_OP(t):
    r'=|!=|>|<|>=|<='
    return t

def t_inCode_INTEGER(t):
    r'\d+'
    return t

def t_inCode_ADD_OP(t):
    r'\+|-'
    return t

def t_inCode_MULT_OP(t):
    r'\*|/'
    return t

def t_inCode_COMMA(t):
    r','
    return t

def t_inCode_SEMICOLON(t):
    r';'
    return t

def t_inCode_DOT(t):
    r'\.'
    return t

t_inCode_ignore  = ' \n \t'

def t_inCode_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_inCode_error(t):
    print("Character Illegal '%s'" %t.value[0])
    return t

#########IN VALUE#########

def t_inValue_APOSTROPHE(t):
    r'\''
    t.lexer.begin('inCode')
    return t

def t_inValue_VALUE(t):
    r'[^\']+'
    return t

def t_inValue_error(t):
    r'.'
    print("Character Illegal '%s'" %t.value[0])
    return t


###########################
if __name__ == "__main__":
    import sys

    lexer = lex.lex()
    file = open(sys.argv[1], 'r')
    input = file.read()
    lexer.input(input)

    for token in lexer:
        print("line %d:%s(%s)" % (token.lineno, token.type, token.value))
