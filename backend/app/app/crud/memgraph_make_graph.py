from datetime import date
from typing import Optional
from app import schemas
import networkx as nx
from gqlalchemy import Field, Memgraph, Node, Relationship

from app.core.config import settings

# gdb = Memgraph(host="memgraph-platform", port=7687)
gdb = Memgraph(host=settings.MEMGRAPH_HOST, port=settings.MEMGRAPH_PORT)


class MGPerson(Node, index=True, db=gdb):
    id: Optional[int] = Field(index=True, exists=True, unique=True, db=gdb)
    display_name: Optional[str] = Field(unique=True)
    match_name: Optional[str] = Field(index=True, unique=True)
    source: Optional[int] = Field(exists=True)


class MGOrganization(Node, index=True, db=gdb):
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


def mapped_memgraph_to_nx(res_dict):
    g = nx.MultiDiGraph()

    nodes = res_dict["nodes"]
    edges = res_dict["edges"]
    node_dict = {x.id: x for x in nodes}

    early_date = date(2100, 1, 1)
    late_date = date(1900, 1, 1)

    for n in nodes:

        if "MGPerson" in n.labels:
            n_val = 3
            n_sec = None
        else:
            n_val = 8
        lbl = list(n.labels)[0]
        lbl = lbl.replace("MG", "")

        g.add_node(
            n.properties["match_name"],
            display_name=n.properties["display_name"],
            type=lbl,
            value=n_val,
        )

    for e in edges:
        if e.type == "COMMUNICATION":
            g.add_edge(
                node_dict[e.start_id].properties["match_name"],
                node_dict[e.end_id].properties["match_name"],
                type=e.type,
                date=e.properties["com_date"],
                amount=1,
                dash=[2, 3],
                color="red",
            )
        elif e.type == "FUNDS":
            g.add_edge(
                node_dict[e.start_id].properties["match_name"],
                node_dict[e.end_id].properties["match_name"],
                type=e.type,
                start_date=e.properties["start_date"],
                end_date=e.properties["end_date"],
                amount=e.properties["amount"],
                dash=[2, 3],
                color="green",
            )
        else:

            g.add_edge(
                node_dict[e.start_id].properties["match_name"],
                node_dict[e.end_id].properties["match_name"],
                start_date=e.properties.get("start_date", early_date),
                end_date=e.properties.get("end_date", late_date),
                type=e.type,
                color="black",
                amount=1,
                dash=[0, 0],
            )

    return g


def nx_to_json(g):
    # convert to json
    nodes = []
    links = []
    for n, d in g.nodes.items():
        nodes.append(
            {"id": n, "name": d["display_name"], "type": d["type"], "val": d["value"]}
        )

    for e, d in g.edges.items():
        comn = {"source": e[0], "target": e[1], "type": d["type"], "color": d["color"]}

        if "dash" in d:
            comn["dash"] = d["dash"]
        if "amount" in d:
            comn["amount"] = d["amount"]
        links.append(comn)

    graph = {"nodes": nodes, "links": links}
    return graph


def filter_edge_by_type(e, e_type):
    return {k: d for k, d in e.items() if d["type"] == e_type}


def adj_edge_summary(adj_of_node):
    edge_summary = []
    for trg, d in adj_of_node.items():
        for k, prop in d.items():
            edge_summary.append((trg, prop["type"]))

    return frozenset(edge_summary)


