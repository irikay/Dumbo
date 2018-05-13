import ply.yacc as yacc

from Code.dumbo_lexical_analyser import tokens
from Code.dumbo_lexical_analyser import variables

variables = variables

output = 0
template = 0
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
    '<=': lambda x, y: x <= y,
    'or': lambda x, y: x or y,
    'and': lambda x, y: x and y
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
        p[0] = p[1].translate()

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

def p_expression_print2(p):
    '''expression : PRINT VAR_INT
                  | PRINT VAR_BOOL
                  | PRINT VARIABLE'''
    p[0] = ExprPrint(Variable(p[2]))

def p_expression_println(p):
    '''expression : PRINTLN stringexpression'''
    p[0] = ExprPrintln(p[2])

def p_expression_println2(p):
    '''expression : PRINTLN VAR_INT
                  | PRINTLN VAR_BOOL
                  | PRINTLN VARIABLE'''
    p[0] = ExprPrintln(Variable(p[2]))

def p_expression_for_strlist(p):
    '''expression : FOR VARIABLE IN stringlist DO expressionslist ENDFOR
                  | FOR VAR_INT IN stringlist DO expressionslist ENDFOR
                  | FOR VAR_STR IN stringlist DO expressionslist ENDFOR
                  | FOR VAR_LIST IN stringlist DO expressionslist ENDFOR
                  | FOR VAR_BOOL IN stringlist DO expressionslist ENDFOR'''
    p[0] = For(p[2], p[4], p[6])

def p_expression_for_var(p):
    '''expression : FOR VARIABLE IN VAR_LIST DO expressionslist ENDFOR
                  | FOR VAR_INT IN VAR_LIST DO expressionslist ENDFOR
                  | FOR VAR_STR IN VAR_LIST DO expressionslist ENDFOR
                  | FOR VAR_LIST IN VAR_LIST DO expressionslist ENDFOR
                  | FOR VAR_BOOL IN VAR_LIST DO expressionslist ENDFOR'''
    p[0] = For(p[2], Variable(p[4]), p[6])

def p_expression_if(p):
    '''expression : IF booleanexpr DO expressionslist ENDIF'''
    if p[2]:
        p[0] = p[4]
    else:
        p[0] = NullExpr()


def p_expression_strexpr_assign(p):
    '''expression : VARIABLE ASSIGN stringexpression
                  | VAR_LIST ASSIGN stringexpression
                  | VAR_INT ASSIGN stringexpression
                  | VAR_BOOL ASSIGN stringexpression
                  | VAR_STR ASSIGN stringexpression'''
    tmp = p[3].getValue()
    p[0] = VariableAssignation(Variable(p[1]).name, tmp)

def p_expression_bool_assign(p):
    '''expression : VARIABLE ASSIGN booleanexpr
                  | VAR_LIST ASSIGN booleanexpr
                  | VAR_INT ASSIGN booleanexpr
                  | VAR_BOOL ASSIGN booleanexpr
                  | VAR_STR ASSIGN booleanexpr'''
    tmp = p[3]
    p[0] = VariableAssignation(Variable(p[1]).name, tmp)

def p_expression_int_assign(p):
    '''expression : VARIABLE ASSIGN intexpr
                  | VAR_LIST ASSIGN intexpr
                  | VAR_INT ASSIGN intexpr
                  | VAR_BOOL ASSIGN intexpr
                  | VAR_STR ASSIGN intexpr'''
    tmp = p[3]
    p[0] = VariableAssignation(Variable(p[1]).name, tmp)

def p_expression_strlist_assign(p):
    '''expression : VARIABLE ASSIGN stringlist
                  | VAR_LIST ASSIGN stringlist
                  | VAR_INT ASSIGN stringlist
                  | VAR_BOOL ASSIGN stringlist
                  | VAR_STR ASSIGN stringlist'''
    tmp = p[3].getValue()
    p[0] = VariableAssignation(Variable(p[1]).name, tmp)

# Boolean Expression

def p_booleanexpr_var(p):
    '''booleanexpr : VAR_BOOL'''
    p[0] = Variable(p[1]).getValue()

def p_booleanexpr_bool(p):
    '''booleanexpr : BOOLEAN'''
    if p[1] == "true":
        p[0] = True
    else:
        p[0] = False

def p_booleanexpr_booleans(p):
    '''booleanexpr : booleanexpr BOOL_OP booleanexpr
                   | booleanexpr BOOL_OP intexpr
                   | intexpr BOOL_OP booleanexpr
                   | intexpr BOOL_OP intexpr
                   | booleanexpr OR booleanexpr
                   | booleanexpr AND booleanexpr'''
    p[0] = operations[p[2]](p[1], p[3])

