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


class UnarOperationNode(ExpressionNode):
    def __init__(self, operator: Token, operand: ExpressionNode):
        self.operator = operator
        self.operand = operand


class NumberNode(ExpressionNode):
    def __init__(self, number):
        self.number = number


def print_ast(node: ExpressionNode, level=-1):
    offset_char = "- "
    if isinstance(node, StatementsNode):
        for i in node.nodes:
            print_ast(i, level + 1)
            print('\n')
        return
    if isinstance(node, VariableNode):
        print((offset_char * level) + str(node.variable))
        return
    if isinstance(node, NumberNode):
        print((offset_char * level) + str(node.number))
        return
    if isinstance(node, UnarOperationNode):
        print((offset_char * level) + str(node.operator))
        print_ast(node.operand, level+1)
        return
    if isinstance(node, BinOperationNode):
        print((offset_char * level) + str(node.operator))
        print_ast(node.left, level+1)
        print_ast(node.right, level+1)
        return
