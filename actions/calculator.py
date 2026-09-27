"""
calculator.py — safe math expression evaluator for X Jarvis.

Evaluates arithmetic expressions using Python's ast module (no eval of
arbitrary code). Supports +, -, *, /, //, %, **, parentheses, and common
math functions: sqrt, sin, cos, tan, log, log10, exp, abs, round, floor,
ceil, pi, e.
"""
import ast
import math
import operator
from typing import Any


# Allowed operators
_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed functions and constants (no builtins that can escape)
_FUNCS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
    "pi": math.pi,
    "e": math.e,
}


def _safe_eval(node: ast.AST) -> Any:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value!r}")
    if isinstance(node, ast.Num):  # older Python
        return node.n
    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op = _BIN_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
        return op(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op = _UNARY_OPS.get(type(node.op))
        if op is None:
            raise ValueError(f"Unsupported unary: {type(node.op).__name__}")
        return op(operand)
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names are allowed")
        name = node.func.id
        if name not in _FUNCS:
            raise ValueError(f"Function not allowed: {name}")
        func = _FUNCS[name]
        if not callable(func):
            # constants used as "func" by mistake
            raise ValueError(f"{name} is not a function")
        args = [_safe_eval(a) for a in node.args]
        if node.keywords:
            raise ValueError("Keyword arguments not allowed")
        return func(*args)
    if isinstance(node, ast.Name):
        if node.id in _FUNCS and not callable(_FUNCS[node.id]):
            return _FUNCS[node.id]
        raise ValueError(f"Unknown name: {node.id}")
    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def evaluate(expression: str) -> str:
    expr = (expression or "").strip()
    if not expr:
        return "Please give me a math expression to calculate."
    # Light sanitisation: allow only safe characters
    allowed = set("0123456789.+-*/%()^, eEsqrtincostanlogabroundfloorceilpi")
    # spaces ok
    cleaned = "".join(c for c in expr if c.isalnum() or c in " .+*-/%()^,")
    if not cleaned:
        return "That does not look like a math expression."
    try:
        tree = ast.parse(cleaned, mode="eval")
        result = _safe_eval(tree)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"{expr} = {result}"
    except Exception as e:
        return f"Could not calculate that: {e}"


def calculator(parameters: dict, player=None, session_memory=None) -> str:
    params = parameters or {}
    expression = params.get("expression", "") or params.get("expr", "") or params.get("math", "")

    result = evaluate(expression)

    if player:
        try:
            player.write_log(f"[Calc] {result[:80]}")
        except Exception:
            pass

    return result


# ── Tool declaration (auto-discovered by core/action_loader.py) ──────────────
TOOL = {
    "name": "calculator",
    "description": (
        "Evaluates a mathematical expression safely. Supports +, -, *, /, //, %, **, "
        "parentheses, and functions: sqrt, sin, cos, tan, log, log10, exp, abs, round, "
        "floor, ceil, and constants pi, e. Use for any arithmetic or simple scientific calculation."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "expression": {
                "type": "STRING",
                "description": "The math expression to evaluate, e.g. '2 + 3 * 4', 'sqrt(16)', 'sin(pi/2)'",
            },
        },
        "required": ["expression"],
    },
    "handler": calculator,
}
