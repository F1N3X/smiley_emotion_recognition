import os
from pathlib import Path

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
TARGET_ERROR = 0.05
RANDOM_SEED = 42

ROOT_DIR = Path(__file__).resolve().parent
METRICS_PATH = ROOT_DIR / "data" / IMAGE_FORMAT / "training_metrics.csv"
OUTPUT_PATH = ROOT_DIR / "data" / IMAGE_FORMAT / "loss_curves_comparison.svg"

base = Path(__file__).parent
labels_path = base / "data" / IMAGE_FORMAT / "labels.csv"
metrics_path = base / "data" / IMAGE_FORMAT / "training_metrics.csv"

BASE_DIR = "data"
IMAGES_PER_CLASS = 100
FORMAT_COULEUR = False  # True = PPM (Couleur P3) | False = PGM (Gris P2)
SUB_DIR = IMAGE_FORMAT
OUTPUT_DIR = os.path.join(BASE_DIR, SUB_DIR)

OUTPUT_CSV = os.path.join(BASE_DIR, "vectors.csv")
INPUT_DIR  = os.path.join(BASE_DIR, IMAGE_FORMAT)