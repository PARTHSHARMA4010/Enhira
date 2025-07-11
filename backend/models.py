from sqlmodel import SQLModel, Field

class Operator(SQLModel, table=True):
    __tablename__ = "operators"
    id: int | None = Field(primary_key=True)
    name: str
    phone_e164: str
    location: str
    upi_id: str | None = None
    scan_count: int | None = None
