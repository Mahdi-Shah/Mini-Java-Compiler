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


class TypeCheckVisitor(MiniJavaGrammarVisitor):
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.error_count = 0

    def error_message(self, ctx):
        return f"[err#{self.error_count} - @{ctx.start.line}:{ctx.stop.column}] "

    def get_error_count(self):
        return self.error_count

    def visitStartRule(self, ctx: MiniJavaGrammarParser.StartRuleContext):
        self.visit(ctx.getChild(0))
        for i in range(1, ctx.getChildCount()):
            self.visitClassDeclaration(ctx.getChild(i))
        return None

    def visitMainClass(self, ctx: MiniJavaGrammarParser.MainClassContext):
        self.symbol_table.enter_scope()
        self.visit(ctx.getChild(3))
        self.symbol_table.exit_scope()
        return None

    def visitBreakStatement(self, ctx: MiniJavaGrammarParser.BreakStatementContext):
        node = ctx
        while node:
            node = node.parentCtx
            if isinstance(node, MiniJavaGrammarParser.WhileStatementContext):
                return None
        print(self.error_message(ctx) + "Break statement is not inside a while loop!")
        self.error_count += 1
        return None

    def visitContinueStatement(self, ctx: MiniJavaGrammarParser.ContinueStatementContext):
        node = ctx
        while node:
            node = node.parentCtx
            if isinstance(node, MiniJavaGrammarParser.WhileStatementContext):
                return None
        print(self.error_message(ctx) + "Continue statement is not inside a while loop!")
        self.error_count += 1
        return None

    def visitClassDeclaration(self, ctx: MiniJavaGrammarParser.ClassDeclarationContext):
        self.symbol_table.enter_scope()
        for i in range(3, ctx.getChildCount() - 1):
            child = ctx.getChild(i)
            if isinstance(child, MiniJavaGrammarParser.FieldDeclarationContext):
                self.visitFieldDeclaration(child)
            else:
                self.visitMethodDeclaration(child)
        self.symbol_table.exit_scope()
        return None

    def visitMainMethod(self, ctx: MiniJavaGrammarParser.MainMethodContext):
        self.symbol_table.enter_scope()
        for i in range(11, ctx.getChildCount()):
            self.visitStatement(ctx.getChild(i))
        self.symbol_table.exit_scope()
        return None

    def visitPrintStatement(self, ctx: MiniJavaGrammarParser.PrintStatementContext):
        expr_type = self.visit(ctx.getChild(2))
        if expr_type not in {"int", "String", "char"}:
            print(self.error_message(ctx) + "Invalid type in print statement")
            self.error_count += 1
        return None

    def visitWhileStatement(self, ctx: MiniJavaGrammarParser.WhileStatementContext):
        expr_type = self.visit(ctx.getChild(2))
        if expr_type != "boolean":
            print(self.error_message(ctx) + "While condition must be boolean")
            self.error_count += 1
        self.visit(ctx.getChild(4))
        return None

    def visitDoWhileStatement(self, ctx: MiniJavaGrammarParser.DoWhileStatementContext):
        expr_type = self.visit(ctx.getChild(4))
        if expr_type != "boolean":
            print(self.error_message(ctx) + "Do-While condition must be boolean")
            self.error_count += 1
        self.visit(ctx.getChild(4))
        return None

    def visitIfElseStatement(self, ctx: MiniJavaGrammarParser.IfElseStatementContext):
        expr_type = self.visit(ctx.getChild(2))
        if expr_type != "boolean":
            print(self.error_message(ctx) + "If condition must be boolean")
            self.error_count += 1
        self.visit(ctx.getChild(4))
        if ctx.getChildCount() > 5:
            self.visit(ctx.getChild(6))
        return None

    def visitArrayAssignmentStatement(self, ctx: MiniJavaGrammarParser.ArrayAssignmentStatementContext):
        type_lhs = self.visit(ctx.getChild(0))
        type_index = self.visit(ctx.getChild(2))
        type_rhs = self.visit(ctx.getChild(5))

        if None in {type_lhs, type_index, type_rhs}:
            print(self.error_message(ctx) + "Null type encountered in assignment")
            self.error_count += 1
            return None

        if type_lhs != "int[]":
            print(self.error_message(ctx) + f"{ctx.getChild(0).getText()} is not of type 'int[]'")
            self.error_count += 1
        if type_index != "int":
            print(self.error_message(ctx) + "Array index must be of type 'int'")
            self.error_count += 1
        if type_rhs != "int":
            print(self.error_message(ctx) + "Cannot assign non-int value to 'int[]'")
            self.error_count += 1
        return None

    def visitMethodCallStatement(self, ctx: MiniJavaGrammarParser.MethodCallStatementContext):
        self.visit(ctx.getChild(0))
        return None

    def visitNestedStatement(self, ctx: MiniJavaGrammarParser.NestedStatementContext):
        for i in range(1, ctx.getChildCount() - 1):
            self.visit(ctx.getChild(i))
        return None

    def visitFieldDeclaration(self, ctx: MiniJavaGrammarParser.FieldDeclarationContext):
        return super().visitFieldDeclaration(ctx)

    def visitMethodDeclaration(self, ctx: MiniJavaGrammarParser.MethodDeclarationContext):
        i = 0
        if ctx.getChild(0).getText() == "public":
            i += 1
        return_type = self.visit(ctx.getChild(i)) if not isinstance(ctx.getChild(i), TerminalNode) else None
        i += 2
        self.symbol_table.enter_scope()
        if isinstance(ctx.getChild(i), MiniJavaGrammarParser.ParameterListContext):
            self.visitParameterList(ctx.getChild(i))
            i += 1
        i += 2
        actual_return = self.visit(ctx.getChild(i))

        if return_type is None and actual_return is None:
            self.symbol_table.exit_scope()
            return None

        if return_type is None or actual_return is None:
            print(self.error_message(ctx.getChild(2)) + f"Return type mismatch in method {ctx.getChild(2).getText()}")
            self.error_count += 1
            self.symbol_table.exit_scope()
            return None

        if return_type != actual_return:
            print(self.error_message(ctx.getChild(
                2)) + f"Mismatch in declared type '{return_type}' and actual return type '{actual_return}' in method {ctx.getChild(2).getText()}")
            self.error_count += 1

        self.symbol_table.exit_scope()
        return None

    def visitParameterList(self, ctx: MiniJavaGrammarParser.ParameterListContext):
        return super().visitParameterList(ctx)

    def visitType(self, ctx: MiniJavaGrammarParser.TypeContext):
        return ctx.getText()

    def visitMethodBody(self, ctx: MiniJavaGrammarParser.MethodBodyContext):
        i = 0
        while isinstance(ctx.getChild(i), MiniJavaGrammarParser.LocalDeclarationContext):
            self.visitLocalDeclaration(ctx.getChild(i))
            i += 1
        while isinstance(ctx.getChild(i), MiniJavaGrammarParser.StatementContext):
            if isinstance(ctx.getChild(i).getChild(0), MiniJavaGrammarParser.ReturnStatementContext):
                return self.visitReturnStatement(ctx.getChild(i).getChild(0))
            self.visitStatement(ctx.getChild(i))
            i += 1
        return None

    def visitReturnStatement(self, ctx: MiniJavaGrammarParser.ReturnStatementContext):
        return self.visit(ctx.getChild(1))

    def visitIdentifier(self, ctx: MiniJavaGrammarParser.IdentifierContext):
        if self.symbol_table.lookup(ctx.getText()) is None:
            print(self.error_message(ctx) + f"Undefined ID: {ctx.getText()}")
            self.error_count += 1
            return None
        return self.symbol_table.lookup(ctx.getText()).getType()

    def visitIdentifierExpression(self, ctx: MiniJavaGrammarParser.IdentifierExpressionContext):
        if ctx.getChildCount() > 1:
            return self.visitIdentifier(ctx.getChild(1))
        return self.visitIdentifier(ctx.getChild(0))

    def visitArrayInstantiationExpression(self, ctx: MiniJavaGrammarParser.ArrayInstantiationExpressionContext):
        type_ = self.visitType(ctx.getChild(1))
        if type_ is not None:
            if type_ == "int":
                return "int[]"
        print(self.error_message(ctx.getChild(1)) + " in MiniJava only 'int[]' arrays are acceptable")
        self.error_count += 1
        return None

    def visitObjectInstantiationExpression(self, ctx: MiniJavaGrammarParser.ObjectInstantiationExpressionContext):
        return self.visitIdentifier(ctx.getChild(1))

    def visitDotlengthExpression(self, ctx: MiniJavaGrammarParser.DotlengthExpressionContext):
        type_ = self.visit(ctx.getChild(0))
        if type_ in ["int[]", "String"]:
            return "int"
        print(self.error_message(ctx.getChild(0)) + f"Error: '.length' is applicable on 'int[]' and 'String' types only")
        self.error_count += 1
        return None

    def visitDotcharatExpression(self, ctx: MiniJavaGrammarParser.DotcharatExpressionContext):
        type1 = self.visit(ctx.getChild(0))
        type2 = self.visit(ctx.getChild(3))
        if type1 is None or type2 is None:
            print(self.error_message(
                ctx.getChild(0)) + f"either {ctx.getChild(0).getText()} or {ctx.getChild(3).getText()} has type null")
            self.error_count += 1
            return None
        if type1 != "String":
            print(self.error_message(ctx.getChild(0)) + f"{ctx.getChild(0).getText()} is not a String")
            self.error_count += 1
            return None
        if type2 != "int":
            print(self.error_message(ctx.getChild(3)) + f"{ctx.getChild(3).getText()} is not an integer")
            self.error_count += 1
            return None
        return "char"

    def visitStringExpression(self, ctx: MiniJavaGrammarParser.StringExpressionContext):
        return "String"

    def visitCharacterExpression(self, ctx: MiniJavaGrammarParser.CharacterExpressionContext):
        return "char"

    def visitIntegerLitExpression(self, ctx: MiniJavaGrammarParser.IntegerLitExpressionContext):
        return "int"

    def visitBoolLitExpression(self, ctx: MiniJavaGrammarParser.BoolLitExpressionContext):
        return "boolean"

    def visitMethodCallExpression(self, ctx: MiniJavaGrammarParser.MethodCallExpressionContext):
        class_name = self.visit(ctx.getChild(0))
        class_rec = self.symbol_table.lookup(class_name)
        if class_rec is None:
            print(self.error_message(ctx.getChild(0)) + f" Undefined Class Name: '{class_name}'")
            self.error_count += 1
            return None

        method_rec = None
        i = 2
        while i < ctx.getChildCount():
            method_name = ctx.getChild(i).getText()
            method_rec = class_rec.method_list.get(method_name)
            if method_rec is None:
                print(self.error_message(
                    ctx.getChild(i)) + f" Undefined Method Name: '{method_name}' in class '{class_name}'")
                self.error_count += 1
                return None

            param_list = method_rec.parameter_list
            i += 1
            method_call_params = self.visitMethodCallParams(ctx.getChild(i))
            if len(param_list) != len(method_call_params):
                print(self.error_message(ctx.getChild(i)) + f"Wrong number of parameters in calling {method_name}")
                self.error_count += 1
            else:
                for j, param in enumerate(method_call_params):
                    method_call_param_type = self.visit(param)
                    actual_type = param_list[j].type
                    if actual_type != method_call_param_type:
                        print(self.error_message(ctx.getChild(
                            i)) + f"Parameter type error in calling '{method_name}' parameter {j + 1} should be {actual_type}, but found {method_call_param_type}")
                        self.error_count += 1
            i += 1
        return method_rec.getType()

    def visitThisExpression(self, ctx: MiniJavaGrammarParser.ThisExpressionContext):
        return self.symbol_table.current.type

    def visitMethodCallParams(self, ctx: MiniJavaGrammarParser.MethodCallParamsContext):
        children = []
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if isinstance(child, TerminalNode) and child.getText() in {"(", ",", ")"}:
                continue
            children.append(child)
        return children

    def visitArrayAccessExpression(self, ctx: MiniJavaGrammarParser.ArrayAccessExpressionContext):
        type1 = self.visit(ctx.getChild(0))  # name
        type2 = self.visit(ctx.getChild(2))  # index
        if type1 is None or type2 is None:
            print(self.error_message(ctx.getChild(0)), "either", ctx.getChild(0).getText(), "or",
                  ctx.getChild(2).getText(), "has type of null")
            self.error_count += 1
            return None
        if type1 != "int[]":
            print(self.error_message(ctx.getChild(0)), ctx.getChild(0).getText(), "is not of type 'int[]'")
            self.error_count += 1
            return None
        if type2 != "int":
            print(self.error_message(ctx.getChild(2)), ctx.getChild(2).getText(), "is not an 'int'")
            self.error_count += 1
            return None
        return "int"

    def visitAddExpression(self, ctx: MiniJavaGrammarParser.AddExpressionContext):
        type_lhs = self.visit(ctx.getChild(0))
        type_rhs = self.visit(ctx.getChild(2))
        if type_lhs is None or type_rhs is None:
            print(self.error_message(ctx.getChild(0)), ctx.getChild(0).getText(), "or",
                  ctx.getChild(2).getText(), "Has type of null")
            self.error_count += 1
            return None
        if type_lhs not in ("int", "String") or type_rhs not in ("int", "String"):
            print(self.error_message(ctx.getChild(0)), "Addition can be done on String or int types only!")
            self.error_count += 1
        if type_lhs != type_rhs:
            print(self.error_message(ctx.getChild(0)), "LHS and RHS should have the same type (int or String)")
            self.error_count += 1
            return None
        return type_lhs

    def visitVariableAssignmentStatement(self, ctx: MiniJavaGrammarParser.VariableAssignmentStatementContext):
        type_lhs = self.visit(ctx.getChild(0))
        type_rhs = self.visit(ctx.getChild(2))
        if type_lhs is None or type_rhs is None:
            print(self.error_message(ctx.getChild(0)), "either", ctx.getChild(0).getText(), "or",
                  ctx.getChild(2).getText(), "Has type of null")
            self.error_count += 1
            return None
        if type_lhs != type_rhs:
            print(self.error_message(ctx.getChild(0)), "assignment LHS and RHS are not compatible")
        return type_lhs

    def visitDivExpression(self, ctx: MiniJavaGrammarParser.DivExpressionContext):
        return self.visit_binary_expression(ctx, "division", "int")

    def visitMulExpression(self, ctx: MiniJavaGrammarParser.MulExpressionContext):
        return self.visit_binary_expression(ctx, "multiplication", "int")

    def visitSubExpression(self, ctx: MiniJavaGrammarParser.SubExpressionContext):
        return self.visit_binary_expression(ctx, "subtraction", "int")

    def visitLessThanExpression(self, ctx: MiniJavaGrammarParser.LessThanExpressionContext):
        return self.visit_compare_expression(ctx, "<")

    def visitGreaterthanExpression(self, ctx):
        return self.visit_compare_expression(ctx, ">")

    def visitAndExpression(self, ctx: MiniJavaGrammarParser.AndExpressionContext):
        return self.visit_binary_expression(ctx, "&&", "boolean", "boolean")

    def visitEqualityExpression(self, ctx: MiniJavaGrammarParser.EqualityExpressionContext):
        type_lhs = self.visit(ctx.getChild(0))
        type_rhs = self.visit(ctx.getChild(3))
        if type_lhs is None or type_rhs is None:
            print(self.error_message(ctx.getChild(0)), "either", ctx.getChild(0).getText(), "or",
                  ctx.getChild(3).getText(), "Has type of null")
            self.error_count += 1
            return None
        if type_lhs != type_rhs:
            print(self.error_message(ctx.getChild(0)), f"{ctx.getChild(0).getText()} has type of {type_rhs} where "
                                                       f"{ctx.getChild(3).getText()} has type of {type_lhs}")
            self.error_count += 1
            return None
        return "boolean"

    def visitOrExpression(self, ctx: MiniJavaGrammarParser.OrExpressionContext):
        return self.visit_binary_expression(ctx, "||", "boolean", "boolean")

    def visitNotExpression(self, ctx: MiniJavaGrammarParser.NotExpressionContext):
        type_expr = self.visit(ctx.getChild(1))
        if type_expr is None:
            print(self.error_message(ctx.getChild(1)), "type of expression after '!' is null")
            self.error_count += 1
            return None
        if type_expr != "boolean":
            print(self.error_message(ctx.getChild(1)), "logical '!' can be done on 'boolean' types only!")
            self.error_count += 1
            return None
        return type_expr

    def visitParenthesesExpression(self, ctx):
        return self.visit(ctx.getChild(1))

    def visit_binary_expression(self, ctx, operation, valid_type, return_type=None):
        type_lhs = self.visit(ctx.getChild(0))
        type_rhs = self.visit(ctx.getChild(2))
        if type_lhs is None or type_rhs is None:
            print(self.error_message(ctx.getChild(0)), "either", ctx.getChild(0).getText(), "or",
                  ctx.getChild(2).getText(), "Has type of null")
            self.error_count += 1
            return None
        if type_lhs != valid_type or type_rhs != valid_type:
            print(self.error_message(ctx.getChild(0)),
                  f"{operation} operation can be done on '{valid_type}' types only!")
            self.error_count += 1
            return None
        return return_type if return_type else type_lhs

    def visit_compare_expression(self, ctx, operator: str):
        n = ctx.getChildCount()
        type_lhs = self.visit(ctx.getChild(0))
        type_rhs = self.visit(ctx.getChild(3)) if n > 3 else self.visit(ctx.getChild(2))
        if type_lhs is None or type_rhs is None:
            print(self.error_message(ctx.getChild(
                0)) + f"either {ctx.getChild(0).getText()} or {ctx.getChild(2).getText()} has type of null")
            self.error_count += 1
            return None
        if type_lhs != "int" or type_rhs != "int":
            print(self.error_message(ctx.getChild(0)) + f"{operator}, {operator}= operations can be done on 'int' types only!")
            self.error_count += 1
            return None
        return "boolean"
