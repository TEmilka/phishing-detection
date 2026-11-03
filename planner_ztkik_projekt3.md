# Planner: ZTKIK Projekt 3 – Wykrywanie phishingu i złośliwych URL-i (TF-IDF + Naive Bayes)

Zasada: zadania odhaczamy zmieniając `[ ]` na `[x]`. Niczego nie usuwamy.

---

## Faza 0: Przygotowanie środowiska
- [x] 0.1 Sprawdzić Pythona w terminalu VS Code: `python --version`
- [x] 0.2 Sprawdzić Gita w terminalu: `git --version`
- [x] 0.3 Zainstalować w VS Code rozszerzenia: Python oraz Jupyter
- [x] 0.4 Utworzyć folder `phishing-detection` i otworzyć go w VS Code (File > Open Folder)
- [x] 0.5 Utworzyć środowisko wirtualne: `python -m venv venv`
- [x] 0.6 Aktywować środowisko wirtualne (sprawdzić, czy w terminalu widać `(venv)`)
- [x] 0.7 Zainstalować biblioteki: `pip install pandas scikit-learn scipy matplotlib jupyter joblib`
- [x] 0.8 Zapisać listę bibliotek: `pip freeze > requirements.txt`
- [x] 0.9 Zainicjować Git: `git init`
- [x] 0.10 Dodać `venv/` i `data/raw/` do pliku `.gitignore`
- [x] 0.11 Utworzyć foldery: `data/raw`, `data/processed`, `src`, `notebooks`, `results`, `report`
- [x] 0.12 Utworzyć pusty plik `README.md`
- [x] 0.13 Pierwszy commit: `git add .` a potem `git commit -m "Initial project structure"`
- [x] 0.14 Założyć konto na Kaggle (potrzebne do pobrania datasetu)

## Faza 1: Threat Model
- [x] 1.1 Wpisać sekcję Threat Model do `README.md` (profil przeciwnika, interfejs, zasada Kerckhoffsa, kryterium sukcesu)
- [x] 1.2 Commit: "Add threat model"

## Faza 2: Dane
- [x] 2.1 Pobrać dataset Phishing URLs (taruntiwarihp/phishing-site-urls) z Kaggle
- [x] 2.2 Umieścić plik CSV w `data/raw/`
- [x] 2.3 Utworzyć notebook `notebooks/01_eksploracja.ipynb`
- [x] 2.4 Wczytać dane w notebooku (pandas) i sprawdzić nazwy kolumn
- [x] 2.5 Sprawdzić rozkład etykiet (ile phishingu, ile legalnych)
- [x] 2.6 Sprawdzić brakujące wartości
- [x] 2.7 Usunąć duplikaty
- [x] 2.8 Zamienić etykiety na 0/1 (0 = legalny, 1 = phishing)
- [x] 2.9 Podzielić dane na train / validation / test (70/15/15, PO DOMENACH przez GroupShuffleSplit, `random_state=42`; stary losowy podział zastąpiony)
- [x] 2.10 Sprawdzić wyciek danych: czy te same domeny są w train i test (przed poprawką: 42,6% wspólnych domen; po podziale po domenach: 0 wspólnych)
- [x] 2.11 Zapisać przetworzone zbiory do `data/processed/`
- [ ] 2.12 Commit: "Data loading, cleaning and split"

## Faza 3: Ekstrakcja cech
- [ ] 3.1 Utworzyć plik `src/features.py`
- [ ] 3.2 Dodać TF-IDF na n-gramach znakowych (`analyzer='char'`, `ngram_range=(3,5)`), fit tylko na train
- [ ] 3.3 Napisać funkcję cech strukturalnych (długość, kropki, myślniki, cyfry, `@`, HTTPS, IP, głębokość subdomen)
- [ ] 3.4 Dodać słowa kluczowe (login, verify, secure, account, update, bank, paypal)
- [ ] 3.5 Dodać entropię Shannona domeny
- [ ] 3.6 Przetestować funkcję cech na 3 przykładowych URL-ach i sprawdzić wynik ręcznie
- [ ] 3.7 Przeskalować cechy strukturalne do wartości nieujemnych (MinMaxScaler, fit tylko na train)
- [ ] 3.8 Połączyć cechy TF-IDF i strukturalne (`scipy.sparse.hstack`)
- [ ] 3.9 Commit: "Feature extraction"

