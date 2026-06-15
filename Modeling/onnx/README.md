# ONNX Playground

A collection of standalone ONNX experiments focused on understanding:
- ONNX graph structure
- PyTorch → ONNX export
- ONNX Runtime execution
- graph optimization and fusion
- inference benchmarking
- low-level graph manipulation

The goal of this directory is to treat ONNX as an intermediate representation (IR) and explore how model execution changes after graph transformations and runtime optimizations.

---

# Objectives

This playground investigates:

1. How neural network layers are represented as ONNX graph nodes
2. How ONNX Runtime executes static computation graphs
3. How graph optimizations affect:
   - node count
   - operator fusion
   - inference latency
4. The difference between:
   - model structure
   - runtime execution
   - compiler-style graph transformations

---

# Intended Directory Structure

```text
onnx/
├── README.md
├── requirements.txt
│
├── models/
│   ├── mlp_baseline.onnx
│   └── mlp_optimized.onnx
│
├── scripts/
│   ├── examine.py
```