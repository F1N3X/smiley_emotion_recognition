# Réseau demandé
# Vous devez coder au minimum un réseau dense avec :
# — une couche d’entrée de taille d ;
# — une couche cachée de h neurones ;
# — une couche de sortie de C neurones, un par classe ;
# — une activation ReLU ou sigmoïde dans la couche cachée ;
# — une activation softmax en sortie.

# pour un dataset d'images 16x16 en niveaux de gris, d = 256
# pour un dataset d'images 16x16 en couleur, d = 768
# pour une couche de sortie de C neurones, C = 5 (par exemple, pour 5 émotions)
# h peut être choisi arbitrairement, par exemple h = 64 ou h = 128

# Construire un réseau de neurones from scratch, sans librairie de machine learning
# Interdiction d'utiliser des librairies externes comme TensorFlow, PyTorch, Keras, NumPy, etc.
# Seules les librairies standard de Python sont autorisées (math, random, etc.)
# Le  programme doit prendre une image de smiley en entrée et renvoyer une classe d'émotion

import math
import csv
import os
import random


# COFNIGURATION
IMAGE_FORMAT = "pgm"   # "pgm" ou "ppm"
DATA_DIR = os.path.join("data", IMAGE_FORMAT)
VECTOR_CSV = os.path.join(DATA_DIR, "vectors.csv")
METRICS_CSV = os.path.join(DATA_DIR, "training_metrics.csv")
INPUT_SIZE = 256 if IMAGE_FORMAT == "pgm" else 768
HIDDEN_SIZE = 8     # h  — nombre de neurones cachés
OUTPUT_SIZE = 5     # C  — nombre de classes (émotions)
ACTIVATION = "relu" # "relu" ou "sigmoid"
LEARNING_RATE = 0.01
TRAIN_RATIO = 0.70
VALIDATION_RATIO = 0.15
TEST_RATIO = 0.15
TARGET_ERROR = 0.01
RANDOM_SEED = 42

EMOTION_NAMES = {0: "happy", 1: "neutral", 2: "sad", 3: "angry", 4: "surprised"}
EMOTION_TO_INDEX = {name: index for index, name in EMOTION_NAMES.items()}


# FONCTIONS D'ACTIVATION
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(x):
    s = sigmoid(x)
    return s * (1 - s)

def relu(x):
    return max(0, x)

def relu_derivative(x):
    return 1.0 if x > 0 else 0.0

def activation(x):
    return relu(x) if ACTIVATION == "relu" else sigmoid(x)

def activation_derivative(x):
    return relu_derivative(x) if ACTIVATION == "relu" else sigmoid_derivative(x)

def softmax(logits):
    max_logit = max(logits)
    exps = [math.exp(logit - max_logit) for logit in logits]
    sum_exps = sum(exps)
    return [exp / sum_exps for exp in exps]


# CHARGEMENT DU DATASET
def load_vectors(csv_path):
    """Charge vectors.csv et retourne une liste de couples (vecteur, label)."""
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"Fichier introuvable : {csv_path}")

    records = []
    with open(csv_path, newline="") as file_handle:
        reader = csv.DictReader(file_handle)
        vector_fields = [name for name in reader.fieldnames if name not in {"filename", "label"}]

        for row in reader:
            vector = [float(row[field]) for field in vector_fields]
            label_value = row["label"]
            label = int(label_value) if label_value.isdigit() else EMOTION_TO_INDEX[label_value]
            records.append((vector, label))

    return records