def aggregate_parallel_edges(g):
    adj_mat = nx.convert.to_dict_of_dicts(g)

    # TODO add in dash and color saving, save edge ids for the different types then remove consistency checks
    # get parallel edges
    fund_parallel_edge_node_pairs = {"FUNDS": {}, "COMMUNICATION": {}, "MEMBERSHIP": {}}
    for src in adj_mat.keys():
        if len(adj_mat[src]) > 0:
            for dst in adj_mat[src].keys():
                if len(adj_mat[src][dst]) > 1:  # this will be the parallel edge

                    for e_type in fund_parallel_edge_node_pairs.keys():

                        filtered_adjacency = filter_edge_by_type(
                            adj_mat[src][dst], e_type
                        )

                        if len(filtered_adjacency) <= 1:
                            continue

                        k = (src, dst)
                        if k not in fund_parallel_edge_node_pairs[e_type].keys():
                            fund_parallel_edge_node_pairs[e_type][k] = {
                                "amount": 0,
                                "e_keys": [],
                                "dash": None,
                                "color": None,
                            }

                        early_date = date(2100, 1, 1)
                        late_date = date(1900, 1, 1)
                        for r in filtered_adjacency.keys():
                            fund_parallel_edge_node_pairs[e_type][k][
                                "amount"
                            ] += filtered_adjacency[r]["amount"]
                            fund_parallel_edge_node_pairs[e_type][k]["e_keys"].append(r)
                            fund_parallel_edge_node_pairs[e_type][k][
                                "dash"
                            ] = filtered_adjacency[r]["dash"]
                            fund_parallel_edge_node_pairs[e_type][k][
                                "color"
                            ] = filtered_adjacency[r]["color"]

                            if "com_date" in filtered_adjacency[r].keys():
                                if filtered_adjacency[r]["com_date"] < early_date:
                                    early_date = filtered_adjacency[r]["com_date"]
                                if filtered_adjacency[r]["com_date"] > late_date:
                                    late_date = filtered_adjacency[r]["com_date"]

                            elif "start_date" in filtered_adjacency[r].keys():
                                sd = filtered_adjacency[r]["start_date"]
                                ed = filtered_adjacency[r].get("end_date", sd)
                                # TODO optimize order
                                if sd < early_date:
                                    early_date = sd
                                elif sd > late_date:
                                    late_date = sd
                                if ed < early_date:
                                    early_date = ed
                                elif ed > late_date:
                                    late_date = ed

                            fund_parallel_edge_node_pairs[e_type][k][
                                "start_date"
                            ] = early_date
                            fund_parallel_edge_node_pairs[e_type][k][
                                "end_date"
                            ] = late_date

    # merge the parallel edges
    for e_type in fund_parallel_edge_node_pairs.keys():
        for k in fund_parallel_edge_node_pairs[e_type].keys():

            # create the data for the new edge
            new_edge = {
                "type": e_type,
                "dash": fund_parallel_edge_node_pairs[e_type][k]["dash"],
                "color": fund_parallel_edge_node_pairs[e_type][k]["color"],
                "amount": fund_parallel_edge_node_pairs[e_type][k]["amount"],
                "start_date": fund_parallel_edge_node_pairs[e_type][k]["start_date"],
                "end_date": fund_parallel_edge_node_pairs[e_type][k]["end_date"],
            }

            # remove all the old edges
            for e in list(fund_parallel_edge_node_pairs[e_type][k]["e_keys"]):
                g.remove_edge(k[0], k[1], e)

            # add in the new edge
            g.add_edge(k[0], k[1], key=None, **new_edge)

    return g


def aggregate_leaves(g, label, threshold):
    fund_degrees = nx.degree(g)
    # get all of the people that just fund
    funding_leaves = [x[0] for x in fund_degrees if x[1] == 1]
    all_degrees = {x[0]: x[1] for x in fund_degrees}

    funding_totals = {}
    leaf_agg_count = {}
    early_date = date(2100, 1, 1)
    late_date = date(1900, 1, 1)
    for (
        leaf
    ) in funding_leaves:  # these are leaves, so they will only ever have one target
        if len(list(g.adj[leaf].keys())) == 0:
            continue

        trg = list(g.adj[leaf].keys())[0]

        if all_degrees[trg] < threshold:
            continue

        edges = g.adj[leaf][trg]
        if len(edges) != 1:
            raise RuntimeError("working on a node that isn't actually a leaf")
        edges = edges[0]

        e_type = edges["type"]
        dash = edges["dash"]
        color = edges["color"]
        amount = edges["amount"]
        if "com_date" in edges.keys():
            sd = edges["com_date"]
            ed = edges["com_date"]
        elif "start_date" in edges.keys():
            sd = edges["start_date"]
            ed = edges["end_date"]
        else:
            sd = date(1900, 1, 1)
            ed = date(1900, 1, 1)

        if trg not in funding_totals.keys():
            funding_totals[trg] = {
                "amount": 0,
                "start_date": sd,
                "end_date": ed,
                "type": e_type,
                "dash": dash,
                "color": color,
            }
            leaf_agg_count[trg] = 0

        # check type, dash and color for consistency
        ft_e_type = funding_totals[trg]["type"]
        ft_dash = funding_totals[trg]["dash"]
        ft_color = funding_totals[trg]["color"]

        if e_type != ft_e_type or dash != ft_dash or color != ft_color:
            continue

        ft_sd = funding_totals[trg]["start_date"]
        ft_ed = funding_totals[trg]["end_date"]

        if sd < ft_sd:
            funding_totals[trg]["start_date"] = sd
        if ed > ft_ed:
            funding_totals[trg]["end_date"] = ed

        funding_totals[trg]["amount"] += amount
        leaf_agg_count[trg] += 1

        # we have aggregated this leaf, so remove it
        g.remove_node(leaf)

    for k in funding_totals.keys():
        new_mn = f"{k}_{e_type}_agg"
        new_dn = f"{label} ({leaf_agg_count[k]})"
        g.add_node(new_mn, display_name=new_dn, type="MGPerson", value=3)
        g.add_edge(new_mn, f"{k}", **funding_totals[k])

    return g


