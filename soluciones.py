import pandas as pd
from typing import Set
import requests

def ej_1_cargar_datos_demograficos() -> pd.DataFrame:
    us_d = pd.read_csv('us-cities-demographics.csv', sep=';')
    return us_d

def ej_2_cargar_calidad_aire(ciudades: Set[str]) -> None:
    missing_cities = []
    air_aqi = []
    for city in ciudades:
        api_url = f'https://api.api-ninjas.com/v1/airquality?city={city}'
        response = requests.get(api_url, headers={'X-Api-Key': 'gBiipiwSiMtD3TpF+QIlYg==OAPqGhEzwXmgGZwS'})
        if response.status_code == requests.codes.ok:
            data = response.json()
            air_aqi.append({'city':city})
            for key, value in data.items():
                if key != 'overall_aqi':
                    air_aqi.append({key:value.get('concentration')})
                if key=='overall_aqi':
                    air_aqi.append({key:value})
        else:
            print("Error:", response.status_code, f'Could not find city: {city}')
            missing_cities.append(city)
    rows = []
    for i in range(0, len(air_aqi), 8):
        row = []
        for j in range(8):
            row.append(list(air_aqi[i+j].values())[0])
        rows.append(row)
    # Define the column names
    columns = ['city', 'CO', 'NO2', 'O3', 'SO2', 'PM2.5', 'PM10', 'overall_aqi']
    # Create the dataframe from the rows and columns
    us_aqi = pd.DataFrame(rows, columns=columns)
    return us_aqi