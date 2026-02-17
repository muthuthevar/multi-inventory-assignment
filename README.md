# Multi-Vendor Inventory System

A FastAPI backend for managing inventory where one item can be associated with multiple approved vendors, with purchase order workflow and stock tracking.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker Compose
- uv (package/environment management)

## Features

- Central stock item registry
- Vendor management
- Many-to-many item-vendor association (approved vendors)
- Purchase order creation with manual vendor selection constraint
- Stock updates when purchase orders are received

## Project Structure

```text
app/
  api/
  core/
  db/
  models/
  repositories/
  schemas/
  services/
```

## Setup

```bash
cd /Users/jarvis/projects/personal-projects/assignment-iventory-system
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
cp .env.example .env
docker compose up -d
```

## Run API

```bash
DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/inventory_db" \
uv run --python .venv/bin/python uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Health Check

```bash
curl -X GET "http://127.0.0.1:8000/health"
```

## Main API Endpoints

- `POST /api/v1/items`
- `GET /api/v1/items`
- `PATCH /api/v1/items/{item_id}/stock`
- `POST /api/v1/items/{item_id}/vendors/{vendor_id}`
- `GET /api/v1/items/{item_id}/approved-vendors`
- `POST /api/v1/vendors`
- `GET /api/v1/vendors`
- `POST /api/v1/purchase-orders`
- `GET /api/v1/purchase-orders`
- `GET /api/v1/purchase-orders/{purchase_order_id}`
- `PATCH /api/v1/purchase-orders/{purchase_order_id}/status`

## Testing Flow

You can use manual curl requests from `SETUP.md` to validate the end-to-end flow.
