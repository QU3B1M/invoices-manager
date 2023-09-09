from fastapi import FastAPI

from app.core.middlewares import SQLAlchemyMiddleware

app = FastAPI()

app.add_middleware(SQLAlchemyMiddleware)
