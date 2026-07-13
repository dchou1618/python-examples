from Algorithms.static_analysis.rule_matcher import find_violations, find_violations_v2

def test_find_violations():
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

    expected_result = [{'line_number': 2, 'line': 'password = input()', 'pattern': 'password = input()', 'severity': 'HIGH'}]

    assert find_violations(code, rules) == expected_result

def test_find_violations_v2():
    code = [
        "import os",
        "eval(user_input)",
        "print(password)",
        "eval(request.args['cmd'])",
        "[eval(input1), eval(input2)]"
    ]

    rules = [
        {
            "pattern": "eval($X)",
            "severity": "HIGH"
        }
    ]

    expected_result = [
        {
            "line_number": 2,
            "pattern": "eval($X)",
            "severity": "HIGH",
            "captures": {
                "X": "user_input"
            }
        },
        {
            "line_number": 4,
            "pattern": "eval($X)",
            "severity": "HIGH",
            "captures": {
                "X": "request.args['cmd']"
            }
        }
    ]
    print("RESULT from find violations v2:",
          find_violations_v2(code, rules))
    assert find_violations_v2(code, rules) == expected_result