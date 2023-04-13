
# Simple C-like Expression Evaluator

This is a simple expression evaluator that can parse and evaluate C-like arithmetic expressions. It supports addition, subtraction, multiplication, and division, as well as parentheses for specifying precedence.


## Features

- Tokenization of input expressions using regular expressions
- Parsing of arithmetic expressions to build an abstract syntax tree (AST)
- Evaluation of the generated AST to produce the result


## Usage

The following example demonstrates how to use the expression evaluator:

```bash
from simple_c_evaluator import compile_c_code

c_code = "3 + 4 * (2 - 1);"
result = compile_c_code(c_code)

print(result)
```


## Functions

- lexer(code: str) -> List[Tuple[str, str]]: Tokenizes the input code and returns a list of tokens.
- compile_c_code(code: str) -> float: Compiles and evaluates the input code, returning the result as a float.
## Classes

- Parser: A parser for arithmetic expressions, responsible for building the AST.
- ExpressionEvaluator: An evaluator for arithmetic expressions, responsible for evaluating the AST and returning the result.
## Limitations

- Only supports simple arithmetic expressions with the four basic operators (+, -, *, /).
- No support for variables or more complex expressions.
