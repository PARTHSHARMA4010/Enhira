from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import select, SQLModel
from models import Operator
from db import engine, get_session
import logging

logger = logging.getLogger("ops-dashboard")

app = FastAPI(title="Ops Dashboard API")

# --- CORS so React dev-server can call us --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------------------------------

@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(engine)

# ---------- health check -------------------------------------
@app.get("/ping")
def ping():
    logger.info("✅  Front-end just pinged the back-end")
    return {"status": "pong"}

# ---------- list operators -----------------------------------
@app.get("/operators")
def list_ops(session=Depends(get_session)):
    ops = session.exec(select(Operator)).all()
    logger.info(f"📤 Sent {len(ops)} operator(s) to front-end")
    return ops

# ---------- create operator (simple seed) --------------------
class OpCreate(BaseModel):
    name: str
    phone_e164: str
    location: str
    upi_id: str | None = None
    scan_count: int | None = None

@app.post("/operators")
def create_op(payload: OpCreate, session=Depends(get_session)):
    op = Operator(**payload.model_dump())
    session.add(op)
    session.commit()
    session.refresh(op)
    logger.info(f"➕ Added operator {op.name}")
    return op
