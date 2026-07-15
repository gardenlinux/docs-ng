#!/usr/bin/env python3

import re
import unicodedata
import uuid
from pathlib import Path
from typing import Any, Dict, Match, Pattern, Tuple

# Default format for marking glossary entries in markdown
GLOSSARY_ENTRY_FORMAT = "{glossary:*}"


class AutoGlossary:
    """Links marked terms to glossary entries.

    Processes markdown files to convert glossary term markers into links
    to the glossary page. Supports configurable marker formats.
    """

    def __init__(self, glossary_path: Path, entry_format: str | None = None):
        """Initialize the glossary linker.

        :param glossary_path: Path to the glossary markdown file
        :param entry_format: Format string for glossary markers (uses GLOSSARY_ENTRY_FORMAT if None).
                             The * character acts as placeholder for the term name.
        """
        self.glossary_path: Path = glossary_path
        # term -> (anchor, display_name)
        self.terms: Dict[str, Tuple[str, str]] = {}
        # alias -> canonical_term
        self.aliases: Dict[str, str] = {}

        # Set entry format (use default if not provided)
        self.entry_format: str = entry_format if entry_format else GLOSSARY_ENTRY_FORMAT

        # Validate entry format contains the placeholder
        if "*" not in self.entry_format:
            raise ValueError(
                f"Entry format must contain '*' as placeholder for term name. "
                f"Got: '{self.entry_format}'"
            )

        # Build regex pattern from entry format
        self._entry_pattern = self._build_pattern_from_format()

        self._parse_glossary()

    def _build_pattern_from_format(self) -> re.Pattern:
        """Build a regex pattern from the entry format string.

        :return: Compiled regex pattern with named group 'term' for the captured term
        """
        # Escape special regex characters except *
        escaped: str = re.escape(self.entry_format)

        # Replace the escaped \* with a named capture group for the term
        # Match non-greedy to handle multiple occurrences on same line
        # Allow alphanumeric, spaces, hyphens, underscores, parentheses in term names
        pattern_str: str = escaped.replace(r"\*", r"(?P<term>[a-zA-Z0-9\s\-_()]+?)")

        # Compile and return
        return re.compile(pattern_str)

    def get_entry_format_example(self, term: str = "example") -> str:
        """Get an example of how to mark a term with the current entry format.

        :param term: Example term to show in the format
        :return: String showing how the term should be marked
        """
        return self.entry_format.replace("*", term)

    def _parse_glossary(self) -> None:
        """Parse glossary.md to extract terms and anchors.

        Reads the glossary file and builds an index of terms mapped to their anchors.
        Terms are stored in lowercase for case-insensitive matching.
        Extracts aliases from parenthesized expansions.
        """
        if not self.glossary_path.exists():
            raise FileNotFoundError(f"Glossary file not found: {self.glossary_path}")

        content: str = self.glossary_path.read_text(encoding="utf-8")

        # Pattern to match level-3 headers
        header_pattern = re.compile(r"^###\s+(.+)$", re.MULTILINE)

        anchors_seen: dict[str, str] = {}

        for match in header_pattern.finditer(content):
            term = match.group(1).strip()

            if not term:
                continue

            # Generate anchor for this term
            anchor: str = self._generate_anchor(term)

            # Check for anchor collisions
            if anchor in anchors_seen:
                original_term: str = anchors_seen[anchor]
                print(
                    f"[Warning][auto-glossary] Anchor collision detected:\n"
                    f"  '{original_term}' and '{term}' both generate anchor '{anchor}'"
                )
            else:
                anchors_seen[anchor] = term

            # Store term with lowercase key for case-insensitive lookup
            term_key: str = term.lower()
            self.terms[term_key] = (anchor, term)

            # Extract aliases from parenthesized expansions
            # e.g., "ADR (Architecture Decision Record)" -> alias "Architecture Decision Record"
            parenthesis_match: Match[str] | None = re.match(
                r"^([^(]+)\s*\(([^)]+)\)$", term
            )
            if parenthesis_match:
                abbreviation: str | Any = parenthesis_match.group(1).strip()
                expansion: str | Any = parenthesis_match.group(2).strip()

                # Store expansion as alias pointing to the full term
                expansion_key: str | Any = expansion.lower()
                if expansion_key not in self.terms:
                    self.aliases[expansion_key] = term_key

                # Also store abbreviation alone as alias
                abbr_key: str = abbreviation.lower()
                if abbr_key != term_key and abbr_key not in self.terms:
                    self.aliases[abbr_key] = term_key

        if not self.terms:
            print(
                f"[Warning][auto-glossary] No glossary terms found in {self.glossary_path}"
            )

    def _generate_anchor(self, term: str) -> str:
        """Generate VitePress-compatible anchor from term.

        :param term: The glossary term to convert
        :return: URL-safe anchor string
        :raises ValueError: If term is empty or results in empty anchor
        """
        if not term or not term.strip():
            raise ValueError(
                "[Error][auto-glossary] Term cannot be empty or whitespace-only!"
            )

        # Normalize by removing accented characters etc.
        normalized: str = unicodedata.normalize("NFD", term.strip())
        ascii_only: str = "".join(
            char for char in normalized if unicodedata.category(char) != "Mn"
        )

        # Replace whitespaces and special characters with hyphens; Strip leading/trailing hyphens.
        anchor = ascii_only.lower().replace(" ", "-")
        anchor = re.sub(r"[^a-z0-9-]", "-", anchor)
        anchor = re.sub(r"-+", "-", anchor)
        anchor = anchor.strip("-")

        if not anchor:
            raise ValueError(
                f"[Error][auto-glossary] Could not generate valid anchor from term: '{term}'"
                "Result was empty after removing special characters"
            )

        if len(anchor) > 100:
            print(
                f"[Warning][auto-glossary] Generated anchor is very long ({len(anchor)} chars): '{anchor[:50]}...'"
            )

        return anchor

    def link_terms(
        self, content: str, file_path: str = "", auto_link: bool = False
    ) -> str:
        """Process markdown content and link glossary terms.

        :param content: Markdown content to process
        :param file_path: Relative path of the file for logging
        :param auto_link: Whether to auto-link first occurrence of known terms
        :return: Content with glossary markers replaced by markdown links
        """
        if file_path == "reference/glossary.md" or file_path.endswith("/glossary.md"):
            return content

        # Extract code blocks and inline code to protect them from modification
        protected_regions: dict[str, str] = {}
        pattern_id: str = uuid.uuid4().hex[:8]
        placeholder_pattern: str = f"<<<GLOSSARY_PLACEHOLDER_{{}}_{pattern_id}_>>>"

        # Pattern for fenced code blocks (``` or ~~~)
        code_block_pattern: Pattern[str] = re.compile(
            r"^(`{3,}|~{3,})[^\n]*\n[\s\S]*?^\1\s*$", re.MULTILINE
        )

        # Pattern for inline code (`code`)
        inline_code_pattern: Pattern[str] = re.compile(r"(`[^`\n]+`)")

        # Pattern for existing markdown links ([text](url))
        link_pattern: Pattern[str] = re.compile(r"(\[([^\]]+)\]\([^\)]+\))")

        # Store and replace code blocks
        def protect_region(match):
            idx: int = len(protected_regions)
            placeholder: str = placeholder_pattern.format(idx)
            protected_regions[placeholder] = match.group(0)
            return placeholder

        work_content: str = code_block_pattern.sub(protect_region, content)
        work_content = link_pattern.sub(protect_region, work_content)
        work_content = inline_code_pattern.sub(protect_region, work_content)

        # Process glossary markers
        def replace_glossary_marker(match):
            term = match.group("term").strip()
            term_lower = term.lower()

            # Check if term exists in glossary
            if term_lower in self.terms:
                anchor, display_name = self.terms[term_lower]
                return f"[{term}](/reference/glossary#{anchor})"
            elif term_lower in self.aliases:
                canonical = self.aliases[term_lower]
                anchor, display_name = self.terms[canonical]
                return f"[{term}](/reference/glossary#{anchor})"
            else:
                print(
                    f"[Warning][auto-glossary] Term '{term}' not found in glossary "
                    f"(referenced in {file_path})"
                )
                # Return original marker if term not found
                return match.group(0)

        work_content: str = self._entry_pattern.sub(
            replace_glossary_marker, work_content
        )

        # Auto-link first occurrence of each term
        if auto_link:
            work_content = self._auto_link_terms(work_content, file_path)

        # Restore protected regions
        for placeholder, original in protected_regions.items():
            work_content = work_content.replace(placeholder, original)

        return work_content

    def _auto_link_terms(self, content: str, file_path: str = "") -> str:
        """Auto-link first occurrence of glossary terms.

        :param content: Markdown content to process
        :param file_path: Relative path for logging
        :return: Content with first occurrences linked
        """
        # Build list of terms sorted by length (longest first) to handle overlapping terms
        all_terms = []

        # Add main terms
        for term_key, (anchor, display_name) in self.terms.items():
            all_terms.append((display_name, anchor))

        # Add aliases (but use actual alias text for matching)
        for alias_key, canonical_key in self.aliases.items():
            anchor, _ = self.terms[canonical_key]
            # Reconstruct proper case for alias
            alias_words = alias_key.split()
            alias_display = " ".join(word.capitalize() for word in alias_words)
            all_terms.append((alias_display, anchor))

        # Sort by length descending to match longer terms first
        all_terms.sort(key=lambda x: len(x[0]), reverse=True)

        # Find all matches first, then apply them
        matches_to_link = []
        linked_terms = set()

        for term_text, anchor in all_terms:
            term_lower = term_text.lower()
            if term_lower in linked_terms:
                continue

            # Create pattern for whole word match
            pattern = re.compile(r"\b(" + re.escape(term_text) + r")\b", re.IGNORECASE)

            # Find first occurrence
            match = pattern.search(content)
            if match:
                # Check if this overlaps with any existing match
                overlaps = False
                for existing_start, existing_end, _, _ in matches_to_link:
                    if not (
                        match.end() <= existing_start or match.start() >= existing_end
                    ):
                        overlaps = True
                        break

                if not overlaps:
                    matches_to_link.append(
                        (match.start(), match.end(), match.group(1), anchor)
                    )
                    linked_terms.add(term_lower)

        # Sort matches by position (reverse order to maintain positions)
        matches_to_link.sort(key=lambda x: x[0], reverse=True)

        # Apply all links from end to start
        result = content
        for start, end, matched_text, anchor in matches_to_link:
            link = f"[{matched_text}](/reference/glossary#{anchor})"
            result = result[:start] + link + result[end:]

        return result

    def _is_valid_term(self, term: str) -> bool:
        """Check if term exists in glossary.

        :param term: Term name to check
        :return: True if term exists in glossary or aliases
        """
        return term.lower() in self.terms or term.lower() in self.aliases


