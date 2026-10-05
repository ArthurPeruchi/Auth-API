from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []

    for error in exc.errors():
        field = error["loc"][-1]

        errors.append({"field": field, "message": get_error_message(error)})

    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )

def get_error_message(error: dict) -> str:
    error_type = error["type"]

    if error_type == "missing":
        return "[!] Campo obrigatório."

    if error_type == "string_too_short":
        return "[!] Campo possui poucos caracteres."

    if error_type == "string_too_long":
        return "[!] Campo possui muitos caracteres."

    if error_type == "value_error":
        return "[!] Valor inválido."

    return "[!] Dados inválidos."
