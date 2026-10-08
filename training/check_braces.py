import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Let's count { and } excluding strings and comments
in_str = None
in_line_comment = False
in_block_comment = False
stack = []
line_num = 1
col_num = 0

i = 0
n = len(code)
while i < n:
    ch = code[i]
    col_num += 1
    if ch == '\n':
        line_num += 1
        col_num = 0
        in_line_comment = False
        i += 1
        continue
    
    if in_line_comment:
        i += 1
        continue
        
    if in_block_comment:
        if ch == '*' and i + 1 < n and code[i+1] == '/':
            in_block_comment = False
            i += 2
            continue
        i += 1
        continue
        
    if in_str:
        if ch == '\\':
            i += 2
            continue
        if ch == in_str:
            in_str = None
        i += 1
        continue
        
    # Not in string or comment
    if ch == '/' and i + 1 < n and code[i+1] == '/':
        in_line_comment = True
        i += 2
        continue
    if ch == '/' and i + 1 < n and code[i+1] == '*':
        in_block_comment = True
        i += 2
        continue
    if ch in ('"', "'", '`'):
        in_str = ch
        i += 1
        continue
        
    if ch == '{':
        stack.append((line_num, col_num))
    elif ch == '}':
        if not stack:
            print(f"Extra closing brace at line {line_num}:{col_num}")
        else:
            stack.pop()
    i += 1

print(f"Unclosed braces remaining: {len(stack)}")
for s in stack[:10]:
    print(f"  Unclosed '{'{'}' opened at line {s[0]}:{s[1]}")
