import ply.lex as lex


# --------------------------------------------------
# 1. TOKEN NAMES
# --------------------------------------------------

tokens = (
    'CHARACTER', 'IDENTIFIER', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO',
    'ASSIGN', 'EQUAL', 'NOT_EQUAL', 'GREATER', 'LESS',
    'GREATER_EQUAL', 'LESS_EQUAL',
    'SEMICOLON', 'COMMA',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'LBRACKET', 'RBRACKET'
)

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


# --------------------------------------------------
# 2. ERROR REPORTING HELPERS
# --------------------------------------------------

def find_column(data, position):
    """Return the 1-based column of an absolute source offset."""
    return position - data.rfind('\n', 0, position)


def report_error(t, message, error_type="Lexical Error"):
    """Record an error at the start of the current match."""
    t.lexer.errors.append({
        "type": error_type,
        "message": message,
        "line": t.lineno,
        "column": find_column(t.lexer.lexdata, t.lexpos)
    })


# --------------------------------------------------
# 3. OPERATORS
# --------------------------------------------------

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'

t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_GREATER_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_GREATER = r'>'
t_LESS = r'<'
t_ASSIGN = r'='


# --------------------------------------------------
# 4. DELIMITERS
# --------------------------------------------------

t_SEMICOLON = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'


# --------------------------------------------------
# 5. STRINGS AND CHARACTER LITERALS
# --------------------------------------------------

def t_STRING(t):
    r'"([^"\\\n]|\\.)*"'
    return t


def t_UNTERMINATED_STRING(t):
    r'"([^"\\\n]|\\.)*\\?'
    report_error(t, "Unterminated string literal")


def t_CHARACTER(t):
    r"'([^'\\\n]|\\.)'"
    return t


def t_BAD_CHARACTER(t):
    r"'([^'\\\n]|\\.)*'?"
    text = t.value

    if len(text) == 2 and text[1] == "'":
        report_error(t, "Empty character literal")
    elif text.endswith("'") and len(text) > 1:
        report_error(
            t,
            "Character literal must contain exactly one character"
        )
    else:
        report_error(t, "Unterminated character literal")


# --------------------------------------------------
# 6. NUMBERS AND INVALID IDENTIFIERS
# --------------------------------------------------

def t_NUMBER(t):
    r'\d+(\.\d+)?[A-Za-z_][A-Za-z0-9_]*|\d+(\.\d+)?'

    if any(c.isalpha() or c == '_' for c in t.value):
        report_error(
            t,
            f"Invalid identifier '{t.value}'. "
            "Identifiers cannot start with a digit.",
            error_type="Identifier Error"
        )

    return t


# --------------------------------------------------
# 7. IDENTIFIERS AND KEYWORDS
# --------------------------------------------------

def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


# --------------------------------------------------
# 8. WHITESPACE, NEWLINES AND COMMENTS
# --------------------------------------------------

t_ignore = ' \t\r'


def t_COMMENT_SINGLE(t):
    r'//[^\n]*'
    pass


def t_COMMENT_MULTI(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass


def t_COMMENT_UNTERMINATED(t):
    r'/\*[\s\S]*'
    report_error(t, "Unterminated comment")
    t.lexer.lineno += t.value.count('\n')


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# --------------------------------------------------
# 9. INVALID CHARACTERS
# --------------------------------------------------

def t_error(t):
    report_error(t, f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# --------------------------------------------------
# 10. BUILD LEXER
# --------------------------------------------------

lexer = lex.lex()
lexer.errors = []


# --------------------------------------------------
# 11. TOKENIZE SOURCE CODE
# --------------------------------------------------

def tokenize(code):
    """Return (token_list, errors) using a fresh lexer instance."""
    lx = lexer.clone()
    lx.errors = []
    lx.lineno = 1
    lx.input(code)

    token_list = []

    while True:
        token = lx.token()

        if token is None:
            break

        token_list.append({
            "type": token.type,
            "value": token.value,
            "line": token.lineno,
            "column": find_column(code, token.lexpos)
        })

    return token_list, lx.errors