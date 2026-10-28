"""
Fix Python 3.12 f-string syntax in notebook for Python 3.10 compatibility.
Python 3.12 allows same-quote nesting in f-strings; 3.10 does not.
Strategy: Change outer single-quote f-strings to double-quote where needed.
"""
import json, re

NB = "drug-toxicity-prediction.ipynb"

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

total_fixes = 0

def fix_fstring_line(line):
    """
    Fix patterns like f'\n{'='*55}' -> f"\n{'='*55}"
    i.e., outer f-string uses single quotes but contains single quotes inside {}.
    Switch outer quotes to double quotes in those cases.
    """
    # Pattern: f'...{...single-quoted content...}...'
    # Find f-strings with single outer quotes that contain single quotes inside {}
    # Simple heuristic: if line has f'{' followed by single-quoted string inside
    
    result = line
    
    # Fix: f'\n{'='*N}') -> f"\n{'='*N}")
    # and f'{'='*N}' -> f"{'='*N}"
    # and similar patterns where f'...{' causes issue
    
    # Replace problematic f-string patterns:
    # Pattern 1: f'...{'...'}...' -> use a variable or double-quote outer
    
    # We'll do targeted replacements for known patterns in this notebook
    replacements = [
        # f'\n{'='*55}' -> '\n' + '='*55
        (r"f'\\n\{'='\*(\d+)\}'", lambda m: f"'\\n' + '='*{m.group(1)}"),
        # f'{'='*55}' -> '='*55  
        (r"f'\{'='\*(\d+)\}'", lambda m: f"'='*{m.group(1)}"),
        # f' {target:<30} {prob:>15.1%}    {risk:>8}  {bar}' - these are fine
    ]
    
    # More robust: detect any f'...{' pattern where inside {} has single quotes
    # and switch the outer quotes to double-quotes
    
    # Find f-strings with single quotes where expression contains single quotes
    # Regex: f'([^'{}]|\\.|\{[^}]*'[^}]*\})*'
    # This is complex - instead do simple string replacement for known patterns
    
    known_fixes = [
        # The separator line pattern
        ("f'\\n{'='*55}'", "f\"\\n{'='*55}\""),
        ("f'\\n{'='*60}'", "f\"\\n{'='*60}\""),
        ("f'\\n{'='*55}\\n'", "f\"\\n{'='*55}\\n\""),
        ("f'{'='*55}'", "f\"{'='*55}\""),
        ("f'{'='*60}'", "f\"{'='*60}\""),
        ("f'{'='*30}'", "f\"{'='*30}\""),
        ("f'{'='*40}'", "f\"{'='*40}\""),
        ("f'{'='*50}'", "f\"{'='*50}\""),
        ("f'{'='*62}'", "f\"{'='*62}\""),
        ("f'{'='*70}'", "f\"{'='*70}\""),
        ("f'{'='*80}'", "f\"{'='*80}\""),
        ("f'{'-'*55}'", "f\"{'-'*55}\""),
        ("f'{'-'*60}'", "f\"{'-'*60}\""),
        ("f'{'-'*30}'", "f\"{'-'*30}\""),
        ("f'{'-'*62}'", "f\"{'-'*62}\""),
        ("f'\\n{'-'*55}'", "f\"\\n{'-'*55}\""),
        ("f'\\n{'-'*60}'", "f\"\\n{'-'*60}\""),
        ("f'\\n{'-'*62}'", "f\"\\n{'-'*62}\""),
        ("f'{'*'*55}'", "f\"{'*'*55}\""),
        ("f'{'*'*60}'", "f\"{'*'*60}\""),
        ("f'{'#'*55}'", "f\"{'#'*55}\""),
        ("f'{'#'*60}'", "f\"{'#'*60}\""),
        # Also fix the specific format string patterns like f'{target:<30}'
        # those use < inside {} which is fine - only problematic when ' inside {}
    ]
    
    for old, new in known_fixes:
        if old in result:
            result = result.replace(old, new)
            return result, True
    
    # Generic approach: find f'...{EXPR}...' where EXPR contains '
    # Switch outer quotes from ' to "
    def fix_fstring_quotes(s):
        """Switch f-string outer quotes from ' to " where inner {} has single quotes."""
        i = 0
        out = []
        changed = False
        while i < len(s):
            # Look for f'
            if i < len(s) - 1 and s[i] == 'f' and s[i+1] == "'":
                # Find the matching closing quote, tracking {} depth
                j = i + 2
                depth = 0
                has_inner_single = False
                while j < len(s):
                    c = s[j]
                    if c == '{':
                        depth += 1
                    elif c == '}':
                        depth -= 1
                    elif c == "'" and depth > 0:
                        has_inner_single = True
                    elif c == "'" and depth == 0:
                        # End of f-string
                        if has_inner_single:
                            # Rewrite with double quotes
                            inner = s[i+2:j]
                            out.append('f"' + inner + '"')
                            i = j + 1
                            changed = True
                        else:
                            out.append(s[i:j+1])
                            i = j + 1
                        break
                    j += 1
                else:
                    out.append(s[i])
                    i += 1
            else:
                out.append(s[i])
                i += 1
        return ''.join(out), changed
    
    fixed, changed = fix_fstring_quotes(result)
    return fixed, changed

fixes_per_cell = []
for cell_idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    new_source = []
    cell_fixes = 0
    for line in cell['source']:
        fixed_line, changed = fix_fstring_line(line)
        if changed:
            cell_fixes += 1
            total_fixes += 1
        new_source.append(fixed_line)
    cell['source'] = new_source
    if cell_fixes:
        fixes_per_cell.append((cell_idx, cell_fixes))

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f"Fixed {total_fixes} f-string compatibility issue(s) across {len(fixes_per_cell)} cell(s):")
for cell_idx, count in fixes_per_cell:
    print(f"  Cell {cell_idx}: {count} fix(es)")
print("Notebook saved.")
