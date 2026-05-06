"""
entity_id=bibliotekar_cli; type=module; state=initial

Command‑line interface for interacting with the autonomous library‑secretary.  This
script enables ingestion of arbitrary files into the wiki, querying the
knowledge base, listing pages, and viewing page contents.  It is intended as
a simple, text‑based UI for demonstration and quick experiments.  The CLI
honours the ``BIBLIOTEKAR_BASE`` environment variable or accepts a
``--base_dir`` argument to select the data directory.

Usage::

    python bibliotekar_ui.py --base_dir /path/to/data

Once started, the CLI will present a menu.  Choose options by entering the
corresponding number.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from bibliotekar.agent import Agent
from bibliotekar.config import Paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Bibliotekar CLI UI")
    parser.add_argument(
        "--base_dir",
        type=str,
        default=os.getenv("BIBLIOTEKAR_BASE"),
        help="Directory for raw and wiki data (overrides BIBLIOTEKAR_BASE)",
    )
    args = parser.parse_args()
    # Initialise Paths and Agent
    paths = Paths(base_dir=Path(args.base_dir)) if args.base_dir else Paths()
    agent = Agent(paths=paths)
    print("Bibliotekar autonomous library‑secretary CLI")
    while True:
        print(
            "\nMenu:\n"
            " 1. Ingest file\n"
            " 2. Ask question\n"
            " 3. Search wiki\n"
            " 4. List pages\n"
            " 5. View page\n"
            " 6. View index\n"
            " 7. View log\n"
            " 8. Maintain wiki\n"
            " 9. Exit"
        )
        choice = input("Enter choice: ").strip()
        if choice == "1":
            path = input("Enter path to source file: ").strip()
            if not os.path.isfile(path):
                print("File not found.")
                continue
            result = agent.ingest(path)
            print(f"Ingested. Summary:\n{result.get('summary','')}")
        elif choice == "2":
            question = input("Enter your question: ").strip()
            response = agent.query(question)
            print(f"Answer:\n{response.get('answer','')}")
        elif choice == "3":
            keywords = input("Enter search terms: ").strip()
            res = agent.search(keywords)
            if not res.get("results"):
                print("No matches.")
            else:
                for idx, (page, score) in enumerate(res["results"], start=1):
                    print(f"{idx}. {Path(page).relative_to(paths.base_dir)} (score={score})")
        elif choice == "4":
            pages = agent.wiki_manager.list_pages()
            if not pages:
                print("No pages found.")
                continue
            for idx, p in enumerate(pages, start=1):
                print(f"{idx}. {p.relative_to(paths.base_dir)}")
        elif choice == "5":
            pages = agent.wiki_manager.list_pages()
            if not pages:
                print("No pages to view.")
                continue
            for idx, p in enumerate(pages, start=1):
                print(f"{idx}. {p.relative_to(paths.base_dir)}")
            sel = input("Select page number: ").strip()
            try:
                sel_idx = int(sel) - 1
                page_path = pages[sel_idx]
                print(page_path.read_text(encoding="utf-8"))
            except Exception:
                print("Invalid selection.")
        elif choice == "6":
            index_path = paths.index_file
            if index_path.exists():
                print(index_path.read_text(encoding="utf-8"))
            else:
                print("No index found.")
        elif choice == "7":
            log_path = paths.log_file
            if log_path.exists():
                print(log_path.read_text(encoding="utf-8"))
            else:
                print("No log found.")
        elif choice == "8":
            # Maintenance pass
            report = agent.maintain()
            print("Maintenance complete. Report:\n", report)
        elif choice == "9":
            print("Exiting.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()