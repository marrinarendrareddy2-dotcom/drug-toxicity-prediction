"""
Patch the SHAP TreeExplainer cell and any other known version-conflict cells
in the notebook for robustness.
"""
import json

NB = "drug-toxicity-prediction.ipynb"

with open(NB, 'r', encoding='utf-8') as f:
    nb = json.load(f)

shap_patch = '''\
# SHAP analysis for the primary target (highest-data target)
primary_target = viable_df.iloc[0]['target']
print(f'Running SHAP analysis for primary target: {primary_target}')

model_xgb = trained_models[primary_target]
X_test_sc = X_test_store[primary_target]

# Use a subsample for speed
n_shap = min(500, len(X_test_sc))
X_shap = X_test_sc[:n_shap]

# Robust TreeExplainer — handles XGBoost 2.x and 3.x base_score formats
try:
    explainer = shap.TreeExplainer(model_xgb)
    shap_values = explainer.shap_values(X_shap)
except (ValueError, TypeError) as e:
    if "base_score" in str(e) or "could not convert" in str(e):
        # XGBoost 3.x compat fix: patch base_score on the booster
        import re as _re
        booster = model_xgb.get_booster()
        cfg = booster.save_config()
        cfg_dict = json.loads(cfg)
        try:
            raw = cfg_dict["learner"]["learner_model_param"]["base_score"]
            # Strip brackets if present: '[7.49E-1]' -> '7.49E-1'
            raw_clean = _re.sub(r'[\[\]]', '', raw)
            cfg_dict["learner"]["learner_model_param"]["base_score"] = raw_clean
            booster.load_config(json.dumps(cfg_dict))
        except Exception:
            pass
        explainer = shap.TreeExplainer(booster)
        shap_values = explainer.shap_values(X_shap)
    else:
        raise

print(f'SHAP values computed for {n_shap} test samples')
'''

patches_applied = 0
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])
    # Find the SHAP TreeExplainer cell
    if 'TreeExplainer(model_xgb)' in src and 'shap_values = explainer' in src and 'try:' not in src:
        print(f"Patching SHAP cell at index {i}")
        cell['source'] = [shap_patch]
        patches_applied += 1

with open(NB, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print(f"Applied {patches_applied} patch(es). Notebook saved.")
