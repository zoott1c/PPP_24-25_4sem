from fastapi import APIRouter
from app.schemas.tsp import Graph, PathResult
from app.services.tsp_service import calculate_shortest_path

router = APIRouter()

@router.get("/")
def read_tsp():
    return {"message": "TSP endpoint ready"}

@router.post("/shortest-path/", response_model=PathResult)
def get_shortest_path(graph: Graph):
    return calculate_shortest_path(graph)
