import re

def generate_code(ir):
    target_code = []

    for line in ir:
        line = line.strip()

        # Print statements
        if line.startswith("print "):
            var = line.split()[1]
            target_code.append(f"PRINT {var}")

        # Binary operations: t3 = a + b
        elif re.match(r"^\w+\s*=\s*\w+\s*[\+\-\*/><]\s*\w+$", line):
            lhs, expr = [x.strip() for x in line.split("=", 1)]
            parts = re.split(r'\s*([\+\-\*/><])\s*', expr)
            if len(parts) == 3:
                arg1, op, arg2 = parts
                asm_op = {
                    '+': 'ADD',
                    '-': 'SUB',
                    '*': 'MUL',
                    '/': 'DIV',
                    '>': 'GT'
                }.get(op, 'OP')  # Default fallback
                target_code.append(f"{asm_op} {lhs}, {arg1}, {arg2}")

        # Assignments: x = y or x = 5
        elif "=" in line:
            lhs, rhs = [x.strip() for x in line.split("=", 1)]
            target_code.append(f"MOV {lhs}, {rhs}")

        # Labels (like t5:)
        elif line.endswith(":"):
            target_code.append(f"{line}")

        # Jumps: goto label
        elif line.startswith("goto "):
            label = line.split()[1]
            target_code.append(f"JMP {label}")

        # Conditional: if x > y goto label
        elif line.startswith("if "):
            match = re.match(r"if\s+(\w+)\s+goto\s+(\w+)", line)
            if match:
                cond, label = match.groups()
                target_code.append(f"JMP_IF {cond}, {label}")

    return target_code
