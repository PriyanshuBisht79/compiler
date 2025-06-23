import ply.lex as lex

# --- Reserved Keywords ---
reserved = {
    'int': 'INT',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT',
}

# --- Token List ---
tokens = [
    'ID', 'EQUALS', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'GT'
] + list(reserved.values())

# --- Token Rules ---
t_EQUALS    = r'='
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_GT        = r'>'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMICOLON = r';'

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# ✅ MUST be at module level
lexer = lex.lex()

# --- Tokenize function used in main.py ---
def tokenize(code):
    lexer.input(code)
    tokens = list(lexer)
    print("TOKENS:", [(t.type, t.value) for t in tokens])
    return tokens

# Optional: run standalone
if __name__ == "__main__":
    code = "int a = 5;"
    tokenize(code)
