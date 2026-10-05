from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.controllers.user_controller import router as user_router
from app.controllers.auth_controller import router as auth_router
from app.infrastructure.exceptions.handlers import validation_exception_handler

from app.infrastructure.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication API",
    description="API para o cadastro e autenticação de usuários.",
    version="1.0.0"
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(user_router)
app.include_router(auth_router)