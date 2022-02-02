import csv
import os

from datetime import datetime

from dotenv import load_dotenv

from sanmar import getInventoryLevel
from gcloud import getDataFromSheets, writeDataToSheets

load_dotenv()

today = datetime.now().strftime("%m_%d_%Y")

spreadsheet_id = os.getenv('SPREADSHEET_ID')

input = getDataFromSheets(spreadsheet_id)

# outputFile = open(f"sanmar_inventory_{today}.csv", "w+")
# output = csv.writer(outputFile)

# output.writerow(["ID", "COLOR", "XS", "S", "M",
#                 "L", "XL", "2XL", "3XL", "4XL"])

values = []
for row in input:
    productInv = getInventoryLevel(row[0], row[3])
    inventory = productInv['inventory']
    for key in inventory.keys():
        curItem = inventory[key]
        store = [curItem.get('XS', 0), curItem.get('S', 0), curItem.get('M', 0),
                 curItem.get('L', 0), curItem.get('XL', 0), curItem.get('2XL', 0), curItem.get('3XL', 0), curItem.get('4XL', 0)]
    values.append(store)

writeDataToSheets(spreadsheet_id, values)

print("DONE!")
