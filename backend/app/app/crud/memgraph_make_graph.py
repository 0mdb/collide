from datetime import date
from app import schemas
import networkx as nx
import cProfile, pstats, io
from pstats import SortKey
import mgclient

from app.core.config import settings

conn = mgclient.connect(host="memgraph-platform", port=7687)


def fetch_and_map(inputs):
    tag = inputs[0]
    poi_mn = inputs[1]
    query = inputs[2]
    connection = inputs[3]

    cursor = connection.cursor()
    cursor.execute(query, {"poi_mn": poi_mn})
    res = cursor.fetchall()
    cursor.close()
    res = list(res)[0][0]
    graph_out = mapped_memgraph_to_nx(res)
    return tag, graph_out


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
                start_date=e.properties["com_date"],
                end_date=e.properties["com_date"],
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
            {"id": n, "name": d["display_name"], "type": d["type"], "value": d["value"]}
        )

    for e, d in g.edges.items():
        comn = {"source": e[0], "target": e[1], "type": d["type"], "linkColor": d["color"]}

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


def aggregate_leaves(g, label, threshold, edge_type, object_of_interest=None):
    fund_degrees = nx.degree(g)
    # get all of the people that just fund
    if object_of_interest is None:
        funding_leaves = [x[0] for x in fund_degrees if x[1] == 1]
    else:  # don't aggregate the object_of_interest
        funding_leaves = [
            x[0] for x in fund_degrees if x[1] == 1 and x[0] != object_of_interest
        ]
    all_degrees = {x[0]: x[1] for x in fund_degrees}

    funding_totals = {}
    leaf_agg_count = {}
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
        if edges["type"] != edge_type:
            continue

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
    non_empty_sets = {}

    object_of_interest = kwargs.pop("object_of_interest_mn", None)
    node_type = kwargs.pop("node_type", "Person")
    if node_type == "Person":
        n_val = 3
    else:
        n_val = 8

    node_list = set(g.nodes)
    if object_of_interest is not None:
        node_list.discard(object_of_interest)  # never aggregate the object of interest

    tg = nx.to_undirected(g)
    unique_combinations = set()
    binned_nodes = {}
    for n in node_list:
        if g.nodes[n]["type"] == node_type:
            es = adj_edge_summary(tg.adj[n])
            if len(es) > 0:
                non_empty_sets[n] = es
                unique_combinations.add(es)
                if es in binned_nodes.keys():
                    binned_nodes[es]["nodes"].append(n)
                    binned_nodes[es]["count"] += 1
                else:
                    binned_nodes[es] = {"nodes": [n], "count": 1}

    binned_nodes = {n: x for n, x in binned_nodes.items() if x["count"] > threshold}

    for uc, j in binned_nodes.items():

        targets_and_types = uc

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

            for src in j["nodes"]:
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
        for src in j["nodes"]:
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
        fund_depth: int,
        membership_depth: int,
        communication_depth: int,
        target_max_nodes: int = 300,
        start_agg_threshold: int = 80,
        aggregation_threshold_step: int = 5,
        verbose=False,
        profile=False,
        # log_file=None,
) -> dict:
    """

    Parameters
    ----------
    poi_mn: str
            person (or org) of interest match name.  This is the starting point for the graph search
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
            whether to print things to stdout or not
    log_file: filepath or None
            if not none, write logs to a file
    Returns
    -------
    dict
        dictionary of nodes and edges that is compatible with json, and can be saved or passed directly (unsure what
        this will need to look like for the integration with the frontend)

    """

    some_letters = ("r", "s", "t", "u", "v", "w", "x", "y", "z")

    cursor = conn.cursor()
    gql = f"""MATCH (n) WHERE n.match_name = $poi_mn
                    RETURN n"""
    cursor.execute(gql, {"poi_mn": poi_mn})
    poi_type = cursor.fetchone()
    poi_type = poi_type[0].labels.pop()
    type_tag = poi_type.replace("MG", "")

    if profile:
        pr = cProfile.Profile()
        pr.enable()

    json_file_name = f"generated_json/{poi_mn}_m{membership_depth}_c{communication_depth}_f{fund_depth}.json"
    if verbose:
        print(json_file_name)

    query_funds_line_1 = (
        f"MATCH p=(n: MG{type_tag} {{match_name: $poi_mn}}) - [l:FUNDS *..1] - (m)"
    )
    query_membership_line_1 = (
        f"MATCH p=(n: MG{type_tag} {{match_name: $poi_mn}}) - [l:MEMBERSHIP *..1] - (m)"
    )
    query_communications_line_1 = f"MATCH p=(n: MG{type_tag} {{match_name: $poi_mn}}) - [l:COMMUNICATION *..1] - (m)"

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

    concurrent_inputs = []
    all_graphs = {}
    if fund_depth > 0:
        concurrent_inputs.append(("fund_g", poi_mn, query_funds, conn))
    else:
        all_graphs["fund_g"] = nx.MultiDiGraph()

    if membership_depth > 0:
        concurrent_inputs.append(("membership_g", poi_mn, query_membership, conn))
    else:
        all_graphs["membership_g"] = nx.MultiDiGraph()

    if communication_depth > 0:
        concurrent_inputs.append(("communication_g", poi_mn, query_communication, conn))
    else:
        all_graphs["communication_g"] = nx.MultiDiGraph()

    cursor.close()

    # doing this concurrently seems to just make things slower
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #    for t, g in executor.map(fetch_and_map, concurrent_inputs):
    for i in concurrent_inputs:
        t, g = fetch_and_map(i)
        all_graphs[t] = g

    # unpack
    fund_g = all_graphs["fund_g"]
    membership_g = all_graphs["membership_g"]
    communication_g = all_graphs["communication_g"]

    # these two reductions just make more sense, so always do them
    fund_g = aggregate_parallel_edges(fund_g)
    communication_g = aggregate_parallel_edges(communication_g)

    tot_graph = create_tot_graph(membership_g, fund_g, communication_g)
    tot_nodes = nx.number_of_nodes(tot_graph)
    tot_edges = nx.number_of_edges(tot_graph)
    if verbose:
        print(f"total nodes in {tot_nodes}")
        print(f"total edges in {tot_edges}")

    reductions = set()
    brk = False

    agg_threshold = start_agg_threshold

    temp_tot_graph = tot_graph.copy(as_view=False)

    while tot_nodes > target_max_nodes and not brk:

        if ("aggregate_fund_leaves", agg_threshold) not in reductions:
            temp_tot_graph = aggregate_leaves(
                temp_tot_graph,
                "Misc Donors",
                agg_threshold,
                edge_type="FUNDS",
                object_of_interest=poi_mn,
            )
            reductions.add(("aggregate_fund_leaves", agg_threshold))
            tot_nodes = nx.number_of_nodes(temp_tot_graph)
            if verbose:
                print(f'{("aggregate_fund_leaves", agg_threshold)}:')
                print(f"\ttot nodes: {tot_nodes}")
            continue

        if ("aggregate_membership_leaves", agg_threshold) not in reductions:
            temp_tot_graph = aggregate_leaves(
                temp_tot_graph,
                "Other Members",
                agg_threshold,
                edge_type="MEMBERSHIP",
                object_of_interest=poi_mn,
            )
            reductions.add(("aggregate_membership_leaves", agg_threshold))
            tot_nodes = nx.number_of_nodes(temp_tot_graph)
            if verbose:
                print(f'{("aggregate_membership_leaves", agg_threshold)}:')
                print(f"\ttot nodes: {tot_nodes}")
            continue

        if ("aggregate_communication_leaves", agg_threshold) not in reductions:
            temp_tot_graph = aggregate_leaves(
                temp_tot_graph,
                "Other Parties",
                agg_threshold,
                edge_type="COMMUNICATION",
                object_of_interest=poi_mn,
            )
            reductions.add(("aggregate_communication_leaves", agg_threshold))
            tot_nodes = nx.number_of_nodes(temp_tot_graph)
            if verbose:
                print(f'{("aggregate_communication_leaves", agg_threshold)}:')
                print(f"\ttot nodes: {tot_nodes}")
            continue

        if ("aggregate_same_edges", agg_threshold) not in reductions:

            if ("aggregate_same_edges_person", agg_threshold) not in reductions:
                temp_tot_graph = aggregate_same_edges(
                    temp_tot_graph,
                    "Other Parties",
                    agg_threshold,
                    object_of_interest_mn=poi_mn,
                    node_type="Person",
                )
                tot_nodes = nx.number_of_nodes(temp_tot_graph)
                reductions.add(("aggregate_same_edges_person", agg_threshold))
                if verbose:
                    print(f'{("aggregate_same_edges_person", agg_threshold)}:')
                    print(f"\ttot nodes: {tot_nodes}")
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
                reductions.add(("aggregate_same_edges_organizations", agg_threshold))
                if verbose:
                    print(f'{("aggregate_same_edges_organizations", agg_threshold)}:')
                    print(f"\ttot nodes: {tot_nodes}")
                continue
            reductions.add(("aggregate_same_edges", agg_threshold))

        if agg_threshold > 1 and (agg_threshold - aggregation_threshold_step) <= 0:
            agg_threshold = 1
        else:
            agg_threshold -= aggregation_threshold_step
        if agg_threshold <= 1:
            brk = True
        else:
            temp_tot_graph = tot_graph.copy(as_view=False)

    tot_graph = temp_tot_graph

    graph_json = nx_to_json(tot_graph)

    if verbose:
        print(f"total nodes out {nx.number_of_nodes(tot_graph)}")
        print(f"total edges out {nx.number_of_edges(tot_graph)}")

    if profile:
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(poi_mn)
        print(s.getvalue())

    if verbose:
        print("done")

    return graph_json


