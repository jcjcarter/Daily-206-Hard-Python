from io import StringIO
import operator
from tokenize import generate_tokens

rpn_str, *initial, n = open("input.txt").read().splitlines()
initial = [list(map(int, line.split(":"))) for line in initial]
start = max(k for k, _ in initial)+1
tab = {k: v for k, v in initial}

rpn = []
for token in generate_tokens(StringIO(rpn_str).readline):
    if token.string not in "()":
        rpn.append(token.string)
    elif token.string == ")":
        rpn[-1] = int(rpn[-1])

def calculate_rpn(rpn, i, tab):
    functions = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
    vals, fun_stack, len_stack = [], [], [0]
    for tok in reversed(rpn):
        if tok in functions:
            fun_stack.append(tok)
            len_stack.append(len(vals))
        else:
            val = int(tok) if isinstance(tok, str) else tab[i-tok]
            vals.append(val)
            while len(vals) == len_stack[-1] + 2:
                len_stack.pop()
                vals.append(functions[fun_stack.pop()](vals.pop(), vals.pop()))
    return vals[0]

for i in range(start, int(n)+1):
    try:
        tab[i] = calculate_rpn(rpn, i, tab)
    except Exception:
        pass 

for i, e in tab.items():
    print("%d: %d" % (i, e))