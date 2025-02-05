from sys import call_tracing

from Tools.scripts.findlinksto import visit
from antlr4 import *
from code_generator.models import *
from parser.MiniJavaGrammarParser import MiniJavaGrammarParser
from parser.MiniJavaGrammarVisitor import MiniJavaGrammarVisitor
from semantic_analyse.models import SymbolTable, ClassRecord


class CodeGenVisitor(MiniJavaGrammarVisitor):
    def __init__(self, symbol_table: SymbolTable):
        self.current_method = None
        self.symbol_table = symbol_table
        self.current_class = None
        self.class_file = ClassFile()
        self.line = 0

    def add_instruction(self, opcode, operand1=None, operand2=None, operand3=None):
        instruction = Instruction(opcode, operand1, operand2, operand3)
        self.class_file.methods[f"{self.current_class}.{self.current_method.id}"].instruction_list.append(instruction)
        self.line += 1


    def visitMainClass(self, ctx: MiniJavaGrammarParser.MainClassContext):
        self.current_class = ctx.getChild(1).getText()
        self.symbol_table.enter_scope()
        self.visitMainMethod(ctx.getChild(3))
        self.symbol_table.exit_scope()
        self.add_instruction(Opcode.RETURN)

    def visitMainMethod(self, ctx: MiniJavaGrammarParser.MainMethodContext):
        self.current_method = self.symbol_table.lookup(self.current_class + ".main")
        method = Method()
        self.class_file.methods[f"{self.current_class}.{self.current_method.id}"] = method
        self.class_file.main_method = method
        self.symbol_table.enter_scope()
        for child in ctx.children:
            if isinstance(child, MiniJavaGrammarParser.StatementContext):
                self.visitStatement(child)
        self.symbol_table.exit_scope()

    def visitClassDeclaration(self, ctx: MiniJavaGrammarParser.ClassDeclarationContext):
        i = 1
        n = ctx.getChildCount()
        self.current_class = ctx.getChild(i).getText()
        i += 2
        self.symbol_table.enter_scope()

        for j in range(i, n - 1):
            child = ctx.getChild(j)
            if isinstance(child, MiniJavaGrammarParser.FieldDeclarationContext):
                pass
            else:
                self.visitMethodDeclaration(child)

        self.symbol_table.exit_scope()

    def visitMethodDeclaration(self, ctx: MiniJavaGrammarParser.MethodDeclarationContext):
        i = 1
        if isinstance(ctx.getChild(0), TerminalNode) and ctx.getChild(0).getText() == "public":
            i += 1
        method_name = ctx.getChild(i).getText()
        i += 1

        self.current_method = self.symbol_table.lookup(f"{self.current_class}.{method_name}")
        self.current_method.parameters_and_values.extend(self.current_method.parameter_list)
        self.current_method.parameters_and_values.extend(self.current_method.variable_list)

        method = Method()
        method.param_list.extend(self.current_method.parameter_list)
        method.list_.extend(self.current_method.parameters_and_values)
        method.var_values = [0] * len(method.list_)

        self.class_file.methods[f"{self.current_class}.{self.current_method.id}"] = method
        self.line = 0
        self.symbol_table.enter_scope()

        while not isinstance(ctx.getChild(i), MiniJavaGrammarParser.MethodBodyContext):
            i += 1
        self.visitMethodBody(ctx.getChild(i))
        self.symbol_table.exit_scope()

    def visitMethodCallExpression(self, ctx: MiniJavaGrammarParser.MethodCallExpressionContext):
        class_name = self.visit(ctx.getChild(0))
        class_rec = self.symbol_table.lookup(class_name)
        if not isinstance(class_rec, ClassRecord):
            class_rec = self.symbol_table.lookup(class_rec.type)
        n = len(ctx.children)
        i = 2
        call_output_temp_var = None
        while i < n:
            method_name = ctx.getChild(i).getText()
            method_rec = class_rec.method_list[method_name]
            i += 1
            self.visitMethodCallParams(ctx.getChild(i))
            if method_rec.type is None:
                self.add_instruction(Opcode.ACALL, f"{class_name}.{method_name}", len(method_rec.parameter_list))
            else:
                call_output_temp_var = self.get_temp_var()
                self.add_instruction(Opcode.LCALL, call_output_temp_var, f"{class_name}.{method_name}", len(method_rec.parameter_list))
            self.add_instruction(Opcode.POP_PARAM, len(method_rec.parameter_list) * 8)
            class_name = method_rec.type
            i += 1
        return call_output_temp_var

    def visitVariableAssignmentStatement(self, ctx: MiniJavaGrammarParser.VariableAssignmentStatementContext):
        lhs = self.visitIdentifier(ctx.getChild(0))
        temp_variable = self.visit(ctx.getChild(2))
        self.add_instruction(Opcode.ASSIGN, lhs, temp_variable)

    def visitIdentifier(self, ctx: MiniJavaGrammarParser.IdentifierContext):
        return ctx.getText()

    def visitThisExpression(self, ctx: MiniJavaGrammarParser.ThisExpressionContext):
        return self.current_class

    def visitIdentifierExpression(self, ctx: MiniJavaGrammarParser.IdentifierExpressionContext):
        if len(ctx.children) > 1 and ctx.getText().startswith('-'):
            var_name = ctx.getText()
            temp_value = self.get_temp_var()
            self.add_instruction(Opcode.ASSIGN, self.get_temp_var(), var_name)
            return temp_value
        else:
            if ctx.getText().startswith('+'):
                return ctx.getText()[1:]
            else:
                return ctx.getText()

    def visitIntegerLitExpression(self, ctx: MiniJavaGrammarParser.IntegerLitExpressionContext):
        return int(ctx.getText())

    def visitBoolLitExpression(self, ctx: MiniJavaGrammarParser.BoolLitExpressionContext):
        return ctx.getText()

    def visitReturnStatement(self, ctx: MiniJavaGrammarParser.ReturnStatementContext):
        return_value = self.visit(ctx.getChild(1))
        self.add_instruction(Opcode.RETURN, return_value)

    def visitWhileStatement(self, ctx: MiniJavaGrammarParser.WhileStatementContext):
        before_while_condition_label = self.get_label()
        self.add_instruction(Opcode.LABEL, before_while_condition_label)
        condition_temp_var = self.visit(ctx.getChild(2))
        if_false_instruction_number = self.line
        self.add_instruction(Opcode.IF_FALSE, condition_temp_var, None)
        self.visitStatement(ctx.getChild(4))  # While body
        self.add_instruction(Opcode.GOTO, before_while_condition_label)
        after_while_label = self.get_label()
        self.add_instruction(Opcode.LABEL, after_while_label)
        self.class_file.methods[self.current_class + "." + self.current_method.id].instruction_list[if_false_instruction_number].operand2 = after_while_label

    def visitPrintStatement(self, ctx: MiniJavaGrammarParser.PrintStatementContext):
        expression_temp_var = self.visit(ctx.getChild(2))
        self.add_instruction(Opcode.PUSH_PARAM, expression_temp_var)
        self.add_instruction(Opcode.ACALL, "print", 1)

    def visitIfElseStatement(self, ctx: MiniJavaGrammarParser.IfElseStatementContext):
        condition_temp_var = self.visit(ctx.getChild(2))  # Condition
        if_instruction_number = self.line
        self.add_instruction(Opcode.IF_FALSE, condition_temp_var, None)
        self.visit(ctx.getChild(4))  # If-body
        goto_instruction_number = self.line
        self.add_instruction(Opcode.GOTO, None)
        before_else_label = self.get_label()
        self.add_instruction(Opcode.LABEL, before_else_label)
        method = self.class_file.methods[self.current_class + '.' + self.current_method.id]
        method.instruction_list[if_instruction_number].operand2 = before_else_label
        if len(ctx.children) > 4:
            self.visit(ctx.getChild(6))  # Else-body
            after_else_label = self.get_label()
            self.add_instruction(Opcode.LABEL, after_else_label)
            method.instruction_list[goto_instruction_number].operand1 = after_else_label

    def visitLessThanExpression(self, ctx: MiniJavaGrammarParser.LessThanExpressionContext):
        op1_temp_var = self.visit(ctx.getChild(0))
        op2_temp_var = self.visit(ctx.getChild(2) if ctx.getChildCount() == 3 else ctx.getChild(3))
        result_temp_var = self.get_temp_var()
        self.add_instruction(Opcode.LT, result_temp_var, op1_temp_var, op2_temp_var)
        return result_temp_var

    def visitMulExpression(self, ctx: MiniJavaGrammarParser.MulExpressionContext):
        return self.visit_operators(ctx, Opcode.MUL)

    def visitAddExpression(self, ctx: MiniJavaGrammarParser.AddExpressionContext):
        return self.visit_operators(ctx, Opcode.ADD)

    def visitDivExpression(self, ctx):
        return self.visit_operators(ctx, Opcode.DIV)

    def visitSubExpression(self, ctx):
        return self.visit_operators(ctx, Opcode.SUB)

    def visitObjectInstantiationExpression(self, ctx: MiniJavaGrammarParser.ObjectInstantiationExpressionContext):
        return ctx.getChild(1).getText()

    def visit_operators(self, ctx: MiniJavaGrammarParser.ExpressionContext, opcode):
        op1_temp_var = self.visit(ctx.getChild(0))
        op2_temp_var = self.visit(ctx.getChild(2))
        result_temp_var = self.get_temp_var()
        self.add_instruction(opcode, result_temp_var, op1_temp_var, op2_temp_var)
        return result_temp_var

    def visitNotExpression(self, ctx):
        op1_temp_var = self.visit(ctx.getChild(1))
        result_temp_var = self.get_temp_var()
        self.add_instruction(Opcode.NOT, result_temp_var, op1_temp_var)
        return result_temp_var

    def visitMethodCallParams(self, ctx: MiniJavaGrammarParser.MethodCallParamsContext):
        i = 1
        n = len(ctx.children)
        while i < n:
            if isinstance(ctx.getChild(i), MiniJavaGrammarParser.ExpressionContext):
                parameter_temp_var = self.visit(ctx.getChild(i))
                self.add_instruction(Opcode.PUSH_PARAM, parameter_temp_var)
            i += 2

    def visitParenthesesExpression(self, ctx: MiniJavaGrammarParser.ParenthesesExpressionContext):
        return self.visit(ctx.getChild(1))

    def visitArrayAssignmentStatement(self, ctx: MiniJavaGrammarParser.ArrayAssignmentStatementContext):
        rhs_array_identifier = self.visitIdentifier(ctx.getChild(0))
        index_var = self.visit(ctx.getChild(2))
        lhs = self.visit(ctx.getChild(5))
        self.add_instruction(Opcode.ASSIGN, f"{rhs_array_identifier}[{index_var}]", lhs)

    def visitArrayAccessExpression(self, ctx: MiniJavaGrammarParser.ArrayAccessExpressionContext):
        identifier = self.visit(ctx.getChild(0))
        index_var = self.visit(ctx.getChild(2))
        return f"{identifier}[{index_var}]"

    def get_temp_var(self):
        return f"t{self.line}"

    def get_label(self):
        return f"L{self.line}"