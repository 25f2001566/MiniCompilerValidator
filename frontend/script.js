const codeInput = document.getElementById("codeInput");
const validateBtn = document.getElementById("validateBtn");

const tokenTableBody = document.getElementById("tokenTableBody");
const errorList = document.getElementById("errorList");
const identifierList = document.getElementById("identifierList");
const statusBox = document.getElementById("statusBox");
const parseTreeContainer = document.getElementById("parseTree");

validateBtn.addEventListener("click", validateCode);

async function validateCode() {
    const code = codeInput.value;

    tokenTableBody.replaceChildren();
    errorList.replaceChildren();
    identifierList.replaceChildren();
    parseTreeContainer.replaceChildren();

    if (!code.trim()) {
        statusBox.textContent = "Please enter some code.";
        statusBox.className = "status-error";
        errorList.textContent = "No code provided.";
        return;
    }

    statusBox.textContent = "Validating...";
    statusBox.className = "";
    validateBtn.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:5000/validate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code })
        });

        if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
        }

        const data = await response.json();

        displayTokens(data.tokens || []);
        displayIdentifiers(
            data.tokens || [],
            data.identifier_errors || []
        );
        displayErrors(data);
        displayStatus(data);
        displayParseTree(
            data.parse_tree,
            data.syntax_errors || []
        );

    } catch (error) {
        console.error(error);

        statusBox.textContent =
            "Connection failed. Make sure Flask is running on port 5000.";
        statusBox.className = "status-error";
        errorList.textContent = error.message;

    } finally {
        validateBtn.disabled = false;
    }
}

function displayTokens(tokens) {
    if (!tokens.length) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");

        cell.colSpan = 3;
        cell.textContent = "No tokens found.";

        row.appendChild(cell);
        tokenTableBody.appendChild(row);
        return;
    }

    tokens.forEach(token => {
        const row = document.createElement("tr");

        [token.value, token.type, token.line].forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = String(value);
            row.appendChild(cell);
        });

        tokenTableBody.appendChild(row);
    });
}

function displayIdentifiers(tokens, errors) {
    const identifiers = tokens.filter(
        token => token.type === "IDENTIFIER"
    );

    if (!identifiers.length && !errors.length) {
        identifierList.textContent = "No identifiers found.";
        return;
    }

    identifiers.forEach(identifier => {
        const item = document.createElement("div");
        item.className = "identifier-item";
        item.textContent =
            `${identifier.value} — recognized identifier — Line ${identifier.line}`;

        identifierList.appendChild(item);
    });

    errors.forEach(error => {
        identifierList.appendChild(createErrorElement(error));
    });
}

function displayErrors(data) {
    const groups = [
        ["Lexical Errors", data.lexical_errors],
        ["Identifier Errors", data.identifier_errors],
        ["PDA / Bracket Errors", data.bracket_errors],
        ["CFG / Syntax Errors", data.syntax_errors]
    ];

    let found = false;

    groups.forEach(([heading, errors]) => {
        if (!errors || !errors.length) return;

        found = true;

        const title = document.createElement("h3");
        title.textContent = heading;
        errorList.appendChild(title);

        errors.forEach(error => {
            errorList.appendChild(createErrorElement(error));
        });
    });

    if (!found) {
        errorList.textContent = "No errors found.";
    }
}

function createErrorElement(error) {
    const item = document.createElement("div");
    item.className = "error";

    const heading = document.createElement("strong");
    heading.textContent = error.type || "Error";

    const message = document.createElement("p");
    message.textContent = error.message || "Unknown error";

    const line = document.createElement("p");
    line.textContent =
        error.line ? `Line: ${error.line}` : "Line unavailable";

    item.append(heading, message, line);
    return item;
}

function displayStatus(data) {
    if (data.success) {
        statusBox.textContent =
            "✓ Validation successful — no errors found.";
        statusBox.className = "status-success";
    } else {
        statusBox.textContent =
            "✗ Validation failed — review the errors below.";
        statusBox.className = "status-error";
    }
}

function displayParseTree(tree, syntaxErrors) {
    if (syntaxErrors.length) {
        parseTreeContainer.textContent =
            "Parse tree unavailable because syntax errors were detected.";
        return;
    }

    if (!tree) {
        parseTreeContainer.textContent =
            "No parse tree was returned by the parser.";
        return;
    }

    const root = document.createElement("ul");
    root.className = "tree";
    root.appendChild(buildTreeNode("Parse Tree", tree));
    parseTreeContainer.appendChild(root);
}

function buildTreeNode(label, value) {
    const item = document.createElement("li");
    const node = document.createElement("div");

    node.className = "tree-node";

    if (isGrammarNode(value)) {
        node.textContent = formatNodeLabel(value[0]);
    } else {
        node.textContent = label;
    }

    item.appendChild(node);

    const children = getChildren(value);

    if (children.length > 0) {
        const list = document.createElement("ul");
        list.className = "tree-children";

        children.forEach(child => {
            list.appendChild(
                buildTreeNode(child.label, child.value)
            );
        });

        item.appendChild(list);
    } else if (
        value !== null &&
        value !== undefined &&
        !Array.isArray(value) &&
        typeof value !== "object"
    ) {
        node.textContent = `${label}: ${String(value)}`;
    }

    return item;
}

function getChildren(value) {
    if (!Array.isArray(value)) {
        return [];
    }

    // A grammar node has a name followed by its child values.
    if (isGrammarNode(value)) {
        const parent = value[0];

        return value.slice(1).map((child, index) => ({
            label: getChildLabel(parent, child, index),
            value: child
        }));
    }

    // A plain array represents a list of elements.
    return value.map((child, index) => ({
        label: `Element ${index + 1}`,
        value: child
    }));
}

function isGrammarNode(value) {
    return (
        Array.isArray(value) &&
        typeof value[0] === "string"
    );
}

function getChildLabel(parent, child, index) {
    if (Array.isArray(child) && typeof child[0] === "string") {
        return formatNodeLabel(child[0]);
    }

    const labels = {
        function_definition: [
            "Return Type",
            "Function Name",
            "Body"
        ],
        declaration: [
            "Datatype",
            "Identifier",
            "Initializer"
        ],
        assignment: [
            "Identifier",
            "Assigned Expression"
        ],
        return_statement: [
            "Return Expression"
        ],
        block: [
            "Statements"
        ],
        statement_list: [
            "Statement",
            "Remaining Statements"
        ],
        if_statement: [
            "Condition",
            "Then Block",
            "Else Block"
        ],
        while_statement: [
            "Condition",
            "Loop Body"
        ],
        condition: [
            "Left Expression",
            "Relational Operator",
            "Right Expression"
        ],
        binary_expression: [
            "Operator",
            "Left Operand",
            "Right Operand"
        ],
        identifier: [
            "Identifier"
        ],
        number: [
            "Number"
        ],
        character: [
            "Character"
        ],
        string: [
            "String"
        ],
        datatype: [
            "Datatype"
        ]
    };

    return labels[parent]?.[index] || `Element ${index + 1}`;
}

function formatNodeLabel(name) {
    const labels = {
        program: "Program",
        function_definition: "Function Definition",
        declaration: "Variable Declaration",
        assignment: "Assignment",
        return_statement: "Return Statement",
        datatype: "Datatype",
        block: "Code Block",
        statement_list: "Statements",
        if_statement: "If Statement",
        while_statement: "While Loop",
        condition: "Condition",
        expression: "Expression",
        term: "Term",
        factor: "Factor",
        number: "Number",
        printf_statement: "Print Statement",
        argument_list: "Arguments"
    };

    return labels[name] || name.replaceAll("_", " ");
}