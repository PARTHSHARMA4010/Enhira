from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware         # ← add
from sqlmodel import select, SQLModel
from models import Operator
from db import engine, get_session

app = FastAPI(title="Ops Dashboard API")

# ─────── CORS (allow React dev server) ───────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # Vite dev URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ─────────────────────────────────────────────

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

import logging
logger = logging.getLogger("ops-dashboard")   # add this once at top

@app.get("/ping")
def ping():
    logger.info("✅  Front-end just pinged the back-end")
    return {"status": "pong"}


@app.get("/operators")
def list_ops(session=Depends(get_session)):
    return session.exec(select(Operator)).all()