def process_glossary_links(
    docs_dir: Path, auto_link: bool = False, entry_format: str | None = None
) -> int:
    """Process all markdown files in docs directory for glossary linking.

    :param docs_dir: Root documentation directory
    :param auto_link: Whether to auto-link first occurrence of known terms
    :param entry_format: Format string for glossary markers
    :return: Number of files processed successfully
    """
    glossary_path: Path = docs_dir / "reference" / "glossary.md"

    if not glossary_path.exists():
        print("[Warning][auto-glossary] Glossary not found, skipping glossary linking!")
        return 1

    linker: AutoGlossary = AutoGlossary(glossary_path, entry_format=entry_format)
    processed: int = 0

    print(f"[INFO] Using glossary entry format: {linker.entry_format}")
    print(f"[INFO] Example usage: {linker.get_entry_format_example('AWS')}")

    # Process all markdown files except glossary itself
    for md_file in docs_dir.rglob("*.md"):
        if md_file.name == "glossary.md":
            continue

        try:
            content: str = md_file.read_text(encoding="utf-8")
            linked_content: str = linker.link_terms(
                content, str(md_file.relative_to(docs_dir)), auto_link=auto_link
            )

            if linked_content != content:
                md_file.write_text(linked_content, encoding="utf-8")
                processed += 1
        except Exception as e:
            print(f"[Warning][auto-glossary] Error processing {md_file.name}: {e}")

    print(f"[Success] Auto-Glossary processed {processed} files successfully.")
    return processed


