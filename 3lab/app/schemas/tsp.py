from pydantic import BaseModel
from typing import List

class Graph(BaseModel):
    adjacency_matrix: List[List[int]]

class PathResult(BaseModel):
    path: List[int]
    total_distance: int
