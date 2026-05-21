# smiley_emotion_recognition

Projet d'apprentissage supervisé pour classer des émotions à partir de petits visages générés en 16x16, en niveaux de gris (PGM) ou en couleur (PPM).

Le projet est volontairement simple et entièrement écrit en Python standard. Il suit une chaîne de traitement fixe : génération du dataset, conversion en vecteurs, entraînement du réseau, analyse des résultats, puis étude de l'overfitting.

## Arborescence

- `dataset_generation.py` : génère les images PGM/PPM et `labels.csv`.
- `images_to_vector.py` : convertit les images en vecteurs normalisés et produit `vectors.csv`.
- `neural_network.py` : entraîne le réseau de neurones from scratch et écrit `training_metrics.csv`.
- `confusion_matrice.py` : lit les métriques finales et reconstruit l'analyse de validation sous forme de matrice de confusion.
- `overfitting_analysis.py` : trace les courbes de loss train/validation dans un fichier SVG.
- `configs.py` : centralise le format d'image et les hyperparamètres du modèle.

Les données sont stockées dans `data/pgm/` ou `data/ppm/` selon `IMAGE_FORMAT`.

## Pré-requis

- Python 3.10+.
- Aucune dépendance externe n'est requise.

## Flux d'exécution

L'ordre des scripts est important. Il faut les exécuter dans cet ordre à chaque fois que le format des images ou les paramètres ont changé :

1. `dataset_generation.py`
2. `images_to_vector.py`
3. `neural_network.py`
4. `confusion_matrice.py`
5. `overfitting_analysis.py`

### 1. Générer le dataset

Ce script crée les images synthétiques dans le dossier défini par `IMAGE_FORMAT` dans `configs.py` et écrit le fichier `labels.csv` correspondant.

```powershell
python dataset_generation.py
```

### 2. Convertir les images en vecteurs

Ce script lit les images générées, les normalise dans `[0, 1]`, puis crée `vectors.csv`.

```powershell
python images_to_vector.py
```

### 3. Entraîner le réseau de neurones

Ce script charge `vectors.csv`, effectue le split train/validation/test, entraîne le modèle, puis sauvegarde les métriques dans `training_metrics.csv`.

```powershell
python neural_network.py
```

À la fin, le script affiche aussi les métriques de test.

### 4. Produire la matrice de confusion

Ce script lit les métriques de validation du dernier epoch et reconstruit une matrice de confusion textuelle ainsi que les scores par classe.

```powershell
python confusion_matrice.py
```

### 5. Tracer les courbes de loss

Ce script lit `training_metrics.csv` et génère un graphique SVG de comparaison entre la loss d'entraînement et la loss de validation.

```powershell
python overfitting_analysis.py
```

## Configuration

Le fichier `configs.py` regroupe les réglages principaux. C'est l'endroit à modifier pour changer le format des images ou les paramètres du modèle.

### Format des images

- `IMAGE_FORMAT` : `"pgm"` pour les niveaux de gris, `"ppm"` pour la couleur.
- `DATA_DIR` / `INPUT_DIR` / `OUTPUT_DIR` : chemins dérivés automatiquement du format choisi.
- `INPUT_SIZE` : vaut `256` en PGM et `768` en PPM.
- `FORMAT_COULEUR` : indicateur booléen utilisé par la génération du dataset.

Quand `IMAGE_FORMAT` change, il faut relancer toute la chaîne, car les fichiers générés dépendent du format.

### Paramètres du modèle

- `HIDDEN_SIZE` : nombre de neurones dans la couche cachée.
- `OUTPUT_SIZE` : nombre de classes à prédire.
- `ACTIVATION` : `"relu"` ou `"sigmoid"`.
- `LEARNING_RATE` : taux d'apprentissage.
- `TRAIN_RATIO`, `VALIDATION_RATIO`, `TEST_RATIO` : répartition du dataset.
- `TARGET_ERROR` : seuil d'arrêt anticipé utilisé pendant l'entraînement.
- `RANDOM_SEED` : graine pour rendre les expériences reproductibles.
- `EARLY_STOPPING` : défini si le modèle s'arrête lorsque la target error est atteinte ou s'il continue jusqu'à sa limite

### Paramètres du dataset

- `IMAGES_PER_CLASS` : nombre d'images générées par classe.

## Résultats produits

- `data/<format>/labels.csv` : correspondance image -> classe.
- `data/vectors.csv` : vecteurs d'entrée normalisés.
- `data/<format>/training_metrics.csv` : métriques par epoch.
- `data/<format>/loss_curves_comparison.svg` : graphique des pertes.

## Exemple de modification

Pour passer du PGM au PPM :

1. Modifier `IMAGE_FORMAT = "ppm"` dans `configs.py`.
2. Relancer `dataset_generation.py`, puis `images_to_vector.py`, puis `neural_network.py`.
3. Relancer ensuite `confusion_matrice.py` et `overfitting_analysis.py`.

Pour tester un autre modèle :

1. Modifier `HIDDEN_SIZE`, `LEARNING_RATE`, `ACTIVATION` ou les ratios de split dans `configs.py`.
2. Relancer la chaîne complète de scripts.
