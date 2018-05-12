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
        p[0] = p[1].translate() + p[2]#''.join(str(e) for e in p[1]) + p[2]
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
        p[0] = ExpressionList(p[1], p[3])
    else:
        p[0] = ExpressionList(p[1], None)

# Expression

def p_expression_print(p):
    '''expression : PRINT stringexpression'''
    p[0] = ExprPrint(p[2])

def p_expression_for_strlist(p):
    '''expression : FOR VARIABLE IN stringlist DO expressionslist ENDFOR'''
    global tmp_str, tmp_var
    tmp_str = ""
    for i in range(0, len(p[4])):
        tmp_str += p_expressionslist_expression(p[4][i])
    p[0] = tmp_str

def p_expression_for_var(p):
    '''expression : FOR VARIABLE IN VARIABLE DO expressionslist ENDFOR'''
    p[0] = For(p[2], Variable(p[4]), p[6])

#def p_varinvar_vars(p):
#    '''varinvar : VARIABLE IN VARIABLE'''
#    #global tmp
#    tmp = p[3][1]
#    t = list(tmp)
#    p[0] = (p[1][0],t)

def p_expression_strexpr(p):
    '''expression : VARIABLE ASSIGN stringexpression'''
    tmp = p[3].getValue()
    p[0] = VariableAssignation(Variable(p[1]).name, tmp)

def p_expression_strlist(p):
    '''expression : VARIABLE ASSIGN stringlist'''
    tmp = p[3].getValue()
    p[0] = VariableAssignation(Variable(p[1]).name, tmp)

# String Expression

def p_stringexpression_var(p):
    '''stringexpression : VARIABLE'''
    p[0] = Variable(p[1])

def p_stringexpression_string(p):
    '''stringexpression : string'''
    p[0] = String(p[1].getValue())

def p_stringexpression_string_concat(p):
    '''stringexpression : stringexpression DOT stringexpression'''
    p[0] = Concat(p[1], p[3])

# String List

def p_stringlist_list(p):
    '''stringlist : OPEN_PAR stringlistinterior CLOSE_PAR'''
    p[0] = p[2]

# String List Interior

def p_stringlistinterior_list(p):
    '''stringlistinterior : string
                          | string COMMA stringlistinterior'''
    if len(p) == 4:
        p[0] = StringList(p[1].getValue(), p[3])
    else:
        p[0] = StringList(p[1].getValue(), None)


# Values

def p_string_str(p):
    '''string : APOSTROPHE VALUE APOSTROPHE'''
    p[0] = Value(p[2])

def p_error(p):
    print("Syntax error in input!")

##############################################
##########       STRUCTURE       #############
##############################################

class Expr: pass

class Value(Expr):
    def __init__(self, value):
        self.type = "value"
        self.value = value

    def getValue(self):
        return self.value

class String(Expr):
    def __init__(self, value):
        self.type = "str"
        self.value = value

    def getValue(self):
        return self.value

class StringList(Expr):
    def __init__(self, value, value2):
        self.type = "strlist"
        if value2 == None:
            self.value = [value]
        else:
            self.value =  [value] + value2.getValue()

    def getValue(self):
        return self.value

class Variable(Expr):
    def __init__(self, value):
        global datas
        self.type = "var"
        self.name = value
        if value in datas:
            t = datas[value]
            self.value = t
        elif value in tmp:
            self.value = tmp[value]
        else:
            self.value = []

    def getValue(self):
        if self.name in tmp:
            return tmp[self.name]
        elif self.name in datas:
            t = datas[self.name]
            return  t
        else:
            return ""

class VariableAssignation(Expr):
    def __init__(self, var, value):
        self.type = "expression"
        global datas
        datas[var] = value
        self.value = value

    def getValue(self):
        return self.value

class ExpressionList(Expr):
    def __init__(self, value, value2):
        self.type = "Expr List"
        if value2 is not None:
            self.value = [value] + value2.getValue()
        else:
            self.value = [value]

    def getValue(self):
        return self.value

    def translate(self, v = None):
        str = ""
        for i in self.value:
            if v is not None:
                str += i.translate()
            else:
                str += i.translate()
        return str

class ExprPrint(Expr):
    def __init__(self, value):
        self.type = "print"
        self.value = value

    def translate(self):
        if self.value.type == "str":
            return self.value.getValue()
        elif self.value.type == "var":
            if self.value.name in tmp:
                return ''.join(str(e) for e in tmp[self.value.name])
            elif self.value.name in datas:
                return ''.join(str(e) for e in datas[self.value.name])
        elif self.value.type == "concat":
            return self.value.getValue()
        else:
            return ""

class For(Expr):
    def __init__(self, name, args, exprs):
        self.name = name
        self.args = args
        self.exprs = exprs

    def translate(self):
        str = ""
        global tmp
        if self.args.type == "var":
            liste = self.args.getValue()
            for i in range(0, len(liste)):
                t = tmp
                tmp[self.name] = liste[i]
                str += self.exprs.translate(liste[i])
                tmp = t
        return str

class Concat(Expr):
    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2
        self.type = "concat"

    def getValue(self):
        return self.str1.getValue() + self.str2.getValue()



##############################################

parser = yacc.yacc(outputdir='generated')

def interpreter(data0, template0, output0):
    global output, datas, template
    output = output0
    d =  parser.parse(data0.read())

    print("AAAAAAA")
    template = parser.parse(template0.read(), debug = False)
    print(template)
    if template is not None:
        output0.write(template)


