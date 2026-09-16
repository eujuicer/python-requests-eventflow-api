# EventFlow — Interroger et exploiter une API en Python

Vous savez déjà appeler et tester une API dans Bruno. Aujourd'hui vous faites les
mêmes requêtes **en Python**, et vous apprenez à **exploiter** les données
renvoyées : filtrer, chercher, croiser, calculer, synthétiser.

> Aujourd'hui on **récupère et on exploite** des données. On ne construit pas
> encore de tests automatisés qui décident PASS/FAIL — ce sera PyTest, à partir
> de demain.

## Mise en route

EventFlow doit tourner. API : `http://localhost:8000` · documentation :
`http://localhost:8000/docs`.

Dans votre dossier de tests :

```bash
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install requests
```

En haut de vos fichiers :

```python
import requests
BASE = "http://localhost:8000"
```

Les résultats attendus sont indiqués pour que vous vérifiiez vous-memes.

---

## Niveau 1 — Prise en main *(guidé)*

On avance ensemble, pas à pas.

1. Récupérer la collection des events (`GET /api/events`) et afficher le nombre
   total. -> **4**
2. Afficher le `status_code` de la réponse. -> **200**
3. Afficher tous les titres, un par ligne.
4. Récupérer l'event d'`id` 1 et afficher son titre et sa ville.
5. Pour chaque event, afficher `titre - ville - capacité`.

## Niveau 2 — Paramètres et lecture des réponses *(semi-guidé)*

On vous donne l'objectif, vous écrivez l'appel.

6. Les events de la ville `Gand` (query param `city`) -> afficher les titres.
7. Les events dont le titre contient `jazz` (query param `q`) -> combien ? (**1**)
8. Essayer `city=gand` en minuscules -> combien ? Notez ce que vous observez.
9. Demander l'event `999` -> afficher le `status_code` (**404**) et le corps.
10. Repérer, dans Swagger, quels paramètres `GET /api/events` accepte réellement,
    et vérifier votre réponse aux questions 6/7.

## Niveau 3 — Vos outils de testeur *(fonctions réutilisables)*

Un testeur se construit une petite boîte à outils pour ne pas réécrire les mêmes
appels partout. **Aucune classe.** Ces fonctions **récupèrent ou transforment**
des données — elles ne jugent rien.

11. `get_events()` -> la liste des events.
12. `get_event(event_id)` -> le détail de l'event, ou `None` s'il n'existe pas.
    (Même logique que `find_user_by_id` du Jour 1.)
13. `search_events(q)` -> les events dont le titre contient `q`.
14. `get_events_by_city(city)` -> les events d'une ville.

Puis des fonctions qui **exploitent** une liste déjà récupérée (Python pur,
comme au Jour 1) :

15. `total_capacity(events)` -> la somme des capacités. (**1640** sur tout le
    catalogue.)
16. `event_with_largest_capacity(events)` -> l'event de plus grande capacité.
17. `cities(events)` -> la liste des villes uniques.

## Niveau 4 — Robustesse *(semi-guidé)*

Un testeur distingue toujours **« l'API a répondu quelque chose »** de **« je
n'ai pas réussi à joindre l'API »**.

18. Appeler l'event `999`. Montrer que votre programme **ne plante pas** et
    affiche simplement le `status_code` 404. (Un 404 est une réponse, pas une
    erreur Python.)
19. Ajouter un `timeout` à un appel (ex. `timeout=5`).
20. Entourer un appel d'un `try/except requests.exceptions.RequestException` et
    afficher un message clair si l'API est injoignable. Testez en arrêtant
    EventFlow puis en relançant votre script.

---

## Mission autonome — Note de synthèse sur le catalogue EventFlow

*(autonome — on vous donne le problème, pas la procédure)*

Un responsable produit vous demande une **note de synthèse** sur l'offre actuelle
d'EventFlow. Vous n'avez pas accès à la base : vous devez tout obtenir **via
l'API**, l'explorer avec Swagger si besoin, et produire un résumé **lisible et
factuel** affiché par votre programme.

Votre note doit répondre au moins à ceci :

- Combien d'événements au catalogue, répartis sur combien de villes, lesquelles ?
- La **répartition par ville** (nombre d'events par ville).
- La **capacité** : totale, moyenne, l'événement le plus grand et le plus petit.
- La **fourchette de prix** du catalogue : l'offre la moins chère et la plus
  chère, en euros (il faudra aller regarder le **détail** des events, où se
  trouvent les catégories de prix — `price_cents`).
- Pour chaque événement, son **taux de disponibilité** (`available / capacity`,
  en %).
- **Une analyse croisée de votre choix** (exemple : les événements d'une ville
  donnée dont le titre contient un mot-clé).

Contraintes de testeur :
- réutilisez vos fonctions du Niveau 3 ;
- **explorez Swagger** pour confirmer les endpoints et les champs disponibles —
  ne devinez pas ;
- gérez proprement les cas gênants : un identifiant demandé qui n'existe pas (ne
  pas planter), et l'API injoignable (message clair) ;
- la sortie est une **synthèse d'observations** (des faits sur le catalogue), pas
  une liste de PASS/FAIL. Vous décrivez ce que contient le catalogue, vous ne
  jugez pas encore s'il est « correct ».

Quelques repères pour vérifier votre note : **4 events**, **3 villes**
(Bruxelles, Gand, Liège), capacité totale **1640**, capacité moyenne **410**,
plus grand = *Festival Jazz au Parc*, plus petit = *Atelier QA & Test automatise*,
offre la moins chère **24,95 €**, la plus chère **75 €**.

---

## Bonus (si vous avez fini)

**B1 — Accéder à une ressource protégée.**

L'endpoint `/api/auth/me` est protégé. Votre objectif : réussir à l'appeler
depuis Python. À l'aide de Swagger et de vos connaissances des API :

- identifiez comment EventFlow permet à un utilisateur de s'authentifier ;
- authentifiez-vous avec un compte de démonstration
  (`client@eventflow.test` / `client1234`) ;
- récupérez l'élément nécessaire pour prouver votre identité lors des appels
  suivants ;
- appelez `/api/auth/me` depuis Python et affichez l'utilisateur ;
- observez aussi ce qui se passe quand vous appelez cette ressource **sans** être
  authentifié.

À vous de trouver les endpoints, le format attendu et la manière de transmettre
l'authentification. (Si vous bloquez, demandez un indice au formateur.)

**B2 — Analyse plus fine.**
- Trier les événements du plus grand au plus petit par capacité.
- Pour l'événement 3, afficher le prix le plus élevé parmi ses catégories, en
  euros. (**75.0 €**)
- Quelle ville concentre la plus grande capacité totale ?

**B3 — Recherche croisée.** Écrire une fonction
`events_matching(city, keyword)` qui renvoie les events d'une ville dont le titre
contient un mot-clé (insensible à la casse), en réutilisant vos fonctions du
Niveau 3.
