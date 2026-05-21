# Premier cas d'entrainement :

## Paramètres :
- INPUT_SIZE       = 256
- HIDDEN_SIZE      = 8
- OUTPUT_SIZE      = 5
- ACTIVATION       = relu
- LEARNING_RATE    = 0.01
- TRAIN_RATIO      = 0.70
- VALIDATION_RATIO = 0.15
- TEST_RATIO       = 0.15
- TARGET_ERROR     = 0.05

### Nombre d'epochs :
75

### Matrice de confusion :
| Vraie \ Prédite | happy | neutral | sad | angry | surprised |
| --- | ---: | ---: | ---: | ---: | ---: |
| happy | 15 | 0 | 0 | 0 | 0 |
| neutral | 1 | 13 | 1 | 0 | 0 |
| sad | 0 | 0 | 15 | 0 | 0 |
| angry | 1 | 0 | 0 | 14 | 0 |
| surprised | 0 | 0 | 0 | 0 | 15 |

Performance par classe:
 - happy : 
    - acc=100.00% 
    - precision=88.24% 
    - recall=100.00% 
    - F1=93.75%
 - neutral : 
    - acc=86.67% 
    - precision=100.00% 
    - recall=86.67% 
    - F1=92.86%
 - sad : 
    - acc=100.00% 
    - precision=93.75% 
    - recall=100.00% 
    - F1=96.77%
 - angry : 
    - acc=93.33% 
    - precision=100.00% 
    - recall=93.33% 
    - F1=96.55%
 - surprised : 
    - acc=100.00% 
    - precision=100.00% 
    - recall=100.00% 
    - F1=100.00%

Accuracy globale : 96.00%

Macro F1: 95.99%

### Interprétation :
- Le modèle est globalement très performant, avec une accuracy élevée et un macro F1 proche de l'accuracy, ce qui indique un comportement assez équilibré entre les classes.
- La classe `surprised` est la mieux reconnue ici, sans erreur sur l'échantillon de validation affiché.
- Les principales confusions concernent `neutral` et, dans une moindre mesure, `angry`, ce qui suggère que ces expressions partagent des caractéristiques visuelles proches dans le jeu de données.
- Les scores de precision et de recall restent élevés pour toutes les classes, donc le modèle ne semble pas déséquilibré sur une classe particulière.
- En pratique, les erreurs restantes sont ponctuelles et la matrice de confusion montre que le modèle généralise correctement sur ce premier entraînement.



# Modification du learning rate 

# Learning rate à 0.1 :
| Vraie \ Prédite | happy | neutral | sad | angry | surprised |
| --- | ---: | ---: | ---: | ---: | ---: |
| happy | 15 | 0 | 0 | 0 | 0 |
| neutral | 15 | 0 | 0 | 0 | 0 |
| sad | 15 | 0 | 0 | 0 | 0 |
| angry | 15 | 0 | 0 | 0 | 0 |
| surprised | 15 | 0 | 0 | 0 | 0 |

Performance par classe:
 - happy : 
    - acc=100.00% 
    - precision=20.00% 
    - recall=100.00% 
    - F1=93.33.33%
 - neutral : 
    - acc=0.00% 
    - precision=0.00% 
    - recall=0.00% 
    - F1=0.00%
 - sad : 
    - acc=0.00% 
    - precision=0.00% 
    - recall=0.00% 
    - F1=0.00%
 - angry : 
    - acc=0.00% 
    - precision=0.00% 
    - recall=0.00% 
    - F1=0.00%
 - surprised : 
    - acc=0.00% 
    - precision=0.00% 
    - recall=0.00% 
    - F1=0.00%

Accuracy globale : 20.00%

Macro F1: 6.67%


## Learning rate à 0.01 :
### Arrêt de la boucle au bout de 300 epochs

| Vraie \ Prédite | happy | neutral | sad | angry | surprised |
| --- | ---: | ---: | ---: | ---: | ---: |
| happy | 12 | 2 | 0 | 1 | 0 |
| neutral | 14 | 0 | 1 | 0 | 0 |
| sad | 0 | 0 | 15 | 0 | 0 |
| angry | 0 | 1 | 0 | 14 | 0 |
| surprised | 1 | 0 | 0 | 0 | 14 |

Performance par classe:
 - happy : 
    - acc=80.00% 
    - precision=92.31% 
    - recall=80.00% 
    - F1=93.85.71%
 - neutral : 
    - acc=93.33% 
    - precision=82.35% 
    - recall=93.33% 
    - F1=87.50%
 - sad : 
    - acc=100.00% 
    - precision=93.75% 
    - recall=100.00% 
    - F1=96.77%
 - angry : 
    - acc=93.33% 
    - precision=93.33% 
    - recall=93.33% 
    - F1=93.33%
 - surprised : 
    - acc=93.33% 
    - precision=100.00% 
    - recall=93.33% 
    - F1=96.55%

Accuracy globale : 92.00%

Macro F1: 91.97%

## Interprétation

- Premier entraînement (LR = 0.01, 75 epochs) : excellente performance globale (accuracy 96%, macro F1 95.99%). Le modèle est équilibré entre les classes, `surprised` et `sad` sont parfaitement reconnus ici. Les confusions restantes sont faibles et localisées (`neutral` ↔ `sad`, `angry` ↔ `happy`).

- Learning rate = 0.1 : effondrement du modèle vers une prédiction majoritaire (tout prédit `happy`). Symptôme d'un taux d'apprentissage trop élevé : le modèle s'enferme dans un classifieur. Cela donne une très haute recall pour `happy` mais des précisions nulles pour les autres classes.

- Learning rate = 0.01 (300 epochs) : performance dégradée par rapport au premier cas (accuracy 92%, macro F1 91.97%). Deux hypothèses plausibles :
   - surapprentissage / instabilité due à un training trop long sans early stopping (le modèle exploite le bruit) ;
   - oscillations d'entraînement conduisant à un minimum moins bon sur la validation que celui atteint au bout de 75 epochs.
