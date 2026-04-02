from fastapi import FastAPI
from app.database import Base, engine

from app.models import user, transaction # import models
from app.schemas.transaction_schema import TransactionCreate
from app.routes import auth_routes, transaction_routes, dashboard_routes, user_routes


app = FastAPI(title="FinanceFlow API")

Base.metadata.create_all(bind=engine)
app.include_router(auth_routes.router)
app.include_router(transaction_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(user_routes.router)
@app.get("/")
def root():
    return {"message": "FinanceFlow API is running"}

