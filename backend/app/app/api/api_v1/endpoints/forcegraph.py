from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import json

router = APIRouter()


@router.get("/", tags=["forcegraph"])
def sample_graph() -> Any:
    """
    Retrieve items.
    """

    with open("app/data/sample_graph3.json") as f:
        graph = json.load(f)
        return graph
