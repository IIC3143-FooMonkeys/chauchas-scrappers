import json
from faker import Faker
import random

fake = Faker()
categories = ["sabores","viajes","bienestar","mascota"]
def random_days():
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    choice = random.choice([
        "Todos los días",
        random.choice(days),
        f"{random.choice(days)} a {random.choice(days)}"
    ])
    return choice
cards = [["","Bronze","Silver","Gold","Silver,Gold","Bronze,Gold","Bronze,Silver"],["","Black","Diamond","Black,Diamond"]]
def generate_discount():
    days = random_days()
    ch = random.choice([0,1])
    mes = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    if ch == 0:
        name = "Banco de Chile"
    else:
        name = "Banco Santander"
    return {
        "id": fake.random_number(digits=5),
        "uuid": fake.uuid4(),
        "created_at": fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
        "updated_at": fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
        "published_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
        "url": fake.url(),
        "title": fake.company(),
        "slug": fake.slug(),
        "excerpt": f"{random.choice([20, 25, 30, 35])}% de dcto. {days}.",
        "description": fake.text(),
        "covers": [fake.image_url() for _ in range(2)],
        "tags": fake.words(nb=4),
        "category": f"beneficios/{random.choice(categories)}",
        "site_id": 1,
        "cards": random.choice(cards[ch]),
        "video_url": fake.url() if random.choice([True, False]) else "",
        "bank":name,
        "details": {
            "summary": f"{random.choice([20, 25, 30, 35])}% de dcto. {days} en consumo presencial.",
            "list": [
                "Solicita tu descuento al momento de pagar en forma presencial.",
                "No válido en menú, happy hour y fechas especiales.",
                "Si tienes Plan Cordillera obtén 10% de dcto. adicional.",
                "Si tienes Plan Océano obtén 20% de dcto. adicional."
            ],
            "conditions": f"Promoción válida hasta el {random.randint(1,27)} de {random.choice(mes)} de {random.randint(2025,2030)}. No acumulable con otras promociones."
        }
    }

def generate_discounts(n):
    return [generate_discount() for _ in range(n)]

# Genera n descuentos
discounts = generate_discounts(10)

with open('descuentos_simulados.json', 'w', encoding='utf-8') as f:
    json.dump(discounts, f, indent=4, ensure_ascii=False)

print("Data simulada guardada en 'descuentos_simulados.json'")
