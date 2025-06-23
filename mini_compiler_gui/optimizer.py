import re

def is_number(s):
    try:
        float(s)
        return True
    except:
        return False

def optimize_ir(ir):
    constants = {}  # Track known constants
    optimized = []

    # First pass: constant folding
    for line in ir:
        line = line.strip()

        # Match 3-address: t3 = t1 + t2
        match = re.match(r"(\w+)\s*=\s*(\w+)\s*([\+\-\*/])\s*(\w+)", line)
        if match:
            dest, left, op, right = match.groups()
            left_val = constants.get(left, left)
            right_val = constants.get(right, right)

            if is_number(left_val) and is_number(right_val):
                result = eval(f"{left_val}{op}{right_val}")
                optimized.append(f"{dest} = {result}")
                constants[dest] = result
            else:
                optimized.append(f"{dest} = {left_val} {op} {right_val}")
                constants[dest] = None

        elif line.startswith("print "):
            var = line.split()[1]
            value = constants.get(var, var)
            optimized.append(f"print {value}")

        elif "=" in line:
            dest, src = [x.strip() for x in line.split("=")]
            value = constants.get(src, src)
            optimized.append(f"{dest} = {value}")
            constants[dest] = value

        else:
            # Keep labels and jumps
            optimized.append(line)

    # Second pass: Dead Code Elimination
    used = set()
    final_ir = []

    for line in reversed(optimized):
        line = line.strip()
        if line.startswith("print "):
            var = line.split()[1]
            used.add(var)
            final_ir.insert(0, line)
        elif "=" in line and not line.endswith(":"):
            dest, expr = [x.strip() for x in line.split("=", 1)]
            # If dest is used, keep line and mark all vars on RHS as used
            if dest in used:
                # Find variables in RHS
                vars_used = re.findall(r"\b[a-zA-Z_]\w*\b", expr)
                used.update(vars_used)
                final_ir.insert(0, line)
            # else: skip (dead assignment)
        else:
            final_ir.insert(0, line)  # Keep labels/jumps

    return final_ir
