import requests
import json
import codecs

WEBHOOK = "https://altaircom.bitrix24.ru/rest/276/u22laahp4pf7zs7b/"
COMPANY_ID = 47650

def main():
    res = {}
    
    # 1. Company
    try:
        r = requests.get(WEBHOOK + f"crm.company.get?id={COMPANY_ID}")
        res["company"] = r.json().get('result', {})
    except Exception as e:
        res["company_err"] = str(e)
        
    # 2. Deals for this company
    try:
        r = requests.post(WEBHOOK + "crm.deal.list", json={
            "filter": {"COMPANY_ID": COMPANY_ID},
            "select": ["ID", "TITLE", "STAGE_ID", "PROBABILITY", "OPPORTUNITY", "CURRENCY_ID", "COMMENTS", "DATE_CREATE", "CLOSEDATE", "CATEGORY_ID", "SOURCE_ID", "SOURCE_DESCRIPTION"]
        })
        res["deals"] = r.json().get('result', [])
    except Exception as e:
        res["deals_err"] = str(e)

    # 3. Contacts for this company
    try:
        r = requests.post(WEBHOOK + "crm.contact.list", json={
            "filter": {"COMPANY_ID": COMPANY_ID},
            "select": ["ID", "NAME", "LAST_NAME", "SECOND_NAME", "POST", "COMMENTS", "PHONE", "EMAIL"]
        })
        res["contacts"] = r.json().get('result', [])
    except Exception as e:
        res["contacts_err"] = str(e)
        
    # 4. Activities (communications) for this company
    try:
        r = requests.post(WEBHOOK + "crm.activity.list", json={
            "filter": {"OWNER_ID": COMPANY_ID, "OWNER_TYPE_ID": 4},
            "select": ["ID", "SUBJECT", "DESCRIPTION", "CREATED", "TYPE_ID", "DIRECTION", "PROVIDER_TYPE_ID", "RESPONSIBLE_ID"]
        })
        res["company_activities"] = r.json().get('result', [])
    except Exception as e:
        res["activities_err"] = str(e)

    # 5. Activities on each Deal
    res["deals_activities"] = {}
    if "deals" in res and isinstance(res["deals"], list):
        for deal in res["deals"]:
            deal_id = deal.get("ID")
            try:
                r = requests.post(WEBHOOK + "crm.activity.list", json={
                    "filter": {"OWNER_ID": deal_id, "OWNER_TYPE_ID": 2},
                    "select": ["ID", "SUBJECT", "DESCRIPTION", "CREATED", "TYPE_ID", "DIRECTION", "PROVIDER_TYPE_ID", "RESPONSIBLE_ID"]
                })
                res["deals_activities"][deal_id] = r.json().get('result', [])
            except Exception as e:
                pass

    # 6. Timeline for company
    try:
        r = requests.post(WEBHOOK + "crm.timeline.comment.list", json={
            "filter": {"ENTITY_ID": COMPANY_ID, "ENTITY_TYPE": "company"}
        })
        res["timeline_comments"] = r.json().get('result', [])
    except Exception as e:
        res["timeline_err"] = str(e)

    with codecs.open('b24_data_47650.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Data saved to b24_data_47650.json")
        
if __name__ == "__main__":
    main()