# Integer Expression

def p_intexpr_var(p):
    '''intexpr : VAR_INT'''
    p[0] = Variable(p[1]).getValue()

def p_intexpr_int(p):
    '''intexpr : INTEGER'''
    p[0] = int(p[1])

def p_intexpr_int_op(p):
    '''intexpr :  intexpr ADD_OP intexpr
                | intexpr MULT_OP intexpr'''
    p[0] = operations[p[2]](p[1], p[3])

# String Expression

def p_stringexpression_var(p):
    '''stringexpression : VAR_STR'''
    p[0] = Variable(p[1])

def p_stringexpression_varlist(p):
    '''stringexpression : VAR_LIST'''
    p[0] = Variable(p[1])


def p_stringexpression_string(p):
    '''stringexpression : string'''
    p[0] = String(p[1].getValue())

def p_stringexpression_string_concat(p):
    '''stringexpression : stringexpression DOT stringexpression
                        |  VARIABLE DOT VARIABLE
                        |  stringexpression DOT VARIABLE
                        |  VARIABLE DOT stringexpression'''
    if isinstance(p[1], str):
        p[1] = Variable(p[1])
    if isinstance(p[3], str):
        p[3] = Variable(p[3])
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

class Concat(Expr):
    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2
        self.type = "concat"

    def getValue(self):
        return self.str1.getValue() + self.str2.getValue()

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
        global variables
        self.type = "var"
        self.name = value
        if value in variables:
            t = variables[value]
            self.value = t
        elif value in tmp:
            self.value = tmp[value]
        else:
            self.value = []

    def getValue(self):
        if self.name in tmp:
            return tmp[self.name]
        elif self.name in variables:
            t = variables[self.name]
            return  t
        else:
            return ""

class VariableAssignation(Expr):
    def __init__(self, var, value):
        self.type = "expression"
        self.var = var
        self.value = value
        variables[var] = value
        print(value)
        print(var)
        global variables


    def getValue(self):
        return self.value

    def translate(self):
        global variables
        variables[self.var] = self.value
        return ""

class ExpressionList(Expr):
    def __init__(self, value, value2):
        self.type = "Expr List"
        if value2 is not None:
            self.value = [value] + value2.getValue()
        else:
            self.value = [value]

    def getValue(self):
        return self.value

    def translate(self):
        str = ""
        for i in self.value:
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
                if isinstance(tmp[self.value.name], int):
                    return str(tmp[self.value.name])
                else:
                    return ''.join(str(e) for e in tmp[self.value.name])
            elif self.value.name in variables:
                if isinstance(variables[self.value.name], int):
                    return str(variables[self.value.name])
                else:
                    return ''.join(str(e) for e in variables[self.value.name])
            else:
                return ""
        elif self.value.type == "concat":
            return self.value.getValue()
        else:
            return ""

class ExprPrintln(Expr):
    def __init__(self, value):
        self.type = "print"
        self.value = value

    def translate(self):
        if self.value.type == "str":
            return self.value.getValue() + "\n"
        elif self.value.type == "var":
            if self.value.name in tmp:
                if isinstance(tmp[self.value.name], int):
                    return str(tmp[self.value.name]) + "\n"
                else:
                    return ''.join(str(e) for e in tmp[self.value.name]) + "\n"
            elif self.value.name in variables:
                if isinstance(variables[self.value.name], int):
                    return str(variables[self.value.name]) + "\n"
                else:
                    return ''.join(str(e) for e in variables[self.value.name]) + "\n"
            else:
                return ""+ "\n"
        elif self.value.type == "concat":
            return self.value.getValue() + "\n"
        else:
            return "" + "\n"

class For(Expr):
    def __init__(self, name, args, exprs):
        self.name = name
        self.args = args
        self.exprs = exprs

    def translate(self):
        str = ""
        global tmp
        if self.args.type == "var" or self.args.type == "strlist":
            liste = self.args.getValue()
            print(list)
            for i in range(0, len(liste)):
                t = tmp
                tmp[self.name] = liste[i]
                str += self.exprs.translate()
                tmp = t

        return str

class If(Expr):
    def __init__(self, exprs):
        self.exprs = exprs

    def translate(self):
        return self.exprs.translate()

class NullExpr(Expr):
    def __init__(self):
        self.type = "null"

    def translate(self):
        return ""


##############################################

parser = yacc.yacc(outputdir='generated')

def interpreter(data0, template0, output0):
    global output, variables, template
    output = output0
    d =  parser.parse(data0.read())
    print("AAAAAAA")
    template = parser.parse(template0.read(), debug = False)
    print(template)
    if template is not None:
        output0.write(template)


