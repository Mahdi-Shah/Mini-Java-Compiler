from antlr4.tree.Trees import Trees
import graphviz


class Visualizer:
    def __init__(self, rule_names):
        self.rule_names = rule_names
        self.__dot = None

    def __add_nodes_edges(self, node, parent_id=None):
        """ Recursively add nodes and edges to the GraphViz tree. """
        node_id = str(id(node))
        label = Trees.getNodeText(node, ruleNames=self.rule_names)
        self.__dot.node(node_id, label)

        if parent_id:
            self.__dot.edge(parent_id, node_id)

        for i in range(node.getChildCount()):
            child = node.getChild(i)
            self.__add_nodes_edges(child, node_id)

    def visualize(self, tree, file_name):
        self.__dot = graphviz.Digraph()
        self.__add_nodes_edges(tree)
        self.__dot.render(file_name, format='png', view=True)