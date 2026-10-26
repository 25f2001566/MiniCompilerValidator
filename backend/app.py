from flask import Flask, request, jsonify
from flask_cors import CORS

from lexer import tokenize
from identifier_checker import check_identifiers
from pda import validate_brackets
from parser import parse

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Mini Compiler Validator Backend is running!"


@app.route("/validate", methods=["POST"])
def validate():

    data = request.get_json(silent=True) or {}
    code = data.get("code", "")

    tokens, lexical_errors = tokenize(code)

    identifier_errors, _ = check_identifiers(code)

    bracket_errors = validate_brackets(code)

    # CFG syntax validation
    parse_tree = None
    syntax_errors = []

    if not lexical_errors:
        parse_tree, syntax_errors = parse(code)

    success = (
        len(lexical_errors) == 0
        and len(identifier_errors) == 0
        and len(bracket_errors) == 0
        and len(syntax_errors) == 0
        and parse_tree is not None
    )

    return jsonify({
        "success": success,
        "tokens": tokens,
        "lexical_errors": lexical_errors,
        "identifier_errors": identifier_errors,
        "bracket_errors": bracket_errors,
        "syntax_errors": syntax_errors,
        "parse_tree": parse_tree
    })


if __name__ == "__main__":
    app.run(debug=True)