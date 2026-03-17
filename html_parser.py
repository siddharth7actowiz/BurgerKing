from lxml import html ,etree
from validation import Store
from pydantic import ValidationError
import re
from utils import read_json 
from config import JSON_PATH

def parse_html(data):
    parsed_data = []
    tree = html.fromstring(data)
    xpaths = read_json(JSON_PATH)
 
    stores = tree.xpath(xpaths.get("stores"))
 
    for store in stores:
        item = {}
        website_url = store.xpath(xpaths.get("website_url")).strip()
        storeid = re.search(r'-(\d+)', website_url)
        
        name_anchor = store.xpath(xpaths.get("name_anchor"))[0]
        item["name"] = name_anchor.text_content().strip()
        item["store_id"] = int(storeid.group(1)) 
        item["city"] = name_anchor.get("data-track-event-city", "").strip()
        item["state"] = name_anchor.get("data-track-event-state", "").strip()

        address = store.xpath(xpaths.get("address"))
        item["address"] = " ".join(a.strip() for a in address if a.strip())

        item["phone"] = store.xpath(xpaths.get("phone"))[0].strip()
        item["timings"] = store.xpath(xpaths.get("timings"))[0].strip()
              
        item["website"] = website_url

        map_url = store.xpath(xpaths.get("map_url"))
        item["map_url"] = map_url[0] if map_url else None

        parsed_data.append(item)
 
    clean_data = []

    for i in parsed_data:
        try:
            validated = Store(**i)
            clean_data.append(validated.model_dump())
        except ValidationError as e:
            print("Validation Error:", e)

    return clean_data