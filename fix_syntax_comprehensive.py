"""
Comprehensive fix: extract all code from notebook, check for Python 3.10
f-string compatibility, and fix all issues.
"""
import json, ast, sys

NB = "drug-toxicity-prediction.ipynb"

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

total_fixes = 0
problem_cells = []

# First pass: find all cells with syntax errors in Python 3.10
for cell_idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])
    if not src.strip():
        continue
    try:
        ast.parse(src)
    except SyntaxError as e:
        problem_cells.append((cell_idx, src, str(e)))

print(f"Found {len(problem_cells)} cell(s) with syntax errors:")
for idx, src, err in problem_cells:
    lines = src.split('\n')
    print(f"\n  Cell {idx}: {err}")
    for i, l in enumerate(lines[:5], 1):
        print(f"    {i}: {l}")

# Fix each problematic cell
for cell_idx, orig_src, err in problem_cells:
    cell = nb['cells'][cell_idx]
    src = ''.join(cell['source'])
    
    # Fix: replace f'...{'...'}...' patterns
    # Strategy: line by line, switch outer f-string quotes from ' to "
    # wherever single-quoted content appears inside {} expressions
    new_lines = []
    for line in src.split('\n'):
        fixed = line
        # Check if this line has an f-string with nested single quotes
        # Pattern: f'...{EXPR_WITH_QUOTES}...'
        # Simple fix: convert f'...' to f"..." when { contains '
        i = 0
        result = []
        while i < len(fixed):
            if i+1 < len(fixed) and fixed[i] == 'f' and fixed[i+1] == "'":
                # Try to find end of f-string, tracking brace depth
                j = i + 2
                depth = 0
                has_sq_in_expr = False
                while j < len(fixed):
                    ch = fixed[j]
                    if ch == '\\':
                        j += 2
                        continue
                    if ch == '{':
                        depth += 1
                    elif ch == '}':
                        if depth > 0:
                            depth -= 1
                    elif ch == "'":
                        if depth > 0:
                            has_sq_in_expr = True
                        elif depth == 0:
                            # End of f-string
                            break
                    j += 1
                end = j
                fstr_content = fixed[i+2:end]  # content between f' and '
                if has_sq_in_expr:
                    # Replace ' with " for outer quotes, keep inner ' as-is
                    result.append(f'f"{fstr_content}"')
                    total_fixes += 1
                else:
                    result.append(fixed[i:end+1])
                i = end + 1
            else:
                result.append(fixed[i])
                i += 1
        new_lines.append(''.join(result))
    
    fixed_src = '\n'.join(new_lines)
    
    # Verify fix works
    try:
        ast.parse(fixed_src)
        print(f"\n  Cell {cell_idx}: Fixed successfully!")
        # Write back to cell
        if fixed_src.endswith('\n'):
            lines_out = fixed_src.splitlines(keepends=True)
        else:
            lines_out = fixed_src.splitlines(keepends=True)
        cell['source'] = lines_out if lines_out else [fixed_src]
    except SyntaxError as e2:
        print(f"\n  Cell {cell_idx}: Still has error after fix: {e2}")
        print("  Attempting backup fix: replace separator print statements...")
        # Backup: replace the entire print(f'\n{'='*N}') pattern
        import re
        fixed2 = fixed_src
        # f'\n{'='*N}' pattern
        fixed2 = re.sub(r"f'\\n\{'='\*(\d+)\}'", lambda m: f"'\\n' + '='*{m.group(1)}", fixed2)
        fixed2 = re.sub(r"f'\{'='\*(\d+)\}'", lambda m: f"'='*{m.group(1)}", fixed2)
        fixed2 = re.sub(r"f'\{'-'\*(\d+)\}'", lambda m: f"'-'*{m.group(1)}", fixed2)
        try:
            ast.parse(fixed2)
            print(f"  Cell {cell_idx}: Backup fix worked!")
            cell['source'] = fixed2.splitlines(keepends=True)
        except SyntaxError as e3:
            print(f"  Cell {cell_idx}: FAILED: {e3}")

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

# Final validation pass
errors_remaining = 0
for cell_idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])
    if not src.strip():
        continue
    try:
        ast.parse(src)
    except SyntaxError as e:
        errors_remaining += 1
        print(f"\nREMAINING ERROR in Cell {cell_idx}: {e}")

if errors_remaining == 0:
    print(f"\n[ALL CLEAR] All cells parse correctly under Python 3.10.")
    print(f"Total additional fixes applied: {total_fixes}")
else:
    print(f"\n{errors_remaining} cell(s) still have errors.")
