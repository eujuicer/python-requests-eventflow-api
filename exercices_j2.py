"""
EventFlow — Interroger et exploiter une API en Python
Corrigé des exercices J2 (niveaux 1 à 4, mission autonome, bonus)
"""

import requests

BASE = "http://localhost:8000"


def section(titre):
    print("\n" + "=" * 70)
    print(titre)
    print("=" * 70)


# ---------------------------------------------------------------------------
# Niveau 1 — Prise en main
# ---------------------------------------------------------------------------

def niveau_1():
    section("NIVEAU 1 — Prise en main")

    # 1 & 2. Récupérer la collection, afficher le total et le status_code
    response = requests.get(f"{BASE}/api/events", timeout=5)
    events = response.json()
    print("Nombre total d'events :", len(events))
    print("Status code :", response.status_code)

    # 3. Tous les titres, un par ligne
    print("\nTitres :")
    for e in events:
        print("-", e["title"])

    # 4. Event id 1 : titre et ville
    event_1 = requests.get(f"{BASE}/api/events/1", timeout=5).json()
    print("\nEvent 1 :", event_1["title"], "-", event_1["city"])

    # 5. Pour chaque event : titre - ville - capacité
    print("\nTitre - ville - capacité :")
    for e in events:
        print(f"{e['title']} - {e['city']} - {e['capacity']}")


# ---------------------------------------------------------------------------
# Niveau 2 — Paramètres et lecture des réponses
# ---------------------------------------------------------------------------

def niveau_2():
    section("NIVEAU 2 — Paramètres et lecture des réponses")

    # 6. Events de la ville Gand
    resp = requests.get(f"{BASE}/api/events", params={"city": "Gand"}, timeout=5)
    events_gand = resp.json()
    print("Events à Gand :", [e["title"] for e in events_gand])

    # 7. Events dont le titre contient "jazz"
    resp = requests.get(f"{BASE}/api/events", params={"q": "jazz"}, timeout=5)
    events_jazz = resp.json()
    print("Events 'jazz' :", len(events_jazz))

    # 8. city=gand en minuscules
    resp = requests.get(f"{BASE}/api/events", params={"city": "gand"}, timeout=5)
    events_gand_minuscule = resp.json()
    print("Events 'gand' (minuscule) :", len(events_gand_minuscule),
          "-> le filtre 'city' semble insensible à la casse" if len(events_gand_minuscule) == len(events_gand)
          else "-> le filtre 'city' est sensible à la casse")

    # 9. Event 999 inexistant
    resp = requests.get(f"{BASE}/api/events/999", timeout=5)
    print("Event 999 -> status_code :", resp.status_code, "- corps :", resp.text)


# ---------------------------------------------------------------------------
# Niveau 3 — Boîte à outils (fonctions réutilisables)
# ---------------------------------------------------------------------------

def get_events():
    """Renvoie la liste des events."""
    response = requests.get(f"{BASE}/api/events", timeout=5)
    return response.json()


def get_event(event_id):
    """Renvoie le détail d'un event, ou None s'il n'existe pas."""
    response = requests.get(f"{BASE}/api/events/{event_id}", timeout=5)
    if response.status_code == 404:
        return None
    return response.json()


def search_events(q):
    """Renvoie les events dont le titre contient q."""
    response = requests.get(f"{BASE}/api/events", params={"q": q}, timeout=5)
    return response.json()


def get_events_by_city(city):
    """Renvoie les events d'une ville."""
    response = requests.get(f"{BASE}/api/events", params={"city": city}, timeout=5)
    return response.json()


def total_capacity(events):
    """Somme des capacités d'une liste d'events."""
    return sum(e["capacity"] for e in events)


def event_with_largest_capacity(events):
    """L'event de plus grande capacité."""
    return max(events, key=lambda e: e["capacity"])


def event_with_smallest_capacity(events):
    """L'event de plus petite capacité."""
    return min(events, key=lambda e: e["capacity"])


