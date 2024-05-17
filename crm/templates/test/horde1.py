import requests
import json

def get_ready(keywords):
    url = "https://trends.google.com/trends/api/explore"
    params = {
        "hl": 'en-US',
        "tz": 360,
        "req": json.dumps({
            "comparisonItem": [{"keyword": str(keywords[0]), "geo": "US", "time": "now 7-d"}]
        })
    }

    response = requests.get(url, params=params)
    data = response.text[5:]  # Removing the first 5 characters from the response
    print("data",data)
    # return json.loads(data)["widgets"]

get_ready(['RR vs PBKS'])