def graph_search_options(search: str) -> list[schemas.GraphSearchOptions]:
    """Search for people and organizations in the graph database."""

    peeps_and_orgs = []

    # limit responses to 50
    query = f"""
    MATCH (n:MGSearchItem) WHERE n.match_name CONTAINS toLower($search) RETURN n.display_name, n.match_name, n.graph_type, n.bill_match_name LIMIT 50;
    """
    cursor = conn.cursor()
    cursor.execute(query, {"search": search})
    res = cursor.fetchall()

    for person_or_org in res:
        if person_or_org[3] is None:
            bm = 'na'
        else:
            bm = person_or_org[3]

        options = {
            # TODO remove value and build it in the front end
            "value": person_or_org[1],
            "label": person_or_org[0],
            "type": person_or_org[2],
            "bill_match": bm
        }

        peeps_and_orgs.append(options)

    return peeps_and_orgs


def fetch_and_map_bill(inputs):
    tag = inputs[0]
    boi_mn = inputs[1]
    query = inputs[2]
    connection = inputs[3]

    cursor = connection.cursor()
    cursor.execute(query, {"boi_mn": boi_mn})
    res = cursor.fetchall()
    cursor.close()
    res = list(res)[0][0]
    graph_out = mapped_memgraph_bill_to_nx(res, tag)
    return tag, graph_out


