import { useState } from 'react';
import { TextField, Button } from '@mui/material';
import './App.css';
import axios from 'axios';
import GraphViewer from './GraphViewer'


const axiosInstance = axios.create({baseURL: "http://localhost:9191"})

function App() {
  const [numberNodes, setNumberNodes] = useState(20)
  const [connectivity,setConnectivity] = useState<GLfloat>(0.4)
  const [graphResult, setGraphResult] = useState<any>(null);
  const [colorResult, setColorResult] = useState<any>(null);

  const generateGraph = () => {
    axiosInstance
        .get('/random', {
            params: {
                number_of_nodes: numberNodes,
                probability_connection: connectivity
            }
        })
        .then(response => {
            setGraphResult(response.data); 
            setColorResult(null);
            console.log('Graphe généré:', response.data);
        })
        .catch(error => {
            console.error('Erreur lors de la génération du graphe:', error);
        });
};



const colorGraph = () => {
  console.log('avant de colorier', graphResult);
  
  // Prépare les données nécessaires pour l'envoi
  const dataToSend = {
      name: graphResult.name,  // Assure-toi que graphResult a un champ name
      nodes: graphResult.nodes.map((node: { id: any; name: any; color: any; }) => ({
          id: node.id,    // Conserve l'identifiant du noeud
          name: node.name, // Conserve le nom du noeud
          color: node.color // Assure-toi que le champ 'color' existe
      })),
      links: graphResult.links.map((link: { source: any; target: any; weight: any; }) => ({
          source: link.source, // Conserve la source du lien
          target: link.target, // Conserve la cible du lien
          weight: link.weight   // Conserve le poids du lien
      }))
  };

  // Envoie uniquement les données nécessaires
  console.log('dataToSend', dataToSend)
  axiosInstance
      .post('/graph/color/dsatur', dataToSend)
      .then(response => {
          setColorResult(response.data); 
          console.log('Graphe colorié:', response.data);
      })
      .catch(error => {
          console.error('Erreur lors de la coloration du graphe:', error);
      });
};





  return (
    <>
      <h2>Génération d'un graph aléatoire</h2>
      <div >
        <TextField type="number"
              label="Nombre de noeuds" 
              value={numberNodes} 
              onChange={(e) => setNumberNodes(e.currentTarget.value)}></TextField>
        <TextField type="number"
              label="Taux de connectivité" 
              value={connectivity} 
              onChange={(e) => setConnectivity(e.currentTarget.value)}></TextField>
      <Button onClick={() => generateGraph()}>Générer</Button>
      <Button onClick={() => colorGraph()}>Colorier</Button>
      {graphResult && <GraphViewer graph={graphResult} />}
      </div>
    </>
  )

  
}

export default App
