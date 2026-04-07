import urllib.request
import json

base_url = "https://altaircom.bitrix24.ru/rest/276/nxv29r67o1qp5hd3/"

endpoints = [
    f"crm.deal.get.json?id=43504",
    f"crm.lead.get.json?id=43504",
    f"crm.company.get.json?id=43504",
    f"crm.contact.get.json?id=43504"
]

results = {}
for ep in endpoints:
    url = base_url + ep
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            results[ep.split('.')[1]] = data
    except Exception as e:
        results[ep.split('.')[1]] = str(e)

print(json.dumps(results, indent=2, ensure_ascii=False))
