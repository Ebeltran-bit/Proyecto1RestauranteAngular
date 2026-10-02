from pydantic import BaseModel


class Product(BaseModel):
    """Menu item that belongs to one category (table `Carta` in the classroom database)."""

    id: int
    name: str
    category_id: int
