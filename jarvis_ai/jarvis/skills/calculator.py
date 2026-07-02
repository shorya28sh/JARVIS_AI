"""
skills/calculator.py — Safe maths evaluator.
"""

import re


def run(command: str, settings) -> dict:
    expr = _extract_expression(command)
    if not expr:
        return {"reply": "Please give me a mathematical expression to calculate."}

    try:
        # Safe eval — only allow numbers and operators
        safe = re.sub(r'[^0-9+\-*/().% ]', '', expr)
        if not safe.strip():
            return {"reply": "I couldn't find a valid expression to calculate."}
        result = eval(safe)  # noqa: S307
        return {"reply": f"The answer is {result}"}
    except ZeroDivisionError:
        return {"reply": "Cannot divide by zero!"}
    except Exception:
        return {"reply": f"I couldn't calculate that. Please rephrase the expression."}


def _extract_expression(command: str) -> str:
    for kw in ["calculate", "compute", "what is", "how much is",
               "hisab karo", "kitna hai"]:
        command = command.replace(kw, "")
    # Convert words to symbols
    command = (command
               .replace("plus", "+").replace("minus", "-")
               .replace("times", "*").replace("multiplied by", "*")
               .replace("divided by", "/").replace("percent", "%")
               .replace("x", "*"))
    return command.strip()
