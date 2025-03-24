# Prefix Mapping:
# cut: <http://www.ease-crc.org/ont/food_cutting#>
# owl: <http://www.w3.org/2002/07/owl#>
# rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# foodon: <http://purl.obolibrary.org/obo/>
# soma: <http://www.ease-crc.org/ont/SOMA.owl#>
# sit_aware: <http://www.ease-crc.org/ont/situation_awareness#>

# Prefixes: owl, cut, rdf, rdfs, foodon
def get_part_connection_query(food: str, part: str) -> str:
    return f"""
    ASK {{
        foodon:{food} rdfs:subClassOf* ?parts_node.
        ?parts_node owl:onProperty cut:hasPart.
        ?parts_node owl:someValuesFrom ?val_node.
        ?val_node owl:intersectionOf ?inter_node.
        ?inter_node rdf:first cut:{part}.
    }}
    """


# Prefixes: owl, cut, soma, rdfs
def get_cutting_position_query(verb: str) -> str:
    return f"""
    SELECT * WHERE {{
        {verb} rdfs:subClassOf* ?pos_node.
        ?pos_node owl:onProperty cut:affordsPosition.
        ?pos_node owl:someValuesFrom ?pos.
        BIND(REPLACE(STR(?pos), "^.*[#/]", "") AS ?res).
    }}
    """


# Prefixes: owl, soma, rdf, rdfs, foodon, sit_aware
def get_cutting_tool_query(food: str) -> str:
    return f"""
    SELECT ?res WHERE {{
        foodon:{food} rdfs:subClassOf* ?peel_dis.
        ?peel_dis owl:onProperty soma:hasDisposition.
        ?peel_dis owl:someValuesFrom ?peel_dis_vals.
        ?peel_dis_vals owl:intersectionOf ?afford_vals.
        ?afford_vals rdf:first sit_aware:Cuttability.
        ?afford_vals rdf:rest ?task_trigger.
        ?task_trigger rdf:rest ?trigger.
        ?trigger rdf:first ?trigger_wo_nil.
        ?trigger_wo_nil owl:onProperty soma:affordsTrigger.
        ?trigger_wo_nil owl:allValuesFrom ?trigger_tool.
        ?trigger_tool owl:allValuesFrom ?tool.
        BIND(REPLACE(STR(?tool), "^.*[#/]", "") AS ?res).
    }}
    """


# Prefixes: owl, cut, soma, rdf, rdfs, foodon
def get_peeling_tool_query(food: str) -> str:
    return f"""
    SELECT ?res WHERE {{
        foodon:{food} rdfs:subClassOf* ?peel_dis.
        ?peel_dis owl:onProperty soma:hasDisposition.
        ?peel_dis owl:someValuesFrom ?peel_dis_vals.
        ?peel_dis_vals owl:intersectionOf ?afford_vals.
        ?afford_vals rdf:first cut:Peelability.
        ?afford_vals rdf:rest ?task_trigger.
        ?task_trigger rdf:rest ?trigger.
        ?trigger rdf:first ?trigger_wo_nil.
        ?trigger_wo_nil owl:onProperty soma:affordsTrigger.
        ?trigger_wo_nil owl:allValuesFrom ?trigger_tool.
        ?trigger_tool owl:allValuesFrom ?tool.
        BIND(REPLACE(STR(?tool), "^.*[#/]", "") AS ?res).
    }}
    """


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
