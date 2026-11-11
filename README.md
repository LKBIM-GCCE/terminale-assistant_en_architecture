# Terminale Bac Pro TEB-AA – site de la classe

Un seul site pour toute la classe : consignes, séances, check-lists et liens vers les ressources.
Les fichiers lourds (plans, CCTP, maquettes) restent sur le Drive.

| Dossier | Contenu |
|---|---|
| `index.html` | Accueil de la classe : projets, agenda, règles |
| `mdqb/` | Projet Maison de quartier Bagatelle (U22) : accueil + séances S1 à S5 |
| `villa/` | Projet Villa DUPONT (U21, U22, U23) – en attente |
| `assets/` | Style et script communs à toutes les pages |
| `ressources/` | Petits fichiers à télécharger (trames, fiches) |

## Modifier le site
1. Modifier les données en tête de `build.py` (MDQB) ou `villa/build.py` (Villa).
2. Coller les liens Drive dans le dictionnaire `DRIVE` de `build.py`.
3. Lancer `python3 build.py`, puis publier (commit + push sur `main`).

## Publication
Settings → Pages → branche `main`, dossier `/ (root)`.

## Saisies des élèves
Les réponses saisies dans les pages (fiches, tableaux, check-lists) sont enregistrées dans le navigateur du poste.
Les élèves doivent imprimer en PDF ou exporter en .csv avant de quitter le poste.
