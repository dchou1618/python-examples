

class Node:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children is not None else []

def find_calls(root: Node, function_name: str):
    """
    This function takes AST root and function name as input and returns all function calls in the AST.
    First child node is the name of the function
    """
    calls = []
    def gather_calls(root, function_name):
        if root:
            if root.node_type == "Call":
                if root.children and root.children[0].node_type == "Name" and \
                    root.children[0].value == function_name:
                    calls.append(root)
            for child in root.children:
                gather_calls(child, function_name)
    gather_calls(root, function_name)
    return calls