def cities(events):
    """Liste des villes uniques."""
    return list({e["city"] for e in events})


def niveau_3():
    section("NIVEAU 3 — Vos outils de testeur")

    events = get_events()
    print("get_events() ->", len(events), "events")

    print("get_event(1) ->", get_event(1)["title"])
    print("get_event(999) ->", get_event(999))

    print("search_events('jazz') ->", [e["title"] for e in search_events("jazz")])
    print("get_events_by_city('Gand') ->", [e["title"] for e in get_events_by_city("Gand")])

    print("total_capacity(events) ->", total_capacity(events))
    print("event_with_largest_capacity(events) ->", event_with_largest_capacity(events)["title"])
    print("cities(events) ->", cities(events))


# ---------------------------------------------------------------------------
# Niveau 4 — Robustesse
# ---------------------------------------------------------------------------

def niveau_4():
    section("NIVEAU 4 — Robustesse")

    # 18. Event 999 : ne pas planter
    resp = requests.get(f"{BASE}/api/events/999", timeout=5)
    print("Event 999 -> status_code :", resp.status_code, "(pas de crash)")

    # 19. timeout
    resp = requests.get(f"{BASE}/api/events", timeout=5)
    print("Appel avec timeout=5 -> status_code :", resp.status_code)

    # 20. try/except si l'API est injoignable
    try:
        resp = requests.get(f"{BASE}/api/events", timeout=5)
        print("API joignable, status_code :", resp.status_code)
    except requests.exceptions.RequestException as exc:
        print("Impossible de joindre l'API EventFlow :", exc)


# ---------------------------------------------------------------------------
# Mission autonome — Note de synthèse sur le catalogue EventFlow
# ---------------------------------------------------------------------------

def note_de_synthese():
    section("MISSION AUTONOME — Note de synthèse sur le catalogue EventFlow")

    try:
        events = get_events()
    except requests.exceptions.RequestException as exc:
        print("EventFlow est injoignable, impossible de produire la note :", exc)
        return

    villes = cities(events)
    print(f"Catalogue : {len(events)} événements, répartis sur {len(villes)} villes : "
          f"{', '.join(sorted(villes))}")

    # Répartition par ville
    print("\nRépartition par ville :")
    repartition = {}
    for e in events:
        repartition[e["city"]] = repartition.get(e["city"], 0) + 1
    for ville, nb in sorted(repartition.items()):
        print(f"  - {ville} : {nb} event(s)")

    # Capacité totale / moyenne / plus grand / plus petit
    cap_totale = total_capacity(events)
    cap_moyenne = cap_totale / len(events)
    plus_grand = event_with_largest_capacity(events)
    plus_petit = event_with_smallest_capacity(events)
    print("\nCapacité :")
    print(f"  - totale : {cap_totale}")
    print(f"  - moyenne : {cap_moyenne:.0f}")
    print(f"  - plus grand event : {plus_grand['title']} ({plus_grand['capacity']})")
    print(f"  - plus petit event : {plus_petit['title']} ({plus_petit['capacity']})")

    # available/categories/price_cents ne sont exposés que par le détail
    # (GET /api/events/{id}), pas par la collection -> un seul aller-retour
    # par event, dont on réutilise le résultat pour le prix et la disponibilité.
    details = [get_event(e["id"]) for e in events]
    details = [d for d in details if d is not None]

    # Fourchette de prix (détail des events -> categories -> price_cents)
    print("\nFourchette de prix :")
    toutes_les_categories = []  # (prix_euros, event_title, categorie_nom)
    for d in details:
        for cat in d.get("categories", []):
            prix_euros = cat["price_cents"] / 100
            toutes_les_categories.append((prix_euros, d["title"], cat["name"]))

    moins_cher = min(toutes_les_categories, key=lambda c: c[0])
    plus_cher = max(toutes_les_categories, key=lambda c: c[0])
    print(f"  - offre la moins chère : {moins_cher[0]:.2f} € "
          f"({moins_cher[1]} - {moins_cher[2]})")
    print(f"  - offre la plus chère : {plus_cher[0]:.2f} € "
          f"({plus_cher[1]} - {plus_cher[2]})")

    # Taux de disponibilité par event
    print("\nTaux de disponibilité (available / capacity) :")
    for d in details:
        taux = d["available"] / d["capacity"] * 100
        print(f"  - {d['title']} : {taux:.1f} %")

    # Analyse croisée au choix : capacité totale par ville
    print("\nAnalyse croisée — capacité totale par ville :")
    capacite_par_ville = {}
    for e in events:
        capacite_par_ville[e["city"]] = capacite_par_ville.get(e["city"], 0) + e["capacity"]
    for ville, cap in sorted(capacite_par_ville.items(), key=lambda x: -x[1]):
        print(f"  - {ville} : {cap}")
    ville_max = max(capacite_par_ville, key=capacite_par_ville.get)
    print(f"  -> la ville qui concentre le plus de capacité est {ville_max}")


