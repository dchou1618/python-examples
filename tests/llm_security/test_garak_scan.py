from pathlib import Path


REPO_ROOT = Path(__file__).parents[2]
SCAN_SCRIPT = REPO_ROOT / "security" / "garak" / "run_scan.sh"


def test_garak_scan_wrapper_is_present_and_requires_a_model() -> None:
    script = SCAN_SCRIPT.read_text()

    assert "GARAK_MODEL_NAME" in script
    assert "GARAK_ALLOW_SKIP" in script
    assert "--model_type" in script
    assert "--probes" in script