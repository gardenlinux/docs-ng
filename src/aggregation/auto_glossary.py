#!/usr/bin/env python3

import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Match, Pattern, Tuple

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# Default format for marking glossary entries in markdown
GLOSSARY_ENTRY_FORMAT: str = "{glossary:*}"
GLOSSARY_PATH: str = "/reference/glossary"

CODE_BLOCK_PATTERN: Pattern[str] = re.compile(
    r"^(`{3,}|~{3,})[^\n]*\n[\s\S]*?^\1\s*$", re.MULTILINE
)
INLINE_CODE_PATTERN: Pattern[str] = re.compile(r"`[^`\n]+`")
LINK_PATTERN: Pattern[str] = re.compile(r"\[[^\]]+\]\([^\)]+\)")


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

    def _ensure_nltk_data(self) -> None:
        """
        Ensure nltk wordnet data is available.
        """
        try:
            import nltk

            nltk.data.find("corpora/wordnet")
        except LookupError:
            try:
                import nltk

                print("[INFO][auto-glossary] Downloading NLTK WordNet data...")
                nltk.download("wordnet", quiet=True)
                nltk.download("omw-1.4", quiet=True)
            except Exception as e:
                print(
                    f"[Warning][auto-glossary] Could not download NLTK WordNet data: {e}"
                )
                print(
                    f"[Warning][auto-glossary] Grammar Handling will use basic wordlist. This is unreliable any may lead to errors down the line."
                )

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

    def _get_protected_region(self, content: str) -> List[Tuple[int, int]]:
        """
        Find all regions that should not be processed.

        Identifies code blocks, inline code, and existing markdown links.
        Returns a sorted, merged list of (start, end) spans.

        :param content: The markdown content to analyze.
        :return: List of (start, end) tuples for protected regions.
        """
        protected: List[Tuple[int, int]] = []
        for pattern in [CODE_BLOCK_PATTERN, INLINE_CODE_PATTERN, LINK_PATTERN]:
            for match in pattern.finditer(content):
                protected.append((match.start(), match.end()))

        protected.sort()

        merged: List[Tuple[int, int]] = []
        for start, end in protected:
            if merged and start <= merged[-1][1]:
                # Overlaps with previous region, extend it
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))

        return merged

    def _get_unprotected_region(
        self, content: str, protected_regions: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """
        Get the inverse of protected regions.

        :param content: The full content string.
        :param protected_regions: Sroted, merged list of protected (start, end) regions
        :return: List of (start, end) tuples for unprotected regions.
        """
        unprotected: List[Tuple[int, int]] = []
        pos = 0

        for prot_start, prot_end in protected_regions:
            if pos < prot_start:
                unprotected.append((pos, prot_start))
            pos = prot_end

        if pos < len(content):
            unprotected.append((pos, len(content)))

        return unprotected

    def link_terms(self, content: str, file_path: str = "") -> str:
        """Process markdown content and link glossary terms.

        :param content: Markdown content to process
        :param file_path: Relative path of the file for logging
        :return: Content with glossary markers replaced by markdown links
        """
        if file_path == GLOSSARY_PATH or file_path.endswith("/glossary.md"):
            return content

        # Find all protected regions and their inverse
        protected_regions: List[Tuple[int, int]] = self._get_protected_region(content)
        unprotected_regions: List[Tuple[int, int]] = self._get_unprotected_region(
            content, protected_regions
        )

        # Process glossary markers
        def replace_glossary_marker(match):
            term = match.group("term").strip()
            term_lower = term.lower()

            if term_lower in self.terms:
                anchor, _ = self.terms[term_lower]
                return f"[{term}]({GLOSSARY_PATH}#{anchor})"
            elif term_lower in self.aliases:
                canonical = self.aliases[term_lower]
                anchor, _ = self.terms[canonical]
                return f"[{term}]({GLOSSARY_PATH}#{anchor})"

            base_forms: List[str] = self._get_base_forms(term)
            for base_form in base_forms:
                if base_form in self.terms:
                    anchor, _ = self.terms[base_form]
                    return f"[{term}]({GLOSSARY_PATH}#{anchor})"
                elif base_form in self.aliases:
                    canonical = self.aliases[base_form]
                    anchor, _ = self.terms[canonical]
                    return f"[{term}]({GLOSSARY_PATH}#{anchor})"

            print(
                f"[Warning][auto-glossary] Term '{term}' not found in glossary! "
                f"(referenced in file '{file_path}')"
            )
            return match.group(0)

        # Build result by processing only unprotected regions
        parts: List[str] = []
        pos = 0

        for span_start, span_end in unprotected_regions:
            parts.append(content[pos:span_start])

            span_content = content[span_start:span_end]
            processed_span = self._entry_pattern.sub(
                replace_glossary_marker, span_content
            )
            parts.append(processed_span)

            pos = span_end

        parts.append(content[pos:])

        result = "".join(parts)

        return result

    def _is_valid_term(self, term: str) -> bool:
        """Check if term exists in glossary.

        :param term: Term name to check
        :return: True if term exists in glossary or aliases
        """
        return term.lower() in self.terms or term.lower() in self.aliases

    def _get_base_forms(self, term: str) -> List[str]:
        """Get possible base forms of a given term.

        :param term: The term to analyze
        :returns: A list of possible base terms
        """
        term = term.lower()
        candidates: List[str] = []

        if term.endswith("'s"):
            candidates.append(term[:-2])
        elif term.endswith("'"):
            candidates.append(term[:-1])

        try:
            if not hasattr(self, "_lemmatizer"):
                self._lemmatizer = WordNetLemmatizer()

            words: List[str] = term.split()
            if len(words) == 1:
                # One word -> Try as noun, adjective or verb.
                # nltk lemmatizer handles irregular forms.
                candidates.append(self._lemmatizer.lemmatize(term, pos=wordnet.NOUN))
                candidates.append(self._lemmatizer.lemmatize(term, pos=wordnet.VERB))
                candidates.append(self._lemmatizer.lemmatize(term, pos=wordnet.ADJ))
            else:
                # Multi-word -> lemmatize last word only (e.g. "Kubernetes cluster" -> "Kubernetes cluster")
                last_lemma = self._lemmatizer.lemmatize(words[-1], pos=wordnet.NOUN)
                if last_lemma != words[-1]:
                    candidates.append(" ".join(words[:-1] + [last_lemma]))
        except LookupError:
            print(
                f"[Warning][auto-glossary] NLTK lookup error. Falling back to basic ruleset..."
            )
            # NLTK data not available -> fallback to basic ruleset.
            suffix_rules: List[Tuple[str, str]] = [
                ("ies", "y"),
                ("sses", "ss"),
                ("ses", "s"),
                ("s", ""),
                ("ed", ""),
                ("ing", ""),
                ("ly", ""),
            ]

            for suffix, replacement in suffix_rules:
                if term.endswith(suffix):
                    base = term[: -len(suffix)] + replacement
                    # handle double consonants
                    if (
                        len(base) >= 2
                        and base[-1] == base[-2]
                        and base[-1] in "bcdfgklmnprstvwz"
                    ):
                        candidates.append(base[:-1])
                    if base:
                        candidates.append(base)

        except Exception as e:
            print(f"[Warning][auto-glossary] Unidentified NLTK Error: {e}")

        # Remove duplicates
        seen = set()
        return [c for c in candidates if c != term and not (c in seen or seen.add(c))]


def process_glossary_links(docs_dir: Path, entry_format: str | None = None) -> int:
    """Process all markdown files in docs directory for glossary linking.

    :param docs_dir: Root documentation directory
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
                content, str(md_file.relative_to(docs_dir))
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
        print(f"Entry format: {args.entry_format or GLOSSARY_ENTRY_FORMAT}")

    try:
        processed = process_glossary_links(
            args.docs_dir, entry_format=args.entry_format
        )
    except Exception as e:
        print(f"[Error][auto-glossary] Failed to process glossary links: {e}")
        return 1

    print(f"[success][auto-glossary] Successfully processed {processed} files.")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
