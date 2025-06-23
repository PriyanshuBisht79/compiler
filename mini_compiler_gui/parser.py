import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'GT'),
)

class Node:
    def __init__(self, type, children=None, value=None):
        self.type = type
        self.children = children if children else []
        self.value = value

def p_program(p):
    "program : statements"
    p[0] = Node("Program", p[1])

def p_statements(p):
    "statements : statement statements"
    p[0] = [p[1]] + p[2]

def p_statements_single(p):
    "statements : statement"
    p[0] = [p[1]]

def p_statement_decl(p):
    "statement : INT ID EQUALS expression SEMICOLON"
    p[0] = Node("Declare", [Node("ID", value=p[2]), p[4]])

def p_statement_if(p):
    "statement : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE"
    p[0] = Node("IfElse", [p[3], Node("Block", p[6]), Node("Block", p[10])])

def p_statement_print(p):
    "statement : PRINT LPAREN expression RPAREN SEMICOLON"
    p[0] = Node("Print", [p[3]])

def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = Node("BinOp", [p[1], p[3]], p[2])

def p_expression_term(p):
    "expression : term"
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = Node("BinOp", [p[1], p[3]], p[2])

def p_term_factor(p):
    "term : factor"
    p[0] = p[1]

def p_factor_group(p):
    "factor : LPAREN expression RPAREN"
    p[0] = p[2]

def p_factor_num(p):
    "factor : NUMBER"
    p[0] = Node("Number", value=p[1])

def p_factor_id(p):
    "factor : ID"
    p[0] = Node("ID", value=p[1])


def p_expression_gt(p):
    "expression : expression GT term"
    p[0] = Node("GT", [p[1], p[3]])

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        print("Syntax error at end of file (EOF)")

parser = yacc.yacc(debug=True, write_tables=False)

def parse(code):
    return parser.parse(code)
