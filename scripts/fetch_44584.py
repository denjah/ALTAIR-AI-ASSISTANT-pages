import requests
import json
import codecs

WEBHOOK = "https://altaircom.bitrix24.ru/rest/276/u22laahp4pf7zs7b/"
COMPANY_ID = 44584

def call(method, params=None):
    try:
        r = requests.post(WEBHOOK + method, json=params or {})
        return r.json().get('result', {})
    except Exception as e:
        return {"error": str(e)}

def main():
    res = {}

    # 1. Company
    res["company"] = call("crm.company.get", {"id": COMPANY_ID})

    # 2. Deals
    res["deals"] = call("crm.deal.list", {
        "filter": {"COMPANY_ID": COMPANY_ID},
        "select": ["ID","TITLE","STAGE_ID","PROBABILITY","OPPORTUNITY","CURRENCY_ID",
                    "COMMENTS","DATE_CREATE","CLOSEDATE","CATEGORY_ID","SOURCE_ID",
                    "SOURCE_DESCRIPTION","BEGINDATE","UF_*"]
    })

    # 3. Contacts
    res["contacts"] = call("crm.contact.list", {
        "filter": {"COMPANY_ID": COMPANY_ID},
        "select": ["ID","NAME","LAST_NAME","SECOND_NAME","POST","COMMENTS","PHONE","EMAIL","WEB"]
    })

    # 4. Company activities
    res["company_activities"] = call("crm.activity.list", {
        "filter": {"OWNER_ID": COMPANY_ID, "OWNER_TYPE_ID": 4},
        "select": ["ID","SUBJECT","DESCRIPTION","CREATED","TYPE_ID","DIRECTION",
                    "PROVIDER_TYPE_ID","RESPONSIBLE_ID","COMPLETED","END_TIME"]
    })

    # 5. Deal activities
    res["deals_activities"] = {}
    if isinstance(res.get("deals"), list):
        for deal in res["deals"]:
            did = deal.get("ID")
            res["deals_activities"][did] = call("crm.activity.list", {
                "filter": {"OWNER_ID": did, "OWNER_TYPE_ID": 2},
                "select": ["ID","SUBJECT","DESCRIPTION","CREATED","TYPE_ID","DIRECTION",
                            "PROVIDER_TYPE_ID","RESPONSIBLE_ID","COMPLETED","END_TIME"]
            })

    # 6. Timeline comments
    res["timeline_comments"] = call("crm.timeline.comment.list", {
        "filter": {"ENTITY_ID": COMPANY_ID, "ENTITY_TYPE": "company"}
    })

    # 7. Deal timeline comments
    res["deals_timeline"] = {}
    if isinstance(res.get("deals"), list):
        for deal in res["deals"]:
            did = deal.get("ID")
            res["deals_timeline"][did] = call("crm.timeline.comment.list", {
                "filter": {"ENTITY_ID": did, "ENTITY_TYPE": "deal"}
            })

    with codecs.open('b24_data_44584.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("Data saved to b24_data_44584.json")

if __name__ == "__main__":
    main()
