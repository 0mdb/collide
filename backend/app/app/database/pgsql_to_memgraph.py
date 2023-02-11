from gqlalchemy import Memgraph, Node, Relationship, Field
from typing import Optional
from datetime import date
import json
import mgclient
from unidecode import unidecode
from schema_creation.sqlmodel_build import (
    Person,
    OrganizationMembership,
    Communications,
    Organization,
    OrganizationType,
    SectorIndustry,
    Funding,
    FundingPersonOrg,
    FundingPersonPerson,
    CommunicationsOrgOrg,
    CommunicationsPersonOrg,
    CommsTopic,
)
from sqlmodel import create_engine, select, Session
from sqlalchemy.sql.operators import is_, is_not
from buffered_logger import BufferedLogger
import progressbar

input_people = True
input_orgs = True
input_person_memberships = True
input_org_memberships = True
input_person_person_comms = True
input_person_org_comms = True
input_org_org_comms = True
input_person_person_funding = True
input_person_org_funding = True
input_org_org_funding = True

db_host = "localhost"  # "192.168.0.10"
db_name = "lq_test"  # "collide"
db_user = "test_user"
db_pw = "change_this"

engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pw}@{db_host}/{db_name}", echo=False
)
sess = Session(engine)

db = Memgraph(host="localhost", port=7687)


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


# class MGBill(Node, db=db):


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
    party_1: Optional[int] = Field(exists=True)
    party_2: Optional[int] = Field(exists=True)
    com_date: Optional[date] = Field(exists=True)
    topic: Optional[str] = Field()
    source: Optional[int] = Field(exists=True)


class MGFunding(Relationship, type="FUNDS"):
    id: Optional[int] = Field(exists=True)
    party_1: Optional[int] = Field(exists=True)
    party_2: Optional[int] = Field(exists=True)
    amount: Optional[int] = Field(exist=True)
    start_date: Optional[date] = Field(exists=True)
    end_date: Optional[date] = Field()
    source: Optional[int] = Field(exists=True)


