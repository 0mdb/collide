from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import json
from app import crud, models, schemas

router = APIRouter()


@router.get("/sample", response_model=schemas.GraphData)
async def sample_graph() -> Any:
    """
    Sample graph data.
    """

    with open("app/data/bloc.json") as f:
        graph = json.load(f)
        return graph


@router.get("/bills", response_model=schemas.GraphData)
def sample_graph() -> Any:
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


@router.get("/memgraph", response_model=schemas.GraphData)
def sample_graph() -> Any:
    """
    Retrieve memgraph 3D data.
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


@router.get("/memgraph/single", response_model=schemas.GraphData)
def sample_graph() -> Any:
    """
    Retrieve search subject and nearest nodes 3D data.
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


@router.get("/memgraph/double", response_model=schemas.GraphData)
def sample_graph() -> Any:
    """
    Retrieve graph data that connects two search subjects.
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


@router.get("/sankey", response_model=schemas.GraphData)
def sample_graph() -> Any:
    """
    Retrieve sankey data.
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


@router.get("/search_terms", response_model=List[schemas.GraphSearch])
def sample_graph() -> Any:
    """
    Retrieve search terms.
    """
    search_terms = ["thing1", "thing2", "thing3"]

    return search_terms
