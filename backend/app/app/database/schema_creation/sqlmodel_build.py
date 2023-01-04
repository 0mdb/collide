from typing import Optional
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field, SQLModel, create_engine
from datetime import date

schema_name = "lf_mockup_2"
meta = sa.MetaData(schema=schema_name)


class Source(SQLModel, table=True):
    # __table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    date_obtained: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    data_source: str
    misc_data: dict = Field(default={}, sa_column=sa.Column(pg.JSONB))

    class Config:
        arbitrary_types_allowed = True

    def as_dict(self):
        return {'id': self.id,
                'date_obtained': self.date_obtained,
                'data_source': self.data_source,
                'misc_data': self.misc_data
                }


class Person(SQLModel, table=True):
    # __table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(unique=True, nullable=False)
    match_name: str = Field(unique=True, nullable=False)
    source: int = Field(foreign_key="source.id", nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'display_name': self.display_name,
                'match_name': self.match_name,
                'source': self.source}


class SectorIndustry(SQLModel, table=True):
    # __table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    sector_display_name: str = Field(default=None)
    sector_match_name: str = Field(default=None)
    industry_display_name: str = Field(default=None)
    industry_match_name: str = Field(default=None)

    def as_dict(self):
        return {'id': self.id,
                'sector_display_name': self.sector_display_name,
                'sector_match_name': self.sector_match_name,
                'industry_display_name': self.industry_display_name,
                'industry_match_name': self.industry_match_name}


class OrganizationType(SQLModel, table=True):
    # __table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(unique=True, nullable=False)
    match_name: str = Field(unique=True, nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'display_name': self.display_name,
                'match_name': self.match_name}


class Organization(SQLModel, table=True):
    # __table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(unique=True, nullable=False)
    match_name: str = Field(unique=True, nullable=False)
    organization_type: int = Field(foreign_key='organizationtype.id', nullable=False)
    parent_organization: int = Field(foreign_key='organization.id', nullable=True)
    sector: int = Field(foreign_key='sectorindustry.id', nullable=True)
    source: int = Field(foreign_key='source.id', nullable=False)
    misc_data: dict = Field(default={}, sa_column=sa.Column(pg.JSONB))

    class Config:
        arbitrary_types_allowed = True

    def as_dict(self):
        return {'id': self.id,
                'display_name': self.display_name,
                'match_name': self.match_name,
                "organization_type": self.organization_type,
                'parent_organization': self.parent_organization,
                'sector': self.sector,
                'source': self.source,
                'misc_data': self.misc_data}


class OrganizationMembership(SQLModel, table=True):
    # __table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    person: int = Field(foreign_key='person.id', nullable=False, index=True)
    organization: int = Field(foreign_key='organization.id', nullable=False, index=True)
    start_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    end_date: date = Field(sa_column=sa.Column(sa.Date))
    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'person': self.person,
                'organization': self.organization,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'source': self.source}


class CommsTopic(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(nullable=False)
    match_name: str = Field(unique=True, nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'display_name': self.display_name,
                'match_name': self.match_name}


class Communications(SQLModel, table=True):
    # __table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    party_1: int = Field(foreign_key='person.id', nullable=False, index=True)
    party_2: int = Field(foreign_key='person.id', nullable=False, index=True)
    com_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    topic: int = Field(foreign_key='commstopic.id')
    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                "party_1": self.party_1,
                'party_2': self.party_2,
                'com_date': self.com_date,
                'topic': self.topic,
                'source': self.source}


class CommunicationsPersonOrg(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    person: int = Field(foreign_key='person.id', nullable=False, index=True)
    organization: int = Field(foreign_key='organization.id', nullable=False, index=True)
    com_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    topic: int = Field(foreign_key='commstopic.id')
    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'person': self.person,
                'organization': self.organization,
                'com_date': self.com_date,
                'topic': self.topic,
                'source': self.source}


class CommunicationsOrgOrg(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    party_1: int = Field(foreign_key='organization.id', nullable=False, index=True)
    party_2: int = Field(foreign_key='organization.id', nullable=False, index=True)
    com_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    topic: int = Field(foreign_key='commstopic.id')
    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'party_1': self.party_1,
                'party_2': self.party_2,
                'com_date': self.com_date,
                'topic': self.topic,
                'source': self.source}


class Funding(SQLModel, table=True):
    # __table_args__ = {"schema": f"{schema_name}"}
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    party_1: int = Field(foreign_key='organization.id', nullable=False, index=True)
    party_2: int = Field(foreign_key='organization.id', nullable=False, index=True)
    amount: int = Field(nullable=False)
    start_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    end_date: date = Field(sa_column=sa.Column(sa.Date))
    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'party_1': self.party_1,
                'party_2': self.party_2,
                'amount': self.amount,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'source': self.source}


class FundingPersonPerson(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    party_1: int = Field(foreign_key='person.id', nullable=False, index=True)
    party_2: int = Field(foreign_key='person.id', nullable=False, index=True)
    amount: int = Field(nullable=False)
    start_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    end_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'party_1': self.party_1,
                'party_2': self.party_2,
                'amount': self.amount,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'source': self.source}


class FundingPersonOrg(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    person: int = Field(foreign_key='person.id', nullable=False, index=True)
    organization: int = Field(foreign_key='organization.id', nullable=False, index=True)
    amount: int = Field(nullable=False)
    start_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    end_date: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'person': self.person,
                'organization': self.organization,
                'amount': self.amount,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'source': self.source}


