from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import random
from random_color import random_color
import pyclustering.gcolor.dsatur as dsatur
from fastapi.middleware.cors import CORSMiddleware

# Instanciation de l'API
app = FastAPI(debug=True)
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


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

def compute_adj_mat(graph: Graph) -> list[list[int]]:
    """Compute adjacency matrix from graph

    Args:
        graph (Graph): Input graph with nodes and links

    Returns:
        list[list[int]]: Adjacency matrix where each cell represents number of connections
    """
    size = len(graph.nodes)
    res = [[0 for _ in range(size)] for _ in range(size)]
    
    # Pour chaque lien, incrémenter la valeur correspondante dans la matrice
    for link in graph.links:
        res[link.source][link.target] += 1
        res[link.target][link.source] += 1
        
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
def color_graph(graph: Graph) -> Graph:
    """Color the graph using DSatur algorithm

    Args:
        graph (Graph): Input graph to color

    Returns:
        Graph: Colored graph
    """
    adj_mat = compute_adj_mat(graph)
    d = dsatur.dsatur(adj_mat)
    d.process()
    colors = d.get_colors()
    
    # Générer des couleurs aléatoires pour chaque groupe de couleur
    colors_array_size = max(colors) + 1
    colors_array = [random_color() for _ in range(colors_array_size)]
    
    # Assigner les couleurs aux nœuds
    for n in graph.nodes:
        n.color = colors_array[colors[n.id]]
    
    return graph