from typing import List

def find_violations(code: List[str], rules: List[str]):
    """
    This function takes a list of code lines and a list of rules, and returns a list of violations found in the code.
    """
    violations = []
    for rule in rules:
        pattern = rule["pattern"]
        severity = rule["severity"]
        for line_number, line in enumerate(code):
            if pattern in line:
                violations.append({
                    "line_number": line_number + 1,
                    "line": line,
                    "pattern": pattern,
                    "severity": severity
                })
    return violations

code = [
    "import os",
    "password = input()",
    "print(password)"
]

rules = [
    {
      "pattern": "password = input()",
      "severity": "HIGH"
    }
]

print(find_violations(code, rules))

