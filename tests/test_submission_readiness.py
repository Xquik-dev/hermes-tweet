from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parents[1]
PHRASE_DIR = ROOT / "tests" / "fixtures" / "route_rejection_phrases"
MAX_FIXTURE_LINES = 600


def _route_rejection_phrase_paths() -> tuple[Path, ...]:
    return tuple(sorted(PHRASE_DIR.glob("*.txt")))


def _route_rejection_phrases() -> tuple[str, ...]:
    phrases: list[str] = []
    for path in _route_rejection_phrase_paths():
        phrases.extend(phrase for phrase in path.read_text().splitlines() if phrase)
    return tuple(phrases)


def test_submission_readiness_rejects_adjacent_marketplace_routes() -> None:
    normalized_checklist = " ".join((ROOT / "docs" / "SUBMISSION_READINESS.md").read_text().split())

    for phrase in _route_rejection_phrases():
        assert phrase in normalized_checklist


def test_submission_readiness_stays_below_quality_boundary() -> None:
    line_count = len((ROOT / "docs" / "SUBMISSION_READINESS.md").read_text().splitlines())

    assert line_count <= 960


def test_route_rejection_phrase_fixtures_stay_explicit() -> None:
    for path in _route_rejection_phrase_paths():
        phrases = path.read_text().splitlines()

        assert all(phrase for phrase in phrases)
        assert len(phrases) == len(set(phrases))


def test_route_rejection_phrase_fixtures_stay_split() -> None:
    for path in _route_rejection_phrase_paths():
        line_count = len(path.read_text().splitlines())

        assert line_count <= MAX_FIXTURE_LINES
