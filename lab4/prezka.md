# Sprawko
Nie, nie użyje worda

## Eksploracja danych
Nie wiem czy jest dużo do analizy, szczególnie kiedy jest to podane w pakiecie danych.

Attribute:   Min     Max      Mean     SD      Correlation with class
 2. RI:       1.5112  1.5339   1.5184  0.0030  -0.1642
 3. Na:      10.73   17.38    13.4079  0.8166   0.5030
 4. Mg:       0       4.49     2.6845  1.4424  -0.7447
 5. Al:       0.29    3.5      1.4449  0.4993   0.5988
 6. Si:      69.81   75.41    72.6509  0.7745   0.1515
 7. K:        0       6.21     0.4971  0.6522  -0.0100
 8. Ca:       5.43   16.19     8.9570  1.4232   0.0007
 9. Ba:       0       3.15     0.1750  0.4972   0.5751
10. Fe:       0       0.51     0.0570  0.0974  -0.1879


## Wybór danych testowych

Jeden zestaw to zwykły random, drugi to wartości minimalne, i maksymalne z każdego atrybutu.


## Naiwny byes
Przeszkolony za pomocą zestawu ogołoconego z wartości minimalnych i maksymalnych oraz randomowych testowych

Dla randomowych wartości testowych
Number of mispredictions: 1
Accuracy: 0.9090909090909091

Dla minimalnych i maksymalnych wartości testowych

Number of mispredictions: 11
Accuracy: 0.3888888888888889

### WNIOSEK
Naiwny klasyfikatory bayesa przeszkolony na danych z uciętymi wartościami krawędziowymi ma poważne problemy z ich klasyfikacją