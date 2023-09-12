from app.models import Invoice
from app.repositories.base import BaseRepository


class InvoiceRepository(BaseRepository[Invoice]):
    """InvoiceRepository with default methods."""
    model = Invoice
