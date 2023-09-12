from app.core.models import Invoice
from app.core.repositories.base import BaseRepository


class InvoiceRepository(BaseRepository[Invoice]):
    """InvoiceRepository with default methods."""
    model = Invoice