def aggregate_same_edges(g, label, threshold, **kwargs):
    # we want to get a list of lists
    # each sublist should contain the nodes that have all the same edges, type shouldn't really factor in here, else we
    # will have to handle splitting out nodes wrt one type and aggregating them in another
    # this operation should be run after all of the different subgraphs have been combined
    edges = {}

    object_of_interest = kwargs.pop("object_of_interest_mn", None)
    node_type = kwargs.pop("node_type", "Person")
    if node_type == "Person":
        n_val = 3
    else:
        n_val = 8

    node_list = list(g.nodes)
    if object_of_interest is not None:
        node_list = [
            x for x in node_list if x != object_of_interest
        ]  # never aggregate the object of interest

    tg = nx.to_undirected(g)
    for n in node_list:
        if g.nodes[n]["type"] == node_type:
            edges[n] = adj_edge_summary(tg.adj[n])

    non_empty_sets = {n: s for n, s in edges.items() if len(s) > 0}
    unique_combinations = list(set([s for n, s in non_empty_sets.items()]))

    binned_nodes = {
        i: [n for n, s in non_empty_sets.items() if s == uc]
        for i, uc in enumerate(unique_combinations)
    }
    binned_nodes = {i: s for i, s in binned_nodes.items() if len(s) > threshold}

    for i, j in binned_nodes.items():

        if len(j) > threshold:
            # merge these nodes

            targets_and_types = unique_combinations[i]

            new_mn = f"{hash(targets_and_types)}_agg"
            new_dn = f"{label} ({len(j)})"
            g.add_node(new_mn, display_name=new_dn, type=node_type, value=n_val)

            for tt in targets_and_types:
                trg = tt[0]
                e_type = tt[1]
                early_date = date(2100, 1, 1)
                late_date = date(1900, 1, 1)
                amount = 0
                dash = None
                color = None

                for src in j:
                    try:
                        fish = g.adj[src][trg]
                    except KeyError:
                        fish = g.pred[src][trg]
                    fish = filter_edge_by_type(fish, e_type)

                    for q in fish.keys():

                        if fish[q]["start_date"] < early_date:
                            early_date = fish[q]["start_date"]
                        if fish[q]["end_date"] > late_date:
                            late_date = fish[q]["end_date"]
                        dash = fish[q]["dash"]
                        color = fish[q]["color"]
                        amount += fish[q]["amount"]

                summ = {
                    "start_date": early_date,
                    "end_date": late_date,
                    "type": e_type,
                    "dash": dash,
                    "color": color,
                    "amount": amount,
                }
                g.add_edge(new_mn, f"{trg}", **summ)
                # remov nodes
            for src in j:
                g.remove_node(src)

    return g


def create_tot_graph(m_g, f_g, c_g):
    t_graph = nx.MultiDiGraph()

    t_graph.add_nodes_from(f_g.nodes(data=True))
    t_graph.add_edges_from(f_g.edges(data=True))

    t_graph.add_nodes_from(m_g.nodes(data=True))
    t_graph.add_edges_from(m_g.edges(data=True))

    t_graph.add_nodes_from(c_g.nodes(data=True))
    t_graph.add_edges_from(c_g.edges(data=True))

    return t_graph


