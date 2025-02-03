from antlr4 import *
from parser.MiniJavaGrammarParser import MiniJavaGrammarParser
from parser.MiniJavaGrammarVisitor import MiniJavaGrammarVisitor
from models import *


class SymbolTableVisitor(MiniJavaGrammarVisitor):
    def __init__(self):
        super().__init__()
        self.symbol_table = SymbolTable()
        self.current_class = None
        self.current_method = None
        self.error_flag = False

    def visitStartRule(self, ctx: MiniJavaGrammarParser.StartRuleContext):
        self.visitMainClass(ctx.getChild(0))
        for j in range(1, ctx.getChildCount()):
            self.visitClassDeclaration(ctx.getChild(j))
        return self.symbol_table

    def visitMainClass(self, ctx: MiniJavaGrammarParser.MainClassContext):
        class_name = ctx.getChild(1).getText()
        self.current_class = ClassRecord(class_name, class_name)
        self.symbol_table.current.records[class_name] = self.current_class
        self.symbol_table.enter_scope()
        self.symbol_table.current = self.current_class
        self.visitMainMethod(ctx.getChild(3))
        self.symbol_table.exit_scope()
        return None

    def visitClassDeclaration(self, ctx: MiniJavaGrammarParser.ClassDeclarationContext):
        class_name = ctx.getChild(1).getText()
        self.current_class = ClassRecord(class_name, class_name)
        if self.symbol_table.lookup(class_name) is not None:
            self.error_flag = True
            print(f"[Duplicated]: Class name \"{class_name}\" already defined")
        else:
            self.symbol_table.current.records[class_name] = self.current_class
            self.symbol_table.enter_scope()
            self.symbol_table.current = self.current_class
        for j in range(2, ctx.getChildCount() - 1):
            child = ctx.getChild(j)
            if isinstance(child, MiniJavaGrammarParser.FieldDeclarationContext):
                self.visitFieldDeclaration(child)
            else:
                self.visitMethodDeclaration(child)
        self.symbol_table.exit_scope()
        return None

    def visitMainMethod(self, ctx: MiniJavaGrammarParser.MainMethodContext):
        self.current_method = MethodRecord("main", None)
        if self.symbol_table.lookup(self.current_class.id + ".main") is not None:
            self.error_flag = True
            print("main method already defined!")
        else:
            self.symbol_table.current.records[self.current_class.id + ".main"] = self.current_method
            self.current_class.method_list["main"] = self.current_method
            self.symbol_table.enter_scope()
            for i in range(11, ctx.getChildCount() - 1):
                self.visit(ctx.getChild(i))
            self.symbol_table.exit_scope()
        return None

    def visitStatement(self, ctx: MiniJavaGrammarParser.StatementContext):
        self.visit(ctx.getChild(0))
        return None

    def visitFieldDeclaration(self, ctx: MiniJavaGrammarParser.FieldDeclarationContext):
        type_ = self.visitType(ctx.getChild(0))
        name = self.visitIdentifier(ctx.getChild(1))
        var = Record(name, type_)
        if self.symbol_table.lookup(name) is not None:
            self.error_flag = True
            print(f"[Duplicated] Field Variable \"{name}\" already defined")
        else:
            self.symbol_table.current.records[name] = var
            self.current_class.field_list.add(name, var)
        return None

    def visitLocalDeclaration(self, ctx:MiniJavaGrammarParser.LocalDeclarationContext):
        type_ = self.visitType(ctx.getChild(0))
        name = self.visitIdentifier(ctx.getChild(1))
        var = Record(name, type_)
        if self.symbol_table.lookup(name) is not None:
            self.error_flag = True
            print(f"[Duplicated] Field Variable \"{name}\" already defined")
        else:
            self.symbol_table.current.records[name] = var
            self.current_method.variable_list.add(name, var)
        return None

    def visitMethodDeclaration(self, ctx: MiniJavaGrammarParser.MethodDeclarationContext):
        i = 1 if ctx.getChild(0).getText() == "public" else 0
        return_type = self.visitType(ctx.getChild(i)) if not isinstance(ctx.getChild(i), TerminalNode) else None
        method_name = self.visitIdentifier(ctx.getChild(i + 1))
        if self.current_class.id == method_name:
            self.error_flag = True
            print("The method name is the same as class name! No constructors in MiniJava.")
        self.current_method = MethodRecord(method_name, return_type)
        if self.symbol_table.lookup(self.current_class.id + "." + method_name) is not None:
            self.error_flag = True
            print(f"[Duplicated] Method name \"{method_name}\" already defined")
        else:
            self.symbol_table.current.records[self.current_class.id + "." + method_name] = self.current_method
            self.current_class.method_list.add(method_name, self.current_method)
            self.symbol_table.enter_scope()
            self.symbol_table.current = self.current_class
            if isinstance(ctx.getChild(i + 3), MiniJavaGrammarParser.ParameterListContext):
                self.visitParameterList(ctx.getChild(i + 3))
            self.visitMethodBody(ctx.getChild(ctx.getChildCount() - 2))
            self.symbol_table.exit_scope()
        return None

    def visitType(self, ctx: MiniJavaGrammarParser.TypeContext):
        return ctx.getText()

    def visitParameterList(self, ctx: MiniJavaGrammarParser.ParameterListContext):
        for i in range(0, ctx.getChildCount(), 2):
            self.visitParameter(ctx.getChild(i))
        return None

    def visitParameter(self, ctx: MiniJavaGrammarParser.ParameterContext):
        type_ = self.visitType(ctx.getChild(0))
        name = self.visitIdentifier(ctx.getChild(1))
        var = Record(name, type_)
        if self.symbol_table.lookup(name) is not None:
            self.error_flag = True
            print(f"[Duplicated] Parameter name \"{name}\" already defined")
        else:
            self.symbol_table.current.records[name] = var
            self.current_method.parameter_list.add(var)
        return None

    def visitMethodBody(self, ctx: MiniJavaGrammarParser.MethodBodyContext):
        for i in range(ctx.getChildCount()):
            self.visit(ctx.getChild(i))
        return None

    def visitNestedStatement(self, ctx: MiniJavaGrammarParser.NestedStatementContext):
        for i in range(1, ctx.getChildCount() - 1):
            if isinstance(ctx.getChild(i), MiniJavaGrammarParser.StatementContext):
                self.visitStatement(ctx.getChild(i))
        return None

    def visitIdentifier(self, ctx: MiniJavaGrammarParser.IdentifierContext):
        return ctx.getText()

    def visitIdentifierExpression(self, ctx: MiniJavaGrammarParser.IdentifierExpressionContext):
        return self.visitIdentifier(ctx.getChild(1)) if ctx.getChildCount() > 1 else self.visitIdentifier(ctx.getChild(0))

