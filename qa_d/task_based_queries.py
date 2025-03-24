from rdflib import Graph

tasks = {
    'quartering': "cut:Quartering",
    'julienning': "cut:Julienning",
    'halving': "cut:Halving",
    'dicing': "soma:Dicing",
    'cutting': "soma:Cutting",
    'slicing': "soma:Slicing",
    'snipping': "cut:Snipping",
    'slivering': "cut:Slivering",
    'sawing': "cut:Sawing",
    'paring': "cut:Paring",
    'carving': "cut:Carving",
    'mincing': "cut:Mincing",
    'cubing': "cut:Cubing",
    'chopping': "cut:Chopping",
    'dividing': "cut:Dividing"
}


def get_qas_for_taks(graph: Graph) -> (str, str):
    res = []
    for task, iri in tasks.items():
        for row in graph.query(get_cutting_position_query(iri)):
            if row.res == 'SlicingPosition':
                res.append((get_cutting_position_question(task), 'End'))
            else:
                res.append((get_cutting_position_question(task), 'Middle'))
        for row in graph.query(get_prior_task_query(iri)):
            res.append((get_prior_task_question(task), row.res))
        for row in graph.query(get_repetitions_query(iri)):
            res.append((get_repetitions_question(task), row.res))
        for row in graph.query(get_action_target_query(iri)):
            res.append((get_action_target_question(task), row.res))
    return res


# Prefixes: owl, cut, soma, rdfs
def get_cutting_position_query(verb: str) -> str:
    return f"""
    SELECT ?res WHERE {{
        {verb} rdfs:subClassOf* ?pos_node.
        ?pos_node owl:onProperty cut:affordsPosition.
        ?pos_node owl:someValuesFrom ?pos.
        BIND(REPLACE(STR(?pos), "^.*[#/]", "") AS ?res).
    }}
    """


def get_cutting_position_question(verb: str) -> str:
    return f"When {verb} a specific fruit or vegetable, where should the knife be placed - in the middle or at the end of the object?"


# Prefixes: owl, cut, soma, rdfs
def get_prior_task_query(verb: str) -> str:
    return f"""
    SELECT ?res WHERE {{
        {verb} rdfs:subClassOf* ?sub.
        ?sub owl:onProperty cut:requiresPriorTask .
        ?sub owl:someValuesFrom ?priortask.
        BIND(REPLACE(STR(?priortask), "^.*[#/]", "") AS ?res).
    }}
    """


def get_prior_task_question(verb: str) -> str:
    return f"When {verb} a specific fruit or vegetable, what other cutting task - if any - should be executed before?"


# Prefixes: owl, cut, soma, rdfs
def get_repetitions_query(verb: str) -> str:
    return f"""
    SELECT ?res WHERE {{
        {{
            {verb} rdfs:subClassOf* ?rep_node.
            ?rep_node owl:onProperty cut:repetitions.
            FILTER EXISTS {{
                ?rep_node owl:hasValue ?val.
                }}
            BIND("exactly 1" AS ?res)
        }}
        UNION
        {{
            {verb} rdfs:subClassOf* ?rep_node.
            ?rep_node owl:onProperty cut:repetitions.
            FILTER EXISTS {{
                ?rep_node owl:minQualifiedCardinality ?val.
            }}
            BIND("at least 1" AS ?res)
        }}
    }}
    """


def get_repetitions_question(verb: str) -> str:
    return f"When {verb} a specific fruit or vegetable, how many cuts need to be made - exactly one or more than one?"


# Prefixes: owl, soma, cut, rdf, rdfs
def get_action_target_query(verb: str) -> str:
    return f"""
    SELECT ?res WHERE {{
        {{
            {verb} rdfs:subClassOf* ?inter_node.
            ?inter_node owl:intersectionOf ?in_res_node.
            ?in_res_node rdf:first ?input_node.
            ?input_node owl:onProperty cut:hasInputObject.
            ?input_node owl:someValuesFrom ?target.
            FILTER NOT EXISTS {{
                ?target owl:unionOf ?union_node.
            }}
            BIND(REPLACE(STR(?target), "^.*[#/]", "") AS ?res).
        }}
        UNION
        {{
            {verb} rdfs:subClassOf* ?inter_node.
            ?inter_node owl:intersectionOf ?in_res_node.
            ?in_res_node rdf:first ?input_node.
            ?input_node owl:onProperty cut:hasInputObject.
            ?input_node owl:someValuesFrom ?targets_node.
            ?targets_node owl:unionOf ?union_node.
            ?union_node rdf:first ?target.
            BIND(REPLACE(STR(?target), "^.*[#/]", "") AS ?res).
        }}
    }}
    """


def get_action_target_question(verb: str) -> str:
    return f"When {verb} a specific fruit or vegetable, what is the target to perform the object on - the whole food or only a specific part?"
