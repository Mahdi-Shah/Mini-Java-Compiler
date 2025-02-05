# Generated from MiniJavaGrammar.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MiniJavaGrammarParser import MiniJavaGrammarParser
else:
    from MiniJavaGrammarParser import MiniJavaGrammarParser

# This class defines a complete generic visitor for a parse tree produced by MiniJavaGrammarParser.

class MiniJavaGrammarVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MiniJavaGrammarParser#startRule.
    def visitStartRule(self, ctx:MiniJavaGrammarParser.StartRuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#mainClass.
    def visitMainClass(self, ctx:MiniJavaGrammarParser.MainClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#mainMethod.
    def visitMainMethod(self, ctx:MiniJavaGrammarParser.MainMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#classDeclaration.
    def visitClassDeclaration(self, ctx:MiniJavaGrammarParser.ClassDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#parameter.
    def visitParameter(self, ctx:MiniJavaGrammarParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#fieldDeclaration.
    def visitFieldDeclaration(self, ctx:MiniJavaGrammarParser.FieldDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#localDeclaration.
    def visitLocalDeclaration(self, ctx:MiniJavaGrammarParser.LocalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#methodDeclaration.
    def visitMethodDeclaration(self, ctx:MiniJavaGrammarParser.MethodDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#parameterList.
    def visitParameterList(self, ctx:MiniJavaGrammarParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#methodBody.
    def visitMethodBody(self, ctx:MiniJavaGrammarParser.MethodBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#type.
    def visitType(self, ctx:MiniJavaGrammarParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#identifier.
    def visitIdentifier(self, ctx:MiniJavaGrammarParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#statement.
    def visitStatement(self, ctx:MiniJavaGrammarParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:MiniJavaGrammarParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#breakStatement.
    def visitBreakStatement(self, ctx:MiniJavaGrammarParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#continueStatement.
    def visitContinueStatement(self, ctx:MiniJavaGrammarParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#arrayAssignmentStatement.
    def visitArrayAssignmentStatement(self, ctx:MiniJavaGrammarParser.ArrayAssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#variableAssignmentStatement.
    def visitVariableAssignmentStatement(self, ctx:MiniJavaGrammarParser.VariableAssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#printStatement.
    def visitPrintStatement(self, ctx:MiniJavaGrammarParser.PrintStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#whileStatement.
    def visitWhileStatement(self, ctx:MiniJavaGrammarParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#ifElseStatement.
    def visitIfElseStatement(self, ctx:MiniJavaGrammarParser.IfElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#nestedStatement.
    def visitNestedStatement(self, ctx:MiniJavaGrammarParser.NestedStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#returnStatement.
    def visitReturnStatement(self, ctx:MiniJavaGrammarParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#methodCallStatement.
    def visitMethodCallStatement(self, ctx:MiniJavaGrammarParser.MethodCallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#objectInstantiationExpression.
    def visitObjectInstantiationExpression(self, ctx:MiniJavaGrammarParser.ObjectInstantiationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#arrayInstantiationExpression.
    def visitArrayInstantiationExpression(self, ctx:MiniJavaGrammarParser.ArrayInstantiationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#identifierExpression.
    def visitIdentifierExpression(self, ctx:MiniJavaGrammarParser.IdentifierExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#methodCallExpression.
    def visitMethodCallExpression(self, ctx:MiniJavaGrammarParser.MethodCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#notExpression.
    def visitNotExpression(self, ctx:MiniJavaGrammarParser.NotExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#divExpression.
    def visitDivExpression(self, ctx:MiniJavaGrammarParser.DivExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#greaterThanExpression.
    def visitGreaterThanExpression(self, ctx:MiniJavaGrammarParser.GreaterThanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#boolLitExpression.
    def visitBoolLitExpression(self, ctx:MiniJavaGrammarParser.BoolLitExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#orExpression.
    def visitOrExpression(self, ctx:MiniJavaGrammarParser.OrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#parenthesesExpression.
    def visitParenthesesExpression(self, ctx:MiniJavaGrammarParser.ParenthesesExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#andExpression.
    def visitAndExpression(self, ctx:MiniJavaGrammarParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#arrayAccessExpression.
    def visitArrayAccessExpression(self, ctx:MiniJavaGrammarParser.ArrayAccessExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#stringExpression.
    def visitStringExpression(self, ctx:MiniJavaGrammarParser.StringExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#addExpression.
    def visitAddExpression(self, ctx:MiniJavaGrammarParser.AddExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#fieldAccessExpression.
    def visitFieldAccessExpression(self, ctx:MiniJavaGrammarParser.FieldAccessExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#thisExpression.
    def visitThisExpression(self, ctx:MiniJavaGrammarParser.ThisExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#lessThanExpression.
    def visitLessThanExpression(self, ctx:MiniJavaGrammarParser.LessThanExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#equalityExpression.
    def visitEqualityExpression(self, ctx:MiniJavaGrammarParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#dotlengthExpression.
    def visitDotlengthExpression(self, ctx:MiniJavaGrammarParser.DotlengthExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#characterExpression.
    def visitCharacterExpression(self, ctx:MiniJavaGrammarParser.CharacterExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#integerLitExpression.
    def visitIntegerLitExpression(self, ctx:MiniJavaGrammarParser.IntegerLitExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#subExpression.
    def visitSubExpression(self, ctx:MiniJavaGrammarParser.SubExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#dotcharatExpression.
    def visitDotcharatExpression(self, ctx:MiniJavaGrammarParser.DotcharatExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#mulExpression.
    def visitMulExpression(self, ctx:MiniJavaGrammarParser.MulExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniJavaGrammarParser#methodCallParams.
    def visitMethodCallParams(self, ctx:MiniJavaGrammarParser.MethodCallParamsContext):
        return self.visitChildren(ctx)



del MiniJavaGrammarParser