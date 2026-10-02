from pydantic import BaseModel


class Table(BaseModel):
    """Restaurant table where orders are taken (table `Mesas` in the classroom database)."""

    id: int
    name: str
