from abs_st import *
from tokens import token_types
from utils import arr_find, arr_part


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
            error_pos = self.tokens[self.pos].get_pos()
            raise Exception(f"на позиции {error_pos} ожидается {expected[0].name}")

        return token

    def parseFile(self) -> StatementsNode:
        root = StatementsNode()
        while self.pos < len(self.tokens):
            func = self.parseFunctionDeclaration()
            if func is None:
                func = self.parseVariableDeclaration()
                if func is not None:
                    self.require(token_types["SEMICOLON"])

            if func is None:
                error_pos = self.tokens[self.pos].get_pos()
                raise Exception(f"Ожидалось определение функции на позиции {error_pos}")
            root.nodes.append(func)
        return root

    def parseCode(self) -> ExpressionNode:
        root = StatementsNode()

        while self.pos < len(self.tokens):
            code_string_node = self.parseExpression()
            if isinstance(code_string_node, tuple):
                for n in code_string_node:
                    if isinstance(n, ForNode | WhileNode | IfNode | ElseNode):
                        self.__match(token_types["SEMICOLON"])
                    else:
                        self.require(token_types["SEMICOLON"])
                    root.add_node(n)
            else:
                if isinstance(code_string_node, ForNode | WhileNode | IfNode | ElseNode):
                    self.__match(token_types["SEMICOLON"])
                else:
                    self.require(token_types["SEMICOLON"])
                root.add_node(code_string_node)

        return root

    def parseExpression(self) -> ExpressionNode:
        if self.__match(token_types["ID"]) is None:
            if_stm = self.parseIf()
            if if_stm is not None:
                return if_stm

            while_stm = self.parseWhile()
            if while_stm is not None:
                return while_stm

            for_stm = self.parseFor()
            if for_stm is not None:
                return for_stm

        self.pos -= 1
        func_invoke = self.parseFunctionInvocation()
        if func_invoke is not None:
            return func_invoke

        variable_node = self.parseVariable()
        assign_operator = self.__match(token_types["ASSIGN"])

        if assign_operator is not None:
            right_formula_node = self.parseFormula()
            binary_node = BinOperationNode(assign_operator, variable_node, right_formula_node)
            return binary_node

        error_pos = self.tokens[self.pos].get_pos()
        raise Exception(f'После переменной ожидается оператор присвоения на позиции {str(error_pos)}')

    # Парсит переменные c присвоением значения, например myvar = 10;
    def parseVariableDeclaration(self) -> BinOperationNode:
        variable_node = self.parseVariable()
        assign_operator = self.__match(token_types["ASSIGN"])

        if assign_operator is not None:
            right_formula_node = self.parseFormula()
            binary_node = BinOperationNode(assign_operator, variable_node, right_formula_node)
            return binary_node

        error_pos = self.tokens[self.pos].get_pos()
        raise Exception(f'После переменной ожидается оператор присвоения на позиции {str(error_pos)}')

    def parseIf(self):
        operator_if = self.__match(token_types["IF"])
        if operator_if is not None:
            cond = self.parseConditionBlockWithBraces()
            inner_stms = self.parseBlock()

            else_node = self.parseElse()
            if else_node is not None:
                return IfNode(operator_if, cond, inner_stms), else_node
            else:
                return IfNode(operator_if, cond, inner_stms)

    def parseElse(self):
        operator_else = self.__match(token_types["ELSE"])
        if operator_else is not None:
            inner_stms = self.parseBlock()
            return ElseNode(operator_else, inner_stms)

    def parseWhile(self):
        operator_while = self.__match(token_types["WHILE"])
        if operator_while is not None:
            cond = self.parseConditionBlockWithBraces()

            inner_stms = self.parseBlock()
            return WhileNode(operator_while, cond, inner_stms)

    def parseFunctionInvocation(self):
        function_invocation_name = self.__match(token_types["ID"])
        if function_invocation_name is not None:
            left_br = self.__match(token_types["LBR"])
            if left_br is not None:
                func_var = self.parseFunctionInvocationVariables()
                self.require(token_types["RBR"])
                return FunctionInvokeNode(function_invocation_name, func_var)
            else:
                self.pos -= 1  # ошибочка выщла вообще то это не функция а переменная скорее всего поэтому возврат

    def parseFor(self):
        operator_for = self.__match(token_types["FOR"])
        if operator_for is not None:
            if operator_for is not None:
                self.require(token_types["LBR"])
                inner_cond_stms = [self.parseExpression()]
                self.require(token_types["SEMICOLON"])
                inner_cond_stms.append(self.parseFormula())
                self.require(token_types["SEMICOLON"])
                inner_cond_stms.append(self.parseExpression())
                self.require(token_types["RBR"])
                if not len(inner_cond_stms) == 3:
                    error_pos = self.tokens[self.pos].get_pos()
                    raise Exception(f"Ожидалось for(stms;stms;stms) позиции ({str(error_pos)})")
                else:
                    if (not isinstance(inner_cond_stms[0], BinOperationNode)
                            or not inner_cond_stms[0].operator.type == token_types["ASSIGN"]):
                        error_pos = self.tokens[self.pos].get_pos()[0]
                        raise Exception(f"Ожидалось определение переменной для for на строке {error_pos}")
                    if not isinstance(inner_cond_stms[1], LogicalOperationNode):
                        error_pos = self.tokens[self.pos].get_pos()[0]
                        raise Exception(f"Ожидалось условие для for на строке {error_pos}")
                    if (not isinstance(inner_cond_stms[0], BinOperationNode) or
                            not inner_cond_stms[0].operator.type == token_types["ASSIGN"]
                    ):
                        error_pos = self.tokens[self.pos].get_pos()[0]
                        raise Exception(f"Ожидалось изменение переменной для for на строке {error_pos}")

                inner_stms = self.parseBlock()
                return ForNode(operator_for, inner_cond_stms, inner_stms)

    # парсит (LogicalOperationNode)
    def parseConditionBlockWithBraces(self):
        self.require(token_types["LBR"])
        cond = self.parseFormula()

        if not isinstance(cond, LogicalOperationNode | VariableNode | BooleanNode):
            error_pos = self.tokens[self.pos].get_pos()
            raise Exception(f"Ожидалось условие или переменная на позиции {error_pos}")
        self.require(token_types["RBR"])

        return cond

    def parseFunctionDeclarationVariables(self):
        fd_vars = []
        var = self.__match(token_types["ID"])
        fd_vars.append(var)

        while var is not None:
            if self.__match(token_types["COMMA"]) is not None:
                var = self.require(token_types["ID"])
                fd_vars.append(var)
            else:
                break

        return fd_vars

    def parseFunctionInvocationVariables(self):
        fd_vars = []
        var = self.__match(token_types["ID"])
        try:
            if var is None:
                var = self.parseFormula()
        except Exception:
            pass
        fd_vars.append(var)

        while var is not None:
            if self.__match(token_types["COMMA"]) is not None:
                var = self.require(token_types["ID"])
                try:
                    if var is None:
                        var = self.parseFormula()
                except Exception:
                    pass
                fd_vars.append(var)
            else:
                break

        if fd_vars[0] == None:
            fd_vars = []
        return fd_vars

    def parseFunctionDeclaration(self):
        operator_fd = self.__match(token_types["FUNDEC"])
        if operator_fd is not None:
            fd_id = self.__match(token_types["ID"])
            if fd_id is None:
                error_pos = self.tokens[self.pos].get_pos()
                raise Exception(f"Ожидалось название функции на позиции {error_pos}")

            self.require(token_types["LBR"])
            fd_vars = self.parseFunctionDeclarationVariables()
            self.require(token_types["RBR"])

            fd_stms = self.parseBlock()

            return FunctionDeclarationNode(fd_id, fd_vars, fd_stms)

    def parseBlock(self) -> StatementsNode:
        self.require(token_types["LBCR"])
        try:
            inner_tokens = arr_part(self.tokens, self.pos,
                                    lambda x: x.type.name == token_types["RBCR"].name,
                                    lambda x: x.type.name == token_types["LBCR"].name)
            self.pos += len(inner_tokens)
            self.require(token_types["RBCR"])
        except Exception as e:
            error_pos = self.tokens[self.pos].get_pos()
            raise Exception(f"Ожидался {token_types['RBCR'].name} на позиции {error_pos}")

        parser = Parser(inner_tokens)
        inner_stms = parser.parseCode()
        return inner_stms

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

        error_pos = self.tokens[self.pos].get_pos()
        raise Exception(f"Ожидается переменная или литерал на позиции {error_pos}")

    def parseVariable(self) -> ExpressionNode:
        variable = self.__match(token_types["ID"])
        if variable is not None:
            return VariableNode(variable)

        error_pos = self.tokens[self.pos].get_pos()
        raise Exception(f"Ожидалась переменная на позиции {error_pos}")

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
                error_pos = self.tokens[self.pos].get_pos()
                raise Exception(f"Слева нелогическое справа логическое на позиции {error_pos}")
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
