from tokens import Token


class ExpressionNode:
    pass


class StatementsNode(ExpressionNode):

    def __init__(self):
        self.nodes = []

    def add_node(self, node: ExpressionNode):
        self.nodes.append(node)


class VariableNode(ExpressionNode):
    def __init__(self, variable: Token):
        self.variable = variable


class BinOperationNode(ExpressionNode):

    def __init__(self,
                 operator: Token,
                 left: ExpressionNode,
                 right: ExpressionNode):
        self.operator = operator
        self.left = left
        self.right = right


class LogicalOperationNode(BinOperationNode):
    pass


class UnarOperationNode(ExpressionNode):
    def __init__(self, operator: Token, operand: ExpressionNode):
        self.operator = operator
        self.operand = operand


class NumberNode(ExpressionNode):
    def __init__(self, number: Token):
        self.number = number


class StringNode(ExpressionNode):
    def __init__(self, string: Token):
        string.text = string.text.replace("\"", "")  # Удаляем лишние ковычки
        self.string = string


class BooleanNode(ExpressionNode):
    def __init__(self, boolean: Token):
        self.boolean = boolean


class IfNode(ExpressionNode):
    def __init__(self, token: Token, cond: LogicalOperationNode, stms: StatementsNode):
        self.token = token
        self.cond = cond
        self.stms = stms

class ElseNode(ExpressionNode):
    def __init__(self, token: Token, stms: StatementsNode):
        self.token = token
        self.stms = stms

class WhileNode(ExpressionNode):
    def __init__(self, token: Token, cond: LogicalOperationNode, stms: StatementsNode):
        self.token = token
        self.cond = cond
        self.stms = stms

class PrintNode(ExpressionNode):
    def __init__(self, token: Token, argument:ExpressionNode):
        self.token = token
        self.argument = argument

class ForNode(ExpressionNode):
    def __init__(self, token: Token, cond_stms, stms: StatementsNode):
        self.token = token
        self.cond = cond_stms
        self.stms = stms
class FunctionDeclarationNode(ExpressionNode):
    def __init__(self, id: Token, variables: list[Token], stms: StatementsNode):
        self.variables = variables
        self.token = id
        self.stms = stms

class FunctionInvokeNode(ExpressionNode):
    def __init__(self, id:Token, variables: list[Token]):
        self.token = id
        self.variables = variables


def print_ast(node: ExpressionNode, level=-1):
    offset_char = "-\t"
    if isinstance(node, StatementsNode):
        for i in node.nodes:
            print_ast(i, level + 1)
        return
    if isinstance(node, VariableNode):
        print((offset_char * level) + str(node.variable))
        return
    if isinstance(node, NumberNode):
        print((offset_char * level) + str(node.number))
        return
    if isinstance(node, StringNode):
        print((offset_char * level) + str(node.string))
        return
    if isinstance(node, BooleanNode):
        print((offset_char * level) + str(node.boolean))
        return
    if isinstance(node, UnarOperationNode):
        print(str(offset_char * level) + "UnarOperation: " + str(node.operator))
        print_ast(node.operand, level + 1)
        return
    if isinstance(node, BinOperationNode):
        if isinstance(node, LogicalOperationNode):
            print(str(offset_char * level) + "LogicalOperation: " + str(node.operator))
        else:
            print(str(offset_char * level) + "BinOperation: " + str(node.operator))

        print(str(offset_char * level) + "left: ")
        print_ast(node.left, level + 1)
        print(str(offset_char * level) + "right: ")
        print_ast(node.right, level + 1)
        return
    if isinstance(node, PrintNode):
        print(str(offset_char * level) + "PrintStatement: " + str(node.token))
        print(str(offset_char * (level+1)) + "Argument:")
        print_ast(node.argument, level + 1)
    if isinstance(node, IfNode):
        print(str(offset_char * level) + "IfStatement: " + str(node.token))
        print(str(offset_char * level) + "Condition: ")
        print_ast(node.cond, level + 1)
        print(str(offset_char * level) + "Stms: ")
        print_ast(node.stms, level + 1)
        return
    if isinstance(node, ElseNode):
        print(str(offset_char * level) + "ElseStatement: " + str(node.token))
        print(str(offset_char * level) + "Stms: ")
        print_ast(node.stms, level + 1)
        return
    if isinstance(node, WhileNode):
        print(str(offset_char * level) + "WhileNode: " + str(node.token))
        print(str(offset_char * level) + "Condition: ")
        print_ast(node.cond, level + 1)
        print(str(offset_char * level) + "Stms: ")
        print_ast(node.stms, level + 1)
        return
    if isinstance(node, ForNode):
        print(str(offset_char * level) + "FOR: " + str(node.token))
        print(str(offset_char * level) + "Condition: ")
        for i in node.cond:
            print_ast(i, level+1)
        print(str(offset_char * level) + "Stms: ")
        print_ast(node.stms, level+1)
    if isinstance(node, FunctionDeclarationNode):
        print(str(offset_char * level) + "FunctionDeclaration: " + str(node.token))
        print(str(offset_char * level) + "Variables:")
        for v in node.variables:
            print(str(offset_char * level) + "- VAR: " + str(v))
        print(str(offset_char * level) + "Stms:")
        print_ast(node.stms, level + 1)
    if isinstance(node, FunctionInvokeNode):
        print(str(offset_char * level) + "FunctionInvocation: " + str(node.token))
        print(str(offset_char * (level+1)) + "Variables:")
        for v in node.variables:
            if isinstance(v, Token):
                print(str(offset_char * level) + " token: " + str(v))
            else:
                print_ast(v, level+1)


