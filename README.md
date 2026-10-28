# Drug Toxicity Prediction

A machine learning pipeline that predicts drug/compound toxicity using the **Tox21 dataset** (7,831 compounds, 12 toxicity targets).

## Project Structure

```
drug_toxicity_prediction/
├── drug-toxicity-prediction.ipynb   # Main notebook
├── drug_tox_env/                    # Python 3.10 virtual environment
├── tox21.csv                        # Dataset
├── requirements.txt                 # Package list
└── README.md                        # This file
```

## Setup

### 1. Create virtual environment
```powershell
uv venv --python 3.10 drug_tox_env
```

### 2. Install dependencies
```powershell
uv pip install --python drug_tox_env -r requirements.txt
```

## Dataset

Download the Tox21 dataset from Kaggle:
- URL: https://www.kaggle.com/datasets/epicskills/tox21-dataset
- Place `tox21.csv` in this project directory

## Run

```powershell
.\drug_tox_env\Scripts\activate
jupyter notebook drug-toxicity-prediction.ipynb
```

## Toxicity Targets Predicted

| Target     | Description                              |
|------------|------------------------------------------|
| NR-AhR     | Aryl hydrocarbon receptor                |
| NR-AR      | Androgen receptor                        |
| NR-AR-LBD  | Androgen receptor ligand-binding domain  |
| NR-Aromatase | Aromatase enzyme                       |
| NR-ER      | Estrogen receptor alpha                  |
| NR-ER-LBD  | Estrogen receptor LBD                    |
| NR-PPAR-gamma | PPAR gamma                            |
| SR-ARE     | Antioxidant response element             |
| SR-ATAD5   | ATPase family AAA domain                 |
| SR-HSE     | Heat shock element                       |
| SR-MMP     | Mitochondrial membrane potential         |
| SR-p53     | p53 tumor suppressor                     |

## Models

- **XGBoost** (primary — best performance)
- **Random Forest**
- **Logistic Regression**

## Imbalance Handling

Uses **SMOTE oversampling** + `class_weight=balanced` to handle class imbalance.

## Evaluation Metrics

- **ROC-AUC** (primary)
- **PR-AUC** (secondary — better for imbalanced data)

## Output Files

| File | Description |
|------|-------------|
| `class_distribution.png` | Class imbalance visualization |
| `roc_curves.png` | ROC curves per target |
| `auc_heatmap.png` | Model comparison heatmap |
| `shap_summary.png` | SHAP feature importance |
| `shap_importance.png` | SHAP bar chart |
| `shap_dependence.png` | SHAP dependence plots |
| `property_vs_toxicity.png` | Molecular property analysis |
| `chemical_space.png` | Chemical space visualization |

## Key Results (XGBoost ROC-AUC)

| Target | ROC-AUC | PR-AUC |
|--------|---------|--------|
| SR-MMP | 0.9229  | 0.7147 |
| NR-AhR | 0.8994  | 0.6288 |
| SR-p53 | 0.8285  | 0.3503 |
| SR-ARE | 0.8234  | 0.5405 |
| NR-ER  | 0.7045  | 0.4569 |
