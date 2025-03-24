from rdflib import Graph

foods = {
    'almond': "obo:FOODON_00003523",
    'apple': "obo:FOODON_03301710",
    'avocado': "obo:FOODON_00003600",
    'banana': "obo:FOODON_00004183",
    'bean': "obo:FOODON_03301403",
    'cherry': "obo:FOODON_03301240",
    'citron': "obo:FOODON_03306596",
    'coconut': "obo:FOODON_00003449",
    'cucumber': "obo:FOODON_00003415",
    'kiwi': "obo:FOODON_00004387",
    'kumquat': "obo:FOODON_03306597",
    'lemon': "obo:FOODON_03301441",
    'lime': "obo:FOODON_00003661",
    'olive': "obo:FOODON_03317509",
    'orange': "obo:FOODON_03309832",
    'peach': "obo:FOODON_03315502",
    'pepper': "obo:FOODON_00003520",
    'pineapple': "obo:FOODON_00003459",
    'pumpkin': "obo:FOODON_00003486",
    'strawberry': "obo:FOODON_00003443",
    'squash': "obo:FOODON_00003539",
    'tomato': "obo:FOODON_03309927"
}

parts = ['Core', 'Shell', 'Peel', 'Stem']


def get_qas_for_food(graph: Graph) -> (str, str):
    res = []
    for food, iri in foods.items():
        for part in parts:
            for row in graph.query(get_part_connection_query(iri, part)):
                if row == True:
                    res.append((get_fruit_part_question(food, part), 'Yes'))
                else:
                    res.append((get_fruit_part_question(food, part), 'No'))
        for row in graph.query(get_cutting_tool_query(iri)):
            res.append((get_cutting_tool_question(food), row.res))
        for row in graph.query(get_peeling_tool_query(iri)):
            res.append((get_peeling_tool_question(food), row.res))
    return res


# Prefixes: owl, cut, rdf, rdfs
def get_part_connection_query(food: str, part: str) -> str:
    return f"""
    ASK {{
        {food} rdfs:subClassOf* ?parts_node.
        ?parts_node owl:onProperty cut:hasPart.
        ?parts_node owl:someValuesFrom ?val_node.
        ?val_node owl:intersectionOf ?inter_node.
        ?inter_node rdf:first cut:{part}.
    }}
    """


def get_fruit_part_question(food: str, part: str) -> str:
    return f"Is a(n) {part} an anatomical part of a(n) {food}?"


# Prefixes: owl, soma, rdf, rdfs, sit_aware
def get_cutting_tool_query(food: str) -> str:
    return f"""
    SELECT ?res WHERE {{
        {food} rdfs:subClassOf* ?peel_dis.
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


def get_cutting_tool_question(food: str) -> str:
    return f"When cutting a(n) {food}, what tool should be used?"


# Prefixes: owl, cut, soma, rdf, rdfs
def get_peeling_tool_query(food: str) -> str:
    return f"""
    SELECT ?res WHERE {{
        {food} rdfs:subClassOf* ?peel_dis.
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


def get_peeling_tool_question(food: str) -> str:
    return f"When peeling a(n) {food}, what tool should be used?"
