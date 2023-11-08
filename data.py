
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Initialisation de la session de cache
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)

# Configuration des paramètres de retry
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

# Initialisation du client Open-Meteo
openmeteo = openmeteo_requests.Client(session=retry_session)

# Paramètres de l'API Open-Meteo
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"]
}

# Appel de l'API Open-Meteo
responses = openmeteo.weather_api(url, params=params)

# Vérification des réponses
if not responses:
    print("Aucune réponse de l'API Open-Meteo.")
    exit()

# Traitement de la première réponse (uniquement pour une seule localisation, ajoutez une boucle pour plusieurs localisations)
response = responses[0]

# Affichage des informations de localisation
print(f"Coordonnées {response.Latitude()}°E {response.Longitude()}°N")
print(f"Altitude {response.Elevation()} m au-dessus du niveau de la mer")
print(f"Fuseau horaire {response.Timezone()} ({response.TimezoneAbbreviation()})")
print(f"Décalage par rapport à GMT+0 {response.UtcOffsetSeconds()} s")

# Traitement des données quotidiennes
daily = response.Daily()

# Extraction des variables quotidiennes
daily_data = {
    "date": pd.date_range(
        start=pd.to_datetime(daily.Time(), unit="s"),
        end=pd.to_datetime(daily.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=daily.Interval()),
        closed="left"
    ),
    "temperature_max": daily.Variables(0).ValuesAsNumpy(),
    "temperature_min": daily.Variables(1).ValuesAsNumpy(),
    "precipitation": daily.Variables(2).ValuesAsNumpy(),
    "wind_speed": daily.Variables(3).ValuesAsNumpy()
}

# Création d'un DataFrame pandas à partir des données quotidiennes
daily_dataframe = pd.DataFrame(data=daily_data)
daily_dataframe = round(daily_dataframe, 2)

# Affichage du DataFrame
print(daily_dataframe)
