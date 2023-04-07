from mediawikiapi import MediaWikiAPI
from tqdm import tqdm
import time
import csv

pages = []

api = MediaWikiAPI()


def scrape(mon):
    count = 0
    print('inizio')
    for link in tqdm(mon.links):
        pages.append([count, api.page(link).title, api.page(link).summary])
        count += 1


header = ["mon_id", "title", "description"]

api.config.language = "it"

scrape(api.page("Monumenti di Firenze"))
# scrape(api.page("Monumenti di Livorno"))
# scrape(api.page("Monumenti di Siena"))
# scrape(api.page("Monumenti di Lucca"))
# scrape(api.page("Monumenti di Arezzo"))
# scrape(api.page("Monumenti di Pisa"))

# Open a new CSV file and write the header row
with open('monument_data_test.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(header)
    # Write each data row
    for row in tqdm(pages):
        writer.writerow(row)
        time.sleep(0.1)

print('Dataset created successfully!')
