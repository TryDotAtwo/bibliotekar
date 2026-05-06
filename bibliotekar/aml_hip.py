"""
entity_id=aml_hip_module; type=module; state=initial

Utilities for constructing and validating messages under the Autistic Meta‑Language High‑Information Protocol (AML‑HIP). The protocol requires high information density, explicit entity references, and structured causal blocks. This module provides helper functions to assemble messages and check for compliance. Tests in ``tests/test_aml_hip.py`` exercise these functions.
"""

import re
from typing import Dict, List, Tuple


def format_message(sections: Dict[str, List[str]]) -> str:
    """Assemble a message from named sections into AML‑HIP format.

    Each key in ``sections`` corresponds to a label (e.g. 'СУЩНОСТЬ', 'КОНТЕКСТ'), and the value is a list of lines. The function concatenates sections in the order provided, adding a section header followed by the lines. It does not enforce content rules; validation is performed separately.

    Parameters
    ----------
    sections: dict
        Ordered mapping of section names to lists of strings representing lines.

    Returns
    -------
    str
        Concatenated AML‑HIP formatted message.
    """
    parts: List[str] = []
    for header, lines in sections.items():
        parts.append(f"{header}:")
        for line in lines:
            parts.append(line)
        parts.append("")  # Blank line as separator between sections
    return "\n".join(parts).strip()


def validate_message(message: str) -> Tuple[bool, List[str]]:
    """Check compliance of a message with AML‑HIP rules.

    The validator enforces:

    * No pronouns (English or Russian common pronouns).
    * Each line must contain at least one '=' or a causal arrow '→' to denote key‑value pairs or causal relations.
    * Prohibits empty words like 'это', 'оно', 'она', etc.
    * Requires section headers to be uppercase and Russian as specified.

    Parameters
    ----------
    message: str
        The message to validate.

    Returns
    -------
    tuple
        A tuple of (is_valid, errors). ``is_valid`` is True if no errors are found; otherwise False. ``errors`` is a list of strings describing each violation.
    """
    errors: List[str] = []
    pronouns = re.compile(r"\b(it|he|she|they|это|она|он|они|there|here)\b", re.IGNORECASE)

    lines = message.strip().split("\n")
    for idx, line in enumerate(lines, 1):
        if pronouns.search(line):
            errors.append(f"Line {idx}: pronoun detected")
        # Skip section headers (end with ':')
        if line.endswith(":"):
            continue
        if line and not re.search(r"=|→", line):
            errors.append(f"Line {idx}: lacks key=value or relation")
    # Check headers
    for header in re.findall(r"^(.*?):", message, flags=re.MULTILINE):
        if not re.match(r"^[А-ЯA-Z]+$", header.strip()):
            errors.append(f"Section header '{header}' not uppercase or contains invalid characters")
    return len(errors) == 0, errors