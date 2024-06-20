from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import re
import locale

# Configurar el locale para español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Definición de modelos y funciones de utilidad
from pydantic import BaseModel
import datetime as d

class Discount(BaseModel): #Modificar en base al E-R
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


def discountEntity(discount) -> dict:
    discount['id'] = str(discount['_id'])
    del discount['_id']
    return {
        "id": discount["id"],
        "name": str(discount["name"]),
        "category": str(discount["category"]),
        "url": str(discount["url"]),
        "local": str(discount["title"]),
        "discount": int(discount["discount"]),
        "description": str(discount["description"]),
        "expiration": discount["expiration"],
        "days": str(discount["days"])
    }

def discountEntities(entity) -> list:
    return [discountEntity(discount) for discount in entity]

# Cargar variables de entorno
envPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.dirname(envPath)
dotenvPath = os.path.join(rootPath, '.env')
load_dotenv(dotenvPath)

mongoUrl = os.getenv("MONGO_URL")
client = MongoClient(mongoUrl)
db = client.foomonkeys123
discountsTable = db["Discounts"]

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

def parse_days(conditions):
    if "Todos los días" in conditions:
        return "Todos los días"
    match = re.search(r'(Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo)( a (Lunes|Martes|Miércoles|Jueves|Viernes|Sábado|Domingo))?', conditions)
    if match:
        if match.group(2):
            return f"{match.group(1)} a {match.group(3)}"
        else:
            return match.group(1)
    return "Desconocido"

def insert_discounts(data):
    for item in data:
        expiration_date = parse_expiration(item["details"].get("conditions"))
        days = parse_days(item["details"].get("conditions"))
        discount = {
            "url": item.get("url"),
            "local": item.get("title"),
            "discount": extract_discount(item.get("excerpt")),
            "description": item.get("description"),
            "category": "Comida" if item.get("category", "").startswith("beneficios/sabores") else item.get("category"),
            "expiration": expiration_date,
            "days": days
        }
        discountsTable.insert_one(discount)

# Leer datos desde discounts.json
with open('Data/descuentos_simulados.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insertar los datos en la base de datos
discountsTable.delete_many({})
insert_discounts(data)
