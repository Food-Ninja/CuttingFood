import csv

import requests
from rdflib import Graph, Namespace
from rdflib.namespace import OWL, RDF, RDFS

from food_based_queries import get_qas_for_food
from task_based_queries import get_qas_for_taks

url = "https://raw.githubusercontent.com/Food-Ninja/CuttingFood/main/owl/food_cutting.owl"
response = requests.get(url)

g = Graph()
g.parse(data=response.content, format='xml')

CUT = Namespace("http://www.ease-crc.org/ont/food_cutting#")
OBO = Namespace("http://purl.obolibrary.org/obo/")
SOMA = Namespace("http://www.ease-crc.org/ont/SOMA.owl#")
SIT_AWARE = Namespace("http://www.ease-crc.org/ont/situation_awareness#")

g.bind("owl", OWL)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("soma", SOMA)
g.bind("sit_aware", SIT_AWARE)
g.bind("cut", CUT)
g.bind("obo", OBO)

food_qas = get_qas_for_food(g)
task_qas = get_qas_for_taks(g)

with open("qa.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Question", "Answer"])
    writer.writerows(food_qas)
    writer.writerows(task_qas)
