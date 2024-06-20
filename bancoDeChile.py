from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import re
import locale
import random

# Configurar el locale para español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Definición de modelos y funciones de utilidad
from pydantic import BaseModel
import datetime as d
class Discount(BaseModel): #Modificar en base al E-R
    id: str
    url: str
    local: str
    discount: int
    description: str
    category: str
    expiration: d.datetime
    days: str


class Bank(BaseModel):
    name: str

class Card(BaseModel):
    bankId: str
    cardType: str
    bank: str

class Category(BaseModel):
    categoryName: str

# Cargar variables de entorno
envPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.dirname(envPath)
dotenvPath = os.path.join(rootPath, '.env')
load_dotenv(dotenvPath)

mongoUrl = "tehee"
client = MongoClient(mongoUrl)
db = client.foomonkeys123
discountsTable = db["Discounts"]
banksTable = db["Banks"]
cardsTable = db["Cards"]
categoriesTable = db["Categories"]
usersTable = db["Users"]

def extract_discount(excerpt):
    match = re.search(r'(\d+)', excerpt)
    return int(match.group(1)) if match else None

def parse_expiration(conditions):
    match = re.search(r'hasta el (.+?)\.', conditions)
    if match:
        date_str = match.group(1)
        try:
            return datetime.strptime(date_str.strip(), '%d de %B de %Y')
        except ValueError:
            pass
    return None

def parse_days(summary):
    days_pattern = r'(Todos los días|Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo)( a (Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo))?'
    match = re.search(days_pattern, summary)
    if match:
        if match.group(3):
            return f"{match.group(1)} a {match.group(3)}"
        else:
            return match.group(1)
    return "Desconocido"

def insert_discounts(data, category_ids, card_ids):
    for item in data:
        expiration_date = parse_expiration(item["details"].get("conditions"))
        days = parse_days(item["details"].get("summary"))

        category = "None"
        if item.get("category", "").startswith("beneficios/sabores"):
            category = category_ids["Comida"]
        elif item.get("category", "").startswith("beneficios/viajes"):
            category = category_ids["Transporte"]
        elif item.get("category", "").startswith("beneficios/bienestar"):
            category = category_ids["Bienestar"]
        elif item.get("category", "").startswith("beneficios/mascota"):
            category = category_ids["Mascotas"]
        lista = item.get("cards").split(",")
        if item.get("bank") == "Banco de Chile":
            if item.get("cards") == "":
                cards = [["Bronze","Debito"],["Silver","Credito"],["Gold","Credito"]]
                for card in cards:
                    discount = {
                        "url": item.get("url"),
                        "local": item.get("title"),
                        "discount": extract_discount(item.get("excerpt")),
                        "description": item.get("description"),
                        "category": category,
                        "expiration": expiration_date,
                        "days": days,
                        "card": card_ids[card[0]],
                        "cardType": card[0],
                        "paymentType": card[1],
                        "bankName": "Banco de Chile"
                    }
                    discountsTable.insert_one(discount)
            else:
                for elemento in lista:
                    if elemento =="Bronze":
                        type = "Debito"
                    else:
                        type = "Credito"

                    discount = {
                        "url": item.get("url"),
                        "local": item.get("title"),
                        "discount": extract_discount(item.get("excerpt")),
                        "description": item.get("description"),
                        "category": category,
                        "expiration": expiration_date,
                        "days": days,
                        "card": card_ids[elemento],
                        "cardType":elemento,
                        "paymentType": type,
                        "bankName": "Banco de Chile"
                    }
                    discountsTable.insert_one(discount)
        else:
            if item.get("cards") == "":
                cards = [["Black", "Debito"], ["Diamond", "Credito"]]
                for card in cards:
                    discount = {
                        "url": item.get("url"),
                        "local": item.get("title"),
                        "discount": extract_discount(item.get("excerpt")),
                        "description": item.get("description"),
                        "category": category,
                        "expiration": expiration_date,
                        "days": days,
                        "card": card_ids[card[0]],
                        "cardType": card[0],
                        "paymentType": card[1],
                        "bankName": "Banco Santander"
                    }
                    discountsTable.insert_one(discount)
            else:
                for elemento in lista:
                    if elemento == "Black":
                        type = "Debito"
                    else:
                        type = "Credito"

                    discount = {
                        "url": item.get("url"),
                        "local": item.get("title"),
                        "discount": extract_discount(item.get("excerpt")),
                        "description": item.get("description"),
                        "category": category,
                        "expiration": expiration_date,
                        "days": days,
                        "card": card_ids[elemento],
                        "cardType": elemento,
                        "paymentType": type,
                        "bankName": "Banco Santander"
                    }
                    discountsTable.insert_one(discount)
def insert_categories():
    categories = ["Comida", "Transporte", "Bienestar", "Mascotas"]
    category_ids = {}
    for category in categories:
        categoria = {
            "name": category
        }
        result = categoriesTable.insert_one(categoria)
        category_ids[category] = str(result.inserted_id)
    return category_ids

def insert_banks():
    banks = ["Banco de Chile", "Banco Santander"]
    bank_ids = {}
    for bank in banks:
        banco = {
            "name": bank
        }
        result = banksTable.insert_one(banco)
        bank_ids[bank] = str(result.inserted_id)
    return bank_ids

def insert_cards(bank_ids):
    cards = [["Bronze","Debito","Banco de Chile"],["Silver","Credito","Banco de Chile"],
             ["Gold","Credito","Banco de Chile"], ["Black","Debito","Banco Santander"],
             ["Diamond", "Credito","Banco Santander"]]
    card_ids = {}
    for card in cards:
        tarjeta = {
            "bankId": bank_ids[card[2]],
            "cardType": card[0],
            "paymentMethod": card[1]
        }
        result = cardsTable.insert_one(tarjeta)
        card_ids[card[0]] = str(result.inserted_id)
    return card_ids

# Leer datos desde discounts.json
with open('Data/descuentos_simulados.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insertar los datos en la base de datos
discountsTable.delete_many({})
categoriesTable.delete_many({})
cardsTable.delete_many({})
banksTable.delete_many({})
usersTable.delete_many({})
bank_ids = insert_banks()
category_ids = insert_categories()
print(category_ids)
card_ids = insert_cards(bank_ids)
insert_discounts(data,category_ids,card_ids)

