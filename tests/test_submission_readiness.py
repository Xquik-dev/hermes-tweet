from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parents[1]
PHRASE_DIR = ROOT / "tests" / "fixtures" / "route_rejection_phrases"


def _route_rejection_phrases() -> tuple[str, ...]:
    phrases: list[str] = []
    for path in sorted(PHRASE_DIR.glob("*.txt")):
        phrases.extend(phrase for phrase in path.read_text().splitlines() if phrase)
    return tuple(phrases)


def test_submission_readiness_rejects_adjacent_marketplace_routes() -> None:
    normalized_checklist = " ".join((ROOT / "docs" / "SUBMISSION_READINESS.md").read_text().split())

    for phrase in _route_rejection_phrases():
        assert phrase in normalized_checklist


def test_submission_readiness_stays_below_quality_boundary() -> None:
    line_count = len((ROOT / "docs" / "SUBMISSION_READINESS.md").read_text().splitlines())

    assert line_count <= 990


def test_route_rejection_phrase_fixtures_stay_explicit() -> None:
    for path in sorted(PHRASE_DIR.glob("*.txt")):
        phrases = path.read_text().splitlines()

        assert all(phrase for phrase in phrases)
        assert len(phrases) == len(set(phrases))
