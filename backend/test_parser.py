from parser import parse


def test_valid_program():
    tree, errors = parse(
        "int main() { int x = 10; return 0; }"
    )
    assert tree is not None
    assert errors == []


def test_declaration_without_initializer():
    tree, errors = parse(
        "int main() { int x; return 0; }"
    )
    assert tree is not None
    assert errors == []


def test_invalid_declaration():
    tree, errors = parse(
        "int main() { int = 10; return 0; }"
    )
    assert errors != []


def test_missing_semicolon():
    tree, errors = parse(
        "int main() { int x = 10 return 0; }"
    )
    assert errors != []


def test_if_statement():
    tree, errors = parse(
        "int main() { if (x > 5) { return 0; } }"
    )
    assert tree is not None
    assert errors == []


def test_while_statement():
    tree, errors = parse(
        "int main() { while (x > 0) { x = x - 1; } }"
    )
    assert tree is not None
    assert errors == []


def test_printf_statement():
    tree, errors = parse(
        'int main() { printf("Hello"); return 0; }'
    )
    assert tree is not None
    assert errors == []


def test_empty_function():
    tree, errors = parse("int main() {}")
    assert tree is not None
    assert errors == []