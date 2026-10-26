# MiniCompilerValidator
### A TOC-Powered Mini-C Code Analyzer

MiniCompilerValidator is a web-based tool for analyzing a subset of C-like Mini-C source code. It combines lexical analysis, identifier validation, bracket verification, context-free grammar (CFG) parsing, and parse-tree visualization in an interactive interface.

The project demonstrates how concepts from **Theory of Computation (TOC)** and compiler design can be applied to source-code validation.

## Table of Contents

- [Overview](#overview)
- [Objectives](#objectives)
- [Features](#features)
- [Theory of Computation Concepts](#theory-of-computation-concepts)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Example Programs](#example-programs)
- [Testing](#testing)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)

## Overview

The application accepts Mini-C source code through a browser-based editor and sends it to a Python Flask backend for analysis.

The backend processes the source code through multiple validation stages and returns structured results. The frontend displays recognized tokens, identifier information, validation errors, syntax-analysis results, and the parse tree when available.

The goal is to make compiler-analysis concepts easier to understand through an interactive visual interface.

## Objectives

- Implement a lexical analyzer for a subset of C-like syntax.
- Validate identifiers using a deterministic finite automaton (DFA).
- Check matching brackets using a stack-based pushdown automaton (PDA).
- Validate program syntax using a CFG-based parser.
- Generate and visualize a parse tree for supported valid programs.
- Integrate the analysis modules into a web application.
- Present validation results and errors in an understandable format.

## Features

### 1. Lexical Analysis

The lexer, implemented using Python's PLY library, converts source code into tokens.

It recognizes supported keywords, identifiers, numeric and string literals, operators, delimiters, and comments. It also reports lexical errors, such as illegal characters and malformed literals where supported.

### 2. Identifier Validation

The identifier-validation module checks identifier tokens against the project's identifier rules using DFA-based validation.

It helps identify invalid identifier names, including names that begin with digits.

### 3. Bracket Validation

The PDA module checks matching parentheses, curly braces, and square brackets using a stack.

It can report unexpected closing brackets, mismatched brackets, and missing closing brackets. The implementation also accounts for brackets inside strings and comments.

### 4. CFG-Based Syntax Analysis

The parser checks whether source code follows the supported Mini-C grammar.

The implemented grammar includes supported constructs such as function definitions, declarations, assignments, conditional statements, loops, output statements, return statements, and expressions.

### 5. Parse-Tree Visualization

For programs accepted by the parser, the frontend displays a tree representing the parser's output.

This visualization helps users understand the hierarchical structure of a program and the relationship between grammar constructs.

### 6. Interactive Web Interface

The browser interface provides a source-code editor and displays tokens, identifier results, validation status, errors, and parse-tree information.

### 7. Backend API

A Flask API receives source code as JSON, runs the validation modules, and returns structured JSON results to the frontend.

## Theory of Computation Concepts

| Concept | Application in the Project |
|---|---|
| Regular Languages | Lexical patterns and token recognition |
| Deterministic Finite Automaton (DFA) | Identifier validation |
| Pushdown Automaton (PDA) | Matching nested brackets using a stack |
| Context-Free Grammar (CFG) | Defining the supported syntax of Mini-C |
| Parsing | Checking syntax against grammar rules |
| Parse Tree | Representing the hierarchical structure of parsed source code |

These components demonstrate different levels of source-code analysis, from recognizing individual tokens to validating grammatical structure.

## Technology Stack

- **Python** — backend logic and validation modules
- **PLY (Python Lex-Yacc)** — lexical analysis and parsing
- **Flask** — HTTP API
- **Flask-CORS** — cross-origin requests from the frontend
- **HTML** — frontend structure
- **CSS** — interface styling
- **JavaScript** — API communication and interactive result visualization
- **pytest** — automated testing

## Project Structure

```text
MiniCompilerValidator/
├── backend/
│   ├── app.py
│   ├── lexer.py
│   ├── parser.py
│   ├── parsetab.py
│   ├── pda.py
│   ├── identifier_checker.py
│   ├── identifier_dfa.py
│   ├── identifier_validator.py
│   ├── test_parser.py
│   ├── test_pda.py
│   └── other test files
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── docs/
├── requirements.txt
└── README.md
```

*Note: The structure above highlights the main project files. Additional test files and generated parser files may also be present.*

## Installation

### Prerequisites

Install Python 3 and Git. Visual Studio Code is recommended for development.

### 1. Clone the repository

```bash
git clone https://github.com/25f2001566/MiniCompilerValidator.git
cd MiniCompilerValidator
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If pytest is not included in the project dependencies, install it separately:

```powershell
python -m pip install pytest
```

## Running the Application

### 1. Start the Flask backend

From the project root, run:

```powershell
python backend/app.py
```

Keep the terminal open while using the application. The backend is expected to be available at:

`http://127.0.0.1:5000`

The root endpoint can be opened in a browser to confirm that the backend is responding.

### 2. Open the frontend

Open `frontend/index.html` using the development method configured for your project, such as the VS Code Live Server extension.

### 3. Validate source code

1. Enter a Mini-C program in the editor.
2. Click **Validate Code**.
3. Review the tokens and identifier results.
4. Inspect bracket and syntax errors, if any.
5. Examine the parse tree when the parser returns one.

The frontend communicates with the backend through the `/validate` endpoint.

## Example Programs

### Example 1: Valid program

```c
int main() {
    int x = 10;
    if (x > 5) {
        printf("Hello");
    }
    return 0;
}
```

**Expected result:** The program should pass validation if it follows the implemented grammar and all validation stages accept it. A parse tree should be available for visualization.

### Example 2: Missing semicolon

```c
int main() {
    int x = 10
    return 0;
}
```

**Expected result:** The parser should report a syntax error for the missing semicolon.

### Example 3: Missing closing brace

```c
int main() {
    int x = 10;
    return 0;
```

**Expected result:** The bracket validator should report an unmatched opening brace, and the program should not be considered valid.

### Example 4: Invalid identifier

```c
int main() {
    int 2value = 10;
    return 0;
}
```

**Expected result:** The identifier or lexical validation stage should report the invalid identifier according to the implemented rules.

## Testing

The project includes automated tests for the parser and PDA, along with other validation modules.

Run the test suite from the project root:

```powershell
python -m pytest -v
```

The current verified result during development is **28 tests passed** after correcting the PDA line-number test. Re-run the command after any code changes to confirm the current result.

## Limitations

- The parser supports a defined subset of C-like Mini-C syntax rather than the complete C language.
- Programs containing unsupported language constructs may be rejected.
- The parse tree represents the parser's grammar structure, not a complete compiler intermediate representation.
- Successful syntax validation does not imply that a program is semantically correct or executable.
- The application is intended for educational analysis and demonstration, not as a production compiler.

## Future Enhancements

- Expand the supported grammar and language constructs.
- Add semantic analysis, including type checking and scope validation.
- Improve error recovery and provide more precise syntax-error messages.
- Add downloadable reports for validation results.
- Add more automated tests and continuous integration.
- Improve parse-tree navigation and visualization.

## Conclusion

MiniCompilerValidator demonstrates the practical application of automata theory and compiler design through a web-based source-code analysis tool.

By combining lexical analysis, DFA-based identifier validation, PDA-based bracket verification, CFG parsing, and parse-tree visualization, the project provides an interactive learning environment for understanding how programming-language analysis works.

---

**Repository:** [MiniCompilerValidator on GitHub](https://github.com/25f2001566/MiniCompilerValidator)