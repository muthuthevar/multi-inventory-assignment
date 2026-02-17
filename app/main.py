from fastapi import FastAPI

from app.api.routes import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import Item, ItemVendor, PurchaseOrder, Vendor

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_router)