def fetch_and_map_votes(inputs):
    tag = inputs[0]
    mn = inputs[1]
    query = inputs[2]
    connection = inputs[3]

    cursor = connection.cursor()
    cursor.execute(query, {"mn": mn})
    res = cursor.fetchall()
    cursor.close()
    resf, resy = list(res)[0]
    if len(resy['nodes']) > 0:
        resf['nodes'].extend(resy['nodes'])
    if len(resy['edges']) > 0:
        resf['edges'].extend(resy['edges'])
    graph_out = mapped_memgraph_bill_to_nx(resf, tag)
    return tag, graph_out


node_color_bill_line = 'black'
node_color_vote = {"yea": 'green',
                   "nay": 'red',
                   "paired": 'grey'}
node_color_outsider = 'purple'
node_color_membership = 'orange'


def mapped_memgraph_bill_to_nx(res_dict, tag):
    g = nx.MultiDiGraph()

    nodes = res_dict["nodes"]
    edges = res_dict["edges"]
    node_dict = {x.id: x for x in nodes}

    for n in nodes:

        if "MGBillStage" in n.labels:
            n_val = 8
            n_sec = None
        else:
            n_val = 2

        if "MGBillStage" in n.labels:
            lbl = 'BillStage'
            g.add_node(
                n.properties["match_name"],
                name=n.properties["match_name"],
                type=lbl,
                stage_date=str(n.properties['stage_date']),
                value=n_val,
                nodeColor=node_color_bill_line
            )
        elif "MGPerson" in n.labels:
            lbl = "Person"
            g.add_node('_'.join([n.properties['match_name'], tag]),
                       name=n.properties['display_name'],
                       type=lbl,
                       value=n_val)
        elif "MGOrganization" in n.labels:
            lbl = "Organization"
            g.add_node('_'.join([n.properties['match_name'], tag]),
                       name=n.properties['display_name'],
                       type=lbl,
                       nodeColor=node_color_membership,
                       value=n_val)

    for e in edges:
        if e.type == "LEGPROGRESSION":
            g.add_edge(
                node_dict[e.start_id].properties["match_name"],
                node_dict[e.end_id].properties["match_name"],
                type=e.type,
                linkColor=node_color_bill_line,
                linkDirectionalArrowLength=6,
                linkDirectionalArrowRelPos=0.5,
                linkWidth=4
            )
        elif e.type == "INDIVIDUALVOTE":
            g.add_edge(
                '_'.join([node_dict[e.start_id].properties["match_name"], tag]),
                node_dict[e.end_id].properties["match_name"],
                type=e.type,
                person_vote=e.properties['person_vote'],
                linkColor=node_color_vote[e.properties['person_vote']],
                linkDirectionalArrowLength=0,
                linkDirectionalArrowRelPos=0,
                linkWidth=1
            )

            if "MGPerson" in node_dict[e.start_id].labels:
                g.nodes['_'.join([node_dict[e.start_id].properties['match_name'], tag])]['nodeColor'] = node_color_vote[
                    e.properties['person_vote']]

        elif e.type == "COMMUNICATION":

            g.add_edge(
                '_'.join([node_dict[e.start_id].properties["match_name"], tag]),
                '_'.join([node_dict[e.end_id].properties["match_name"], tag]),
                type=e.type,
                linkColor=node_color_outsider,
                linkDirectionalArrowLength=0,
                linkDirectionalArrowRelPos=0,
                linkWidth=1
            )
            if "MGPerson" in node_dict[e.start_id].labels:
                g.nodes['_'.join([node_dict[e.end_id].properties['match_name'], tag])][
                    'nodeColor'] = node_color_outsider

        elif e.type == 'MEMBERSHIP':
            g.add_edge(
                '_'.join([node_dict[e.start_id].properties["match_name"], tag]),
                '_'.join([node_dict[e.end_id].properties["match_name"], tag]),
                type=e.type,
                linkColor=node_color_membership,
                linkDirectionalArrowLength=0,
                linkDirectionalArrowRelPos=0,
                linkWidth=1
            )

        else:
            raise RuntimeError('Problem')

    return g


