import shutil, json, os

src = r'C:\Users\ADMIN\Downloads\drug-toxicity-prediction.ipynb'
dst = r'C:\Users\ADMIN\.gemini\antigravity-ide\scratch\drug_toxicity_prediction\drug-toxicity-prediction.ipynb'

# Copy notebook
shutil.copy2(src, dst)
print('Notebook copied.')

# Fix dataset path
with open(dst, 'r', encoding='utf-8') as f:
    nb = json.load(f)

fixed = 0
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        new_src = []
        for line in cell['source']:
            if '/kaggle/input' in line and 'tox21' in line.lower() and 'DATA_PATH' in line:
                line = "DATA_PATH = './tox21.csv'  # Updated to local path\n"
                fixed += 1
            new_src.append(line)
        cell['source'] = new_src

# Also fix the os.walk kaggle cell - replace with local listing
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src_text = ''.join(cell['source'])
        if 'os.walk' in src_text and '/kaggle/input' in src_text:
            cell['source'] = [
                "import os\n",
                "# List files in current directory\n",
                "for f in os.listdir('.'):\n",
                "    print(f)\n"
            ]
            fixed += 1

with open(dst, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f'Fixed {fixed} Kaggle-specific path(s) in notebook.')
print('Done!')
