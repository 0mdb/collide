from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Node(BaseModel):
    id: Optional[str]
    name: Optional[str]
    type: Optional[str]
    nodeColor: Optional[str]
    value: Optional[int]


class Link(BaseModel):
    source: Optional[str]
    target: Optional[str]
    type: Optional[str]
    linkColor: Optional[str]
    linkDirectionalArrowLength: Optional[int]
    linkDirectionalArrowRelPos: Optional[float]
    linkWidth: Optional[int]
    dash: Optional[List[int]]
    amount: Optional[int]


class GraphData(BaseModel):
    nodes: Optional[List[Node]]
    links: Optional[List[Link]]


class GraphSearchOptions(BaseModel):
    value: str
    label: str
    type: str
    bill_match: str
