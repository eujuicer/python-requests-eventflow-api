import requests
from rich import print as better_print

BASE_URL = "http://localhost:8000/api/"

# response = requests.get(BASE_URL + "events")

# Permet de convertir JSON renvoyé en lsit en dictionnaires python
# events = response.json()

# better_print(events) # => Print le tableau d'events

# better_print(events[0]) # => Print le premier element

# better_print('***************************************')

# Boucler dans le tableau d'events
# for e in events:
#     print(e.get("id")) # Methode d'acces dictionnaires python

# status = response.status_code

# print(f'STATUS : {status}')

# On recupere le text brut, en string
# print(response.text)
# print(response.text[0])

# print(type(events)) # list python
# print(type(events[0])) # dictionnaire python


# A eviter, query params direct dans l'URL brut
# response2 = requests.get(BASE_URL + 'events?city=Bruxelles')

# req2_params = {"city": "Bruxelles"}

# response2 = requests.get(BASE_URL + 'events', params=req2_params)

# events_filtre_bxl = response2.json()

# better_print(events_filtre_bxl)

# google_params = {"q": "facebook"}

# response_google = requests.get('https://www.google.com/search', params=google_params)

# print(response_google.json())   => Erreur : La reponse envoyée ici n'est pas un format json mais du HTML

# print(response_google.text[:200])

# Demande utilsiateur ville de l'event, mot clef et renvoyer seuelment titre et l'id de l'event si il existe, sinon 'Pas d'event trouvé'

# Exo 1

# city = input("Donne une ville (ou pas) : ")
# mot_clef = input("Donne un mot clef (ou pas) : ")

# exo_params = {"city": city, "q": mot_clef}

# res_exo1 = requests.get(BASE_URL + 'events', params=exo_params)

# event_exo1 = res_exo1.json()

# if not event_exo1:
#     print("Pas d'events")
# else:
#     for e in event_exo1:
#         print(f'ID : {e.get('id')} --- Titre : {e.get('title')}')

event_id = 1

response_path = requests.get(BASE_URL + f'events/{event_id}')

event_1 = response_path.json()

# print(event_1, response_path.status_code)

# print('Headers = ', response_path.headers)

req_google = requests.get('https://www.google.com/search?q=test')

# print('Header google = ', req_google.headers)

# try:
#     res = requests.get('kajvchgahejhka')
# except requests.exceptions.RequestException:
#     print('Erreur reseau')
# except TypeError:
#     print('Type error')
# except:
#     print('Erreur inconnue')
