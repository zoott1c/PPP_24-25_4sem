from fastapi import APIRouter
from . import tsp, auth

router = APIRouter()
router.include_router(tsp.router, prefix="/tsp", tags=["TSP"])
router.include_router(auth.router, tags=["Auth"])