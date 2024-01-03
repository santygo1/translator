from abs_st import *


class ScopeFrame:
    def __init__(self, global_names):
        self.global_names = global_names
        self.local_names = []

    def add_local(self, name):
        self.local_names.append(name)

    def is_name_in_scope(self, name):
        # return name in self.global_names or name in self.local_names
        for token in self.local_names + self.global_names:
            if token.text == name.text:
                return True
        return False

    def debug_print_frame(self):
        print('local: ', self.local_names)
        print('global: ', self.global_names)


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if len(self.stack) == 0:
            return None
        removed = self.stack.pop()
        return removed

    def current_frame(self) -> ScopeFrame:
        return self.stack[-1]

    def load_new_frame(self):
        self.push(ScopeFrame(self.current_frame().global_names + self.current_frame().local_names))


class SemanticAnalyzer:

    def __init__(self, nodes: ExpressionNode):
        self.root_node = nodes
        self.scope_stack = Stack()
        self.scope_stack.push(ScopeFrame([]))

    def analyze(self):
        try:
            print("[+] Semantic analyze started...")
            self.analyze_scope(self.root_node.nodes)
            print("[+] Semantic analyze passed")
        except Exception as e:
            print(e)
            print('[-] Semantic Error. Exiting...')
            exit(1)

    def analyze_scope(self, nodes):
        for node in nodes:
            if isinstance(node, FunctionDeclarationNode):
                self.scope_stack.current_frame().add_local(node.token)  # добавляем новую локальную переменную в текущий кадр
                self.add_func_params(node.variables)
                self.scope_stack.load_new_frame()  # загружаем новый кадр в стек
                self.analyze_scope(node.stms.nodes)  # идем проверять новый scope
                continue

            if isinstance(node, FunctionInvokeNode):
                if not self.scope_stack.current_frame().is_name_in_scope(node.token):
                    raise Exception(f'[-] <Uncaught ReferenceError> {node.token.text} в позиции {node.token.get_pos()}')
                for token in node.variables:
                    self.check_node(token)
                continue

            if isinstance(node, PrintNode):
                self.check_node(node.argument)
                continue

            if isinstance(node, BinOperationNode):
                self.check_node(node)
                continue

            if isinstance(node, IfNode):
                self.check_node(node.cond)
                self.scope_stack.load_new_frame()
                self.analyze_scope(node.stms.nodes)
                continue

            if isinstance(node, ElseNode):
                self.scope_stack.load_new_frame()
                self.analyze_scope(node.stms.nodes)
                continue

            if isinstance(node, WhileNode):
                self.check_node(node.cond)
                self.scope_stack.load_new_frame()
                self.analyze_scope(node.stms.nodes)
                continue

            if isinstance(node, ForNode):
                self.scope_stack.load_new_frame()
                for condition in node.cond:
                    self.check_node(condition)
                self.analyze_scope(node.stms.nodes)
                continue

            # self.debug()

        self.scope_stack.pop()  # выходим из scope, выталкиваем кадр из стека

    def check_node(self, node):
        if isinstance(node, Token):
            if not self.scope_stack.current_frame().is_name_in_scope(node): # чекаем ее
                raise Exception(f'[-] <Uncaught ReferenceError> {node.text} в позиции {node.get_pos()}')
        if isinstance(node, BinOperationNode):
            if node.operator.type.name == "ASSIGN":
                self.scope_stack.current_frame().add_local(node.left.variable)
                self.recurse_check_expression_variables(node.right)
            else:
                self.recurse_check_expression_variables(node)
        else:
            self.recurse_check_expression_variables(node)

    def add_func_params(self, param_list: list[Token]):
        if len(param_list) != 0 and param_list[0] is not None:
            for var in param_list:
                self.scope_stack.current_frame().add_local(var)

    def recurse_check_expression_variables(self, node):
        node_data = self.is_it_variable_node(node)
        if node_data:
            if not self.scope_stack.current_frame().is_name_in_scope(node_data): # чекаем ее
                raise Exception(f'[-] <Uncaught ReferenceError> {node_data.text} в позиции {node.variable.get_pos()}')
        else:
            if not isinstance(node, BinOperationNode):
                return
            else:
                self.recurse_check_expression_variables(node.left)
                self.recurse_check_expression_variables(node.right)

    def is_it_variable_node(self, node: ExpressionNode):
        if isinstance(node, VariableNode):
            return node.variable
        return None

    def debug(self):
        self.scope_stack.current_frame().debug_print_frame()
