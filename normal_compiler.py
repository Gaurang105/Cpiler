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

# Expression Evaluator
class ExpressionEvaluator:
    def __init__(self):
        pass

    def evaluate(self, ast):
        return self._evaluate_expression(ast)

    def _evaluate_expression(self, node):
        if isinstance(node, tuple) and len(node) == 3:
            op, left, right = node
            left_value = self._evaluate_expression(left)
            right_value = self._evaluate_expression(right)
            return self._evaluate_operator(op[1], left_value, right_value)
        elif node[0] == 'NUMBER':
            return float(node[1])

    def _evaluate_operator(self, op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        else:
            raise ValueError(f"Unknown operator: {op}")

# Compiler
def compile_c_code(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    ast = parser.parse()
    evaluator = ExpressionEvaluator()
    result = evaluator.evaluate(ast)
    return result

# Example usage
c_code = "3 + 4 * (2 - 1);"
result = compile_c_code(c_code)
print(result)  # Output: 7.0

