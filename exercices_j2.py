import requests

BASE_URL = "http://localhost:8000/api/"


def section(titre):
    print("\n" + "=" * 70)
    print(titre)
    print("=" * 70)


# ---------------------------------------------------------------------------
# Niveau 1 - Prise en main
# ---------------------------------------------------------------------------

def niveau_1():
    section("NIVEAU 1 - Prise en main")

    # 1 & 2. Recuperer la collection, afficher le total et le status_code
    r = requests.get(BASE_URL + "events", timeout=5)
    events = r.json()
    print("Nombre total d'events :", len(events))
    print("Status code :", r.status_code)

    # 3. Tous les titres, un par ligne
    for e in events:
        print(e["title"])

    # 4. Event id 1 : titre et ville
    event_1 = requests.get(BASE_URL + "events/1", timeout=5).json()
    print(event_1["title"], "-", event_1["city"])

    # 5. Pour chaque event : titre - ville - capacite
    for e in events:
        print(e["title"], "-", e["city"], "-", e["capacity"])


# ---------------------------------------------------------------------------
# Niveau 2 - Parametres et lecture des reponses
# ---------------------------------------------------------------------------

def niveau_2():
    section("NIVEAU 2 - Parametres et lecture des reponses")

    # 6. Events de la ville Gand
    r = requests.get(BASE_URL + "events", params={"city": "Gand"}, timeout=5)
    events_gand = r.json()
    if not events_gand:
        print("Pas d'event trouve")
    else:
        for e in events_gand:
            print(e["title"])

    # 7. Events dont le titre contient "jazz"
    r = requests.get(BASE_URL + "events", params={"q": "jazz"}, timeout=5)
    events_jazz = r.json()
    if not events_jazz:
        print("Pas d'event trouve")
    else:
        print(len(events_jazz))

    # 8. city=gand en minuscules
    r = requests.get(BASE_URL + "events", params={"city": "gand"}, timeout=5)
    events_gand_minuscule = r.json()
    if not events_gand_minuscule:
        print("Pas d'event trouve -> le filtre city est sensible a la casse")
    else:
        print(len(events_gand_minuscule))

    # 9. Event 999 inexistant
    r = requests.get(BASE_URL + "events/999", timeout=5)
    print(r.status_code, r.text)


# ---------------------------------------------------------------------------
# Niveau 3 - Boite a outils (fonctions reutilisables)
# ---------------------------------------------------------------------------

def get_events(base_url=BASE_URL):
    r = requests.get(base_url + "events", timeout=5)
    return r.json()


def get_event(event_id, base_url=BASE_URL):
    r = requests.get(base_url + "events/" + str(event_id), timeout=5)
    if r.status_code == 404:
        return None
    return r.json()


def search_events(q, base_url=BASE_URL):
    r = requests.get(base_url + "events", params={"q": q}, timeout=5)
    return r.json()


def get_events_by_city(city, base_url=BASE_URL):
    r = requests.get(base_url + "events", params={"city": city}, timeout=5)
    return r.json()


def total_capacity(events):
    total = 0
    for e in events:
        total = total + e["capacity"]
    return total


def event_with_largest_capacity(events):
    return max(events, key=lambda e: e["capacity"])


def event_with_smallest_capacity(events):
    return min(events, key=lambda e: e["capacity"])


def cities(events):
    result = []
    for e in events:
        if e["city"] not in result:
            result.append(e["city"])
    return result


def niveau_3():
    section("NIVEAU 3 - Vos outils de testeur")

    events = get_events()
    if not events:
        print("Aucun event")
    else:
        print(len(events))

    event = get_event(1)
    if not event:
        print("Event introuvable")
    else:
        print(event["title"])

    event = get_event(999)
    if not event:
        print("Event introuvable")
    else:
        print(event["title"])

    resultats = search_events("jazz")
    if not resultats:
        print("Aucun resultat")
    else:
        print(resultats)

    resultats = get_events_by_city("Gand")
    if not resultats:
        print("Aucun resultat")
    else:
        print(resultats)

    if not events:
        print("Aucun event, pas de calcul possible")
    else:
        print(total_capacity(events))
        print(event_with_largest_capacity(events))
        print(cities(events))


# ---------------------------------------------------------------------------
# Niveau 4 - Robustesse
# ---------------------------------------------------------------------------

def niveau_4():
    section("NIVEAU 4 - Robustesse")

    # 18. Event 999 : ne pas planter
    r = requests.get(BASE_URL + "events/999", timeout=5)
    print(r.status_code)

    # 19. timeout
    r = requests.get(BASE_URL + "events", timeout=5)
    print(r.status_code)

    # 20. try/except si l'API est injoignable
    try:
        r = requests.get(BASE_URL + "events", timeout=5)
        print(r.status_code)
    except Exception as e:
        print("API injoignable :", e)


# ---------------------------------------------------------------------------
# Mission autonome - Note de synthese sur le catalogue EventFlow
# ---------------------------------------------------------------------------

