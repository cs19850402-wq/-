import requests

def get_trending():
    url = "https://api.github.com/search/repositories"

    params = {
        "q": "AI",
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    response = requests.get(url, params=params)

    return response.json()