class Bill(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)

    bill_name: str = Field(nullable=False)
    parliament: int = Field(nullable=False)
    parliament_session: int = Field(nullable=False)
    match_name: str = Field(unique=True, nullable=False)  # parl_session_name

    description: str = Field(nullable=False)

    is_house_bill: bool = Field(nullable=False)
    is_senate_bill: bool = Field(nullable=False)

    first_house_read_date: date = Field(sa_column=sa.Column(sa.Date, nullable=True))
    second_house_read_date: date = Field(sa_column=sa.Column(sa.Date, nullable=True))
    third_house_read_date: date = Field(sa_column=sa.Column(sa.Date, nullable=True))
    first_senate_read_date: date = Field(sa_column=sa.Column(sa.Date, nullable=True))
    second_senate_read_date: date = Field(sa_column=sa.Column(sa.Date, nullable=True))
    third_senate_read_date: date = Field(sa_column=sa.Column(sa.Date, nullable=True))
    royal_assent_date: date = Field(sa_column=sa.Column(sa.Date, nullable=True))

    is_read_first_house: bool = Field(nullable=False)
    is_read_second_house: bool = Field(nullable=False)
    is_read_third_house: bool = Field(nullable=False)
    is_read_first_senate: bool = Field(nullable=False)
    is_read_second_senate: bool = Field(nullable=False)
    is_read_third_senate: bool = Field(nullable=False)
    is_passed_royal_assent: bool = Field(nullable=False)

    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'bill_name': self.bill_name,
                'parliament': self.parliament,
                'parliament_session': self.parliament_session,
                'match_name': self.match_name,
                'description': self.description,
                'is_house_bill': self.is_house_bill,
                'is_senate_bill': self.is_senate_bill,
                "first_house_read_date": self.first_house_read_date,
                "second_house_read_date": self.second_house_read_date,
                "third_house_read_date": self.third_house_read_date,
                "first_senate_read_date": self.first_senate_read_date,
                "second_senate_read_date": self.second_senate_read_date,
                "third_senate_read_date": self.third_senate_read_date,
                "royal_assent_date": self.royal_assent_date,
                "is_read_first_house": self.is_read_first_house,
                "is_read_second_house": self.is_read_second_house,
                "is_read_third_house": self.is_read_third_house,
                "is_read_first_senate": self.is_read_first_senate,
                "is_read_second_senate": self.is_read_second_senate,
                "is_read_third_senate": self.is_read_third_senate,
                "is_passed_royal_assent": self.is_passed_royal_assent,
                'source': self.source
                }


class Vote(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)

    parliament: int = Field(nullable=False)
    parliament_session: int = Field(nullable=False)
    date_held: date = Field(sa_column=sa.Column(sa.Date, nullable=False))
    vote_number: int = Field(nullable=False)
    match_name: str = Field(unique=True, nullable=False)  # parl_session_voteno

    description: str = Field(nullable=False)
    yeas: int = Field(nullable=False)
    nays: int = Field(nullable=False)
    paired: int = Field(nullable=False)
    result: str = Field(nullable=False)

    bill: int = Field(foreign_key='bill.id', nullable=True, index=True)
    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'parliament': self.parliament,
                'parliament_session': self.parliament_session,
                'date_held': self.date_held,
                'vote_number': self.vote_number,
                'match_name': self.match_name,
                'description': self.description,
                'yeas': self.yeas,
                'nays': self.nays,
                'paired': self.paired,
                'result': self.result,
                'bill': self.bill,
                'source': self.source
                }


class VoteIndividual(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)

    vote: int = Field(foreign_key='vote.id', nullable=False, index=True)
    person: int = Field(foreign_key='person.id', nullable=False, index=True)

    is_yea: bool = Field(nullable=False)
    is_nay: bool = Field(nullable=False)
    is_paired: bool = Field(nullable=False)

    source: int = Field(foreign_key='source.id', nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'vote': self.vote,
                'person': self.person,
                'is_yea': self.is_yea,
                'is_nay': self.is_nay,
                'is_paired': self.is_paired,
                'source': self.source}


class LegStage(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)
    display_name: str = Field(unique=True, nullable=False)
    match_name: str = Field(unique=True, nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'display_name': self.display_name,
                'match_name': self.match_name}


class BillDiff(SQLModel, table=True):
    metadata = meta
    id: Optional[int] = Field(default=None, primary_key=True)

    bill: int = Field(foreign_key='bill.id', nullable=False, index=True)
    stage_1: int = Field(foreign_key='legstage.id', nullable=False, index=True)
    stage_2: int = Field(foreign_key='legstage.id', nullable=False, index=True)
    txt_diff: str = Field(nullable=False)

    def as_dict(self):
        return {'id': self.id,
                'bill': self.bill,
                'stage_1': self.stage_1,
                'stage_2': self.stage_2,
                'txt_diff': self.txt_diff}

# class CorporateInfo(SQLModel, table=True):
#     #__table_args__ = {"schema": f"{schema_name}"}
#     metadata = meta
#     id: Optional[int] = Field(default=None, primary_key=True)
#     organization: int = Field(foreign_key='organization.id', nullable=False, unique=True)
#     corporate_number: int = Field(nullable=False, unique=True)
#     stock_ticker: str = Field(max_length=10, unique=True)
#     source: int = Field(foreign_key='source.id', nullable=False)
