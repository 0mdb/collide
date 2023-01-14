from gqlalchemy import Node, Relationship, Field
from typing import Optional
from datetime import date
import networkx as nx
from app.db.session import get_gdb

db = get_gdb()


class MGSource(Node, db=db):
    id: Optional[int] = Field(index=True, exists=True, unique=True, db=db)
    date_obtained: Optional[date] = Field()
    data_source: Optional[str]
    misc_data: Optional[str]


class MGPerson(Node, index=True, db=db):
    id: Optional[int] = Field(index=True, exists=True, unique=True, db=db)
    display_name: Optional[str] = Field(unique=True)
    match_name: Optional[str] = Field(index=True, unique=True)
    source: Optional[int] = Field(exists=True)


class MGSectorIndustry(Node, db=db):
    id: Optional[int] = Field(exists=True, unique=True)
    sector_display_name: Optional[str] = Field(exists=True, unique=True)
    sector_match_name: Optional[str] = Field(exists=True, unique=True)
    industry_display_name: Optional[str] = Field(exists=True, unique=True)
    industry_match_name: Optional[str] = Field(exists=True, unique=True)


class MGOrganizationType(Node, db=db):
    id: Optional[int] = Field(exists=True, unique=True)
    display_name: Optional[str] = Field(unique=True)
    match_name: Optional[str] = Field(unique=True)


class MGOrganization(Node, index=True, db=db):
    id: Optional[int] = Field(index=True, unique=True, exists=True)
    display_name: Optional[str] = Field(unique=True)
    match_name: Optional[str] = Field(index=True, unique=True)
    organization_type: Optional[str] = Field(exists=True)
    sector: Optional[str]
    industry: Optional[str]
    source: Optional[int] = Field()
    misc_data: Optional[str] = Field()


class MGMembership(Relationship, type="MEMBERSHIP"):
    id: Optional[int] = Field(unique=True)
    start_date: Optional[date] = Field()
    end_date: Optional[date] = Field()
    source: Optional[int] = Field(exists=True)


class MGCommsTopic(Node, db=db):
    id: Optional[int] = Field(unique=True, exists=True)
    display_name: Optional[str] = Field(exists=True, unique=True)
    match_name: Optional[str] = Field(exists=True, unique=True)


class MGCommunications(Relationship, type="COMMUNICATION"):
    id: Optional[int] = Field(exists=True, unique=True)
    party_0: Optional[int] = Field(exists=True)
    party_1: Optional[int] = Field(exists=True)
    com_date: Optional[date] = Field(exists=True)
    topic: Optional[str] = Field()
    source: Optional[int] = Field(exists=True)


class MGFunding(Relationship, type="FUNDS"):
    id: Optional[int] = Field(exists=True)
    party_0: Optional[int] = Field(exists=True)
    party_1: Optional[int] = Field(exists=True)
    amount: Optional[int] = Field(exist=True)
    start_date: Optional[date] = Field(exists=True)
    end_date: Optional[date] = Field()
    source: Optional[int] = Field(exists=True)
