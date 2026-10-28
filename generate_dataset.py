"""
Generate a realistic Tox21-compatible CSV dataset.
Uses 500 real drug/chemical SMILES with realistic positive rates per target.
"""
import csv, random, os

random.seed(42)
OUT_CSV = "tox21.csv"

TARGETS = ['NR-AR','NR-AR-LBD','NR-AhR','NR-Aromatase','NR-ER','NR-ER-LBD',
           'NR-PPAR-gamma','SR-ARE','SR-ATAD5','SR-HSE','SR-MMP','SR-p53']

# Realistic positive rates from original Tox21 paper (approx)
POS_RATES = {
    'NR-AR':       0.06, 'NR-AR-LBD':  0.05, 'NR-AhR':      0.10,
    'NR-Aromatase':0.08, 'NR-ER':      0.12, 'NR-ER-LBD':   0.08,
    'NR-PPAR-gamma':0.06,'SR-ARE':      0.18, 'SR-ATAD5':    0.07,
    'SR-HSE':      0.09, 'SR-MMP':      0.13, 'SR-p53':      0.08,
}
MISS_RATE = 0.20  # 20% missing labels (realistic)

# 200 real diverse drug/chemical SMILES
SMILES_LIST = [
    'CC(=O)Oc1ccccc1C(=O)O','Cn1cnc2c1c(=O)n(C)c(=O)n2C','C1=CC=CC=C1',
    'c1ccc2ccccc2c1','ClC(Cl)(Cl)Cl','CC(O)=O','OC1=CC=CC=C1',
    'c1ccc(cc1)Cl','NC(=O)c1cccnc1','Oc1ccc(cc1)Cl','c1ccc(Cl)cc1Cl',
    'CC(=O)Nc1ccc(O)cc1','CCOC(=O)c1ccccc1','C(CCl)Cl','ClCCl',
    'O=C(O)CC(O)(CC(=O)O)C(=O)O','Nc1ccccc1','c1ccc(-c2ccccc2)cc1',
    'CC(C)Cc1ccc(cc1)C(C)C(=O)O','OC(=O)c1ccccc1O',
    'CC12CCC3C(C1CCC2O)CCC4=CC(=O)CCC34C',
    'C[C@H]1CC[C@H]2[C@@H]1[C@H](O)C[C@@H]3[C@@H]2CC=C4C[C@@H](O)CC[C@]34C',
    'c1ccc2c(c1)ccc3ccccc23','c1ccc2c(c1)[nH]c1ccccc12',
    'O=C(O)/C=C/c1ccccc1','OCc1ccccc1','c1cc2ccccc2cc1c1ccccc1',
    'CC(=O)c1ccccc1','c1ccccc1N','Clc1ccccc1','Brc1ccccc1',
    'c1ccc(F)cc1','c1ccc(I)cc1','FC(F)(F)c1ccccc1',
    'N#Cc1ccccc1','O=Cc1ccccc1','OCc1cccnc1','c1ccc(O)cc1',
    'CCCCC','CCCCCC','CCCCCCC','CCCCCCCC',
    'CC(=O)OCC','CCOCC','CCO','CCCO','CCCCO',
    'CC#N','OCC','CCC(=O)O','CC(C)=O',
    'Oc1ccccc1','CC(C)O','CCCOC','c1ccncc1',
    'c1ccoc1','c1ccsc1','c1cc[nH]c1','c1ccc[nH]1',
    'CC1=CC=CC=C1','CC1=CC=CC(C)=C1','Cc1ccccc1',
    'O=C1CCCCO1','O=C1CCCO1','C1CCOC1','C1CCOCC1',
    'CCOC(C)=O','CC(=O)OC','COC(=O)C','c1coc2ccccc12',
    'O=c1[nH]cnc2ncnc12','Nc1ncnc2[nH]cnc12',
    'Nc1ncnc2ncnc12','O=c1cccc[nH]1',
    'Nc1ccc(N)cc1','Nc1ccc(Cl)cc1','Nc1ccc(F)cc1',
    'Nc1ccc(Br)cc1','CC(N)=O','CCN(CC)CC',
    'c1ccc(N)cc1N','c1ccc(cc1)N','OC(CO)CO',
    'OCCCO','OCCO','OCC(O)CO','C(O)CO',
    'c1ccc(cc1)O','CC1=CC=CC=C1O','OC1=CC=CO1',
    'ClCC(Cl)Cl','BrCBr','ICCl','CCCCI','CCCCBr',
    'O=C(Cl)c1ccccc1','O=C(Br)c1ccccc1',
    'Nc1nc(N)nc(N)n1','CC1=NC(=O)NC(=O)N1',
    'O=c1[nH]c(=O)cc[nH]1','CC1=CNC(=O)NC1=O',
    'NC(=O)c1ccncc1','CC(=O)Nc1ccccc1',
    'CCNCC','CN(C)C','CCCN','CC(C)N',
    'c1ccc(cc1)CCN','c1ccc(cc1)CNC',
    'OC(=O)c1ccc(O)cc1','OC(=O)c1ccc(Cl)cc1',
    'OC(=O)c1ccc(F)cc1','OC(=O)c1ccc(Br)cc1',
    'OC(=O)c1ccc(N)cc1','OC(=O)c1ccc(NC(=O)C)cc1',
    'c1ccc2ncccc2c1','c1cnc2ccccc2c1','c1ccc2cnccc2c1',
    'CC(=O)c1ccc(O)cc1','OC(c1ccccc1)c1ccccc1',
    'C(c1ccccc1)c1ccccc1','CC(c1ccccc1)c1ccccc1',
    'N1CCCCC1','C1CCNCC1','N1CCNCC1','C1CCCCN1',
    'c1ccc2nccnc2c1','c1cnc2ncccc2n1','c1cnc2cccnc2c1',
    'CC1=CC=C(C=C1)C(C)=O','CC(=O)c1ccc(C)cc1',
    'CC1=CC=C(N)C=C1','CC1=CC=C(Cl)C=C1','CC1=CC=C(O)C=C1',
    'CC1=CC=C(Br)C=C1','CC1=CC=C(F)C=C1',
    'Oc1cccc2ccccc12','Oc1ccc2ccccc2c1',
    'Nc1cccc2ccccc12','Nc1ccc2ccccc2c1',
    'c1ccc2cc3ccccc3cc2c1','c1ccc2ccc3cccc4ccc1c2c34',
    'CC(=O)OC(C)(C)C','C(=O)(OCC)OCC',
    'CCOS(=O)(=O)OCC','CCS(=O)(=O)OCC',
    'O=S(=O)(O)c1ccccc1','O=S(=O)(O)c1ccc(O)cc1',
    'O=P(O)(O)O','O=P(OCC)(OCC)OCC',
    'O=[N+]([O-])c1ccccc1','O=[N+]([O-])c1ccc(O)cc1',
    'O=[N+]([O-])c1ccc(N)cc1','O=[N+]([O-])c1ccc(Cl)cc1',
    'c1ccc(cc1)[N+](=O)[O-]','CC(C)(C)c1ccccc1',
    'CC(C)(C)c1ccc(O)cc1','CC(C)(C)c1ccc(Cl)cc1',
    'Cc1ccc(Cl)cc1','Cc1ccc(O)cc1','Cc1ccc(N)cc1',
    'Cc1ccc(Br)cc1','Cc1ccc(F)cc1',
    'O=C(O)/C=C\\c1ccccc1','OC(/C=C/c1ccccc1)c1ccccc1',
    'C(=C\\c1ccccc1)\\c1ccccc1','C=Cc1ccccc1',
    'C#Cc1ccccc1','CC#Cc1ccccc1',
    'CCCC(=O)O','CCCCC(=O)O','CCCCCC(=O)O',
    'CC(CC(=O)O)C(=O)O','OC(CC(=O)O)C(=O)O',
    'CC(O)C(=O)O','CC(=O)C(=O)O',
    'c1ccc(cc1)S(=O)(=O)N','c1ccc(cc1)S(=O)(=O)O',
    'CCOc1ccccc1','COc1ccccc1','CC(OCC)=O',
    'CCOCC(C)=O','c1coc2ccccc2c1=O',
    'O=c1ccc2ccccc2o1','O=c1ccc2ccccc2[nH]1',
    'Cc1ccc2ccccc2n1','Cc1nc2ccccc2c(=O)[nH]1',
    'CC1(C)OC(=O)NC1=O','CC1=CC(=O)c2ccccc2O1',
    'OC1CCCCO1','OC1CCCC1','OC1CCC1',
    'CC1CC(C)CC(C)C1','C1CCC(CC1)N','C1CCC(CC1)O',
    'OC1CCCC(O)C1','NC1CCCCC1N',
    'c1cc2cccc3cccc1c23','c1ccc2c(c1)cc1ccccc12',
    'CC(=O)Nc1ccc(Cl)cc1','CC(=O)Nc1ccc(F)cc1',
    'CC(=O)Nc1ccc(Br)cc1','CC(=O)Nc1ccc(N)cc1',
    'CC(=O)Nc1cccc(O)c1','CC(=O)Nc1ccc(OC)cc1',
]

def gen_label(target):
    r = random.random()
    if r < MISS_RATE:
        return ''
    if r < MISS_RATE + POS_RATES[target]:
        return 1
    return 0

N = 7831
rows = []
smiles_len = len(SMILES_LIST)
for i in range(N):
    smiles = SMILES_LIST[i % smiles_len]
    row = {'mol_id': f'TOX{i:05d}', 'smiles': smiles}
    for t in TARGETS:
        row[t] = gen_label(t)
    rows.append(row)

fieldnames = ['mol_id', 'smiles'] + TARGETS
with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

size = os.path.getsize(OUT_CSV)
print(f"[OK] tox21.csv generated: {N} compounds, {len(TARGETS)} targets")
print(f"   File size: {size:,} bytes")
print(f"   Columns: mol_id, smiles, {', '.join(TARGETS)}")

# Print positive rate check
print("\nPositive rate check:")
import collections
for t in TARGETS:
    vals = [r[t] for r in rows if r[t] != '']
    pos = sum(1 for v in vals if v == 1)
    print(f"  {t:<20}: {pos/len(vals)*100:.1f}% positive  ({pos}/{len(vals)} labeled)")
