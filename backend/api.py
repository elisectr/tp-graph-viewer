from dataclasses import dataclass
import json
import logging
from fastapi import HTTPException
from fastapi import FastAPI
from typing import Any, Optional
from pydantic import BaseModel
import random
from random_color import random_color
import pyclustering.gcolor.dsatur as dsatur
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("logger")

# Instanciation de l'API
app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
   id: Optional[int] = None
   name: str
   color: str

class Link(BaseModel):
   source: int
   target: int
   weight: float # random de 0 à 1

class Graph(BaseModel):
   name: str
   nodes: list[Node]
   links: list[Link]



def random_name():
    """create random name for graph

    Returns:
        str: name
    """
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    name_chars = list(characters)
    name_length = random.randint(5,15)
    name = ''.join([random.choice(name_chars) for _ in range(name_length)])
    return name

def random_condition(probability):
    return random.uniform(0,1) < probability

def random_source(i:int,number_of_nodes:int):
    c=i
    while c==i:
      c=random.randint(0,number_of_nodes-1)
    return c

# def compute_adj_mat(graph: Graph) -> list[list[int]]:
def compute_adj_mat(graph: dict) -> list[list[int]]:
    """Compute adjacency matrix from graph

    Args:
        graph (Graph): Input graph with nodes and links

    Returns:
        list[list[int]]: Adjacency matrix where each cell represents number of connections
    """
    size = len(graph.get("nodes", []))  # Utiliser une liste vide par défaut
    res = [[0 for _ in range(size)] for _ in range(size)]
    
    # Pour chaque lien, incrémenter la valeur correspondante dans la matrice
    for link in graph.get("links", []):  # Utiliser une liste vide par défaut
        source_id = link.get("source", {}).get("id", None)  # Récupérer l'ID du nœud source
        target_id = link.get("target", {}).get("id", None)  # Récupérer l'ID du nœud cible

        if source_id is not None and target_id is not None:
            res[source_id][target_id] += 1
            res[target_id][source_id] += 1
    logger.debug(f"type de res: {type(res)}")
    return res



@app.get("/random")
def random_graph(number_of_nodes:int, probability_connection:float) -> Graph:
    """Generate a random graph

    Args:
        number_of_nodes (int): Number of nodes to generate
        probability_connection (float): Probability of connection between nodes

    Returns:
        Graph: Generated random graph
    """
    nodes = []
    links = []

    for i in range(number_of_nodes):
        nodes.append(Node(id=i, name=f"Node {i}", color=random_color()))

    for i in range(number_of_nodes):
        for j in range(number_of_nodes):
            if i != j and random_condition(probability_connection):
                links.append(Link(source=i, target=j, weight=random.random()))

    graph = Graph(name=random_name(), nodes=nodes, links=links)
    return graph

@app.post("/graph/color/dsatur")
def color_graph(graph: dict) -> dict:
    """Color the graph using DSatur algorithm

    Args:
        graph (dict): Input graph to color

    Returns:
        Graph: Colored graph
    """
    logger.info("Je suis dans color_graph")
    logger.warning(f"-"*500)

    try:
        adj_mat = compute_adj_mat(graph)
        d = dsatur.dsatur(adj_mat)
        d.process()
        colors = d.get_colors()
        
        # Générer des couleurs aléatoires pour chaque groupe de couleur
        colors_array_size = max(colors) + 1
        colors_array = [random_color() for _ in range(colors_array_size)]
        
        # Assigner les couleurs aux nœuds
        for n in graph['nodes']:
            n['color'] = colors_array[colors[n['id']]]

        return graph   
    except Exception as e:
        logger.error("Erreur lors de la coloration du graphe : %s", str(e))
        # raise e
        return None
    


# def print_graph_details(graph: dict) -> None:
#     """Print the main characteristics of the graph.

#     Args:
#         graph (dict): The graph to print details about.
#     """
#     # Imprimer le nom du graph
#     logger.debug(f"Graph Name: {graph['name']}")
    
#     # Imprimer les détails des nœuds
#     logger.debug("Nodes:")
#     for node in graph['nodes']:
#         logger.debug(f"  - ID: {node['id']}, Name: {node['name']}, Color: {node['color']}")
    
#     # Imprimer les détails des liens
#     logger.debug("Links:")
#     for link in graph['links']:
#         logger.debug(f"  - Source: {link['source']}, Target: {link['target']}, Weight: {link['weight']}")

