from abs_st import *
from abs_st import ExpressionNode


# Просто парсит ноды в почти аналогичный код на JS
# Не проверяет области видимости
# И вообще ничего не проверяет, кажется, это вообще не задача генератора кода
# Но если что, можно добавить лэйер семантической проверки между парсером и генератором
# Ну или просто впилить её сюда, хотя, как по мне, не к месту, если посмотреть референсы генераторов

class CodeGenerator:

    def __init__(self, nodes: ExpressionNode):
        self.root_node = nodes
        self.result_code = ""
        self.standard_function = \
            {"PRINT": "console.log"}

    def generate(self):
        """
        Инициирует обход корневой ноды
        :return:
        """
        try:
            print("[+] Generating code...")
            self.result_code = self.generate_from_node(self.root_node.nodes)
            print("[+] Generated")
        except Exception as e:
            print(e)
            print('[-] Code generator Error. Exiting...')
            exit(1)

    def generate_from_node(self, nodes, result_code=""):
        '''
        Проходит по массиву нод, заходит на рекурсию там, когда попадаем в новый скоуп
        Всего понимает инстансы UnarOperationNode - как я понял вызов функции,
        BinOperationNode - парсит сложные выражения
        IfNode и WhileNode - переход в скоуп условных и циклов
        :param nodes:
        :param result_code:
        :return:
        '''
        for node in nodes:
            if isinstance(node, FunctionDeclarationNode):
                tmp_code = f"function {node.token.text}({self.parse_func_arguments(node.variables)}) {{\n"
                # result_code += f"function {node.token.text}({self.parse_func_arguments(node.variables)}) {{"
                # result_code += "\n"
                result_code += self.generate_from_node(node.stms.nodes, tmp_code)
                result_code += "}"
                result_code += "\n"

            if isinstance(node, FunctionInvokeNode):
                result_code += f"{node.token.text}({self.parse_func_arguments(node.variables)})"
                result_code += "\n"

            if isinstance(node, PrintNode):
                result_code += f"{node.token.text}({self.get_data_from_node_by_instance(node.argument)})"
                result_code += "\n"

            if isinstance(node, UnarOperationNode):
                if node.operator.type.name in self.standard_function.keys():
                    result_code += f"{self.standard_function[node.operator.type.name]}({self.parce_binary_expression_from_node(node.operand, '')})"
                    result_code += "\n"

            if isinstance(node, BinOperationNode):
                result_code += self.parce_binary_expression_from_node(node, '')
                result_code += "\n"

            if isinstance(node, IfNode):
                result_code += f"if({self.parce_binary_expression_from_node(node.cond, '')}) {{"
                result_code += "\n"
                result_code = self.generate_from_node(node.stms.nodes, result_code)
                result_code += "}"
                result_code += "\n"

            if isinstance(node, ElseNode):
                result_code += f"else {{"
                result_code += "\n"
                result_code = self.generate_from_node(node.stms.nodes, result_code)
                result_code += "}"
                result_code += "\n"

            if isinstance(node, WhileNode):
                result_code += f"while({self.parce_binary_expression_from_node(node.cond, '')}) {{"
                result_code += "\n"
                result_code = self.generate_from_node(node.stms.nodes, result_code)
                result_code += "}"
                result_code += "\n"

            if isinstance(node, ForNode):
                params = ''
                for condition in node.cond:
                    params += self.parce_binary_expression_from_node(condition, '') + ';'
                result_code += f"for({params[0:-1]}) {{"
                result_code += "\n"
                result_code = self.generate_from_node(node.stms.nodes, result_code)
                result_code += "}"
                result_code += "\n"

        return result_code

    def parce_binary_expression_from_node(self, node: ExpressionNode, generated_code: str):
        """
        Парсит бинарные выражения
        :param node:
        :param generated_code:
        :return:
        """
        node_data = self.get_data_from_node_by_instance(node)
        if node_data:
            return node_data
        else:
            generated_code += (self.parce_binary_expression_from_node(node.left, generated_code)
                               + ' ' + str(node.operator.text) + ' ' + self.parce_binary_expression_from_node(
                        node.right, generated_code))
            return generated_code

    def get_data_from_node_by_instance(self, node: ExpressionNode):
        """
            Определяет некоторые инстансы ноды, возвращает строку с представлением ее значащей части
                или None если инстанс не входит в перечень
                [VariableNode, NumberNode, StringNode, BooleanNode]
        :param node: ExpressionNode
        :return: str || None
        """
        if isinstance(node, VariableNode):
            return str(node.variable.text)
        if isinstance(node, NumberNode):
            return str(node.number.text)
        if isinstance(node, StringNode):
            return "'" + str(node.string.text) + "'"
        if isinstance(node, BooleanNode):
            return str(node.boolean.text)
        return None

    def parse_func_arguments(self, param_list: list[Token]):
        if len(param_list) != 0 and param_list[0] is None:
            return ''
        else:
            parameters = ""
            for var in param_list:
                if isinstance(var, Token):
                    parameters += var.text + ' '
                elif isinstance(var, BinOperationNode):
                    parameters += self.parce_binary_expression_from_node(var, '').replace(" ", "")
                else:
                    parameters += self.get_data_from_node_by_instance(var) + ' '
            parameters = parameters.strip()
            return parameters.replace(' ', ', ')

    def write_generated_code(self, result_file_path):  # пока просто выводит в консоль
        with open(result_file_path, 'w') as file:
            file.write(self.result_code)
