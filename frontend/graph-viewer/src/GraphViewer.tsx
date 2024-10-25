import React from 'react';
import { ForceGraph3D } from 'react-force-graph';



// interface GraphViewerProps {
//   graph: {
//     nodes: { id: string }[];
//     links: { source: string | number; target: string | number }[];
//   };
// }


const GraphViewer =(props)=> {
  return (
    <ForceGraph3D
width={window.innerWidth*0.6}
height={window.innerHeight*0.8}
graphData={props.graph}></ForceGraph3D>);
};



export default GraphViewer;
