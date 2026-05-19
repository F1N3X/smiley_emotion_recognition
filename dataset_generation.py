import os
import random

# ==========================================
# CONFIGURATION
# ==========================================
BASE_DIR = "data"
IMAGES_PER_CLASS = 100
FORMAT_COULEUR = False  # True = PPM (Couleur P3) | False = PGM (Gris P2)
# ==========================================

# Détermination dynamique du dossier de sortie selon le format
if FORMAT_COULEUR:
    SUB_DIR = "ppm" 
else:
    SUB_DIR = "pgm"
OUTPUT_DIR = os.path.join(BASE_DIR, SUB_DIR)

EMOTION_NAMES = {0: "happy", 1: "neutral", 2: "sad", 3: "angry", 4: "surprised"}

# Création des dossiers imbriqués (ex: data/ppm/happy/)
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

def generate_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generate_image_matrix(template, is_couleur):
    """Génère la matrice finale (Gris ou Couleur) avec décalage et bruit appliqué."""
    shift_x, shift_y = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
    
    if is_couleur:
        bg = generate_random_color()
        fg = generate_random_color()
        while sum(abs(f - b) for f, b in zip(fg, bg)) < 150: # Contraste minimum
            fg = generate_random_color()
    else:
        bg, fg = 255, 0 # Blanc et Noir par défaut pour le PGM
        
    matrix = [[bg]*16 for _ in range(16)]
    
    for y in range(16):
        for x in range(16):
            orig_x, orig_y = x - shift_x, y - shift_y
            if 0 <= orig_x < 16 and 0 <= orig_y < 16:
                val = template[orig_y][orig_x]
                pixel_val = fg if val == 1 else bg
                
                if random.random() < 0.05:
                    noise = random.choice([-30, 30])
                    if is_couleur:
                        pixel_val = tuple(max(0, min(255, c + noise)) for c in pixel_val)
                    else:
                        pixel_val = max(0, min(255, pixel_val + noise))
                        
                matrix[y][x] = pixel_val
    return matrix

# Génération des fichiers
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

# Sauvegarde du fichier de labels CSV au bon endroit
with open(os.path.join(OUTPUT_DIR, "labels.csv"), "w") as f:
    f.write("filename,label\n" + "\n".join(labels_csv))

print(f"Dataset [{ext.upper()}] généré avec succès dans '{OUTPUT_DIR}' ! (Total : {img_counter} images)")