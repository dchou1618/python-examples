import onnx
from onnx import numpy_helper
from collections import Counter

def examine(fpath: str):
    model = onnx.load(fpath)
    onnx.checker.check_model(model)

    print("=" * 80)
    print("GRAPH SUMMARY")
    print("=" * 80)

    print("Graph name:", model.graph.name)
    print("Nodes:", len(model.graph.node))
    print("Inputs:", len(model.graph.input))
    print("Outputs:", len(model.graph.output))
    print("Initializers:", len(model.graph.initializer))

    counter = Counter(node.op_type for node in model.graph.node)

    print("\nOPERATOR HISTOGRAM")
    print("-" * 80)

    for op, count in counter.items():
        print(f"{op:<20} {count}")
    
    print("\nGRAPH TOPOLOGY")
    print("-" * 80)
    # node: [op_type] [inputs] -> [outputs]
    for idx, node in enumerate(model.graph.node):
        inputs = ", ".join(node.input)
        outputs = ", ".join(node.output)

        print(
            f"[{idx:03d}] "
            f"{node.op_type:<15} "
            f"{inputs} -> {outputs}"
        )

    print("\nPOTENTIAL OPTIMIZATION OPPORTUNITIES")
    print("-" * 80)

    nodes = list(model.graph.node)

    for i in range(len(nodes) - 1):
        a = nodes[i]
        b = nodes[i + 1]

        # MatMul + Add can often become Gemm
        if a.op_type == "MatMul" and b.op_type == "Add":
            print(
                f"Possible fusion at nodes {i}->{i+1}: "
                f"MatMul + Add -> Gemm"
            )

        # redundant identities
        if a.op_type == "Identity":
            print(f"Redundant Identity node at {i}")

        # transpose chains
        if a.op_type == "Transpose" and b.op_type == "Transpose":
            print(f"Consecutive Transpose ops at {i}->{i+1}")
    
    print("\nINITIALIZERS")
    print("-" * 80)

    for init in model.graph.initializer:
        arr = numpy_helper.to_array(init)

        print(
            f"{init.name:<20} "
            f"shape={str(arr.shape):<20} "
            f"dtype={arr.dtype}"
        )
    
    inferred = onnx.shape_inference.infer_shapes(model)
    print("\nINTERMEDIATE TENSORS")
    print("-" * 80)

    for value in inferred.graph.value_info:
        tensor_type = value.type.tensor_type

        dims = [
            d.dim_param or d.dim_value
            for d in tensor_type.shape.dim
        ]

        print(f"{value.name:<20} {dims}")
    
    print("\nLINEARIZED EXECUTION VIEW")
    print("-" * 80)

    for idx, node in enumerate(model.graph.node):
        print(f"{idx:03d} {node.op_type}")

        for inp in node.input:
            print(f"    IN  <- {inp}")

        for out in node.output:
            print(f"    OUT -> {out}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Inspect an ONNX model")
    parser.add_argument("fpath", type=str, help="Path to the ONNX model file")
    args = parser.parse_args()
    examine(args.fpath)