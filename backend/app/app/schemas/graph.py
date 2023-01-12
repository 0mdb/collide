from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Node(BaseModel):
    id: str
    name: str
    type: str
    val: int


class Link(BaseModel):
    source: str
    target: str
    type: str
    color: str
    dash: List[int]
    amount: int


class GraphData(BaseModel):
    nodes: List[Node]
    links: List[Link]


class GraphSearch(BaseModel):
    search: str


class GraphSubjet(BaseModel):
    subject: str
