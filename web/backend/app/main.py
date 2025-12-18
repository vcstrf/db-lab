from fastapi import FastAPI
from . import routes
from app.database import get_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(routes.router)

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    get_db()