def stratified_split(dataset, train_ratio=TRAIN_RATIO, validation_ratio=VALIDATION_RATIO, test_ratio=TEST_RATIO, seed=RANDOM_SEED):
    """Sépare le dataset en 70/15/15 pour chaque émotion."""
    if not math.isclose(train_ratio + validation_ratio + test_ratio, 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("Les ratios train/validation/test doivent sommer à 1.0")

    grouped = {label: [] for label in range(OUTPUT_SIZE)}
    for sample in dataset:
        grouped[sample[1]].append(sample)

    rng = random.Random(seed)
    train_set      = []
    validation_set = []
    test_set       = []

    for label, samples in grouped.items():
        rng.shuffle(samples)
        total = len(samples)
        train_count = int(total * train_ratio)
        validation_count = int(total * validation_ratio)
        test_count = total - train_count - validation_count

        train_set.extend(samples[:train_count])
        validation_set.extend(samples[train_count:train_count + validation_count])
        test_set.extend(samples[train_count + validation_count:train_count + validation_count + test_count])

        print(f"[SPLIT] {EMOTION_NAMES[label]}: {train_count} train, {validation_count} validation, {test_count} test")

    rng.shuffle(train_set)
    rng.shuffle(validation_set)
    rng.shuffle(test_set)
    return train_set, validation_set, test_set


# POIDS ET BIAIS
def init_network(d, h, C):
    """
    Crée et retourne les poids et biais du réseau.
 
    d : taille de l'entrée  (ex: 256 ou 768)
    h : nombre de neurones cachés
    C : nombre de classes en sortie (5 pour les émotions)
 
    W1 : matrice [h x d]  — poids entrée → cachée
    b1 : vecteur [h]      — biais de la couche cachée
    W2 : matrice [C x h]  — poids cachée → sortie
    b2 : vecteur [C]      — biais de la couche de sortie
    """
    W1 = [[random.uniform(-0.5, 0.5) for _ in range(d)] for _ in range(h)]
    b1 = [random.uniform(-0.5, 0.5) for _ in range(h)]
    W2 = [[random.uniform(-0.5, 0.5) for _ in range(h)] for _ in range(C)]
    b2 = [random.uniform(-0.5, 0.5) for _ in range(C)]
    return W1, b1, W2, b2


# FORWARD PASS
def forward_pass(x, W1, b1, W2, b2):
    h = len(W1)
    C = len(W2)
 
    # Couche cachée
    z1 = [sum(W1[j][i] * x[i] for i in range(len(x))) + b1[j] for j in range(h)]
    a1 = [activation(z) for z in z1]
 
    # Couche de sortie
    z2    = [sum(W2[k][j] * a1[j] for j in range(h)) + b2[k] for k in range(C)]
    y_hat = softmax(z2)
 
    return {"x": x, "z1": z1, "a1": a1, "z2": z2, "y_hat": y_hat}


# FONCTION D'ERREUR (CROSS-ENTROPY)
def cross_entropy(y_hat, y_true):
    return -math.log(y_hat[y_true] + 1e-12)


# BACKPROPAGATION
def backward(cache, y_true, W2):
    """
    Gradient couche de sortie :
        delta2[k] = y_hat[k] - y[k]
        dW2[k][j] = a1[j] * delta2[k]
        db2[k]    = delta2[k]
 
    Gradient couche cachée :
        delta1[j] = f'(z1[j]) * sum_k( W2[k][j] * delta2[k] )
        dW1[j][i] = x[i] * delta1[j]
        db1[j]    = delta1[j]
    """
    x, z1, a1, y_hat = cache["x"], cache["z1"], cache["a1"], cache["y_hat"]
    h = len(a1)
    C = len(y_hat)
    d = len(x)
 
    # delta couche de sortie
    delta2 = [y_hat[k] - (1.0 if k == y_true else 0.0) for k in range(C)]
    dW2    = [[a1[j] * delta2[k] for j in range(h)] for k in range(C)]
    db2    = delta2[:]
 
    # delta couche cachée
    delta1 = [
        activation_derivative(z1[j]) * sum(W2[k][j] * delta2[k] for k in range(C))
        for j in range(h)
    ]
    dW1 = [[x[i] * delta1[j] for i in range(d)] for j in range(h)]
    db1 = delta1[:]
 
    return dW1, db1, dW2, db2


# MISE À JOUR DES POIDS
def update_weights(W1, b1, W2, b2, dW1, db1, dW2, db2):
    h, d, C = len(W1), len(W1[0]), len(W2)
 
    for j in range(h):
        for i in range(d):
            W1[j][i] -= LEARNING_RATE * dW1[j][i]
        b1[j] -= LEARNING_RATE * db1[j]
 
    for k in range(C):
        for j in range(h):
            W2[k][j] -= LEARNING_RATE * dW2[k][j]
        b2[k] -= LEARNING_RATE * db2[k]


# ENTRAÎNEMENT
def train_epoch(dataset, W1, b1, W2, b2):
    random.shuffle(dataset)
    total_loss = 0.0
 
    for x, y_true in dataset:
        cache = forward_pass(x, W1, b1, W2, b2)
        total_loss += cross_entropy(cache["y_hat"], y_true)
        dW1, db1, dW2, db2 = backward(cache, y_true, W2)
        update_weights(W1, b1, W2, b2, dW1, db1, dW2, db2)
 
    return total_loss / len(dataset)


def evaluate(dataset, W1, b1, W2, b2):
    """Retourne les métriques globales et les métriques par classe sur un ensemble."""
    total_loss = 0.0
    correct = 0
    true_positives  = [0] * len(W2)  # Nombre de véritables positifs pour chaque classe
    false_positives = [0] * len(W2)  # Nombre de faux positifs pour chaque classe
    false_negatives = [0] * len(W2)  # Nombre de faux négatifs pour chaque classe
    class_loss_sums = [0.0] * len(W2)
    class_counts    = [0] * len(W2)

    for x, y_true in dataset:
        cache = forward_pass(x, W1, b1, W2, b2)
        y_hat = cache["y_hat"]
        sample_loss = cross_entropy(y_hat, y_true)
        total_loss += sample_loss
        class_loss_sums[y_true] += sample_loss
        class_counts[y_true] += 1

        predicted_class = y_hat.index(max(y_hat))
        if predicted_class == y_true:
            correct += 1
            true_positives[y_true] += 1
        else:
            false_positives[predicted_class] += 1
            false_negatives[y_true] += 1

    average_loss = total_loss / len(dataset)
    accuracy = correct / len(dataset)
    error_rate = 1.0 - accuracy

    # Calcul des métriques par classe
    precisions = []
    recalls = []
    f1_scores = []
    class_metrics = []

    for i in range(len(W2)):
        tp = true_positives[i]
        fp = false_positives[i]
        fn = false_negatives[i]
        tn = len(dataset) - tp - fp - fn

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        class_loss = class_loss_sums[i] / class_counts[i] if class_counts[i] > 0 else 0.0
        class_accuracy = (tp + tn) / len(dataset) if len(dataset) > 0 else 0.0

        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1_score)
        class_metrics.append({
            "class_index": i,
            "class_name": EMOTION_NAMES[i],
            "loss": class_loss,
            "accuracy": class_accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1_score,
        })

    macro_precision = sum(precisions) / len(precisions)
    macro_recall = sum(recalls) / len(recalls)
    macro_f1 = sum(f1_scores) / len(f1_scores)

    return {
        "loss": average_loss,
        "accuracy": accuracy,
        "error_rate": error_rate,
        "precision": macro_precision,
        "recall": macro_recall,
        "f1": macro_f1,
        "per_class": class_metrics,
    }


