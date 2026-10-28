"""
Run the drug toxicity prediction notebook.
Executes all cells and saves the output notebook.
"""
import subprocess
import sys
import os

PROJECT = r"C:\Users\ADMIN\.gemini\antigravity-ide\scratch\drug_toxicity_prediction"
PYTHON  = os.path.join(PROJECT, "drug_tox_env", "Scripts", "python.exe")
NB      = os.path.join(PROJECT, "drug-toxicity-prediction.ipynb")

# Verify dataset exists
csv_path = os.path.join(PROJECT, "tox21.csv")
if not os.path.exists(csv_path):
    print(f"ERROR: tox21.csv not found at {csv_path}")
    sys.exit(1)

print(f"Dataset found: {csv_path} ({os.path.getsize(csv_path):,} bytes)")
print("Running notebook...")

# Execute notebook
result = subprocess.run(
    [PYTHON, "-m", "jupyter", "nbconvert",
     "--to", "notebook",
     "--execute",
     "--inplace",
     "--ExecutePreprocessor.timeout=600",
     "--ExecutePreprocessor.kernel_name=python3",
     NB],
    cwd=PROJECT,
    capture_output=False
)

if result.returncode == 0:
    print("\n✅ Notebook executed successfully!")
    print(f"Output saved to: {NB}")
    # List generated images
    print("\nGenerated files:")
    for f in os.listdir(PROJECT):
        if f.endswith('.png'):
            print(f"  📊 {f}")
else:
    print(f"\n❌ Notebook execution failed (code {result.returncode})")
    sys.exit(result.returncode)
