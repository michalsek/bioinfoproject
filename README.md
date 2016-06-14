### Projekt Bioinformatyka - Klasyfikator pseudowęzłów

Napisz program, który dla zadanej na wejściu struktury drugorzędowej (zapis w formacie dot-brackets) zidentyfikuje pseudowęzły oraz określi ich klasyfikację wg podziału stosowanego przez Pseudoviewer2: H, HH, HHH, HLin, HLout, LL.

##### Wymagania

* Python 2.7 https://www.python.org/download/releases/2.7/
* numpy http://www.numpy.org/

##### Run

Program jako parametr przyjmuje ścieżkę do pliku zawierającego w osobnych liniach struktury w notacji dot-bracket (niesparowane nukleotydy zapisywane za pomocą '.'). Na standardowe wyjście wypisywany są wszystkie podstruktury znalezione w strukturze oraz ich klasyfikacja (H, HH, HHH, HL_in, HL_out, LL, niesklasyfikowany). W przypadku niepodania parametru program używa jako wejścia pliku test.in

```
python run.py [input.file]
```

##### Test

Skrypt testowy jako parametr przyjmuje ścieżkę do pliku pickle, zawierającego trzy tablice: dane wejściowe (struktury dot bracket), oraz dwie tablice zawierające poprawną klasyfikację pseudowęzłów. W przypadku niepodania parametru używany jest plik test.pickle zawierający 304 struktury pochodzące z bazy PseudoBase++, sklasyfikowane na podstawie informacji zawartych w artykule **PSEUDOVIEWER2: Visualization of RNA pseudoknots of any type**.

```
  python test.py [inputFile.pickle]
```

##### Rozwiązanie

Zaimplementowane rozwiązanie polega na redukcji struktury do prostszego zapisu, który następnie jest klasyfikowany za pomocą mapy.
Kroki algorytmu:
1. usunęcie znaków, od których typ pseudowęzła nie zależy (niesparowane nukleotydy, przerwy)
2. zredukowanie kolejno występujących tych samych symboli do pojedynczego wystąpenia np. ((((((( -> (
3. Znalezenie oraz zastąpenie pojedynczym symbolem zamkniętych podstruktur np. ([)()()()] -> ([)SSS] -> ([)S]
4. redukcja podstruktur znajdujących się poza pseudowęzłem np. ([)]S -> ([)]
5. Klasyfikacja za pomocą mapy szablonów
