from fastapi import FastAPI

from app.core.middlewares import SQLAlchemyMiddleware
from app.core.db.session import init_models


app = FastAPI()

app.add_middleware(SQLAlchemyMiddleware)


@app.on_event("startup")
async def startup_event():
    await init_models()
