import ply.yacc as yacc
from lexer import tokens


# --------------------------------------------------
# PARSER ERRORS
# --------------------------------------------------

parser_errors = []


# --------------------------------------------------
# PROGRAM
# --------------------------------------------------

def p_program(p):
    """
    program : function_definition
    """
    p[0] = ("program", p[1])


# --------------------------------------------------
# FUNCTION DEFINITION
# --------------------------------------------------

def p_function_definition(p):
    """
    function_definition : datatype IDENTIFIER LPAREN RPAREN block
    """
    p[0] = (
        "function_definition",
        p[1],
        p[2],
        p[5]
    )


# --------------------------------------------------
# BLOCK
# --------------------------------------------------

def p_block(p):
    """
    block : LBRACE statement_list RBRACE
    """
    p[0] = ("block", p[2])


# --------------------------------------------------
# STATEMENT LIST
# --------------------------------------------------

def p_statement_list_recursive(p):
    """
    statement_list : statement statement_list
    """
    p[0] = [p[1]] + p[2]


def p_statement_list_empty(p):
    """
    statement_list : empty
    """
    p[0] = []


# --------------------------------------------------
# STATEMENT
# --------------------------------------------------

def p_statement(p):
    """
    statement : declaration
               | assignment
               | if_statement
               | while_statement
               | printf_statement
               | return_statement
    """
    p[0] = p[1]


# --------------------------------------------------
# DATA TYPE
# --------------------------------------------------

def p_datatype(p):
    """
    datatype : INT
             | FLOAT
             | CHAR
    """
    p[0] = ("datatype", p[1])


# --------------------------------------------------
# DECLARATION
# --------------------------------------------------

def p_declaration_simple(p):
    """
    declaration : datatype IDENTIFIER SEMICOLON
    """
    p[0] = (
        "declaration",
        p[1],
        p[2]
    )


def p_declaration_initialized(p):
    """
    declaration : datatype IDENTIFIER ASSIGN expression SEMICOLON
    """
    p[0] = (
        "declaration",
        p[1],
        p[2],
        p[4]
    )


# --------------------------------------------------
# ASSIGNMENT
# --------------------------------------------------

def p_assignment(p):
    """
    assignment : IDENTIFIER ASSIGN expression SEMICOLON
    """
    p[0] = (
        "assignment",
        p[1],
        p[3]
    )


# --------------------------------------------------
# IF STATEMENT
# --------------------------------------------------

def p_if_statement(p):
    """
    if_statement : IF LPAREN condition RPAREN block
                 | IF LPAREN condition RPAREN block ELSE block
    """

    if len(p) == 6:
        p[0] = (
            "if_statement",
            p[3],
            p[5]
        )

    else:
        p[0] = (
            "if_statement",
            p[3],
            p[5],
            p[7]
        )


# --------------------------------------------------
# WHILE STATEMENT
# --------------------------------------------------

def p_while_statement(p):
    """
    while_statement : WHILE LPAREN condition RPAREN block
    """
    p[0] = (
        "while_statement",
        p[3],
        p[5]
    )


# --------------------------------------------------
# PRINTF STATEMENT
# --------------------------------------------------

def p_printf_statement(p):
    """
    printf_statement : PRINTF LPAREN printf_arguments RPAREN SEMICOLON
    """
    p[0] = (
        "printf_statement",
        p[3]
    )


# --------------------------------------------------
# PRINTF ARGUMENTS
# --------------------------------------------------

def p_printf_arguments_string(p):
    """
    printf_arguments : STRING
    """
    p[0] = [("string", p[1])]


def p_printf_arguments_with_expressions(p):
    """
    printf_arguments : STRING COMMA argument_list
    """
    p[0] = [
        ("string", p[1])
    ] + p[3]


# --------------------------------------------------
# ARGUMENT LIST
# --------------------------------------------------

def p_argument_list_expression(p):
    """
    argument_list : expression
    """
    p[0] = [p[1]]


def p_argument_list_multiple(p):
    """
    argument_list : expression COMMA argument_list
    """
    p[0] = [p[1]] + p[3]


# --------------------------------------------------
# RETURN STATEMENT
# --------------------------------------------------

def p_return_statement(p):
    """
    return_statement : RETURN expression SEMICOLON
    """
    p[0] = (
        "return_statement",
        p[2]
    )


# --------------------------------------------------
# CONDITION
# --------------------------------------------------

def p_condition(p):
    """
    condition : expression relational_operator expression
    """
    p[0] = (
        "condition",
        p[1],
        p[2],
        p[3]
    )


# --------------------------------------------------
# RELATIONAL OPERATOR
# --------------------------------------------------

def p_relational_operator(p):
    """
    relational_operator : GREATER
                        | LESS
                        | GREATER_EQUAL
                        | LESS_EQUAL
                        | EQUAL
                        | NOT_EQUAL
    """
    p[0] = p[1]


# --------------------------------------------------
# EXPRESSION
# --------------------------------------------------

def p_expression_plus(p):
    """
    expression : expression PLUS term
    """
    p[0] = (
        "binary_expression",
        "+",
        p[1],
        p[3]
    )


def p_expression_minus(p):
    """
    expression : expression MINUS term
    """
    p[0] = (
        "binary_expression",
        "-",
        p[1],
        p[3]
    )


def p_expression_term(p):
    """
    expression : term
    """
    p[0] = p[1]


# --------------------------------------------------
# TERM
# --------------------------------------------------

def p_term_multiply(p):
    """
    term : term MULTIPLY factor
    """
    p[0] = (
        "binary_expression",
        "*",
        p[1],
        p[3]
    )


def p_term_divide(p):
    """
    term : term DIVIDE factor
    """
    p[0] = (
        "binary_expression",
        "/",
        p[1],
        p[3]
    )


def p_term_modulo(p):
    """
    term : term MODULO factor
    """
    p[0] = (
        "binary_expression",
        "%",
        p[1],
        p[3]
    )


def p_term_factor(p):
    """
    term : factor
    """
    p[0] = p[1]


# --------------------------------------------------
# FACTOR
# --------------------------------------------------

def p_factor_number(p):
    """
    factor : NUMBER
    """
    p[0] = ("number", p[1])


def p_factor_character(p):
    """
    factor : CHARACTER
    """
    p[0] = ("character", p[1])


def p_factor_identifier(p):
    """
    factor : IDENTIFIER
    """
    p[0] = ("identifier", p[1])


def p_factor_expression(p):
    """
    factor : LPAREN expression RPAREN
    """
    p[0] = p[2]


# --------------------------------------------------
# EMPTY
# --------------------------------------------------

def p_empty(p):
    """
    empty :
    """
    p[0] = []


# --------------------------------------------------
# SYNTAX ERROR
# --------------------------------------------------

def p_error(p):
    if p:
        parser_errors.append({
            "type": "Syntax Error",
            "message": f"Unexpected token '{p.value}'",
            "line": getattr(p, "lineno", 0)
        })
    else:
        parser_errors.append({
            "type": "Syntax Error",
            "message": "Unexpected end of input",
            "line": 0
        })


# --------------------------------------------------
# BUILD PARSER
# --------------------------------------------------

parser = yacc.yacc()


# --------------------------------------------------
# PARSE FUNCTION
# --------------------------------------------------

def parse(code):
    """
    Parse Mini-C source code.

    Returns:
        parse_tree, syntax_errors
    """

    global parser_errors

    parser_errors = []

    from lexer import lexer

    lexer.lineno = 1
    result = parser.parse(code, lexer=lexer)

    return result, parser_errors