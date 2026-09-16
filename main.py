import requests
from rich.rule import Rule
from rich.console import Console

console = Console()

BASE_URL = "http://localhost:8000/api/"

console.print(Rule("Recherche d'event"))

ville = input("Ville de l'event : ").strip().capitalize()
mot_cle = input("Mot clé : ")

params = {"city": ville, "q": mot_cle}

response = requests.get(BASE_URL + "events", params=params)

events_recherche = response.json()

if events_recherche:
    for e in events_recherche:
        print(f'{e["id"]} - {e["title"]}')
else:

    print("Pas d'event trouvé")

event_id = 1

response_path = requests.get(BASE_URL + f'events/{events_id}`)

event_1 = response_path.json()


     