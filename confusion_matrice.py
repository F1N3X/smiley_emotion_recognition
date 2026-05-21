import math
import csv
from pathlib import Path
from configs import *


# Charger les labels
labels = []
with open(labels_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        label = int(row['label'])
        labels.append(label)

# Compter les classes
class_counts = {i: 0 for i in range(5)}
for label in labels:
    class_counts[label] += 1

counts = class_counts

# Calculer les supports (validation set size)
supports = {}
for i in range(5):
    total = counts[i]
    train = int(total * 0.70)
    val = int(total * 0.15)
    test = total - train - val
    supports[i] = val

N = sum(supports.values())

# Charger les métriques
metrics_data = []
headers = None
with open(metrics_path, 'r') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    for row in reader:
        metrics_data.append(row)

last = metrics_data[-1] if metrics_data else {}

# Noms des émotions
EMOTION_NAMES = {0: "happy", 1: "neutral", 2: "sad", 3: "angry", 4: "surprised"}

def get_metric(kind, i, is_validation=True):
    """Extrait une métrique spécifique (precision/recall) pour une classe"""
    prefix = "validation" if is_validation else "train"
    candidates = [
        f"{prefix}_{kind}_{i}",
        f"{prefix}_class_{i}_{kind}",
        f"val_{kind}_{i}",
        f"val_{kind}_class_{i}",
        f"{kind}_{i}",
        f"{kind}_class_{i}",
    ]
    for c in candidates:
        if c in last and last[c]:
            try:
                v = float(last[c])
                return v
            except:
                pass
    
    return 0.0

# Extraire precision, recall et F1 de validation
precision = {}
recall = {}
f1_score = {}
for i in range(5):
    p = get_metric("precision", i, True)
    r = get_metric("recall", i, True)
    f1 = get_metric("f1", i, True)
    
    # Chercher dans les colonnes spécifiques
    prec_col = f"validation_class_{i}_precision"
    recall_col = f"validation_class_{i}_recall"
    f1_col = f"validation_class_{i}_f1"
    
    if prec_col in last and last[prec_col]:
        try:
            p = float(last[prec_col])
        except:
            pass
    
    if recall_col in last and last[recall_col]:
        try:
            r = float(last[recall_col])
        except:
            pass

    if f1_col in last and last[f1_col]:
        try:
            f1 = float(last[f1_col])
        except:
            pass

    if f1 <= 0.0 and (p > 0.0 or r > 0.0):
        denom = p + r
        f1 = (2.0 * p * r / denom) if denom > 0.0 else 0.0
    
    precision[i] = p
    recall[i] = r
    f1_score[i] = f1

print("=" * 70)
print("ANALYSE DES MATRICES DE CONFUSION")
print("=" * 70)

def distribute_integer(total, targets, weights):
    """Distribue un entier selon les poids"""
    if total <= 0 or not targets:
        return {t: 0 for t in targets}
    s = sum(weights)
    if s <= 0:
        base = total // len(targets)
        rem = total % len(targets)
        out = {t: base for t in targets}
        for t in targets[:rem]:
            out[t] += 1
        return out
    raw = [total * (w / s) for w in weights]
    floors = [int(math.floor(x)) for x in raw]
    rem = total - sum(floors)
    fracs = sorted([(raw[k] - floors[k], k) for k in range(len(targets))], reverse=True)
    for _, k in fracs[:rem]:
        floors[k] += 1
    return {targets[k]: floors[k] for k in range(len(targets))}

# Calcul des matrices one-vs-rest
ovr_matrices = {}
for i in range(5):
    s = supports[i]
    r = recall[i]
    p = precision[i]
    
    # TP = True Positives (prédits correctement comme classe i)
    tp = int(round(r * s)) if s > 0 else 0
    
    # FN = False Negatives (images de classe i mal prédites)
    fn = s - tp
    
    # FP = False Positives (images autres classes prédites comme i)
    if p > 0 and tp > 0:
        fp = int(round(tp * (1.0 / p - 1.0)))
    else:
        fp = 0
    
    # TN = True Negatives
    tn = N - tp - fn - fp
    
    ovr_matrices[i] = {
        'TP': tp, 'FN': fn, 'FP': fp, 'TN': tn,
        'matrix': [[tp, fp], [fn, tn]]
    }
    
    

conf = [[0 for _ in range(5)] for _ in range(5)]

# Diagonal = vrais positifs
for i in range(5):
    conf[i][i] = ovr_matrices[i]['TP']

# Distribuer les faux négatifs
for i in range(5):
    fn = ovr_matrices[i]['FN']
    targets = [j for j in range(5) if j != i]
    weights = [max(ovr_matrices[j]['FP'], 0) for j in targets]
    alloc = distribute_integer(fn, targets, weights)
    for j, v in alloc.items():
        conf[i][j] = v

# Afficher la matrice
print(f"\nVraie \\ Prédite{' ' * 14}", end="")
for j in range(5):
    print(f"{EMOTION_NAMES[j]:12s}", end="")
print()
print("-" * (25 + 12*5))

for i in range(5):
    print(f"{EMOTION_NAMES[i]:20s}", end="")
    for j in range(5):
        print(f"{conf[i][j]:12d}", end="")
    print()

# Analyse et interprétation
print("\n6. INTERPRÉTATION DES RÉSULTATS:")
print("-" * 70)

total_correct = sum(conf[i][i] for i in range(5))
total_samples = N
accuracy = total_correct / total_samples if total_samples > 0 else 0

print(f"\nAccuracité globale: {total_correct}/{total_samples} = {accuracy:.2%}")

print("\nPerformance par classe:")
for i in range(5):
    s = supports[i]
    if s > 0:
        class_accuracy = conf[i][i] / s
        print(
            f"  {EMOTION_NAMES[i]:12s}: acc={class_accuracy:.2%} "
            f"precision={precision[i]:.2%} recall={recall[i]:.2%} F1={f1_score[i]:.2%}"
        )

macro_f1 = sum(f1_score.values()) / len(f1_score) if f1_score else 0.0

print(f"\nAccuracy: {float(last.get('validation_accuracy', accuracy)):.2%}")
print(f"Macro F1: {macro_f1:.2%}")

print("\nProblèmes identifiés:")
for i in range(5):
    max_confusion = max([(conf[i][j], j) for j in range(5) if j != i])
    if max_confusion[0] > 0:
        print(f"  • {EMOTION_NAMES[i]:12s} confus avec {EMOTION_NAMES[max_confusion[1]]:12s}: {max_confusion[0]:2d} cas")

print("\nForces du modèle:")
for i in range(5):
    if recall[i] >= 0.8:
        print(f"  • {EMOTION_NAMES[i]:12s} bien reconnu (recall = {recall[i]:.2%})")

print("\nFaiblesses du modèle:")
for i in range(5):
    if recall[i] < 0.5:
        print(f"  • {EMOTION_NAMES[i]:12s} mal reconnu (recall = {recall[i]:.2%})")

print("\n" + "=" * 70)
