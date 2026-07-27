from typing import Dict


class Node:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        if self.value:
            return f"{self.node_type}({self.value})"
        return f"{self.node_type}({self.children})"

    def __eq__(self, other):
        return (
            self.node_type == other.node_type
            and self.value == other.value
            and self.children == other.children
        )


def find_calls(root: Node, function_name: str):
    """
    This function takes AST root and function name as input and returns all function calls in the AST.
    First child node is the name of the function
    """
    calls = []

    def gather_calls(root, function_name):
        if root:
            if root.node_type == "Call":
                if (
                    root.children
                    and root.children[0].node_type == "Name"
                    and root.children[0].value == function_name
                ):
                    calls.append(root)
            for child in root.children:
                gather_calls(child, function_name)

    gather_calls(root, function_name)
    return calls


def match(rule_node: Node, code_node: Node, captures: Dict[str, Node]):
    """
    Returns True if code_node matches rule_node.

    captures should be populated with metavariable bindings.
    """
    if rule_node is None or code_node is None:
        return rule_node is code_node

    if rule_node.node_type == "MetaVar":
        name = rule_node.value
        if name in captures:
            return captures[name] == code_node
        captures[name] = code_node
        return True

    if rule_node.node_type != code_node.node_type:
        return False

    if rule_node.value is not None:
        if code_node.value is None or rule_node.value != code_node.value:
            return False

    if len(rule_node.children) != len(code_node.children):
        return False

    for rule_child, code_child in zip(rule_node.children, code_node.children):
        if not match(rule_child, code_child, captures):
            return False

    return True