def validate_glossary(glossary_path: Path) -> int:
    """
    Validate glossary structure and report statistics.

    :param glossary_path: Path to the glossary markdown file.
    :return: Exit code (0 for success, 1 for error)
    """
    try:
        linker = AutoGlossary(glossary_path)

        print(f"Glossary structure valid.")
        print(f"Terms found: {len(linker.terms)}")
        print(f"Aliases found: {len(linker.aliases)}")

        return 0
    except FileNotFoundError as e:
        print(f"[Error][auto-glossary] {e}")
        return 1
    except Exception as e:
        print(f"[Error][auto-glossary] Filed to validate glossary: {e}")
        return 1


def main() -> int:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Process glossary links in markdown documentation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
            %(prog)s docs/
            %(prog)s docs/ --auto-link
            %(prog)s docs/ --entry-format "[[*]]"
        """,
    )

    parser.add_argument(
        "docs_dir",
        type=Path,
        nargs="?",
        default=Path("docs"),
        help="Documentation directory to process (default: docs/)",
    )

    parser.add_argument(
        "--auto-link",
        action="store_true",
        help="Automatically link first occurrence of known terms (experimental)",
    )

    parser.add_argument(
        "--entry-format",
        type=str,
        default=None,
        help=f"Custom entry format pattern (default: '{GLOSSARY_ENTRY_FORMAT}')",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "--check", action="store_true", help="Validate glossary structure only"
    )

    args = parser.parse_args()

    if args.check:
        glossary_path = args.docs_dir / "reference" / "glossary.md"
        return validate_glossary(glossary_path)

    if not args.docs_dir.exists():
        print(f"[Error][auto-glossary] Directory not found: {args.docs_dir}")
        return 1

    if args.verbose:
        print(f"Processing directory: {args.docs_dir}")
        print(f"Auto-link: {args.auto_link}")
        print(f"Entry format: {args.entry_format or GLOSSARY_ENTRY_FORMAT}")

    try:
        processed = process_glossary_links(
            args.docs_dir, auto_link=args.auto_link, entry_format=args.entry_format
        )
    except Exception as e:
        print(f"[Error][auto-glossary] Failed to process glossary links: {e}")
        return 1

    print(f"[success][auto-glossary] Successfully processed {processed} files.")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
