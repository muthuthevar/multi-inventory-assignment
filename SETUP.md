# Setup and Run Guide

## 1) Prerequisites

- Python 3.9+
- `uv` installed
- Docker (for PostgreSQL)

## 2) Install dependencies

```bash
cd /Users/jarvis/projects/personal-projects/assignment-iventory-system
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

## 3) Configure environment

```bash
cp .env.example .env
```

Default DB URL in `.env`:

`postgresql+psycopg2://postgres:postgres@localhost:5432/inventory_db`

## 4) Start PostgreSQL

```bash
docker compose up -d
docker compose ps
```

## 5) Run API

```bash
DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/inventory_db" \
uv run --python .venv/bin/python uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## 6) Verify service

```bash
curl -X GET "http://127.0.0.1:8000/health"
```

Expected response:

`{"status":"ok"}`

## 7) Quick API flow test (manual)

### Create item

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/items" \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "SKU-1001",
    "name": "Laptop",
    "description": "15 inch business laptop",
    "current_stock": 10
  }'
```

### Create vendor

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/vendors" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tech Supplies Ltd",
    "contact_email": "sales@techsupplies.com",
    "is_active": true
  }'
```

### Link vendor to item

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/items/1/vendors/1"
```

### Create purchase order

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/purchase-orders" \
  -H "Content-Type: application/json" \
  -d '{
    "item_id": 1,
    "vendor_id": 1,
    "quantity": 5
  }'
```

### Mark purchase order as received

```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/purchase-orders/1/status" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "received"
  }'
```
