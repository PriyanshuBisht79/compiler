temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

def generate_ir(ast):
    global temp_count
    temp_count = 0  # Reset temp counter for each run
    ir = []

    def visit(node):
        if node.type == "Program":
            for stmt in node.children:
                visit(stmt)

        elif node.type == "Declare":
            var_node = node.children[0]
            expr_node = node.children[1]
            expr_temp = visit(expr_node)
            ir.append(f"{var_node.value} = {expr_temp}")

        elif node.type == "Print":
            val = visit(node.children[0])
            ir.append(f"print {val}")

        elif node.type == "BinOp":
            left = visit(node.children[0])
            right = visit(node.children[1])
            temp = new_temp()
            ir.append(f"{temp} = {left} {node.value} {right}")
            return temp

        elif node.type == "GT":
            left = visit(node.children[0])
            right = visit(node.children[1])
            temp = new_temp()
            ir.append(f"{temp} = {left} > {right}")
            return temp

        elif node.type == "Number":
            return str(node.value)

        elif node.type == "ID":
            return node.value

        elif node.type == "IfElse":
            cond = visit(node.children[0])
            true_block = node.children[1].children
            false_block = node.children[2].children

            label_true = new_temp()
            label_false = new_temp()
            label_end = new_temp()

            ir.append(f"if {cond} goto {label_true}")
            ir.append(f"goto {label_false}")

            ir.append(f"{label_true}:")
            for stmt in true_block:
                visit(stmt)
            ir.append(f"goto {label_end}")

            ir.append(f"{label_false}:")
            for stmt in false_block:
                visit(stmt)

            ir.append(f"{label_end}:")

    visit(ast)
    return ir
