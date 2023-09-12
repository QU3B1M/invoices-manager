"""
File to generate invoices using the file backend/app/invoices/static/invoice_temp.html as Jinja2 template
and using a pydantic model to force the user to send the correct data to generate the invoice.
"""
import os

from jinja2 import Environment, FileSystemLoader

from app.api.schemas import Invoice
from app.repositories import InvoiceRepository


async def render(invoice: Invoice) -> Invoice:
    """
    Method to generate the invoice using the file backend/app/invoices/static/invoice_temp.html as Jinja2 template
    and using a pydantic model to force the user to send the correct data to generate the invoice.
    """
    # Get the template file
    template_path = os.path.join('app', 'static', 'invoice_template.html')
    # Create the Jinja2 environment
    env = Environment(loader=FileSystemLoader(searchpath="/"))
    # Load the template file
    template = env.get_template(template_path)
    # Render the template with the data
    invoice_html = template.render(
        invoice_id=invoice.id,
        invoice_date=invoice.date,
        invoice_due_date=invoice.due_date,
        invoice_amount=invoice.amount,
        invoice_currency=invoice.currency,
        invoice_description=invoice.description,
    )
    # Save the invoice in the database
    invoice = Invoice(**invoice, invoice_html=invoice_html)
    InvoiceRepository.create(invoice)

    return invoice
