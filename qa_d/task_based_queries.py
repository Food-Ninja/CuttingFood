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
        l_b = len(res)
        # Cutting position
        for row in graph.query(get_cutting_position_query(iri)):
            if str(row.res) == 'SlicingPosition':
                res.append((get_cutting_position_question(task), 'End'))
            else:
                res.append((get_cutting_position_question(task), 'Middle'))
        # Prior task to execute
        for row in graph.query(get_prior_task_query(iri)):
            res.append((get_prior_task_question(task), row.res))
        # Repetitions
        for row in graph.query(get_repetitions_query(iri)):
            res.append((get_repetitions_question(task), row.res))
        # Input form
        inputs = graph.query(get_input_form_query(iri))
        ins = set()
        for row in inputs:
            if str(row.res) == "Food":
                ins.add("Whole")
            else:
                ins.add(str(row.res))
        res.append((get_input_form_question(task), " or ".join(ins)))
        # Output form
        outputs = graph.query(get_result_obj_query(iri))
        outs = set()
        for row in outputs:
            outs.add(f"{row.cardinality} {str(row.res)}")
        res.append((get_result_obj_question(task), " and ".join(outs)))
        print(f"{len(res) - l_b} new Questions added for {task}")
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
def get_input_form_query(verb: str) -> str:
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
            # Recursive traversal of rdf:first and rdf:rest
            {{
                ?union_node rdf:first ?target.
                BIND(REPLACE(STR(?target), "^.*[#/]", "") AS ?res).
            }}
            UNION
            {{
                ?union_node rdf:rest*/rdf:first ?target.
                BIND(REPLACE(STR(?target), "^.*[#/]", "") AS ?res).
            }}
        }}
    }}
    """


def get_input_form_question(verb: str) -> str:
    return f"When {verb} a specific fruit or vegetable, what is form of the input to perform the action on?"

# Prefixes: owl, soma, cut, rdf, rdfs
def get_result_obj_query(verb: str) -> str:
    return f"""
    SELECT ?res ?cardinality WHERE {{
        {{
            {verb} rdfs:subClassOf* ?inter_node.
            ?inter_node owl:intersectionOf ?in_res_node.
            ?in_res_node rdf:rest*/rdf:first ?result_node.
            ?result_node owl:onProperty cut:hasResultObject.
            # Handling "someValuesFrom" (no explicit cardinality)
            OPTIONAL {{
                ?result_node owl:someValuesFrom ?target.
                BIND("some" AS ?cardinality).
            }}
            # Handling "exactly X" constraints (qualified cardinality)
            OPTIONAL {{
                ?result_node owl:qualifiedCardinality ?card.
                ?result_node owl:onClass ?target.
                BIND(STR(?card) AS ?cardinality).
            }}
            # Handling "exactly X" constraints (non-qualified cardinality)
            OPTIONAL {{
                ?result_node owl:cardinality ?card.
                BIND(STR(?card) AS ?cardinality).
            }}
            BIND(REPLACE(STR(?target), "^.*[#/]", "") AS ?res).
        }}
    }}
    """


def get_result_obj_question(verb: str) -> str:
    return f"When {verb} a specific fruit or vegetable, what is form and amount of the resulting pieces?"
