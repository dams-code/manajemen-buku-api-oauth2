from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers.buku import router_buku

from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.exception_handler(HTTPException)
async def set_Format_JSON_Handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "pesan": str(exc.detail),
            "data": None
        }
    )

app.include_router(router_buku)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8080",
]

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
