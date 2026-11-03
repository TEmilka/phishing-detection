# Wykrywanie phishingu i złośliwych URL-i (TF-IDF + Naive Bayes)

## Threat Model

**Profil przeciwnika:** Active Attacker. Przeciwnik tworzy e-maile i domeny
phishingowe podszywające się pod banki i modyfikuje je, aby ominąć filtr.

**Interfejs dostępny dla przeciwnika:** Black-box. Przeciwnik może przesyłać
URL-e do klasyfikatora i obserwować decyzję (phishing / legalny), ale nie zna
wag modelu ani danych treningowych.

**Zasada Kerckhoffsa:** Zakładamy pełną znajomość algorytmu (TF-IDF + Naive Bayes),
architektury i kodu. Bezpieczeństwo opiera się na jakości cech, a nie na ukryciu modelu.

**Kryterium sukcesu:** F1-Score > 0.92 oraz FPR < 2% na zbiorze testowym.


## Dane
1. Pobierz dataset: https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls
2. Rozpakuj i umieść `phishing_site_urls.csv` w `data/raw/`.
3. Uruchom `notebooks/01_eksploracja.ipynb` od początku do końca. Wygeneruje to `data/processed/`.