def note_de_synthese():
    section("MISSION AUTONOME - Note de synthese sur le catalogue EventFlow")

    try:
        events = get_events()
    except Exception as e:
        print("EventFlow est injoignable, impossible de produire la note :", e)
        return

    if not events:
        print("Aucun event au catalogue")
        return

    villes = cities(events)
    print(len(events), "evenements, repartis sur", len(villes), "villes")
    print(villes)

    # Repartition par ville
    print("\nRepartition par ville :")
    repartition = {}
    for e in events:
        ville = e["city"]
        if ville in repartition:
            repartition[ville] = repartition[ville] + 1
        else:
            repartition[ville] = 1
    print(repartition)

    # Capacite totale / moyenne / plus grand / plus petit
    cap_totale = total_capacity(events)
    cap_moyenne = cap_totale / len(events)
    plus_grand = event_with_largest_capacity(events)
    plus_petit = event_with_smallest_capacity(events)
    print("\nCapacite :")
    print("totale :", cap_totale)
    print("moyenne :", cap_moyenne)
    print("plus grand event :", plus_grand["title"], plus_grand["capacity"])
    print("plus petit event :", plus_petit["title"], plus_petit["capacity"])

    # available/categories/price_cents ne sont exposes que par le detail
    # (GET /api/events/{id}), pas par la collection -> un appel par event
    details = []
    for e in events:
        d = get_event(e["id"])
        if d is not None:
            details.append(d)

    # Fourchette de prix (detail des events -> categories -> price_cents)
    print("\nFourchette de prix :")
    toutes_les_categories = []
    for d in details:
        for cat in d["categories"]:
            prix_euros = cat["price_cents"] / 100
            toutes_les_categories.append((prix_euros, d["title"], cat["name"]))

    if not toutes_les_categories:
        print("Aucune categorie trouvee")
    else:
        moins_cher = min(toutes_les_categories, key=lambda c: c[0])
        plus_cher = max(toutes_les_categories, key=lambda c: c[0])
        print("offre la moins chere :", moins_cher)
        print("offre la plus chere :", plus_cher)

    # Taux de disponibilite par event
    print("\nTaux de disponibilite (available / capacity) :")
    for d in details:
        taux = d["available"] / d["capacity"] * 100
        print(d["title"], taux)

    # Analyse croisee au choix : capacite totale par ville
    print("\nAnalyse croisee - capacite totale par ville :")
    capacite_par_ville = {}
    for e in events:
        ville = e["city"]
        if ville in capacite_par_ville:
            capacite_par_ville[ville] = capacite_par_ville[ville] + e["capacity"]
        else:
            capacite_par_ville[ville] = e["capacity"]
    print(capacite_par_ville)
    ville_max = max(capacite_par_ville, key=capacite_par_ville.get)
    print("ville qui concentre le plus de capacite :", ville_max)


# ---------------------------------------------------------------------------
# Bonus
# ---------------------------------------------------------------------------

def bonus_1_auth():
    section("BONUS 1 - Ressource protegee /api/auth/me")

    # Sans authentification
    r = requests.get(BASE_URL + "auth/me", timeout=5)
    print(r.status_code, r.text)

    # Authentification : /api/auth/token attend un formulaire
    login_data = {"username": "client@eventflow.test", "password": "client1234"}
    r_token = requests.post(BASE_URL + "auth/token", data=login_data, timeout=5)
    print(r_token.status_code)

    if r_token.status_code != 200:
        print("Echec de l'authentification :", r_token.text)
        return

    token = r_token.json()["access_token"]
    print(token)

    headers = {"Authorization": "Bearer " + token}
    r_me = requests.get(BASE_URL + "auth/me", headers=headers, timeout=5)
    print(r_me.status_code)
    print(r_me.json())


def bonus_2_analyse_fine():
    section("BONUS 2 - Analyse plus fine")

    events = get_events()
    if not events:
        print("Aucun event")
        return

    # Tri du plus grand au plus petit par capacite
    events_tries = sorted(events, key=lambda e: e["capacity"], reverse=True)
    for e in events_tries:
        print(e["title"], e["capacity"])

    # Prix le plus eleve pour l'event 3
    event_3 = get_event(3)
    if not event_3:
        print("Event 3 introuvable")
    else:
        prix_cat = []
        for cat in event_3["categories"]:
            prix_cat.append(cat["price_cents"])
        print(max(prix_cat) / 100)

    # Ville qui concentre la plus grande capacite totale
    capacite_par_ville = {}
    for e in events:
        ville = e["city"]
        if ville in capacite_par_ville:
            capacite_par_ville[ville] = capacite_par_ville[ville] + e["capacity"]
        else:
            capacite_par_ville[ville] = e["capacity"]
    ville_max = max(capacite_par_ville, key=capacite_par_ville.get)
    print(ville_max, capacite_par_ville[ville_max])


def events_matching(city, keyword):
    evs = get_events_by_city(city)
    result = []
    for e in evs:
        if keyword.lower() in e["title"].lower():
            result.append(e)
    return result


def bonus_3_recherche_croisee():
    section("BONUS 3 - Recherche croisee")

    resultats = events_matching("Bruxelles", "nuit")
    print(resultats)


if __name__ == "__main__":
    niveau_1()
    niveau_2()
    niveau_3()
    niveau_4()
    note_de_synthese()
    bonus_1_auth()
    bonus_2_analyse_fine()
    bonus_3_recherche_croisee()
