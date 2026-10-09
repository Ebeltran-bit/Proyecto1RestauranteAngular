from pydantic import BaseModel


class Presentation(BaseModel):
    """Serving size a product can be ordered in (table `Tipos` in the classroom database)."""

    id: int
    name: str
