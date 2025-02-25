import React, { useRef, useEffect, useState } from 'react';
import { ForceGraph2D } from 'react-force-graph';
import { GraphData, SubgoalNode } from '../types';
import { transformToGraphData } from '../utils/graphUtils';

interface GoalGraphProps {
  nodes: SubgoalNode[];
}

// Extended GraphNode type with position properties added by the force graph
interface ForceGraphNode {
  id: string;
  name: string;
  description?: string;
  val?: number;
  x?: number;
  y?: number;
  z?: number;
}

const GoalGraph: React.FC<GoalGraphProps> = ({ nodes }) => {
  const [graphData, setGraphData] = useState<GraphData>({ nodes: [], links: [] });
  const [selectedNode, setSelectedNode] = useState<ForceGraphNode | null>(null);
  const graphRef = useRef<any>();

  useEffect(() => {
    if (nodes && nodes.length > 0) {
      setGraphData(transformToGraphData(nodes));
    }
  }, [nodes]);

  const handleNodeClick = (node: ForceGraphNode) => {
    setSelectedNode(node);
    
    // Center the view on the clicked node
    if (graphRef.current && node.x !== undefined && node.y !== undefined) {
      graphRef.current.centerAt(node.x, node.y, 1000);
      graphRef.current.zoom(2, 1000);
    }
  };

  return (
    <div className="goal-graph-container">
      <div className="graph-visualization">
        {graphData.nodes.length > 0 ? (
          <ForceGraph2D
            ref={graphRef}
            graphData={graphData}
            nodeLabel="name"
            nodeColor={() => '#1f77b4'}
            linkColor={() => '#999'}
            nodeRelSize={6}
            onNodeClick={handleNodeClick}
            width={800}
            height={600}
          />
        ) : (
          <div className="no-data">No graph data available</div>
        )}
      </div>
      
      {selectedNode && (
        <div className="node-details">
          <h3>{selectedNode.name}</h3>
          {selectedNode.description && <p>{selectedNode.description}</p>}
        </div>
      )}
    </div>
  );
};

export default GoalGraph; 