

class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

def find_calls(root: Node, function_name: str):
    """
    This function takes AST root and function name as input and returns all function calls in the AST.
    """
    pass