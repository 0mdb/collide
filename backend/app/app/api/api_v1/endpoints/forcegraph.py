import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app import schemas
from app.crud.memgraph_make_graph import (
    graph_search_options,
    memgraph_query_and_aggregate,
)

router = APIRouter()


@router.get("/sample", response_model=schemas.GraphData)
def sample_graph() -> Any:
    """
    Sample graph data.
    """

    with open("app/data/bloc.json") as f:
        graph = json.load(f)
        return graph


@router.get("/bills", response_model=schemas.GraphData)
def bills() -> Any:
    """
    Return sample 2D BILL data.
    """
    sample_json = {
        "nodes": [
            {"id": "Myriel", "group": 1},
            {"id": "Napoleon", "group": 1},
            {"id": "Mlle.Baptistine", "group": 1},
        ],
        "links": [
            {"source": "Napoleon", "target": "Myriel", "value": 1},
            {"source": "Mlle.Baptistine", "target": "Myriel", "value": 8},
        ],
    }

    return sample_json


@router.post("/search/{id}", response_model=schemas.GraphData)
async def search_id(id: str) -> Any:
    """
    Retrieve search terms.
    """

    return memgraph_query_and_aggregate(
        poi_mn=id,
        fund_depth=2,
        membership_depth=2,
        communication_depth=2,
    )


@router.post("/search_options", response_model=list[schemas.GraphSearchOptions])
# @router.post("/search_options")
async def search_options(query: str) -> Any:
    """
    Retrieve search terms.
    """

    return graph_search_options(query)