def save_metrics_csv(history, output_path):
    """Sauvegarde les métriques d'entraînement au fil des epochs."""
    dirpath = os.path.dirname(output_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    class_metrics_fieldnames = []
    for prefix in ("train", "validation"):
        for class_index in range(OUTPUT_SIZE):
            class_metrics_fieldnames.extend([
                f"{prefix}_class_{class_index}_name",
                f"{prefix}_class_{class_index}_loss",
                f"{prefix}_class_{class_index}_accuracy",
                f"{prefix}_class_{class_index}_precision",
                f"{prefix}_class_{class_index}_recall",
                f"{prefix}_class_{class_index}_f1",
            ])

    fieldnames = [
        "epoch",
        "train_loss",
        "train_accuracy",
        "train_error",
        "train_precision",
        "train_recall",
        "train_f1",
        "validation_loss",
        "validation_accuracy",
        "validation_error",
        "validation_precision",
        "validation_recall",
        "validation_f1",
    ] + class_metrics_fieldnames

    with open(output_path, "w", newline="") as file_handle:
        writer = csv.DictWriter(file_handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in history:
            flat_row = dict(row)

            train_per_class = flat_row.pop("train_per_class", [])
            validation_per_class = flat_row.pop("validation_per_class", [])

            for prefix, class_metrics_list in (("train", train_per_class), ("validation", validation_per_class)):
                for class_index in range(OUTPUT_SIZE):
                    class_name = EMOTION_NAMES[class_index]
                    class_metrics = class_metrics_list[class_index] if class_index < len(class_metrics_list) else {}
                    flat_row[f"{prefix}_class_{class_index}_name"] = class_metrics.get("class_name", class_name)
                    flat_row[f"{prefix}_class_{class_index}_loss"] = class_metrics.get("loss", 0.0)
                    flat_row[f"{prefix}_class_{class_index}_accuracy"] = class_metrics.get("accuracy", 0.0)
                    flat_row[f"{prefix}_class_{class_index}_precision"] = class_metrics.get("precision", 0.0)
                    flat_row[f"{prefix}_class_{class_index}_recall"] = class_metrics.get("recall", 0.0)
                    flat_row[f"{prefix}_class_{class_index}_f1"] = class_metrics.get("f1", 0.0)

            writer.writerow(flat_row)


def train_until_target(train_set, validation_set, W1, b1, W2, b2, target_error=TARGET_ERROR):
    history = []
    epoch = 0
    MAX_EPOCHS = 1000
    while epoch < MAX_EPOCHS:  
        epoch += 1
        train_loss = train_epoch(train_set, W1, b1, W2, b2)
        
        validation_metrics = evaluate(validation_set, W1, b1, W2, b2)
        validation_loss      = validation_metrics["loss"]
        validation_accuracy  = validation_metrics["accuracy"]
        validation_error     = validation_metrics["error_rate"]
        validation_precision = validation_metrics["precision"]
        validation_recall    = validation_metrics["recall"]
        validation_f1        = validation_metrics["f1"]
        validation_per_class = validation_metrics["per_class"]

        train_metrics = evaluate(train_set, W1, b1, W2, b2)
        train_loss = train_metrics["loss"]
        train_accuracy = train_metrics["accuracy"]
        train_error = train_metrics["error_rate"]
        train_precision = train_metrics["precision"]
        train_recall = train_metrics["recall"]
        train_f1 = train_metrics["f1"]
        train_per_class = train_metrics["per_class"]

        history.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "train_accuracy": train_accuracy,
            "train_error": train_error,
            "train_precision": train_precision,
            "train_recall": train_recall,
            "train_f1": train_f1,
            "train_per_class": train_per_class,
            "validation_loss": validation_loss,
            "validation_accuracy": validation_accuracy,
            "validation_error": validation_error,
            "validation_precision": validation_precision,
            "validation_recall": validation_recall,
            "validation_f1": validation_f1,
            "validation_per_class": validation_per_class
        })

        print(
            f"Epoch {epoch:03d} | "
            f"train_loss={train_loss:.4f} train_error={train_error:.4f} | "
            f"validation_loss={validation_loss:.4f} validation_error={validation_error:.4f} | "
        )
        print(
            f"          | "
            f"train_acc={train_accuracy:.4f} train_precision={train_precision:.4f} train_recall={train_recall:.4f} train_f1={train_f1:.4f} | "
            f"validation_acc={validation_accuracy:.4f} validation_precision={validation_precision:.4f} validation_recall={validation_recall:.4f} validation_f1={validation_f1:.4f}"
            "\n"
        )

        if validation_error < target_error:
            print(f"[STOP] Erreur de validation < {target_error:.2f} atteinte à l'epoch {epoch}.")
            break

    return history


