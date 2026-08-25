from pathlib import Path

base = Path('blueprint/tools/apply_c044_step4_replay.py')
code = base.read_text(encoding='utf-8')
start = code.find('def find_function_span(text, name):')
end = code.find('def replace_function(name, new_text):', start)
if start < 0 or end < 0:
    raise SystemExit('base patcher parser boundary not found')

robust = r'''def find_function_span(text, name):
    marker = name + '('
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit(f'function not found: {name}')
    start = text.rfind('\n', 0, idx) + 1
    brace = text.find('{', idx)
    if brace < 0:
        raise SystemExit(f'opening brace not found: {name}')
    depth = 0
    pos = brace
    in_string = False
    in_line_comment = False
    in_block_comment = False
    escaped = False
    while pos < len(text):
        ch = text[pos]
        nxt = text[pos + 1] if pos + 1 < len(text) else ''
        if in_line_comment:
            if ch == '\n':
                in_line_comment = False
        elif in_block_comment:
            if ch == '*' and nxt == '/':
                in_block_comment = False
                pos += 1
        elif in_string:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '/' and nxt == '/':
                in_line_comment = True
                pos += 1
            elif ch == '/' and nxt == '*':
                in_block_comment = True
                pos += 1
            elif ch == '"':
                in_string = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end = pos + 1
                    while end < len(text) and text[end] in '\r\n':
                        end += 1
                    return start, end
        pos += 1
    raise SystemExit(f'closing brace not found: {name}')

'''
code = code[:start] + robust + code[end:]
exec(compile(code, str(base), 'exec'))
