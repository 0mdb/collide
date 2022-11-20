from typing import Optional

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

from sqlmodel import Field, SQLModel, create_engine
from datetime import date


schema_name = "lf_mockup"

meta = sa.MetaData(schema=schema_name)


class Source(SQLModel, table=True):
    #__table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    date_obtained: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    data_source: str
    misc_data: dict = Field(default={}, sa_column=sa.Column(pg.JSONB))

    class Config:
        arbitrary_types_allowed = True


class Person(SQLModel, table=True):
    #__table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(unique=True, nullable=False)
    match_name: str = Field(unique=True, nullable=False)
    source: int = Field(foreign_key="source.id", nullable=False)


class Sector(SQLModel, table=True):
    #__table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(unique=True, nullable=False)
    match_name: str = Field(unique=True, nullable=False)


class OrganizationType(SQLModel, table=True):
    #__table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(unique=True, nullable=False)
    match_name: str = Field(unique=True, nullable=False)


class Organization(SQLModel, table=True):
    #__table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(unique=True, nullable=False)
    match_name: str = Field(unique=True, nullable=False)
    organization_type: int = Field(foreign_key='organizationtype.id', nullable=False)
    parent_organization: int = Field(foreign_key='organization.id', nullable=True)
    sector: int = Field(foreign_key='sector.id', nullable=False)
    source: int = Field(foreign_key='source.id', nullable=False)
    misc_data: dict = Field(default={}, sa_column=sa.Column(pg.JSONB))

    class Config:
        arbitrary_types_allowed = True


class OrganizationMembership(SQLModel, table=True):
    #__table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    person: int = Field(foreign_key='person.id', nullable=False)
    organization: int = Field(foreign_key='organization.id', nullable=False)
    start_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    end_date: date = Field(sa_column=sa.Column(sa.Date))
    source: int = Field(foreign_key='source.id', nullable=False)


class Communications(SQLModel, table=True):
    #__table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    party_1: int = Field(foreign_key='person.id', nullable=False)
    party_2: int = Field(foreign_key='person.id', nullable=False)
    com_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    sector: int = Field(foreign_key='sector.id')
    source: int = Field(foreign_key='source.id', nullable=False)


class Funding(SQLModel, table=True):
    #__table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    party_1: int = Field(foreign_key='organization.id', nullable=False)
    party_2: int = Field(foreign_key='organization.id', nullable=False)
    amount: int = Field(nullable=False)
    start_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    end_date: date = Field(sa_column=sa.Column(sa.Date))
    source: int = Field(foreign_key='source.id', nullable=False)


class CorporateInfo(SQLModel, table=True):
    #__table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    organization: int = Field(foreign_key='organization.id', nullable=False, unique=True)
    corporate_number: int = Field(nullable=False, unique=True)
    stock_ticker: str = Field(max_length=10, unique=True)
    source: int = Field(foreign_key='source.id', nullable=False)


if __name__ == "__main__":
    db_host = "localhost"
    db_name = "lq_test"
    db_user = "test_user"
    db_pw = "changethis"
    schema_name = "lf_mockup"

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pw}@localhost/{db_name}",  echo=True)
    meta.create_all(engine)
