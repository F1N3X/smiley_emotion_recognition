import os
import random
import math

# ==========================================
# CONFIGURATION
# ==========================================
BASE_DIR = "data"
IMAGES_PER_CLASS = 100
FORMAT_COULEUR = False  # True = PPM (Couleur P3) | False = PGM (Gris P2)
# ==========================================

if FORMAT_COULEUR:
    SUB_DIR = "ppm"
else:
    SUB_DIR = "pgm"
OUTPUT_DIR = os.path.join(BASE_DIR, SUB_DIR)

EMOTION_NAMES = {0: "happy", 1: "neutral", 2: "sad", 3: "angry", 4: "surprised"}

os.makedirs(OUTPUT_DIR, exist_ok=True)
for name in EMOTION_NAMES.values():
    os.makedirs(os.path.join(OUTPUT_DIR, name), exist_ok=True)

BASE_TEMPLATES = {
    0: [  # Happy
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0], [0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ],
    1: [  # Neutral
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0], [0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ],
    2: [  # Sad
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0], [0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ],
    3: [  # Angry
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0], [0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0], [0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ],
    4: [  # Surprised
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,1,0,1,0,0,0,0,1,0,1,0,0,0], [0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0], [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
}

# ==========================================
# AUGMENTATION HELPERS
# ==========================================

def apply_shift(template, shift_x, shift_y):
    """Décalage translation (comme avant)."""
    result = [[0]*16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            ox, oy = x - shift_x, y - shift_y
            if 0 <= ox < 16 and 0 <= oy < 16:
                result[y][x] = template[oy][ox]
    return result

def apply_scale(template, scale):
    """
    Zoom centré sur la grille 16x16.
    scale > 1 = zoom in (traits plus grands), scale < 1 = zoom out.
    """
    result = [[0]*16 for _ in range(16)]
    cx, cy = 7.5, 7.5
    for y in range(16):
        for x in range(16):
            ox = int((x - cx) / scale + cx)
            oy = int((y - cy) / scale + cy)
            if 0 <= ox < 16 and 0 <= oy < 16:
                result[y][x] = template[oy][ox]
    return result

def apply_rotation(template, angle_deg):
    """
    Rotation légère (conseillée : ±10°) centrée sur la grille.
    """
    result = [[0]*16 for _ in range(16)]
    cx, cy = 7.5, 7.5
    angle_rad = math.radians(-angle_deg)
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    for y in range(16):
        for x in range(16):
            dx, dy = x - cx, y - cy
            ox = int(cos_a * dx - sin_a * dy + cx)
            oy = int(sin_a * dx + cos_a * dy + cy)
            if 0 <= ox < 16 and 0 <= oy < 16:
                result[y][x] = template[oy][ox]
    return result

def apply_thickness(template, thicken=True):
    """
    Épaissit les traits de 1 pixel dans toutes les directions (dilatation morphologique).
    """
    if not thicken:
        return template
    result = [[0]*16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if template[y][x] == 1:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        ny, nx = y + dy, x + dx
                        if 0 <= nx < 16 and 0 <= ny < 16:
                            result[ny][nx] = 1
    return result

def apply_erosion(template):
    """
    Érode les traits : supprime les pixels allumés qui ont au moins un voisin
    (4-connexité) éteint — inverse de l'épaississement.
    """
    result = [[0]*16 for _ in range(16)]
    for y in range(16):
        for x in range(16):
            if template[y][x] == 1:
                neighbors = [
                    template[y-1][x] if y > 0  else 0,
                    template[y+1][x] if y < 15 else 0,
                    template[y][x-1] if x > 0  else 0,
                    template[y][x+1] if x < 15 else 0,
                ]
                if all(n == 1 for n in neighbors):  # Garde seulement les pixels "intérieurs"
                    result[y][x] = 1
    return result

def apply_dropout(template, rate=0.15):
    """
    Supprime aléatoirement une fraction des pixels allumés (traits incomplets).
    """
    result = [row[:] for row in template]
    for y in range(16):
        for x in range(16):
            if result[y][x] == 1 and random.random() < rate:
                result[y][x] = 0
    return result

def apply_blur(matrix, is_color, bg, fg):
    """
    Flou local : moyenne 3x3 des voisins pour les pixels de bord de trait.
    Appliqué sur la matrice finale (valeurs réelles, pas 0/1).
    """
    result = [row[:] for row in matrix]
    for y in range(1, 15):
        for x in range(1, 15):
            if random.random() < 0.3:  # Appliqué seulement à 30% des pixels
                if is_color:
                    neighbors = [matrix[y+dy][x+dx] for dy in [-1,0,1] for dx in [-1,0,1]]
                    avg = tuple(int(sum(n[c] for n in neighbors) / 9) for c in range(3))
                    result[y][x] = avg
                else:
                    neighbors = [matrix[y+dy][x+dx] for dy in [-1,0,1] for dx in [-1,0,1]]
                    result[y][x] = int(sum(neighbors) / 9)
    return result

# ==========================================
# GÉNÉRATION PRINCIPALE
# ==========================================

def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generate_image_matrix(template, is_color):
    """
    Pipeline d'augmentation complet :
      1. Rotation aléatoire légère
      2. Mise à l'échelle aléatoire
      3. Translation (décalage)
      4. Épaississement optionnel des traits
      5. Dropout de pixels
      6. Conversion en niveaux de gris ou couleur avec intensité variable
      7. Bruit salt & pepper
      8. Flou local optionnel
    """
    # --- Étape 1 : Transformations géométriques ---
    # Sur 16×16, ±5° est déjà significatif (≈1px de décalage en bord de grille)
    angle    = random.uniform(-5, 5)            # Rotation ±5°
    # Zoom très limité : à 0.9, un trait de 2px reste à 2px ; en dessous il risque de disparaître
    scale    = random.uniform(0.90, 1.10)       # Zoom ±10%
    shift_x  = random.randint(-1, 1)            # Translation ±1 px
    shift_y  = random.randint(-1, 1)

    t = apply_rotation(template, angle)
    t = apply_scale(t, scale)
    t = apply_shift(t, shift_x, shift_y)

    # --- Étape 2 : Variation structurelle des traits ---
    # Érosion retirée : sur des traits de 1–2px elle efface complètement les features
    morph = random.random()
    if morph < 0.30:                            # 30% épaississement (conservateur)
        t = apply_thickness(t)
    # Dropout très faible : sur 2px de largeur, chaque pixel compte
    dropout_rate = random.uniform(0.0, 0.08)    # 0–8% maximum
    t = apply_dropout(t, dropout_rate)

    # --- Étape 3 : Couleurs / intensités ---
    if is_color:
        bg = generate_random_color()
        fg = generate_random_color()
        while sum(abs(f - b) for f, b in zip(fg, bg)) < 150:
            fg = generate_random_color()
    else:
        # Fond légèrement variable, encre légèrement variable — contraste toujours lisible
        bg = random.randint(220, 255)
        fg = random.randint(0, 30)

    # --- Étape 4 : Construction de la matrice ---
    matrix = [[bg]*16 for _ in range(16)]
    noise_rate = random.uniform(0.01, 0.05)     # Salt & pepper 1–5% (au-delà ça pollue trop)
    gaussian_std = random.uniform(0, 8)         # Gaussien doux : std max 8 sur une plage 0–255

    for y in range(16):
        for x in range(16):
            pixel_val = fg if t[y][x] == 1 else bg

            # Bruit gaussien simulé (somme de petites perturbations aléatoires ≈ loi normale)
            if gaussian_std > 0:
                gauss = sum(random.uniform(-1, 1) for _ in range(6)) / 6  # ≈ N(0,1) par TCL
                gauss_noise = int(gauss * gaussian_std)
                if is_color:
                    pixel_val = tuple(max(0, min(255, c + gauss_noise)) for c in pixel_val)
                else:
                    pixel_val = max(0, min(255, pixel_val + gauss_noise))

            # Bruit salt & pepper
            if random.random() < noise_rate:
                salt_or_pepper = 255 if random.random() < 0.5 else 0
                pixel_val = (salt_or_pepper,)*3 if is_color else salt_or_pepper

            matrix[y][x] = pixel_val

    # --- Étape 5 : Flou local optionnel ---
    if random.random() < 0.3:
        matrix = apply_blur(matrix, is_color, bg, fg)

    return matrix

# ==========================================
# ÉCRITURE DES FICHIERS
# ==========================================

labels_csv = []
img_counter = 0
ext = SUB_DIR
header = "P3" if FORMAT_COULEUR else "P2"

for label, template in BASE_TEMPLATES.items():
    name = EMOTION_NAMES[label]

    for i in range(IMAGES_PER_CLASS):
        filename = f"{img_counter}.{ext}"
        filepath = os.path.join(OUTPUT_DIR, name, filename)

        variant_matrix = generate_image_matrix(template, FORMAT_COULEUR)
        with open(filepath, "w") as f:
            f.write(f"{header}\n16 16\n255\n")
            for row in variant_matrix:
                if FORMAT_COULEUR:
                    row_str = " ".join(f"{p[0]} {p[1]} {p[2]}" for p in row)
                else:
                    row_str = " ".join(map(str, row))
                f.write(row_str + "\n")

        labels_csv.append(f"{name}/{filename},{label}")
        img_counter += 1

with open(os.path.join(OUTPUT_DIR, "labels.csv"), "w") as f:
    f.write("filename,label\n" + "\n".join(labels_csv))

print(f"Dataset [{ext.upper()}] généré avec succès dans '{OUTPUT_DIR}' ! (Total : {img_counter} images)")