## Faza 4: Modele i grupa kontrolna
- [ ] 4.1 Utworzyć plik `src/train.py`
- [ ] 4.2 Baseline: `DummyClassifier(strategy='most_frequent')`, zapisać wynik
- [ ] 4.3 Model kontrolny: Naive Bayes tylko na cechach strukturalnych, zapisać wynik
- [ ] 4.4 Model główny: MultinomialNB na pełnych cechach
- [ ] 4.5 Porównanie: LinearSVC lub Logistic Regression
- [ ] 4.6 GridSearchCV dla `alpha` (scoring='f1', cv=5, tylko na train)
- [ ] 4.7 Zapisać najlepszy model przez `joblib.dump` do `results/`
- [ ] 4.8 Commit: "Models and control group"

## Faza 5: Ewaluacja
- [ ] 5.1 Utworzyć plik `src/evaluate.py`
- [ ] 5.2 Policzyć metryki na walidacji: Accuracy, Precision, Recall, F1
- [ ] 5.3 Policzyć FPR = FP / (FP + TN)
- [ ] 5.4 Dobrać próg decyzji tak, żeby FPR < 2% (na walidacji)
- [ ] 5.5 Policzyć metryki na teście (TYLKO RAZ, na końcu)
- [ ] 5.6 Sprawdzić kryterium: F1 > 0.92 i FPR < 2%
- [ ] 5.7 Wygenerować macierz pomyłek (zapis do `results/`)
- [ ] 5.8 Wygenerować krzywą ROC i krzywą Precision-Recall
- [ ] 5.9 Zapisać wszystkie metryki do pliku `results/metrics.json`
- [ ] 5.10 Commit: "Evaluation and results"

## Faza 6: Próba ataku (Analiza bezpieczeństwa)
- [ ] 6.1 Utworzyć plik `src/attack.py`
- [ ] 6.2 Atak 1: podmiana znaków (homoglyphs, np. cyrylica)
- [ ] 6.3 Atak 2: wstawianie myślników w domenie
- [ ] 6.4 Atak 3: dopychanie legalnymi słowami w ścieżce
- [ ] 6.5 Atak 4: subdomeny-zasłony (np. google.com.evil-domain.xyz)
- [ ] 6.6 Atak 5: kodowanie procentowe lub skracanie URL-i
- [ ] 6.7 Dla każdego ataku policzyć odsetek, który przeszedł przez filtr
- [ ] 6.8 Zapisać wyniki ataków do `results/attack_results.json`
- [ ] 6.9 (Opcjonalnie) Adversarial training: dodać przykłady ataków do treningu
- [ ] 6.10 (Opcjonalnie) Porównać skuteczność ataków przed i po
- [ ] 6.11 Commit: "Attack analysis"

## Faza 7: Raport IEEE
- [ ] 7.1 Pobrać szablon IEEE (Word lub LaTeX)
- [ ] 7.2 Napisać Abstract
- [ ] 7.3 Napisać Introduction i motywację (scenariusz: bramka pocztowa w firmie)
- [ ] 7.4 Napisać Related Work (Sahingoz 2019, Pedregosa 2011, i inne z listy)
- [ ] 7.5 Przepisać Threat Model do raportu
- [ ] 7.6 Opisać metodykę: dane, cechy, podział, grupa kontrolna
- [ ] 7.7 Wstawić wyniki: tabele, wykresy, macierze pomyłek
- [ ] 7.8 Opisać analizę bezpieczeństwa i wyniki ataków
- [ ] 7.9 Napisać ograniczenia i wnioski
- [ ] 7.10 Sprawdzić bibliografię w stylu IEEE
- [ ] 7.11 Sprawdzić, czy każda liczba w raporcie ma swój zapisany wynik w `results/`

## Faza 8: Porządki i obrona
- [ ] 8.1 Uporządkować kod (komentarze, nazwy, usunąć martwe fragmenty)
- [ ] 8.2 Uzupełnić `README.md` (jak uruchomić projekt)
- [ ] 8.3 Upewnić się, że `requirements.txt` jest aktualny
- [ ] 8.4 Przygotować listę pytań, które mogą paść na obronie, wraz z odpowiedziami
- [ ] 8.5 Przećwiczyć prezentację na głos
- [ ] 8.6 Przygotować prezentację (slajdy)
- [ ] 8.7 Ostatni commit i sprawdzenie historii w `git log`
