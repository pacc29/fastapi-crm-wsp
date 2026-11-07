from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Maneja errores de integridad de la base de datos.
    """

    original_error = exc.orig

    # PostgreSQL / psycopg
    sqlstate = getattr(original_error, "sqlstate", None)
    if sqlstate is None:
        sqlstate = getattr(original_error, "pgcode", None)

    constraint_name = getattr(
        getattr(original_error, "diag", None),
        "constraint_name",
        None,
    )

    if sqlstate == "23505":
        return JSONResponse(
            status_code=409,
            content={
                "detail": "A record with this value already exists.",
                "code": "unique_violation",
                "constraint": constraint_name,
            },
        )

    if sqlstate == "23503":
        return JSONResponse(
            status_code=409,
            content={
                "detail": "The operation violates a foreign key constraint.",
                "code": "foreign_key_violation",
            },
        )

    if sqlstate == "23502":
        return JSONResponse(
            status_code=422,
            content={
                "detail": "A required database field cannot be null.",
                "code": "not_null_violation",
            },
        )

    if sqlstate == "23514":
        return JSONResponse(
            status_code=422,
            content={
                "detail": "The operation violates a database check constraint.",
                "code": "check_violation",
            },
        )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "A database integrity error occurred.",
            "code": "database_integrity_error",
        },
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Request validation failed.",
            "code": "validation_error",
            "errors": exc.errors(),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "code": "http_error",
        },
        headers=exc.headers,
    )


async def general_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error.",
            "code": "internal_server_error",
        },
    )



def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(
        IntegrityError,
        integrity_error_handler
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_error_handler,
    )

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        general_exception_handler,
    )