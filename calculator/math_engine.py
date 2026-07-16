import ast
import operator


# Allowed operations
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod
}


def calculate(expression):

    try:

        expression = expression.replace("^", "**")

        tree = ast.parse(
            expression,
            mode="eval"
        )


        result = evaluate(tree.body)

        return f"{expression} = {result}"


    except Exception:

        return "I couldn't calculate that."


def evaluate(node):

    if isinstance(node, ast.Num):

        return node.n


    elif isinstance(node, ast.BinOp):

        operation = operators[type(node.op)]

        return operation(
            evaluate(node.left),
            evaluate(node.right)
        )


    else:

        raise ValueError("Invalid expression")