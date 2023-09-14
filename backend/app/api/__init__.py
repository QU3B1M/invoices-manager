from fastapi import APIRouter

from .routers import user, invoice


router = APIRouter()

router.include_router(user.router)
router.include_router(invoice.router)