def memgraph_query_and_aggregate(
    poi_mn: str,
    is_person: bool,
    fund_depth: int,
    membership_depth: int,
    communication_depth: int,
    target_max_nodes: int = 300,
    start_agg_threshold: int = 80,
    aggregation_threshold_step: int = 5,
    verbose=False,
    # log_file=None,
) -> dict:
    """

    Parameters
    ----------
    poi_mn: str
            person (or org) of interest match name.  This is the starting point for the graph search
    is_person: bool
            flag denoting whether the poi_mn is from a person or an org
    fund_depth: int
            this is the number of hops to traverse the graph with respect to funding.  The initial hop only considers
            the FUNDING relationship, and the subsequent hops consider FUNDING and MEMBERSHIP, to try and capture the
            memberships of any funding sources
    membership_depth: int
            see fund_depth
    communication_depth: int
            see fund_depth
    target_max_nodes: int
            this is the number of nodes that all the aggregation is shooting for, i.e. aggregations are done until
            we are at or below this number, or we can't do any more
    start_agg_threshold: int
            this the threshold over which we start to aggregate things.  It is gradually lowered after successive
            aggregations, trying to get the total nodes under target_max_nodes
    aggregation_threshold_step: int
            this is the amount that start_agg_threshold is reduced by during successive aggregation steps.  Higher
            values will make the process go faster, but may end up overdoing the aggregation
    verbose: bool
            whether or not to print things to stdout or not
    log_file: filepath or None
            if not none, write logs to a file
    Returns
    -------
    dict
        dictionary of nodes and edges that is compatible with json, and can be saved or passed directly (unsure what
        this will need to look like for the integration with the frontend)

    """

    some_letters = ("r", "s", "t", "u", "v", "w", "x", "y", "z")

    if is_person:
        type_tag = "Person"
    else:
        type_tag = "Organization"

    json_file_name = f"generated_json/{poi_mn}_m{membership_depth}_c{communication_depth}_f{fund_depth}.json"
    if verbose:
        print(json_file_name)

    query_funds_line_1 = (
        f'MATCH p=(n: MG{type_tag} {{match_name: "{poi_mn}"}}) - [l:FUNDS *..1] - (m)'
    )
    query_membership_line_1 = f'MATCH p=(n: MG{type_tag} {{match_name: "{poi_mn}"}}) - [l:MEMBERSHIP *..1] - (m)'
    query_communications_line_1 = f'MATCH p=(n: MG{type_tag} {{match_name: "{poi_mn}"}}) - [l:COMMUNICATION *..1] - (m)'

    query_last_lines = ["with project(p) as f", "return f"]

    for i in range(0, fund_depth - 1):
        query_funds_line_1 += f" - [{some_letters[2 * i]}:FUNDS|MEMBERSHIP *..1] - ({some_letters[2 * i + 1]})"

    for i in range(0, communication_depth - 1):
        query_communications_line_1 += f" - [{some_letters[2 * i]}:COMMUNICATION|MEMBERSHIP *..1] - ({some_letters[2 * i + 1]})"

    for i in range(0, membership_depth - 1):
        query_membership_line_1 += (
            f" - [{some_letters[2 * i]}:MEMBERSHIP *..1] - ({some_letters[2 * i + 1]})"
        )

    query_funds = "\n".join([query_funds_line_1] + query_last_lines)
    query_communication = "\n".join([query_communications_line_1] + query_last_lines)
    query_membership = "\n".join([query_membership_line_1] + query_last_lines)

    if fund_depth > 0:
        funding_res = gdb.execute_and_fetch(query_funds)
        funding_res = list(funding_res)[0]["f"]
        fund_g = mapped_memgraph_to_nx(funding_res)
    else:
        fund_g = nx.MultiDiGraph()

    if membership_depth > 0:
        membership_res = gdb.execute_and_fetch(query_membership)
        membership_res = list(membership_res)[0]["f"]
        membership_g = mapped_memgraph_to_nx(membership_res)
    else:
        membership_g = nx.MultiDiGraph()

    if communication_depth > 0:
        communication_res = gdb.execute_and_fetch(query_communication)
        communication_res = list(communication_res)[0]["f"]
        communication_g = mapped_memgraph_to_nx(communication_res)
    else:
        communication_g = nx.MultiDiGraph()

    # these two reductions just make more sense, so always do them
    fund_g = aggregate_parallel_edges(fund_g)
    communication_g = aggregate_parallel_edges(communication_g)

    # just ignore any overlap between these subgraphs for now
    nn_f = nx.number_of_nodes(fund_g)
    nn_m = nx.number_of_nodes(membership_g)
    nn_c = nx.number_of_nodes(communication_g)
    tot_nodes = nn_f + nn_m + nn_c

    temp_tot_graph = create_tot_graph(membership_g, fund_g, communication_g)
    if verbose:
        print(f"total nodes in {nx.number_of_nodes(temp_tot_graph)}")
        print(f"total edges in {nx.number_of_edges(temp_tot_graph)}")

    reductions = []
    brk = False

    temp_fund_g = fund_g.copy(as_view=False)
    temp_membership_g = membership_g.copy(as_view=False)
    temp_communication_g = communication_g.copy(as_view=False)
    agg_threshold = start_agg_threshold

    while tot_nodes > target_max_nodes and not brk:

        if "aggregate_fund_leaves" not in reductions:
            temp_fund_g = aggregate_leaves(temp_fund_g, "Misc Donors", 0)
            reductions.append("aggregate_fund_leaves")
            tot_nodes -= nn_f
            nn_f = nx.number_of_nodes(temp_fund_g)
            tot_nodes += nn_f
            continue

        if ("aggregate_membership_leaves", agg_threshold) not in reductions:
            temp_membership_g = membership_g.copy(as_view=False)
            temp_membership_g = aggregate_leaves(
                temp_membership_g, "Other Members", agg_threshold
            )
            reductions.append(("aggregate_membership_leaves", agg_threshold))
            tot_nodes -= nn_m
            nn_m = nx.number_of_nodes(temp_membership_g)
            tot_nodes += nn_m
            continue

        if ("aggregate_communication_leaves", agg_threshold) not in reductions:
            temp_communication_g = communication_g.copy(as_view=False)
            temp_communication_g = aggregate_leaves(
                temp_communication_g, "Other Parties", agg_threshold
            )
            reductions.append(("aggregate_communication_leaves", agg_threshold))
            tot_nodes -= nn_c
            nn_c = nx.number_of_nodes(temp_communication_g)
            tot_nodes += nn_c
            continue

        if ("aggregate_same_edges", agg_threshold) not in reductions:

            if ("aggregate_same_edges_person", agg_threshold) not in reductions:
                temp_tot_graph = create_tot_graph(
                    temp_membership_g, temp_fund_g, temp_communication_g
                )

                temp_tot_graph = aggregate_same_edges(
                    temp_tot_graph,
                    "Other Parties",
                    agg_threshold,
                    object_of_interest_mn=poi_mn,
                    node_type="Person",
                )
                tot_nodes = nx.number_of_nodes(temp_tot_graph)
                reductions.append(("aggregate_same_edges_person", agg_threshold))
                continue

            if (
                "aggregate_same_edges_organizations",
                agg_threshold,
            ) not in reductions:
                temp_tot_graph = aggregate_same_edges(
                    temp_tot_graph,
                    "Other Orgs",
                    agg_threshold,
                    object_of_interest_mn=poi_mn,
                    node_type="Organization",
                )
                tot_nodes = nx.number_of_nodes(temp_tot_graph)
                reductions.append(("aggregate_same_edges_organizations", agg_threshold))
                continue
            reductions.append(("aggregate_same_edges", agg_threshold))

        agg_threshold -= aggregation_threshold_step
        if agg_threshold <= 1:
            brk = True

    fund_g = temp_fund_g
    membership_g = temp_membership_g
    communication_g = temp_communication_g

    # tot_graph = create_tot_graph(membership_g, fund_g, communication_g)
    tot_graph = temp_tot_graph

    graph_json = nx_to_json(tot_graph)

    if verbose:
        print(f"total nodes out {nx.number_of_nodes(tot_graph)}")
        print(f"total edges out {nx.number_of_edges(tot_graph)}")

    # with open(json_file_name, "w") as h:
    #     json.dump(graph_json, h, indent=4)

    # with open("sample_graph4.json", "w") as h:
    #     json.dump(graph_json, h, indent=4)

    if verbose:
        print("done")

    return graph_json


def graph_search_options(search: str) -> list[schemas.GraphSearchOptions]:

    peeps = []
    # orgs = set()

    query = f"""
    MATCH (n:MGPerson) WHERE n.match_name CONTAINS toLower("{search}") RETURN n.display_name LIMIT 10;
    """

    res = gdb.execute_and_fetch(query)

    # for org in all_organizations:
    #     orgs.append(org["o"].display_name)

    for person in res:
        label = person["n.display_name"]
        print(label)
        value = label.lower().replace(" ", "")
        print(value)
        options = {
            # TODO remove value and build it in the front end
            "value": value,
            "label": label,
        }

        peeps.append(options)

    return peeps
