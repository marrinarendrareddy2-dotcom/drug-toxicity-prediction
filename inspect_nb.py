import json

with open("drug-toxicity-prediction.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb["cells"]):
    cell_type = cell.get("cell_type")
    src = "".join(cell.get("source", []))
    first_line = src.strip().split("\n")[0] if src.strip() else "(empty)"
    print(f"Cell {i:02d} [{cell_type:8s}]: {first_line[:100]}")
