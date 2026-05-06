"""
entity_id=utils_module; type=module; state=initial

General utility functions supporting the autonomous library‑secretary. These helpers are reused across modules and aim to minimize duplication. The utilities avoid side effects and maintain high information density in logs.
"""

import hashlib
from pathlib import Path
from typing import Iterable


def compute_file_hash(path: Path, chunk_size: int = 65536) -> str:
    """Compute the SHA256 hash of a file.

    entity_id=compute_file_hash; type=function; state=initial
    condition=file_exists → action=read_chunks → result=hex_digest
    check=nonempty_digest; expected=True

    Parameters
    ----------
    path: Path
        Path to the file.
    chunk_size: int
        Block size for reading.

    Returns
    -------
    str
        Hexadecimal SHA256 digest.
    """
    sha256 = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def slugify(text: str) -> str:
    """Convert arbitrary text into a filesystem‑safe slug.

    Replaces non‑alphanumeric characters with hyphens and trims redundant separators.

    entity_id=slugify_function; type=function; state=initial

    Parameters
    ----------
    text: str
        Input string.

    Returns
    -------
    str
        Slugified string.
    """
    import re
    slug = re.sub(r"[^\w]+", "-", text.lower()).strip('-')
    return re.sub(r"-+", "-", slug)


def ensure_dirs(paths: Iterable[Path]) -> None:
    """Ensure that directories exist for each provided path.

    entity_id=ensure_dirs_function; type=function; state=initial

    Parameters
    ----------
    paths: Iterable[Path]
        Sequence of directory paths.
    """
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)