# ---------------------------------------------------------------------------
# Bonus
# ---------------------------------------------------------------------------

def bonus_1_auth():
    section("BONUS 1 — Ressource protégée /api/auth/me")

    # Sans authentification
    resp = requests.get(f"{BASE}/api/auth/me", timeout=5)
    print("Sans authentification -> status_code :", resp.status_code, "-", resp.text)

    # Authentification : /api/auth/token attend un formulaire (OAuth2PasswordRequestForm)
    login_data = {"username": "client@eventflow.test", "password": "client1234"}
    resp_token = requests.post(f"{BASE}/api/auth/token", data=login_data, timeout=5)
    print("\nLogin -> status_code :", resp_token.status_code)

    if resp_token.status_code != 200:
        print("Échec de l'authentification :", resp_token.text)
        return

    token = resp_token.json()["access_token"]
    print("Token récupéré :", token[:20] + "...")

    headers = {"Authorization": f"Bearer {token}"}
    resp_me = requests.get(f"{BASE}/api/auth/me", headers=headers, timeout=5)
    print("\nAvec authentification -> status_code :", resp_me.status_code)
    print("Utilisateur :", resp_me.json())


def bonus_2_analyse_fine():
    section("BONUS 2 — Analyse plus fine")

    events = get_events()

    # Tri du plus grand au plus petit par capacité
    events_tries = sorted(events, key=lambda e: e["capacity"], reverse=True)
    print("Events triés par capacité décroissante :")
    for e in events_tries:
        print(f"  - {e['title']} ({e['capacity']})")

    # Prix le plus élevé pour l'event 3
    event_3 = get_event(3)
    prix_max = max(cat["price_cents"] for cat in event_3["categories"]) / 100
    print(f"\nEvent 3 - prix le plus élevé : {prix_max:.1f} €")

    # Ville qui concentre la plus grande capacité totale
    capacite_par_ville = {}
    for e in events:
        capacite_par_ville[e["city"]] = capacite_par_ville.get(e["city"], 0) + e["capacity"]
    ville_max = max(capacite_par_ville, key=capacite_par_ville.get)
    print(f"Ville avec la plus grande capacité totale : {ville_max} "
          f"({capacite_par_ville[ville_max]})")


def events_matching(city, keyword):
    """Events d'une ville dont le titre contient keyword (insensible à la casse)."""
    events_ville = get_events_by_city(city)
    keyword_lower = keyword.lower()
    return [e for e in events_ville if keyword_lower in e["title"].lower()]


def bonus_3_recherche_croisee():
    section("BONUS 3 — Recherche croisée")

    resultats = events_matching("Bruxelles", "nuit")
    print("events_matching('Bruxelles', 'nuit') ->", [e["title"] for e in resultats])


if __name__ == "__main__":
    niveau_1()
    niveau_2()
    niveau_3()
    niveau_4()
    note_de_synthese()
    bonus_1_auth()
    bonus_2_analyse_fine()
    bonus_3_recherche_croisee()
