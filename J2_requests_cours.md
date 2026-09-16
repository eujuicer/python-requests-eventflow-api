# J2 — Python `requests` pour testeurs

Vous savez déjà appeler et tester une API dans **Bruno**. Ce document montre
comment faire **exactement les mêmes choses en Python**, pour pouvoir ensuite les
automatiser. Rien de neuf côté HTTP : on change juste d'outil.

## Bruno → Python `requests`

| Dans Bruno            | En Python `requests`              |
|-----------------------|-----------------------------------|
| Choisir GET + une URL | `requests.get("...")`             |
| Query Params          | `params={...}`                    |
| Headers               | `headers={...}`                   |
| Body JSON             | `json={...}`                      |
| Le code de réponse    | `response.status_code`            |
| Le corps de réponse   | `response.json()`                 |
| Envoyer la requête    | exécuter la ligne Python          |

## Installer et importer

Une seule fois par projet :

```bash
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install requests
pip freeze > requirements.txt
```

Puis dans le code :

```python
import requests
```

## Le premier appel

```python
response = requests.get("http://localhost:8000/api/events")

print(response.status_code)   # le code HTTP, ex. 200
print(response.json())        # le corps traduit en objets Python
```

- `response.status_code` → un entier (200, 404, 401…). **C'est le vrai code
  HTTP**, pas une donnée du corps.
- `response.json()` → convertit le JSON en **listes et dictionnaires Python**.
  C'est exactement ce que vous manipuliez au Jour 1.
- `response.text` → le corps brut, en texte (utile pour déboguer si ce n'est pas
  du JSON).

```python
data = response.json()
print(type(data))       # <class 'list'>
print(type(data[0]))    # <class 'dict'>
print(data[0]["title"]) # accès comme au Jour 1
```

## Query parameters (les « Query Params » de Bruno)

```python
# À éviter : tout coller à la main dans l'URL
requests.get("http://localhost:8000/api/events?city=Bruxelles")

# Recommandé : laisser requests construire l'URL
requests.get("http://localhost:8000/api/events", params={"city": "Bruxelles"})
```

Sur EventFlow, `GET /api/events` accepte deux filtres :

```python
requests.get(BASE + "/api/events", params={"city": "Gand"})
requests.get(BASE + "/api/events", params={"q": "jazz"})
```

- `city` est **exact et sensible à la casse** : `"Bruxelles"` fonctionne,
  `"bruxelles"` renvoie une liste vide.
- `q` est **insensible à la casse** et cherche dans le titre : `"jazz"` trouve
  « Festival Jazz au Parc ».

## Path parameters (l'ID dans le chemin)

Le path parameter fait partie du chemin, il identifie **une** ressource :

```python
event_id = 1
response = requests.get(f"http://localhost:8000/api/events/{event_id}")
```

Repère : le **path** dit *lequel* (`/events/1`), le **query** dit *lesquels /
comment* (`/events?city=Gand`).

## Headers (les « Headers » de Bruno)

On envoie des headers avec `headers={...}`, comme dans Bruno. Exemple générique :

```python
response = requests.get(BASE + "/api/events", headers={"Accept": "application/json"})
```

On peut aussi **lire** les headers de la réponse :

```python
print(response.headers["content-type"])   # application/json
```

Les endpoints protégés attendent en général que vous prouviez votre identité via
un header dédié. La façon exacte dont EventFlow s'authentifie, à vous de la
repérer dans Swagger (voir le bonus) ; on la formalisera au J5.

## Codes HTTP vs exceptions Python — important

Un `404` ou un `401` **n'est pas** une erreur Python : la requête a réussi, le
serveur a répondu, `requests` vous rend simplement un `status_code` de 404. Votre
code continue normalement.

```python
response = requests.get("http://localhost:8000/api/events/999")
print(response.status_code)   # 404, aucune exception
```

Une **exception Python** survient quand la requête elle-même échoue : serveur
injoignable, DNS, délai dépassé. C'est là que `try/except` (vu au Jour 1) sert :

```python
try:
    response = requests.get("http://localhost:8000/api/events", timeout=5)
except requests.exceptions.RequestException as e:
    print("La requête a échoué :", e)
```

- `timeout=5` : ne pas attendre indéfiniment si le serveur ne répond pas.
- `requests.exceptions.RequestException` couvre les erreurs réseau de `requests`.

À distinguer clairement pour un testeur : « l'API a répondu 404 » (comportement à
tester) ≠ « je n'ai pas réussi à joindre l'API » (problème d'environnement).

## `raise_for_status()` — à connaître, à utiliser avec prudence

```python
response = requests.get(BASE + "/api/events/999")
response.raise_for_status()   # lève une exception si le code est 4xx ou 5xx
```

Pratique dans un script utilitaire. **Mais en test, on veut souvent le
contraire** : vérifier *nous-mêmes* que le code vaut ce qu'on attend (y compris
un 404 attendu). Donc pour tester, on regarde `status_code` et on l'affirme, on
ne laisse pas `raise_for_status` décider à notre place.

## Le corps d'une requête (`json={...}`)

Pour créer/modifier (POST, PUT, PATCH), on envoie un body :

```python
requests.post(BASE + "/api/...", json={"title": "..."})
```

On s'en servira vraiment au prochain bloc (création, CRUD). Aujourd'hui on reste
sur la lecture (GET).

> Toutes les données d'un POST ne partent pas forcément en `json=` : selon ce que
> l'API attend, on utilise parfois `data={...}` (formulaire) plutôt que
> `json={...}`. À regarder au cas par cas dans la doc de l'endpoint.

## `requests.Session` — pour plus tard

`requests.Session()` permet de réutiliser des headers (ex. le token) sur
plusieurs appels sans les répéter. Utile quand on aura beaucoup de requêtes
authentifiées — on l'introduira avec les fixtures PyTest, pas aujourd'hui.

## Ce qu'il faut retenir pour tester

- `requests.get(url, params=..., headers=...)` = votre requête Bruno, en code.
- `response.status_code` = le code HTTP (à **affirmer** dans un test).
- `response.json()` = des listes/dicts Python (à **exploiter** et à **vérifier**).
- 4xx/5xx = réponses à tester, pas des plantages ; les vrais plantages réseau se
  gèrent avec `try/except` + `timeout`.
