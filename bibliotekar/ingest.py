"""
entity_id=ingest_module; type=module; state=initial

Source ingestion utilities. This module accepts arbitrary files and extracts text or structured content for downstream wiki integration. The goal is to provide uniform interfaces for different file types (Markdown, plain text, code, PDF, DOCX, images, videos, presentations, LaTeX). Parsing functions should return a dictionary containing extracted textual content, metadata, and optional structured data. Summarization and entity extraction leverage the OpenRouter LLM via ``agent.llm_summarize``. Unparsable types raise ``UnsupportedFileTypeError``.
"""

import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

import docx2txt  # type: ignore
import pdfminer.high_level  # type: ignore

from .utils import compute_file_hash, slugify


class UnsupportedFileTypeError(Exception):
    """Raised when ingest receives a file type it cannot handle."""


def ingest_file(path: Path) -> Dict[str, Any]:
    """Ingest a single file and return extracted content and metadata.

    entity_id=ingest_file; type=function; state=initial
    condition=file_exists → action=detect_and_parse → result=content_dict

    Parameters
    ----------
    path: Path
        Path to the source file.

    Returns
    -------
    dict
        Extracted content with keys ``text``, ``metadata``, ``hash``.
    """
    # Validate existence
    if not path.exists():
        raise FileNotFoundError(f"File {path} does not exist")

    ext = path.suffix.lower()
    logging.debug("Ingesting file", extra={"file": str(path), "ext": ext})

    text: Optional[str] = None
    try:
        # Simple text and code formats
        if ext in {".md", ".txt", ".log", ".py", ".cpp", ".c", ".cu", ".java", ".js", ".ts", ".tex"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
        elif ext == ".docx":
            # DOCX extraction via docx2txt; catch exceptions if library fails
            text = docx2txt.process(str(path))
        elif ext == ".pdf":
            # PDF extraction via pdfminer; returns empty string on failure
            try:
                text = pdfminer.high_level.extract_text(str(path)) or ""
            except Exception as pdf_exc:
                logging.error("PDF extraction failed", exc_info=True, extra={"file": str(path)})
                text = ""
        elif ext == ".pptx":
            text = _extract_pptx_text(path)
        elif ext in {".png", ".jpg", ".jpeg", ".webp"}:
            # OCR stub; returns empty string
            text = _extract_image_text(path)
        elif ext in {".mp4", ".mkv", ".mov"}:
            text = _extract_video_text(path)
        else:
            raise UnsupportedFileTypeError(f"Unsupported file type: {ext}")
    except UnsupportedFileTypeError:
        # Bubble up unsupported type for caller to handle
        raise
    except Exception as exc:
        # Catch all unexpected errors to prevent crashing the agent
        logging.error("Error ingesting file", exc_info=True, extra={"file": str(path)})
        # Provide best‑effort fallback by reading as binary and returning empty text
        text = ""

    metadata: Dict[str, Any] = {
        "filename": path.name,
        "slug": slugify(path.stem),
        "hash": compute_file_hash(path),
        "size": path.stat().st_size,
    }
    return {"text": text, "metadata": metadata}


def _extract_pptx_text(path: Path) -> str:
    """Extract textual content from a PowerPoint file using pandoc as fallback.

    This helper attempts to convert the PPTX to plain markdown using pandoc; if pandoc is not available, returns an empty string. This is a heavy operation and should be invoked sparingly.
    """
    try:
        result = subprocess.run([
            "pandoc",
            "-t",
            "markdown",
            str(path),
        ], capture_output=True, check=False)
        if result.returncode == 0:
            return result.stdout.decode("utf-8", errors="ignore")
        return ""
    except FileNotFoundError:
        return ""


def _extract_image_text(path: Path) -> str:
    """Stub for OCR extraction from image files.

    Real implementation should call Tesseract OCR or a cloud service. This stub returns an empty string.
    """
    logging.warning("OCR extraction not implemented", extra={"file": str(path)})
    return ""


def _extract_video_text(path: Path) -> str:
    """Stub for video transcription.

    Real implementation should transcribe audio tracks via ffmpeg and a speech‑to‑text engine. This stub returns an empty string.
    """
    logging.warning("Video transcription not implemented", extra={"file": str(path)})
    return ""