import sys
from antlr4 import *
from parser.MiniJavaGrammarLexer import MiniJavaGrammarLexer
from parser.MiniJavaGrammarParser import MiniJavaGrammarParser
from semantic_analyse.controller import SymbolTableVisitor
from semantic_analyse.controller import TypeCheckVisitor
from code_generator.controller import CodeGenVisitor
from visual.visualizer import Visualizer


def main():
    file_name = None
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
            file_name = "examples/BinarySearch.java"
            input_stream = FileStream(file_name, encoding='utf-8')
            file_name = file_name.rsplit('.', 1)[0]
        except IOError:
            print("THE GIVEN FILE PATH IS WRONG!!", file=sys.stderr)
            print("IF EXECUTING THE SCRIPT, CHECK YOUR COMMAND:", file=sys.stderr)
            print("python CodeGen.py <filePath>", file=sys.stderr)
            return

    lexer = MiniJavaGrammarLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MiniJavaGrammarParser(stream)
    tree = parser.startRule()

    Visualizer(parser.ruleNames).visualize(tree, file_name)

    symbol_table_visitor = SymbolTableVisitor()
    visited_st = symbol_table_visitor.visit(tree)

    if symbol_table_visitor.error_flag:
        print("THE PROGRAM CONTAINS ERRORS! CHECK CONSOLE AND PARSE TREE WINDOW FOR MORE INFO!", file=sys.stderr)
    else:
        visited_st.print_table()
        visited_st.reset_table()

        tcv = TypeCheckVisitor(visited_st)
        tcv.visit(tree)

        if tcv.error_count > 0:
            print(f"Program Contains {tcv.error_count()} Type Errors!", file=sys.stderr)
            print("The bytecode cannot be generated!", file=sys.stderr)
        else:
            visited_st.reset_table()
            cgv = CodeGenVisitor(visited_st)
            cgv.visit(tree)
            print("\n\t PRINTING Three Address Codes")
            cgv.class_file.print()


if __name__ == "__main__":
    main()
