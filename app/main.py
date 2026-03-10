import logging
from urllib.request import Request

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from app.api.core.error_handler import ResponseException
from app.api.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

app = FastAPI(
    title="Video FLow"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ResponseException)
def response_error_handler(_: Request, exc: ResponseException) -> Response:
    """Turns any ResponseException into a JSON with the exception content"""
    return JSONResponse(status_code=exc.code, content=exc.content)


@app.exception_handler(Exception)
def generic_exception_handler(_: Request, _exc: Exception) -> Response:
    """Torna uma exceção qualquer em uma reposta de Internal Server Error"""

    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"},
    )


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
