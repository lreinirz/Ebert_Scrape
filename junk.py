import requests

s = requests.Session()

base_url = "https://en.wikipedia.org/w/api.php"

parameters_ = {
    "action": "opensearch",
    "namespace": "0",
    "search": "The Ballad of Narayama",
    "limit": "5",
    "format": "json"
}

r = s.get(url=base_url, params=parameters_)
data = r.json()


film_year = 1958

print(len(data))
for x in data:
    print(x)
    if f"{film_year}" in x:
        print(x)

#returned format:
#0: The searched for term
#1: Full list of results
#2: Comes up blank
#3: Bunch of URLS 