"""Local storage helpers for saved Nimbus analyses."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re


ANALYSES_DIRECTORY = Path(__file__).resolve().parent.parent / "analyses-data"


def _safe_filename_part(value: str) -> str:
    """Return a readable filename component without path characters."""
    cleaned = re.sub(r"[^A-Za-z0-9.-]+", "-", value.strip())
    return cleaned.strip(".-") or "analysis"


def generate_analysis_filename(
    ticker: str,
    analysis_type: str,
    created_at: datetime | None = None,
) -> str:
    """Generate a safe, timestamped Markdown filename."""
    timestamp = (created_at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return (
        f"{_safe_filename_part(ticker)}-"
        f"{_safe_filename_part(analysis_type)}-"
        f"{timestamp:%Y%m%d-%H%M%S-%f}Z.md"
    )


def save_analysis(
    markdown: str,
    ticker: str,
    analysis_type: str,
    created_at: datetime | None = None,
) -> Path:
    """Save Markdown content without overwriting an existing analysis."""
    ANALYSES_DIRECTORY.mkdir(parents=True, exist_ok=True)
    filename = generate_analysis_filename(ticker, analysis_type, created_at)
    path = ANALYSES_DIRECTORY / filename
    counter = 1

    while True:
        candidate = path if counter == 1 else path.with_name(
            f"{path.stem}-{counter}{path.suffix}"
        )
        try:
            with candidate.open("x", encoding="utf-8") as analysis_file:
                analysis_file.write(markdown)
            return candidate
        except FileExistsError:
            counter += 1


def list_saved_analyses() -> list[Path]:
    """Return saved Markdown files newest first."""
    if not ANALYSES_DIRECTORY.exists():
        return []

    def sort_key(path: Path) -> tuple[int, int, str]:
        collision_match = re.search(r"-(\d+)$", path.stem)
        collision_number = int(collision_match.group(1)) if collision_match else 0
        return (path.stat().st_mtime_ns, collision_number, path.name)

    return sorted(
        (path for path in ANALYSES_DIRECTORY.glob("*.md") if path.is_file()),
        key=sort_key,
        reverse=True,
    )


def read_analysis(path: Path) -> str:
    """Read one saved analysis and reject paths outside the storage directory."""
    resolved_path = path.resolve()
    storage_directory = ANALYSES_DIRECTORY.resolve()
    if resolved_path.parent != storage_directory or resolved_path.suffix.lower() != ".md":
        raise ValueError("The selected analysis file is not in the analyses folder.")
    return resolved_path.read_text(encoding="utf-8")


def analysis_label(path: Path) -> str:
    """Turn a generated filename into a readable selection label."""
    return re.sub(r"-+", " ", path.stem).strip()
