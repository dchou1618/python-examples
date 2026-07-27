import pytest
from Algorithms.static_analysis.ast_tree import Node, find_calls, match


@pytest.mark.parametrize(
    "input_node, target, expected_count",
    (
        [
            (
                Node(
                    "Program",
                    children=[
                        Node(
                            "Call",
                            children=[Node("Name", "eval"), Node("Name", "user_input")],
                        ),
                        Node(
                            "Call",
                            children=[Node("Name", "print"), Node("String", "hello")],
                        ),
                        Node(
                            "Call",
                            children=[
                                Node("Name", "eval"),
                                Node(
                                    "IndexAccess",
                                    children=[
                                        Node(
                                            "AttributeAccess",
                                            children=[
                                                Node("Name", "request"),
                                                Node("Identifier", "args"),
                                            ],
                                        ),
                                        Node("String", "cmd"),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                "eval",
                2,
            )
        ]
    ),
)
def test_ast_tree(input_node, target, expected_count):
    result = find_calls(input_node, target)

    assert len(result) == expected_count


def test_rule_match_ast_tree():
    rule = Node("Call", children=[Node("Name", "eval"), Node("MetaVar", "X")])

    code = Node("Call", children=[Node("Name", "eval"), Node("Name", "user_input")])

    captures = {}

    result = match(rule, code, captures)
    assert result
    assert captures == {"X": Node("Name", "user_input")}
