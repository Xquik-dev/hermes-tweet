from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).parents[1]
SUBMISSION_READINESS_PATH = ROOT / "docs" / "SUBMISSION_READINESS.md"
PHRASE_DIR = ROOT / "tests" / "fixtures" / "route_rejection_phrases"
EXPECTED_PHRASE_FILES = (
    "agent_runtime.txt",
    "marketplaces_core.txt",
    "marketplaces_people_governance.txt",
    "marketplaces_specialized.txt",
    "safety_duplicates.txt",
)
MAX_SUBMISSION_READINESS_LINES = 960
MAX_FIXTURE_LINES = 600


def _route_rejection_phrase_paths() -> tuple[Path, ...]:
    return tuple(sorted(PHRASE_DIR.glob("*.txt")))


def _route_rejection_phrases() -> tuple[str, ...]:
    phrases: list[str] = []
    for path in _route_rejection_phrase_paths():
        phrases.extend(phrase for phrase in path.read_text().splitlines() if phrase)
    return tuple(phrases)


def test_submission_readiness_rejects_adjacent_marketplace_routes() -> None:
    normalized_checklist = " ".join(SUBMISSION_READINESS_PATH.read_text().split())

    for phrase in _route_rejection_phrases():
        assert phrase in normalized_checklist


def test_submission_readiness_stays_below_quality_boundary() -> None:
    line_count = len(SUBMISSION_READINESS_PATH.read_text().splitlines())

    assert line_count <= MAX_SUBMISSION_READINESS_LINES


def test_route_rejection_phrase_fixtures_stay_explicit() -> None:
    for path in _route_rejection_phrase_paths():
        phrases = path.read_text().splitlines()

        assert all(phrase for phrase in phrases)
        assert all(phrase == phrase.strip() for phrase in phrases)
        assert all("\t" not in phrase for phrase in phrases)
        assert len(phrases) == len(set(phrases))


def test_route_rejection_phrase_fixtures_stay_in_reviewed_buckets() -> None:
    fixture_names = tuple(path.name for path in _route_rejection_phrase_paths())

    assert fixture_names == EXPECTED_PHRASE_FILES


def test_route_rejection_phrase_fixture_directory_stays_flat() -> None:
    entries = tuple(sorted(PHRASE_DIR.iterdir()))
    entry_names = tuple(path.name for path in entries)

    assert entry_names == EXPECTED_PHRASE_FILES
    assert all(path.is_file() for path in entries)


def test_route_rejection_phrase_fixtures_stay_split() -> None:
    for path in _route_rejection_phrase_paths():
        line_count = len(path.read_text().splitlines())

        assert line_count <= MAX_FIXTURE_LINES
