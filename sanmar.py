import os

from zeep import Client
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("SANMAR_USER")
PASSWORD = os.getenv("SANMAR_PASS")


def connect_to_wsdl(wsdl):
    attempts = 1
    while attempts <= 5:
        try:
            return Client(wsdl)
        except:
            print(f"Attempt: {attempts}")
            attempts += 1

    print("Failed to connect to WSDL")


def getInventoryLevel(productId, colorList):
    wsdl = "https://ws.sanmar.com:8080/promostandards/InventoryServiceBindingV2final?WSDL"  # prod
    # wsdl = "https://euat-ws.sanmar.com:8080/promostandards/InventoryServiceBindingV2final?WSDL"  # euat
    client = connect_to_wsdl(wsdl)

    request_data = {
        'wsVersion': '2.0.0',
        'id': USERNAME,
        'password': PASSWORD,
        'productId': productId,
        'Filter': {
            'PartColorArray': colorList
        }
    }

    result = client.service.getInventoryLevels(**request_data)

    colorAndSize = {}

    try:
        inventory = result['Inventory']['PartInventoryArray']['PartInventory']
    except Exception as e:
        print("Error: ", e)

    for item in inventory:
        curColor = item['partColor']
        curItem = {} if not colorAndSize.get(
            curColor, False) else colorAndSize[curColor]
        curItem[item['labelSize']] = int(
            item['quantityAvailable']['Quantity']['value'])
        colorAndSize[curColor] = curItem

    return {
        'productId': productId,
        'inventory': colorAndSize
    }
