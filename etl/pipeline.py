import requests
import psycopg2
import logging
import time
from statistics import mean
from models import MarketData

API_URL = "http://api:8000/v1/market-data"

logging.basicConfig(level=logging.INFO)

def get_connection():
    return psycopg2.connect(
        host="db",
        database="market",
        user="postgres",
        password="postgres"
    )

def extract():
    try:
        r = requests.get(API_URL, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        logging.error(f"API error: {e}")
        return []

def validate(records):
    valid = []
    for r in records:
        try:
            obj = MarketData(**r)
            valid.append(obj)
        except Exception:
            logging.warning("Validation failed")
    return valid

def detect_outliers(records):
    if not records:
        return []

    prices = [r.price for r in records]
    avg_price = mean(prices)

    clean = []

    for r in records:
        deviation = abs(r.price - avg_price) / avg_price
        if deviation > 0.15:
            logging.warning("Outlier detected")
            continue
        clean.append(r)

    return clean

def load(records):
    conn = get_connection()
    cur = conn.cursor()

    for r in records:
        cur.execute(
        '''
        INSERT INTO market_data (instrument_id, price, volume, timestamp)
        VALUES (%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
        ''',
        (r.instrument_id, r.price, r.volume, r.timestamp)
        )

    conn.commit()
    cur.close()
    conn.close()

def run():
    while True:
        start = time.time()

        raw = extract()
        validated = validate(raw)
        clean = detect_outliers(validated)
        load(clean)

        logging.info(f"Processed {len(clean)} records")
        logging.info(f"Execution Time: {time.time()-start}")

        time.sleep(10)

if __name__ == "__main__":
    run()