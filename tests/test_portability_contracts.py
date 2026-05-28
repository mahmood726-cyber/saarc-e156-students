"""Portability contracts for repo-local build behavior."""

from pathlib import Path


def test_build_script_uses_repo_local_output_root():
    build_path = Path(__file__).resolve().parent.parent / "build.py"
    text = build_path.read_text(encoding="utf-8")
    assert 'Path("C:/saarc-e156-students")' not in text
    assert r'Path("C:\saarc-e156-students")' not in text
    assert "PROJECT_ROOT = Path(__file__).resolve().parent" in text
