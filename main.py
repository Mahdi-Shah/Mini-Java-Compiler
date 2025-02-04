import sys
from antlr4 import *
from parser.MiniJavaGrammarLexer import MiniJavaGrammarLexer
from parser.MiniJavaGrammarParser import MiniJavaGrammarParser
from semantic_analyse.controller import SymbolTableVisitor
from semantic_analyse.controller import TypeCheckVisitor
from code_generator.controller import CodeGenVisitor
from antlr4.tree.Trees import Trees
import graphviz


def main():
    file_name = "C:\\Users\\Mahdi\\Desktop\\Class\\Compiler\\Project\\2\\compiler-antlr4\\4DV506.sm222cf.PA1\\testFiles\\factorial.java"
    input_stream = None

    if len(sys.argv) > 1:
        try:
            file_name = sys.argv[1]
            input_stream = FileStream(file_name, encoding='utf-8')
            file_name = file_name.rsplit('.', 1)[0]  # Remove file extension
        except IOError:
            print("THE GIVEN FILE PATH IS WRONG!", file=sys.stderr)
            print("IF EXECUTING THE SCRIPT, CHECK YOUR COMMAND:", file=sys.stderr)
            print("python CodeGen.py <filePath>", file=sys.stderr)
            return
    else:
        try:
            file_name = "C:\\Users\\Mahdi\\Desktop\\Class\\Compiler\\Project\\2\\compiler-antlr4\\4DV506.sm222cf.PA1\\testFiles\\factorial.java"
            input_stream = FileStream(file_name, encoding='utf-8')
            file_name = file_name.rsplit('.', 1)[0]
        except IOError:
            print("THE GIVEN FILE PATH IS WRONG!!", file=sys.stderr)
            print("IF EXECUTING THE SCRIPT, CHECK YOUR COMMAND:", file=sys.stderr)
            print("python CodeGen.py <filePath>", file=sys.stderr)
            return

    # Parsing input program
    lexer = MiniJavaGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniJavaGrammarParser(stream)
    tree = parser.startRule()

    rule_names = parser.ruleNames

    dot = graphviz.Digraph()

    def add_nodes_edges(node, parent_id=None):
        """ Recursively add nodes and edges to the GraphViz tree. """
        node_id = str(id(node))
        label = Trees.getNodeText(node, ruleNames=rule_names)  # FIXED LINE
        dot.node(node_id, label)  # Add node

        if parent_id:
            dot.edge(parent_id, node_id)  # Connect edge

        for i in range(node.getChildCount()):
            child = node.getChild(i)
            add_nodes_edges(child, node_id)  # Recursively add children

    add_nodes_edges(tree)

    # Render and display the tree
    # dot.render('parse_tree', format='png', view=True)

    # Symbol Table Visitor
    symbol_table_visitor = SymbolTableVisitor()
    visited_st = symbol_table_visitor.visit(tree)

    if symbol_table_visitor.error_flag:
        print("THE PROGRAM CONTAINS ERRORS! CHECK CONSOLE AND PARSE TREE WINDOW FOR MORE INFO!", file=sys.stderr)
    else:
        visited_st.print_table()
        visited_st.reset_table()

        # Type Check Visitor
        tcv = TypeCheckVisitor(visited_st)
        tcv.visit(tree)

        if tcv.error_count > 0:
            print(f"Program Contains {tcv.error_count()} Type Errors!", file=sys.stderr)
            print("The bytecode cannot be generated!", file=sys.stderr)
        else:
            visited_st.reset_table()
            cgv = CodeGenVisitor(visited_st)
            cgv.visit(tree)
            print("\n\t PRINTING ICODEs")
            cgv.class_file.print()
            # cgv.writeToFile(file_name)


if __name__ == "__main__":
    main()
