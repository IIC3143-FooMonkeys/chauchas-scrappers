import json
from faker import Faker
import random

fake = Faker()

def random_days():
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    choice = random.choice([
        "Todos los días",
        random.choice(days),
        f"{random.choice(days)} a {random.choice(days)}"
    ])
    return choice

def generate_discount():
    days = random_days()
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
        "category": "beneficios/sabores/restaurantes-y-bares",
        "site_id": 1,
        "video_url": fake.url() if random.choice([True, False]) else "",
        "details": {
            "summary": f"{random.choice([20, 25, 30, 35])}% de dcto. {days} en consumo presencial.",
            "list": [
                "Solicita tu descuento al momento de pagar en forma presencial.",
                "No válido en menú, happy hour y fechas especiales.",
                "Si tienes Plan Cordillera obtén 10% de dcto. adicional.",
                "Si tienes Plan Océano obtén 20% de dcto. adicional."
            ],
            "conditions": "Promoción válida hasta el 31 de diciembre de 2025. No acumulable con otras promociones."
        }
    }

def generate_discounts(n):
    return [generate_discount() for _ in range(n)]

# Genera n descuentos
discounts = generate_discounts(10)

with open('descuentos_simulados.json', 'w', encoding='utf-8') as f:
    json.dump(discounts, f, indent=4, ensure_ascii=False)

print("Data simulada guardada en 'descuentos_simulados.json'")
