
import ply.lex as lex

errors = []

# 1. TOKEN NAMES
tokens = (
    'CHARACTER', 'IDENTIFIER', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO',
    'ASSIGN', 'EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS',
    'GREATER_EQUAL', 'LESS_EQUAL',
    'SEMICOLON', 'COMMA',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET'
)

# 2. KEYWORDS
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'return': 'RETURN',
    'printf': 'PRINTF'
}

tokens = tokens + tuple(reserved.values())

# 3. OPERATORS
t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_GREATER_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_GREATER = r'>'
t_LESS = r'<'

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_ASSIGN = r'='

# 4. DELIMITERS
t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# 5. STRING LITERALS
def t_STRING(t):
    r'"([^"\\\n]|\\.)*"'
    return t

def t_CHARACTER(t):
    r"'([^'\\\n]|\\.)'"
    return t

# 6. NUMBERS AND INVALID IDENTIFIERS
# Match a number followed directly by identifier characters
# as one invalid token, e.g. 2value or 123abc.
def t_NUMBER(t):
    r'\d+(\.\d+)?[A-Za-z_][A-Za-z0-9_]*|\d+(\.\d+)?'

    if any(c.isalpha() or c == '_' for c in t.value):
        errors.append({
            "type": "Identifier Error",
            "message": (
                f"Invalid identifier '{t.value}'. "
                "Identifiers cannot start with a digit."
            ),
            "value": t.value,
            "line": t.lineno,
            "column": t.lexpos
        })

    return t

# 7. IDENTIFIERS AND KEYWORDS
def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# 8. COMMENTS
def t_COMMENT_SINGLE(t):
    r'//[^\n]*'
    pass

def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# 9. LINE NUMBERS
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 10. IGNORE WHITESPACE
t_ignore = ' \t\r'

# 11. INVALID CHARACTERS
def t_error(t):
    errors.append({
        "type": "Lexical Error",
        "message": f"Illegal character '{t.value[0]}'",
        "line": t.lineno,
        "column": t.lexpos
    })
    t.lexer.skip(1)

# 12. BUILD LEXER
lexer = lex.lex()

# 13. TOKENIZE SOURCE CODE
def tokenize(code):
    global errors

    errors = []
    lexer.lineno = 1
    lexer.input(code)

    token_list = []

    while True:
        token = lexer.token()
        if token is None:
            break

        token_list.append({
            "type": token.type,
            "value": token.value,
            "line": token.lineno
        })

    return token_list, errors
