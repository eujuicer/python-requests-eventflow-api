# Request — Exercices Python `requests`

Dépôt d'entraînement : interroger et exploiter l'API **EventFlow** en Python
avec la librairie [`requests`](https://requests.readthedocs.io/).

## Prérequis

- Python 3.10+
- L'API EventFlow doit tourner en local sur `http://localhost:8000`
  (documentation Swagger : `http://localhost:8000/docs`)

## Installation

```bash
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. L'activer
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux

# 3. Installer les dépendances
pip install -r requirement.txt
```

Le terminal affiche `(venv)` en début de ligne quand l'environnement est actif.
Pour en sortir : `deactivate`.

## Utilisation

```bash
python main.py
```

Pour lancer le corrigé des exercices J2 :

```bash
python exercices_j2.py
```

## Contenu du dépôt

| Fichier                    | Description                                              |
|-----------------------------|-----------------------------------------------------------|
| `main.py`                   | Script d'exploration de l'API (requêtes GET, query params, path params) |
| `exercices_j2.py`           | Corrigé des exercices J2 (niveaux 1 à 4, mission autonome, bonus) |
| `J2_requests_cours.md`      | Cours : `requests` pour testeurs (Bruno → Python)          |
| `J2_exercices_eleves.md`    | Énoncés des exercices J2                                   |
| `requirement.txt`           | Dépendances Python du projet                                |

## Notes

- Le dossier `venv/` (ou équivalent) ne doit jamais être versionné — il est
  déjà exclu via `.gitignore`.
- Après ajout d'une dépendance : `pip freeze > requirement.txt`.
