import { SubgoalNode, GraphData, GraphNode, GraphLink } from '../types';

/**
 * Transforms the API response nodes into a format suitable for the force-directed graph visualization
 */
export const transformToGraphData = (nodes: SubgoalNode[]): GraphData => {
  // Create graph nodes
  const graphNodes: GraphNode[] = nodes.map(node => ({
    id: node.id,
    name: node.label,
    description: node.description,
    val: 1, // Default size
  }));

  // Create graph links based on parent-child relationships
  const graphLinks: GraphLink[] = nodes
    .filter(node => node.parent_id !== null)
    .map(node => ({
      source: node.parent_id as string,
      target: node.id,
    }));

  return {
    nodes: graphNodes,
    links: graphLinks,
  };
};

/**
 * Finds the root node in the graph (the one with no parent)
 */
export const findRootNode = (nodes: SubgoalNode[]): SubgoalNode | undefined => {
  return nodes.find(node => node.parent_id === null);
};

/**
 * Finds all direct children of a node
 */
export const findChildNodes = (nodes: SubgoalNode[], parentId: string): SubgoalNode[] => {
  return nodes.filter(node => node.parent_id === parentId);
}; 