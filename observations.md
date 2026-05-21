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