from abs_st import *
from tokens import token_types
from utils import arr_find


class Parser:

    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.scope = {}

    def __match(self, *expected) -> Token | None:
        if self.pos < len(self.tokens):
            cur_token = self.tokens[self.pos]

            if arr_find(lambda t: t.name == cur_token.type.name, expected):
                self.pos += 1
                return cur_token
        return None

    def require(self, *expected) -> Token:
        token = self.__match(*expected)
        if not token:
            raise Exception(f"на позиции {self.pos} ожидается {expected[0].name}")

        return token

    def parseCode(self) -> ExpressionNode:
        root = StatementsNode()

        while self.pos < len(self.tokens):
            code_string_node = self.parseExpression()
            self.require(token_types["SEMICOLON"])
            root.add_node(code_string_node)

        return root

    def parseExpression(self) -> ExpressionNode:
        if self.__match(token_types["ID"]) is None:
            print_node = self.parsePrint()
            return print_node

        self.pos -= 1
        variable_node = self.parseVariable()
        assign_operator = self.__match(token_types["ASSIGN"])

        if assign_operator is not None:
            right_formula_node = self.parseFormula()
            binary_node = BinOperationNode(assign_operator, variable_node, right_formula_node)
            return binary_node

        raise Exception(f'После переменной ожидается оператор присвоения на позиции ${self.pos}')

    def parseVariableOrNumberOrStringOrBoolean(self) -> ExpressionNode:
        number = self.__match(token_types["INT-LITERAL"], token_types["FLOAT-LITERAL"])

        if number is not None:
            return NumberNode(number)

        variable = self.__match(token_types["ID"])
        if variable is not None:
            return VariableNode(variable)

        string = self.__match(token_types["STRING-LITERAL"])
        if string is not None:
            return StringNode(string)

        boolean = self.__match(token_types["BOOLEAN-LITERAL"])
        if boolean is not None:
            return BooleanNode(boolean)

        raise Exception(f"Ожидается переменная или число или бул или стринг на {self.pos} позиции")

    def parseVariable(self) -> ExpressionNode:
        variable = self.__match(token_types["ID"])
        if variable is not None:
            return VariableNode(variable)

        raise Exception(f"Ожидалась переменная")

    def parsePrint(self) -> ExpressionNode:
        operator_log = self.__match(token_types["PRINT"])
        if operator_log is not None:
            return UnarOperationNode(operator_log, self.parseFormula())

        raise Exception(f'Ожидается унарный оператор КОНСОЛЬ на ${self.pos} позиции')

    def parseParentheses(self) -> ExpressionNode:
        if self.__match(token_types['LBR']) is not None:
            node = self.parseFormula()
            self.require(token_types["RBR"])
            return node
        else:
            return self.parseVariableOrNumberOrStringOrBoolean()

    def parseFormula(self) -> ExpressionNode:
        left_node = self.parseParentheses()

        operator = self.__match(token_types["MINUS"],
                                token_types["PLUS"],
                                token_types["MULT"],
                                token_types["DIV"],
                                token_types["E"],
                                token_types["NE"],
                                token_types["L"],
                                token_types["LE"],
                                token_types["G"],
                                token_types["GE"],
                                token_types["AND"],
                                token_types["OR"])

        if (operator is not None
                and not isinstance(left_node, LogicalOperationNode) and
                (operator.type == token_types["E"] or
                 operator.type == token_types["NE"] or
                 operator.type == token_types["L"] or
                 operator.type == token_types["LE"] or
                 operator.type == token_types["G"] or
                 operator.type == token_types["GE"])):
            right_node = self.parseParentheses()
            if isinstance(right_node, LogicalOperationNode | BooleanNode):
                raise Exception("Слева нелогическое справа логическое")
            left_node = LogicalOperationNode(operator, left_node, right_node)
            operator = self.__match(token_types["OR"], token_types["AND"])

        while operator is not None:
            right_node = self.parseParentheses()

            if (isinstance(left_node, BinOperationNode) and
                    (operator.type == token_types["MULT"] or
                     operator.type == token_types["DIV"])):
                right_node = BinOperationNode(operator, left_node.right, right_node)
                operator = left_node.operator
                left_node = left_node.left

            if operator.type == token_types["AND"] or operator.type == token_types["OR"]:
                if isinstance(left_node, LogicalOperationNode | BooleanNode) and \
                        not isinstance(right_node, LogicalOperationNode | BooleanNode):
                    raise Exception(f"Ожидалось логическое выражение на позиции {self.pos}")
                else:
                    left_node = LogicalOperationNode(operator, left_node, right_node)
                    operator = self.__match(token_types["OR"], token_types["AND"])
            else:
                left_node = BinOperationNode(operator, left_node, right_node)
                operator = self.__match(token_types["MINUS"],
                                        token_types["PLUS"],
                                        token_types["MULT"],
                                        token_types["DIV"],
                                        token_types["E"],
                                        token_types["NE"],
                                        token_types["L"],
                                        token_types["LE"],
                                        token_types["G"],
                                        token_types["GE"]
                                        )
        return left_node


    # запуск парсера(Плохо работает на логических выражениях)
    def run(self, node: ExpressionNode):
        if isinstance(node, NumberNode):
            return int(node.number.text)

        if isinstance(node, BooleanNode):
            return bool(node.boolean.text)

        if isinstance(node, StringNode):
            return node.string.text

        if isinstance(node, UnarOperationNode):
            if node.operator.type.name == token_types["PRINT"].name:
                print(self.run(node.operand))
                return

        if isinstance(node, BinOperationNode):

            if node.operator.type.name == token_types["PLUS"].name:
                return self.run(node.left) + self.run(node.right)
            if node.operator.type.name == token_types["MINUS"].name:
                return self.run(node.left) - self.run(node.right)
            if node.operator.type.name == token_types["MULT"].name:
                return self.run(node.left) * self.run(node.right)
            if node.operator.type.name == token_types["DIV"].name:
                return self.run(node.left) / self.run(node.right)

            if node.operator.type.name == token_types["E"].name:
                return self.run(node.left) == self.run(node.right)
            if node.operator.type.name == token_types["NE"].name:
                return not (self.run(node.left) == self.run(node.right))
            if node.operator.type.name == token_types["G"].name:
                return self.run(node.left) > self.run(node.right)
            if node.operator.type.name == token_types["L"].name:
                return self.run(node.left) < self.run(node.right)
            if node.operator.type.name == token_types["LE"].name:
                return self.run(node.left) <= self.run(node.right)
            if node.operator.type.name == token_types["GE"].name:
                return self.run(node.left) >= self.run(node.right)

            if node.operator.type.name == token_types["ASSIGN"].name:
                result = self.run(node.right)
                variable_node = node.left
                self.scope[variable_node.variable.text] = result
                return result

        if isinstance(node, VariableNode):
            if self.scope[node.variable.text]:
                return self.scope[node.variable.text]
            else:
                raise Exception(f'Переменная с названием {node.variable.text} не обнаружена')

        if isinstance(node, StatementsNode):
            for n in node.nodes:
                self.run(n)
            return

        raise Exception('Ошибка!')
