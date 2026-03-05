import random
from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

instruments = ["AAPL", "BTC-USD", "ETH-USD", "TSLA"]

@app.get("/v1/market-data")
def get_market_data():
    # Chaos engineering (5%)
    if random.random() < 0.05:
        if random.choice([True, False]):
            raise HTTPException(status_code=500, detail="Internal Server Error")
        else:
            return [{"instrument_id": "AAPL", "price": "INVALID"}]

    data = []

    for instrument in instruments:
        data.append({
            "instrument_id": instrument,
            "price": round(random.uniform(100, 500), 2),
            "volume": round(random.uniform(10, 1000), 2),
            "timestamp": datetime.utcnow().isoformat()
        })

    return data