# Data Engineering Market Pipeline

FastAPI → ETL → PostgreSQL → Docker

## Run

docker-compose up --build

API Endpoint:
http://localhost:8000/v1/market-data

## Quality Controls

- Schema validation with Pydantic
- Outlier detection (>15% deviation)
- Duplicate protection using primary key (instrument_id, timestamp)

## Scaling (1B events/day)

API → Kafka → Spark Streaming → Data Lake/Warehouse

## Monitoring

Prometheus, Grafana, ELK stack

## Idempotency

Primary key + UPSERT logic