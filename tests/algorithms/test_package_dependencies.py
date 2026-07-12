from Algorithms.static_analysis.package_dependency import find_dependency_cycle
import pytest

@pytest.mark.parametrize(
    "input_deps, expected",
    [
        ({
            "A": ["B"],
            "B": ["C"],
            "C": ["A"],
            "D": []
        }, [['A', 'B', 'C', 'A']]),
        ({
            "A": ["B"],
            "B": ["C"],
            "C": ["A"],

            "D": ["E"],
            "E": ["F"],
            "F": ["D"],
        }, [['A', 'B', 'C', 'A'], ['D', 'E', 'F', 'D']]),
        ({
            "A": ["B"],
            "B": ["C"],
            "C": ["A"],

            "X": ["Y"],
            "Y": [],
        }, [['A', 'B', 'C', 'A']]),
        ({
            "A": ["A"],
            "B": ["C"],
            "C": []
        }, [['A', 'A']]),
        ({
            "A": ["B"],
            "B": ["C", "D"],
            "C": ["A"],
            "D": ["B"]
        }, [['A', 'B', 'C', 'A'], ['B', 'D', 'B']]),
        ({
            "A": ["B"],
            "B": ["C"],
            "C": ["D"],
            "D": ["B", "E"],
            "E": []
        }, [['B', 'C', 'D', 'B']])
    ]
)
def test_basic_cases(input_deps, expected):
    cycle_output = find_dependency_cycle(input_deps)
    assert sorted(cycle_output) == sorted(expected)

def test_non_back_edges():
    deps = {
        "A": ["B"],
        "B": ["C", "D"],
        "C": ["A"],
        "D": ["E"],
        "E": ["B"]
    }
    output = [['A', 'B', 'C', 'A'], ['B', 'D', 'E', 'B']]
    assert sorted(find_dependency_cycle(deps)) == sorted(output)