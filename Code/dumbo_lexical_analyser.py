import ply.lex as lex
#Pour sauvegarder les nom de variable et sa/ses valeurs
variables = {}
tmp = []
inListe = False

states = (
    ('inCode', 'exclusive'),
    ('inValue', 'exclusive')
)

reserved = {
    'for' : 'FOR',
    'in' : 'IN',
    'print' : 'PRINT',
    'println' : 'PRINTLN',
    'endfor' : 'ENDFOR',
    'endif' : 'ENDIF',
    'if' : 'IF',
    'do' : 'DO',
    'and' : 'AND',
    'or' : 'OR'
}

tokens = ['HTLM', 'START', 'STOP',
          'BOOL_OP', 'BOOLEAN',
          'INTEGER', 'ADD_OP', 'MULT_OP',
          'VARIABLE', 'ASSIGN', 'VALUE', 'APOSTROPHE', 'OPEN_PAR', 'CLOSE_PAR',
          'COMMA', 'SEMICOLON', 'DOT', 'VAR_BOOL', 'VAR_INT', 'VAR_STR', 'VAR_LIST'
          ] + list(reserved.values())

#Explication

#HTLM: tout ce qui est avant ou apres les START/STOP dans les template, qui est donc de l'HTLM
#START et STOP : "{{", "}}"
#BOOL_OP, BOOLEAN: les opérations booléennes, et les booléens "true" et "false"
#INTEGER, ADD_OP, MULT_OP: un int, opérations + et -, opérations * et /
#VARIABLE: le nom d'une variable
#ASSIGN: l'opérateur assignetion ":="
#VALUE: le(s) valeur(s) d'une variable/constante
#APOSTROPHE: "'", début d'une VALUE
#OPEN_PAR, CLOSE_PAR: "(", ")", début d'une liste de VALUE
#COMMA, SEMICOLON, DOT: ",", ";", "."
#FOR, IN, PRINT, ... : les nom résérvé par le language

##########INITIAL##########

def t_START(t):
    r'{{'
    lexer.begin('inCode')
    return t

def t_HTLM(t):
    r'[^({{)]+'
    return t

t_ignore  = ' \t \n'

def t_error(t):
    print("Character Illegal '%s'" %t.value[0])
    return t

##########IN CODE##########

def t_inCode_STOP(t):
    r'}}'
    t.lexer.begin('INITIAL')
    return t


def t_inCode_BOOLEAN(t):
    r'true|false'
    return t

def t_inCode_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VARIABLE')    # On vérifie les mots reservé
    global variables
    if t.value in variables:
        t.type = changeType(variables[t.value])
    return t

def changeType(data):
    if isinstance(data, bool):
        return "VAR_BOOL"
    elif isinstance(data, int):
        return "VAR_INT"
    elif isinstance(data, str):
        return "VAR_STR"
    elif isinstance(data, list):
        return "VAR_LIST"

def t_inCode_ASSIGN(t):
    r':='
    return t

def t_inCode_APOSTROPHE(t):
    r'\''
    lexer.begin('inValue')
    return t

def t_inCode_OPEN_PAR(t):
    r'\('
    global inListe
    inListe = True
    return t

def t_inCode_CLOSE_PAR(t):
    r'\)'
    #global tmp
    global inListe
    inListe = False
    return t

def t_inCode_BOOL_OP(t):
    r'=|!=|>|<|>=|<='
    return t

def t_inCode_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
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

t_inCode_ignore = ' \n \t'

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
    #if not inListe:
    #    variables[tmp[0]] = tmp[1:]
    return t

def t_inValue_VALUE(t):
    r'[^\']+'
    #global tmp
    #tmp.append(t.value)
    return t

def t_inValue_error(t):
    r'.'
    print("Character Illegal '%s'" %t.value[0])
    return t

###########################

lexer = lex.lex()

def get_variables(data):
    return variables

if __name__ == "__main__":
    import sys

    file = open(sys.argv[1], 'r')
    input = file.read()
    lexer.input(input)

    for token in lexer:
        print("line %d:%s(%s)" % (token.lineno, token.type, token.value))
    for cle, valeur in variables.items():
        print("La clé {} contient la valeur {}.".format(cle, valeur))
