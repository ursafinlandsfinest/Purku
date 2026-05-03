import requests
import json

URL = "https://api.hankintailmoitukset.fi/api/v1/search"

def fetch():
    params = {
        "query": "purku demolition"
    }

    res = requests.get(URL, params=params)
    data = res.json()

    results = []

    for item in data.get("results", []):
        results.append({
            "title": item.get("title"),
            "organization": item.get("organization"),
            "description": item.get("description")
        })

    return results


def save(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    data = fetch()
    save(data)
    print(len(data))