def nx_bill_to_json(g):
    # convert to json
    nodes = []
    links = []
    for n, d in g.nodes.items():
        comn = {"id": n}
        for k in d.keys():
            comn[k] = d[k]

        nodes.append(comn)

    for e, d in g.edges.items():
        comn = {"source": e[0], "target": e[1]}
        for k in d.keys():
            comn[k] = d[k]
        links.append(comn)

    graph = {"nodes": nodes, "links": links}
    return graph


def memgraph_bill_query(
        boi_mn: str,
        verbose=False,
) -> dict:
    """

    Parameters
    ----------
    boi_mn: str
            bill of interest match name.  This is the starting point for the graph search

    verbose: bool
            whether to print things to stdout or not

    Returns
    -------
    dict
        dictionary of nodes and edges that is compatible with json, and can be saved or passed directly (unsure what
        this will need to look like for the integration with the frontend)

    """
    print(boi_mn)
    bill_stage_progression_query = (
        f"MATCH p=(n: MGBillStage {{bill_match_name: $boi_mn}}) - [l:LEGPROGRESSION] - (m:MGBillStage) with project(p) as f return f;"
    )

    concurrent_inputs = []

    concurrent_inputs.append(('leg_prog', boi_mn, bill_stage_progression_query, conn))

    all_graphs = {}

    # doing this concurrently seems to just make things slower
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #    for t, g in executor.map(fetch_and_map, concurrent_inputs):
    for i in concurrent_inputs:
        t, g = fetch_and_map_bill(i)
        all_graphs[t] = g

    # unpack
    leg_prog_g = all_graphs["leg_prog"]

    vote_graphs = {}
    for legstage in leg_prog_g.nodes:
        print(leg_prog_g.nodes[legstage])
        gql = """MATCH p=(n:MGPerson) - [l:INDIVIDUALVOTE]- (m:MGBillStage {match_name: $mn}) 
        OPTIONAL MATCH x=(n) - [r:COMMUNICATION] -(o) - [q:MEMBERSHIP] - (s) 
        where r.com_date <= m.stage_date and r.com_date > m.stage_date - duration({day:30}) 
        with project(p) as f, project(x) as y return f, y;"""
        tag, g = fetch_and_map_votes((legstage, legstage, gql, conn))
        vote_graphs[tag] = g

    total_graph = nx.MultiDiGraph()
    total_graph.add_nodes_from(leg_prog_g.nodes(data=True))
    total_graph.add_edges_from(leg_prog_g.edges(data=True))
    for tag in vote_graphs.keys():
        total_graph.add_nodes_from(vote_graphs[tag].nodes(data=True))
        total_graph.add_edges_from(vote_graphs[tag].edges(data=True))

    graph_json = nx_bill_to_json(total_graph)

    if verbose:
        print("done")

    import json
    with open("test.json", 'w') as h:
        json.dump(graph_json, h)

    return graph_json


def memgraph_get_graph(ooi_mn: str, graph_type: str, bill_match: str):
    print(f"{ooi_mn} {graph_type} {bill_match}")

    if graph_type == "bill":
        return memgraph_bill_query(bill_match)
    elif graph_type == "force":
        return memgraph_query_and_aggregate(ooi_mn, fund_depth=2,
                                            membership_depth=2,
                                            communication_depth=2,
                                            aggregation_threshold_step=20, )
