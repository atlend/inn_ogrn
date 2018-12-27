import json
import requests


def send_query(query):
    r = requests.post("https://rmsp.nalog.ru/search-proc.json", data={'query': query})
    d = json.loads(r.text)
    if d['data']:
        return True
    else:
        return False
