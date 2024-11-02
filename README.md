# tp-graph-viewer

Ce projet est un TP noté réalisé lors de mes cours à IMT Mines Albi, permettant de visualiser des graphes en 3D et d’appliquer des algorithmes de coloration. Il est basé sur une architecture **Full Stack** avec **FastAPI** et **Python** pour le backend et **React** avec **TypeScript** pour le frontend.

L’utilisateur peut générer des graphes aléatoires en spécifiant le nombre de noeuds et le taux de connectivité souhaités, puis visualiser les graphes en 3D. Un algorithme de coloration de graphe (Dsatur) est également utilisé, permettant de colorier les noeuds du graphe en fonction de leurs connexions.


## Architecture

Le projet est structuré en deux parties :
- **Backend (FastAPI, Python)** : Fournit une API REST pour gérer la génération et la coloration de graphes.
- **Frontend (React, TypeScript)** : Interface utilisateur avec formulaire de génération, visualisation des graphes, et boutons d'interaction.


## Technologies Utilisées

### Backend
- **Python**
- **FastAPI**
- **pyclustering** pour l’algorithme de coloration
- **random_color** pour générer des couleurs aléatoires
  
### Frontend
- **React** (TypeScript)
- **axios** pour la connexion API
- **@emotion/styled**, **@mui/material** pour les composants d’interface
- **react-force-graph** pour la visualisation des graphes

## Installation

### Prérequis

- **Python 3**
  
### Backend
1. Naviguer dans le dossier `backend` :
    ```bash
    cd graph_viewer/backend
    ```
2. Créer un environnement virtuel et installer les dépendances :
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Lancer le serveur backend :
    ```bash
    uvicorn api:app --port 9191 --reload
    ```

### Frontend
1. Créer et configurer l'application React :
    ```bash
    cd graph_viewer/frontend/graph-viewer
    npm install
    ```
2. Lancer le frontend :
    ```bash
    npm run dev
    ```

## Utilisation

- **Accès Backend** : l’API est documentée à l’adresse [http://localhost:9191/docs](http://localhost:9191/docs).
- **Accès Frontend** : l’application Web est accessible via [http://localhost:5173/](http://localhost:5173/).


## API Backend

### Routes REST

| Méthode | URL                      | Input                             | Output      |
|---------|---------------------------|-----------------------------------|-------------|
| GET     | `/random`                 | `number_of_nodes`, `probability`  | `Graph`     |
| POST    | `/graph/color/dsatur`     | `Graph`                           | `Graph`     |

## Modèles

- **Node** : `id: int`, `name: str`, `color: str`
- **Link** : `source: int`, `target: int`, `weight: int`
- **Graph** : `name: str`, `nodes: List[Node]`, `links: List[Link]`


