from pydantic import BaseModel
from datetime import datetime


class SaleCreate(BaseModel):
    """What the incoming POST /sales request must contain."""
    product_id: int
    quantity: int
    region: str


class SaleResponse(BaseModel):
    """What we send back after saving a sale."""
    id: int
    product_id: int
    quantity: int
    region: str
    timestamp: datetime

    class Config:
        from_attributes = True  # lets Pydantic read data straight from the DB model
