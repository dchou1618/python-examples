from typing import List, Dict
import re

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

def compile_rule(pattern):
    METAVAR = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")
    captures = []
    regex_parts = []
    last = 0
    for match in METAVAR.finditer(pattern):
        regex_parts.append(re.escape(pattern[last:match.start()]))
        name = match.group(1)
        captures.append(name)

        regex_parts.append(f"(?P<{name}>.*?)")
        last = match.end()
    regex_parts.append(re.escape(pattern[last:]))
    return re.compile("^"+"".join(regex_parts)+"$"), captures

def find_violations_v2(code: List[str], rules: List[Dict]) -> List[Dict]:
    """
    Support wildcards
    """
    compiled_rules = []
    for rule in rules:
        regex_parts, captures = compile_rule(rule["pattern"])
        compiled_rules.append({
            "regex": regex_parts,
            "captures": captures,
            "severity": rule["severity"],
            "pattern": rule["pattern"]
        })
    violations = []
    for line_number, line in enumerate(code):
        for rule in compiled_rules:
            match = rule["regex"].match(line)
            if match:
                violations.append(
                    {
                        "line_number": line_number + 1,
                        "pattern": rule["pattern"],
                        "severity": rule["severity"],
                        "captures": match.groupdict()
                    }
                )
    return violations



