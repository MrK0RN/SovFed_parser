import json

import scraper

scrap = scraper.Scraper()
scrap.parse_links_from_files()
f = open("output.txt", "w")
f.write("")
f.close()
scrap.parse_all_files()
print(scrap.all_senators)
with open("output.json", 'w', encoding='utf-8') as f:
    json.dump(scrap.all_senators, f, indent=2, ensure_ascii=False)