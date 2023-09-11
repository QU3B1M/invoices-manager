"""Repository for CRUD operations on the Invoice model using the base repository, also implementing the specific functionalities required for this case."""

from typing import Optional

from app.core.db.session import session
from app.core.db.transactional import Transactional
from app import models, schemas
from app.repositories.base import BaseRepository


class InvoiceRepository(BaseRepository[models.Invoice, schemas.Invoice]):
    """InvoiceRepository with default methods."""
    schema = schemas.Invoice
    model = models.Invoice
