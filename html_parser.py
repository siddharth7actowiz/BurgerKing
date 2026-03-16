from lxml import html
from validation import Store
from pydantic import ValidationError
def parse_html(data):
    parsed_data = []
    tree = html.fromstring(data)
 
    stores = tree.xpath('//div[@class="store-info-box"]')
 
    for store in stores:
        item = {}
 
        name_anchor = store.xpath('.//li[contains(@class,"outlet-name")]//a')[0]
        item["name"] = name_anchor.text_content().strip()
        item["city"] = name_anchor.get("data-track-event-city", "").strip()
        item["state"] = name_anchor.get("data-track-event-state", "").strip()
        address = store.xpath('.//li[contains(@class,"outlet-address")]//span/text()')
        item["address"] = " ".join(a.strip() for a in address if a.strip())
        item["phone"] = store.xpath('.//li[contains(@class,"outlet-phone")]//a/text()')[0].strip()
        item["timings"] = store.xpath('.//li[contains(@class,"outlet-timings")]//span/text()')[0].strip()
        website = store.xpath('.//a[contains(@class,"btn-website")]/@href')
        item["website"] = website[0] if website else None
        map_url = store.xpath('.//a[contains(@class,"btn-direction")]/@href')
        item["map_url"] = map_url[0] if map_url else None
        parsed_data.append(item)
 
    try:
        for i in parsed_data:
            Store(**i)
        return parsed_data
    except ValidationError as v:
        print("Error",parse_html.__name__,v)