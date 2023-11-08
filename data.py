import requests
import pandas as pd

url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Créez un DataFrame à partir des données
    df = pd.DataFrame(data["daily"])

    # Définissez un dictionnaire pour mapper les anciens noms de colonnes aux nouveaux noms
    column_mapping = {
        "temperature_2m_max": "Temp Max (°C)",
        "temperature_2m_min": "Temp Min (°C)",
        "precipitation_sum": "Precipitation (mm)",
        "wind_speed_10m_max": "Wind Speed Max (m/s)"
    }

    # Renommez les colonnes en utilisant le dictionnaire de mappage
    df = df.rename(columns=column_mapping)

    # Affichez le DataFrame avec les nouveaux noms de colonnes
    print(df)
else:
    print("Erreur lors de la requête. Statut de réponse :", response.status_code)


