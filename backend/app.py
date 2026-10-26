from flask import Flask, request, jsonify
from flask_cors import CORS

from lexer import tokenize
from identifier_checker import check_identifier_tokens
from pda import validate_brackets
from parser import parse

app = Flask(__name__)
CORS(app)

MAX_CODE_LENGTH = 100_000


@app.route("/")
def home():
    return "Mini Compiler Validator Backend is running!"


def tag(errors, category):
    """Copy errors and label them with the module that found them."""
    return [{**error, "category": category} for error in errors]


def source_order(error):
    return (error.get("line") or 0, error.get("column") or 0)


@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": 'Request body must be JSON like {"code": "..."}'
        }), 400

    code = data.get("code", "")

    if not isinstance(code, str):
        return jsonify({"error": "'code' must be a string"}), 400

    if len(code) > MAX_CODE_LENGTH:
        return jsonify({
            "error": f"Code is too long (limit {MAX_CODE_LENGTH} characters)"
        }), 413

    # Tokenize once and reuse the result
    tokens, lexical_errors = tokenize(code)

    identifier_errors = check_identifier_tokens(tokens)
    bracket_errors = validate_brackets(code)

    # CFG syntax validation and parse-tree generation
    parse_tree = None
    syntax_errors = []

    if not lexical_errors:
        parse_tree, syntax_errors = parse(code)

    # Combine errors and order them by source location
    all_errors = sorted(
        tag(lexical_errors, "lexical")
        + tag(identifier_errors, "identifier")
        + tag(bracket_errors, "bracket")
        + tag(syntax_errors, "syntax"),
        key=source_order
    )

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
        "parse_tree": parse_tree,
        "errors": all_errors
    })


if __name__ == "__main__":
    app.run(debug=True)