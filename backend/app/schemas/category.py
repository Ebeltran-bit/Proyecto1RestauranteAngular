from pydantic import BaseModel


class Category(BaseModel):
    """Group of products on the menu (table `Grupos` in the classroom database)."""

    id: int
    name: str
