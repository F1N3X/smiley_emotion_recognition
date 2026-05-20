import os
import csv

# CONFIGURATION
base_dir     = "data"
format       = "pgm"   # "pgm" ou "ppm"
OUTPUT_CSV   = os.path.join(base_dir, format, "vectors.csv")
INPUT_DIR    = os.path.join(base_dir, format)


def read_file(filepath):
    """
    Lit un fichier PGM ou PPM et retourne une liste plate de ses pixels.
    Retourne une liste plate de longueur width*height (=256 pour 16x16) pour PGM, ou width*height*3 (768) pour PPM.
    """
    with open(filepath, "r") as f:
        f.readline()  # "P2" ou "P3"
        f.readline()  # "16 16"
        f.readline()  # "255"
        pixels = []
        for line in f:
            pixels.extend(int(v) for v in line.split())
    return pixels     # vecteur de taille 256 ou 768


# Normalisation
def normalize(vector, maxval=255):
    """Ramène chaque composante dans [0.0, 1.0]."""
    return [round(v / maxval, 6) for v in vector]


# Parcours du dataset et écriture du CSV
def build_vectors(input_dir, fmt):
    """
    Parcourt input_dir/<classe>/<image>.<fmt> et retourne une liste de dicts :
      {"filename": ..., "label": ..., "vector": [...]}
    """
    reader = read_file
    records = []

    # Lecture du labels.csv pour connaître les labels
    labels_path = os.path.join(input_dir, "labels.csv")
    label_map = {}
    if os.path.isfile(labels_path):
        with open(labels_path, newline="") as f:
            for row in csv.DictReader(f):
                label_map[row["filename"]] = row["label"]

    # Parcours des sous-dossiers (une émotion par dossier)
    for class_name in sorted(os.listdir(input_dir)):
        class_dir = os.path.join(input_dir, class_name)
        if not os.path.isdir(class_dir):
            continue

        # Parcours des fichiers d'images dans le dossier de classe
        for fname in sorted(os.listdir(class_dir)):
            if not fname.endswith(f".{fmt}"):
                continue

            rel_path = os.path.join(class_name, fname)   # ex: happy/0.pgm
            filepath  = os.path.join(class_dir, fname)

            try:
                pixels = reader(filepath)
            except Exception as e:
                print(f"[ERREUR] {rel_path} : {e}")
                continue

            vector = normalize(pixels)
            label  = label_map.get(rel_path, class_name)  # fallback = nom du dossier

            records.append({
                "filename": rel_path,
                "label":    label,
                "vector":   vector,
            })

    return records


# Sauvegarde en CSV  (1 ligne = 1 image)
def save_csv(records, output_path, fmt):
    """
    Colonnes : filename, label, x1, x2, ..., xN
    N = 256 pour PGM, 768 pour PPM.
    """
    if not records:
        print("Aucun enregistrement à sauvegarder.")
        return

    vector_len = len(records[0]["vector"])
    header = ["filename", "label"] + [f"x{i+1}" for i in range(vector_len)]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for rec in records:
            writer.writerow([rec["filename"], rec["label"]] + rec["vector"])

    fmt_str  = "PPM (couleur)" if fmt == "ppm" else "PGM (gris)"
    norm_str = "normalisé [0,1]"
    print(f"[OK] {len(records)} vecteurs {fmt_str} {norm_str} "
          f"(dim={vector_len}) sauvegardés dans : {output_path}")


# Point d'entrée
if __name__ == "__main__":
    print(f"Conversion des images {format.upper()} en vecteurs...")
    records = build_vectors(INPUT_DIR, format)
    save_csv(records, OUTPUT_CSV, format)

    # Aperçu du premier vecteur
    if records:
        v = records[0]
        print(f"\nExemple — {v['filename']} (label={v['label']}) :")
        print(f"  Taille du vecteur : {len(v['vector'])}")
        print(f"  5 premières valeurs : {v['vector'][:5]}")
        print(f"  5 dernières valeurs  : {v['vector'][-5:]}")