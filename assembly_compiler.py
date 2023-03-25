import re

# Lexer
TOKENS = [
    ('NUMBER', r'\d+(\.\d+)?'),
    ('OPERATOR', r'(\+|\-|\*|\/)'),
    ('WHITESPACE', r'\s+'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('SEMICOLON', r';'),
]

def lexer(code):
    tokens = []
    code = code.strip()

    while code:
        for token_type, pattern in TOKENS:
            match = re.match(pattern, code)
            if match:
                token = (token_type, match.group(0))
                tokens.append(token)
                code = code[match.end():].strip()
                break
        else:
            raise ValueError(f"Unexpected character: {code[0]}")
    return tokens

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        expr = self.parse_expression()
        if self._peek_token_type() == 'SEMICOLON':
            self._next_token()
        return expr

    def parse_expression(self):
        left = self.parse_term()

        while self._peek_token_type() == 'OPERATOR':
            op_token = self._next_token()
            right = self.parse_term()
            left = (op_token, left, right)

        return left

    def parse_term(self):
        token = self._next_token()

        if token[0] == 'NUMBER':
            return token
        elif token[0] == 'LPAREN':
            expression = self.parse_expression()
            self._expect_token_type('RPAREN')
            return expression

    def _next_token(self):
        if self.index < len(self.tokens):
            token = self.tokens[self.index]
            self.index += 1
            return token
        return None

    def _peek_token_type(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index][0]
        return None

    def _expect_token_type(self, token_type):
        token = self._next_token()
        if token[0] != token_type:
            raise ValueError(f"Expected {token_type}, but got {token[0]}")

# Code generator
class CodeGenerator:
    def __init__(self):
        self.assembly_code = []

    def generate(self, ast):
        self._generate_expression(ast)
        self.assembly_code.append('ret')
        return '\n'.join(self.assembly_code)

    def _generate_expression(self, node):
        if isinstance(node, tuple) and len(node) == 3:
            op, left, right = node
            self._generate_expression(left)
            self.assembly_code.append('push eax')
            self._generate_expression(right)
            self.assembly_code.append('pop ebx')
            self._generate_operator(op[1])
        elif node[0] == 'NUMBER':
            self.assembly_code.append(f'mov eax, {node[1]}')

    def _generate_operator(self, op):
        if op == '+':
            self.assembly_code.append('add eax, ebx')
        elif op == '-':
            self.assembly_code.append('sub eax, ebx')
        elif op == '*':
            self.assembly_code.append('imul eax, ebx')
        elif op == '/':
            self.assembly_code.append('cdq')  # Sign-extend EAX into EDX:EAX
            self.assembly_code.append('idiv ebx')  # Divide EDX:EAX by EBX
        else:
            raise ValueError(f"Unknown operator: {op}")

# Compiler
def compile_c_code(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()
    codegen = CodeGenerator()
    assembly_code = codegen.generate(ast)
    return assembly_code

# Example usage
c_code = "3 + 4 * (2 - 1);"
assembly_code = compile_c_code(c_code)
print(assembly_code)

