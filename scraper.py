import requests
import json
import re

URL = "https://api.hankintailmoitukset.fi/api/v1/search"

KEYWORDS = [
    "purku",
    "rakennuksen purku",
    "demolition",
    "saneeraus",
    "purkutyö",
    "rakennusurakka"
]

def fetch():
    results = []

    for kw in KEYWORDS:
        try:
            res = requests.get(URL, params={"query": kw}, timeout=20)
            data = res.json()

            for item in data.get("results", []):
                text = (item.get("title") or "") + " " + (item.get("description") or "")

                # suodatus: oikeasti purkuun liittyvät
                if not re.search(r"purku|demolition|saneeraus|rakennus", text, re.I):
                    continue

                results.append({
                    "title": item.get("title"),
                    "organization": item.get("organization"),
                    "description": item.get("description")
                })

        except Exception as e:
            print("error:", e)

    return results


def save(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    data = fetch()

    # fallback ettei jää tyhjäksi
    if not data:
        data = [{
            "title": "Ei vielä uusia purkukohteita",
            "organization": "HILMA-haku käynnissä",
            "description": "Ei osumia tällä hetkellä"
        }]

    save(data)
    print("items:", len(data))
