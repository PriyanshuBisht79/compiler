class SemanticError(Exception):
    pass

def build_symbol_table(ast):
    symbol_table = {}
    errors = []

    def visit(node):
        if node.type == "Program":
            for child in node.children:
                visit(child)

        elif node.type == "Declare":
            var_node = node.children[0]
            expr_node = node.children[1]
            var_name = var_node.value
            if var_name in symbol_table:
                errors.append(f"Variable '{var_name}' already declared")
            else:
                symbol_table[var_name] = "int"  # Assume int for simplicity
                visit(expr_node)

        elif node.type == "Print":
            visit(node.children[0])

        elif node.type == "IfElse":
            visit(node.children[0])  # condition
            for stmt in node.children[1].children:
                visit(stmt)
            for stmt in node.children[2].children:
                visit(stmt)

        elif node.type == "BinOp" or node.type == "GT":
            visit(node.children[0])
            visit(node.children[1])

        elif node.type == "ID":
            if node.value not in symbol_table:
                errors.append(f"Variable '{node.value}' used before declaration")

        elif node.type == "Number":
            pass  # Always valid

    visit(ast)

    if errors:
        raise SemanticError("\\n".join(errors))

    return symbol_table
