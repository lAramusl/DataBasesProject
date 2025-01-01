import random
from datetime import datetime, timedelta
import requests
from faker import Faker #just for data generation

# Инициализация Faker
faker = Faker()

# URL-адреса вашего REST API
BASE_URL = "http://127.0.0.1:8000"
LAPTOP_URL = f"{BASE_URL}/laptops"
PRODUCER_URL = f"{BASE_URL}/producers"
MARKET_OFFER_URL = f"{BASE_URL}/marketoffers"

# Генерация тестовых данных
def generate_laptops(n):
    laptops = []
    for _ in range(n):
        laptops.append({
            "model": faker.word(),
            "cpu": f"Intel Core {random.choice(['i5', 'i7', 'i9'])}",
            "gpu": random.choice(["NVIDIA GTX 1650", "RTX 3060", "RTX 4060"]),
            "ram": f"{random.choice([8, 16, 32])}GB DDR5",
            "screensize": f"{random.choice([13.3, 15.6, 17.3])} inch",
            "matrix": random.choice(["IPS", "OLED", "TN"]),
        })
    return laptops

def generate_producers(n):
    producers = []
    for _ in range(n):
        producers.append({
            "name": faker.company(),
            "country": faker.country(),
            "placement": faker.city(),
            "warranty": random.choice([True, False]),
        })
    return producers

def generate_market_offers(n, laptop_ids, producer_ids):
    offers = []
    for _ in range(n):
        offers.append({
            "laptopid": random.choice(laptop_ids),
            "producerid": random.choice(producer_ids),
            "price": round(random.uniform(500.0, 5000.0), 2),
            "date": faker.date_between(start_date='-2y', end_date='today').isoformat(),
        })
    return offers

# Отправка данных через REST API
def post_data(url, data):
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Insertion error: {response.status_code} - {response.text}")
        return None


if __name__ == "__main__":

    producers = generate_producers(10)
    producer_ids = []
    for producer in producers:
        response = post_data(PRODUCER_URL, producer)
        if response:
            producer_ids.append(response["id"])


    laptops = generate_laptops(15)
    laptop_ids = []
    for laptop in laptops:
        response = post_data(LAPTOP_URL, laptop)
        if response:
            laptop_ids.append(response["id"])

    market_offers = generate_market_offers(10, laptop_ids, producer_ids)
    for offer in market_offers:
        post_data(MARKET_OFFER_URL, offer)

    print("DONE!")
