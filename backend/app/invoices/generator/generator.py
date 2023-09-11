"""
File to generate invoices using the file backend/app/invoices/static/invoice_temp.html as Jinja2 template
and using a pydantic model to force the user to send the correct data to generate the invoice.
"""
import os
from datetime import datetime
from typing import Optional

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field

from app.core.config import config
from app.core.db.session import session
from app.core.db.transactional import Transactional
from app.models import Invoice


class InvoiceGenerator:
    """
    Model to force the user to send the correct data to generate the invoice.
    """

    @Transactional()
    async def generate(self, invoice : Invoice) -> Invoice:
        """
        Method to generate the invoice using the file backend/app/invoices/static/invoice_temp.html as Jinja2 template
        and using a pydantic model to force the user to send the correct data to generate the invoice.
        """
        # Get the template file
        template_path = os.path.join(
            config.BASE_DIR, "invoices", "static", "invoice_temp.html"
        )
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
        session.add(invoice)
        return invoice

    @Transactional()
    async def update(self, invoice_id: str) -> Invoice:
        """
        Method to update the invoice using the file backend/app/invoices/static/invoice_temp.html as Jinja2 template
        and using a pydantic model to force the user to send the correct data to generate the invoice.
        """
        # Get the template file
        template_path = os.path.join(
            config.BASE_DIR, "invoices", "static", "invoice_temp.html"
        )
        # Create the Jinja2 environment
        env = Environment(loader=FileSystemLoader(searchpath="/"))
        # Load the template file
        template = env.get_template(template_path)
        # Render the template with the data
        invoice_html = template.render(
            invoice_id=self.invoice_id,
            invoice_date=self.invoice_date,
            invoice_due_date=self.invoice_due_date,
            invoice_amount=self.invoice_amount,
            invoice_currency=self.invoice_currency,
            invoice_description=self.invoice_description,
        )
        # Save the invoice in the database
        invoice = Invoice(
            invoice_id=self.invoice_id,
            invoice_date=self.invoice_date,
            invoice_due_date=self.invoice_due_date,
            invoice_amount=self.invoice_amount,
            invoice_currency=self.invoice_currency,
            invoice_description=self.invoice_description,
            invoice_html=invoice_html,
        )
        session.query(Invoice).filter(Invoice.invoice_id == invoice_id).update(
            {
                Invoice.invoice_id: invoice.invoice_id,
                Invoice.invoice_date: invoice.invoice_date,
                Invoice.invoice_due_date: invoice.invoice_due_date,
                Invoice.invoice_amount: invoice.invoice_amount,
                Invoice.invoice_currency: invoice.invoice_currency,
                Invoice.invoice_description: invoice.invoice_description,
                Invoice.invoice_html: invoice.invoice_html,
            }
        )
        return invoice
