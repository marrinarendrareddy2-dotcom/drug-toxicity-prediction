"""
Final check: verify the specific cell that failed (cell 15/20 in nbconvert)
and confirm all f-string issues are resolved. Also strip the !pip cell.
"""
import json, ast

NB = "drug-toxicity-prediction.ipynb"

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Remove/skip !pip install cell (not needed since packages already installed)
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if '!pip install' in src:
            print(f"Cell {i}: Replacing !pip install with pass (packages already installed)")
            cell['source'] = ["# Packages already installed in drug_tox_env\nprint('All packages ready!')"]

# Check all remaining cells
errors = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])
    if not src.strip():
        continue
    try:
        ast.parse(src)
    except SyntaxError as e:
        if '!pip' not in src and '!conda' not in src:
            errors.append((i, str(e), src[:100]))

if errors:
    print(f"\n{len(errors)} real syntax error(s) found:")
    for i, err, preview in errors:
        print(f"  Cell {i}: {err}")
        print(f"    Preview: {preview[:80]}")
else:
    print("\n[ALL CLEAR] No Python 3.10 syntax errors found in notebook.")

# Also fix the os.walk kaggle cell if it crept back
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if 'os.walk' in src and '/kaggle' in src:
            print(f"Cell {i}: Fixing kaggle os.walk cell")
            cell['source'] = [
                "import os\n",
                "# List local files\n",
                "for f in sorted(os.listdir('.')):\n",
                "    print(f)\n"
            ]

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook saved.")