if __name__ == "__main__":
    blogger = BufferedLogger(
        "", "memgraph_log.log", log_to_file=True, log_to_stream=True
    )

    # only nodes in the graph are going to be people and orgs, so read in the list of each of those and populate
    if input_people:
        blogger("people nodes")
        sq = select(Person)
        all_people = sess.exec(sq)
        for p in progressbar.progressbar(all_people):
            try:
                n = MGPerson(
                    id=p.id,
                    display_name=p.display_name,
                    match_name=p.match_name,
                    source=p.source,
                ).save(db)
            except mgclient.DatabaseError as e:
                try:
                    n = MGPerson(
                        id=p.id,
                        display_name=unidecode(p.display_name),
                        match_name=p.match_name,
                        source=p.source,
                    ).save(db)
                except Exception as e:
                    raise e
            except Exception as e:
                blogger(p)
                blogger(e)
        blogger("people entered")
    else:
        blogger("skipping person node entry")

    if input_orgs:
        blogger("org nodes")
        sq = (
            select(Organization, OrganizationType, SectorIndustry)
            .join(OrganizationType, isouter=True)
            .join(SectorIndustry, isouter=True)
        )
        all_orgs = sess.exec(sq)
        for r in progressbar.progressbar(all_orgs):
            o, t, s = r
            try:
                if o.sector is not None:
                    if s.industry_display_name is not None:
                        n = MGOrganization(
                            id=o.id,
                            display_name=o.display_name,
                            match_name=o.match_name,
                            organization_type=t.display_name,
                            sector=s.sector_display_name,
                            industry=s.industry_display_name,
                            source=o.source,
                            misc_data=json.dumps(o.misc_data),
                        ).save(db)
                    else:
                        n = MGOrganization(
                            id=o.id,
                            display_name=o.display_name,
                            match_name=o.match_name,
                            organization_type=t.display_name,
                            sector=s.sector_display_name,
                            source=o.source,
                            misc_data=json.dumps(o.misc_data),
                        ).save(db)
                else:
                    n = MGOrganization(
                        id=o.id,
                        display_name=o.display_name,
                        match_name=o.match_name,
                        organization_type=t.display_name,
                        source=o.source,
                        misc_data=json.dumps(o.misc_data),
                    ).save(db)
            except Exception as e:
                blogger(o)
                blogger(e)
        blogger("orgs entered")
    else:
        blogger("skipping node org entry")

    # all of the different tables for the different perms and coms of communications, funding and memberships need to be mapped to the 3 relationships we have in this graph

    if input_org_memberships:
        blogger("entering organization parent/child relationships")
        sq = select(Organization).where(is_not(Organization.parent_organization, None))
        orgs_with_parents = sess.exec(sq)
        for o in progressbar.progressbar(orgs_with_parents):
            try:
                child = MGOrganization(id=o.id).load(db=db)
                parent = MGOrganization(id=o.parent_organization).load(db=db)
                om = MGMembership(
                    _start_node_id=child._id,
                    _end_node_id=parent._id,
                    source=child.source,
                ).save(db=db)
            except Exception as e:
                blogger(o)
                blogger(e)

        blogger("organization parent/child orgs entered")
    else:
        blogger("skipping org/org memberships")

    if input_person_memberships:
        blogger("entering person/org memberships")
        sq = select(OrganizationMembership)
        person_memberships = sess.exec(sq)
        for mem in progressbar.progressbar(person_memberships):
            try:
                p = MGPerson(id=mem.person).load(db=db)
                o = MGOrganization(id=mem.organization).load(db=db)

                om = MGMembership(
                    _start_node_id=p._id,
                    _end_node_id=o._id,
                    start_date=mem.start_date,
                    end_date=mem.end_date,
                    source=mem.source,
                    id=mem.id,
                ).save(db=db)
            except Exception as e:
                blogger(mem)
                blogger(e)
        blogger("person/org memberships entered")
    else:
        blogger("skipping person/org memberships")

    if input_person_person_comms:
        blogger("entering person/person communications")
        sq = select(Communications, CommsTopic).join(CommsTopic, isouter=True)
        person_person_comms = sess.exec(sq)
        for r in progressbar.progressbar(person_person_comms):
            c, t = r
            try:
                p1 = MGPerson(id=c.party_1).load(db=db)
                p2 = MGPerson(id=c.party_2).load(db=db)

                if c.topic is not None:
                    mc = MGCommunications(
                        _start_node_id=p1._id,
                        _end_node_id=p2._id,
                        id=c.id,
                        party_1=c.party_1,
                        party_2=c.party_2,
                        com_date=c.com_date,
                        topic=t.display_name,
                        source=c.source,
                    ).save(db=db)
                else:
                    mc = MGCommunications(
                        _start_node_id=p1._id,
                        _end_node_id=p2._id,
                        id=c.id,
                        party_1=c.party_1,
                        party_2=c.party_2,
                        com_date=c.com_date,
                        source=c.source,
                    ).save(db=db)

            except Exception as e:
                blogger(c)
                blogger(e)

        blogger("person/person communications entered")
    else:
        blogger("skipping person/person communications")

    if input_person_org_comms:
        blogger("entering person/org communications")
        sq = select(CommunicationsPersonOrg, CommsTopic).join(CommsTopic, isouter=True)
        person_org_comms = sess.exec(sq)
        for r in progressbar.progressbar(person_org_comms):
            c, t = r
            try:
                p = MGPerson(id=c.person).load(db=db)
                o = MGOrganization(id=c.organization).load(db=db)

                if c.topic is not None:
                    mc = MGCommunications(
                        _start_node_id=p._id,
                        _end_node_id=o._id,
                        party_1=c.person,
                        party_2=c.organization,
                        com_date=c.com_date,
                        topic=t.display_name,
                        source=c.source,
                        id=c.id,
                    ).save(db=db)
                else:
                    mc = MGCommunications(
                        _start_node_id=p._id,
                        _end_node_id=o._id,
                        party_1=c.person,
                        party_2=c.organization,
                        com_date=c.com_date,
                        topic=t.display_name,
                        source=c.source,
                        id=c.id,
                    ).save(db=db)
            except Exception as e:
                blogger(c)
                blogger(e)

        blogger("person org communications entered")
    else:
        blogger("skipping person/org communications")

    if input_org_org_comms:
        blogger("entering org/org communications")
        sq = select(CommunicationsOrgOrg, CommsTopic).join(CommsTopic, isouter=True)
        org_org_comms = sess.exec(sq)
        for r in org_org_comms:
            c, t = r
            try:
                p1 = MGOrganization(id=c.party_1).load(db=db)
                p2 = MGOrganization(id=c.party_2).load(db=db)

                if c.topic is not None:
                    mc = MGCommunications(
                        _start_node_id=p1._id,
                        _end_node_id=p2._id,
                        party_1=c.party_1,
                        party_2=c.party_2,
                        com_date=c.com_date,
                        topic=t.display_name,
                        source=c.source,
                    ).save(db=db)
                else:
                    mc = MGCommunications(
                        _start_node_id=p1._id,
                        _end_node_id=p2._id,
                        party_1=c.party_1,
                        party_2=c.party_2,
                        com_date=c.com_date,
                        source=c.source,
                    ).save(db=db)

            except Exception as e:
                blogger(c)
                blogger(e)

        blogger("org/org communications entered")
    else:
        blogger("skipping org/org communications")

    if input_person_person_funding:
        blogger("entering person/person funding")
        sq = select(FundingPersonPerson)
        person_person_funding = sess.exec(sq)
        for f in progressbar.progressbar(person_person_funding):
            try:
                p1 = MGPerson(id=f.party_1).load(db=db)
                p2 = MGPerson(id=f.party_2).load(db=db)

                if f.amount > 0:
                    mf = MGFunding(
                        _start_node_id=p1._id,
                        _end_node_id=p2._id,
                        party_1=f.party_1,
                        party_2=f.party_2,
                        amount=f.amount,
                        start_date=f.start_date,
                        end_date=f.end_date,
                        source=f.source,
                        id=f.id,
                    ).save(db=db)
                else:
                    mf = MGFunding(
                        _start_node_id=p2._id,
                        _end_node_id=p1._id,
                        party_1=f.party_2,
                        party_2=f.party_1,
                        amount=-1 * f.amount,
                        start_date=f.start_date,
                        end_date=f.end_date,
                        source=f.source,
                        id=f.id,
                    ).save(db=db)
            except Exception as e:
                blogger(f)
                blogger(e)

        blogger("person to person fundings entered")
    else:
        blogger("skipping person/person funding")

    if input_person_org_funding:
        blogger("entering person/org funding")
        sq = select(FundingPersonOrg)
        person_person_funding = sess.exec(sq)
        for f in progressbar.progressbar(person_person_funding):
            try:
                p = MGPerson(id=f.person).load(db=db)
                o = MGOrganization(id=f.organization).load(db=db)

                if f.amount > 0:
                    mf = MGFunding(
                        _start_node_id=p._id,
                        _end_node_id=o._id,
                        party_1=f.person,
                        party_2=f.organization,
                        amount=f.amount,
                        start_date=f.start_date,
                        end_date=f.end_date,
                        source=f.source,
                        id=f.id,
                    ).save(db=db)
                else:
                    mf = MGFunding(
                        _start_node_id=o._id,
                        _end_node_id=p._id,
                        party_1=f.organization,
                        party_2=f.person,
                        amount=-1 * f.amount,
                        start_date=f.start_date,
                        end_date=f.end_date,
                        source=f.source,
                        id=f.id,
                    ).save(db=db)
            except Exception as e:
                blogger(f)
                blogger(e)
        blogger("person/org funding entered")
    else:
        blogger("skipping person/org funding")

    if input_org_org_funding:
        blogger("entering org/org funding")
        sq = select(Funding)
        person_person_funding = sess.exec(sq)
        for f in progressbar.progressbar(person_person_funding):
            try:
                p1 = MGPerson(id=f.party_1).load(db=db)
                p2 = MGPerson(id=f.party_2).load(db=db)

                if f.amount > 0:
                    mf = MGFunding(
                        _start_node_id=p1._id,
                        _end_node_id=p2._id,
                        party_1=f.party_1,
                        party_2=f.party_2,
                        amount=f.amount,
                        start_date=f.start_date,
                        end_date=f.end_date,
                        source=f.source,
                        id=f.id,
                    ).save(db=db)
                else:
                    mf = MGFunding(
                        _start_node_id=p2._id,
                        _end_node_id=p1._id,
                        party_1=f.party_2,
                        party_2=f.party_1,
                        amount=-1 * f.amount,
                        start_date=f.start_date,
                        end_date=f.end_date,
                        source=f.source,
                        id=f.id,
                    ).save(db=db)
            except Exception as e:
                blogger(f)
                blogger(e)
        blogger("org/org funding entered")
    else:
        blogger("skipping org/org funding")

    sess.close()