def main():
    random.seed(RANDOM_SEED)

    dataset = load_vectors(VECTOR_CSV)
    if not dataset:
        raise ValueError("Aucune donnée trouvée dans vectors.csv")

    input_size = len(dataset[0][0])
    if input_size != INPUT_SIZE:
        print(f"[INFO] INPUT_SIZE ajusté automatiquement de {INPUT_SIZE} à {input_size}")

    train_set, validation_set, test_set = stratified_split(dataset)
    print(f"[DATA] train={len(train_set)} validation={len(validation_set)} test={len(test_set)}")

    W1, b1, W2, b2 = init_network(input_size, HIDDEN_SIZE, OUTPUT_SIZE)
    history = train_until_target(train_set, validation_set, W1, b1, W2, b2)
    save_metrics_csv(history, METRICS_CSV)
    print(f"[CSV] métriques sauvegardées dans {METRICS_CSV}")

    test_metrics = evaluate(test_set, W1, b1, W2, b2)
    test_loss = test_metrics["loss"]
    test_accuracy = test_metrics["accuracy"]
    test_error = test_metrics["error_rate"]
    test_precision = test_metrics["precision"]
    test_recall = test_metrics["recall"]
    test_f1 = test_metrics["f1"]
    print(f"[TEST] loss={test_loss:.4f} accuracy={test_accuracy:.4f} error={test_error:.4f} precision={test_precision:.4f} recall={test_recall:.4f} f1={test_f1:.4f}")

    for class_metrics in test_metrics["per_class"]:
        print(
            f"[TEST][{class_metrics['class_name']}] "
            f"loss={class_metrics['loss']:.4f} accuracy={class_metrics['accuracy']:.4f} "
            f"precision={class_metrics['precision']:.4f} recall={class_metrics['recall']:.4f} "
        )


if __name__ == "__main__":
    main()
