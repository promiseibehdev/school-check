import requests

API_URL = "http://universities.hipolabs.com/search"

def search_universities(name="", country=""):
    params = {}

    if name:
        params["name"] = name

    if country:
        params["country"] = country

    try:
        response = requests.get(API_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []
