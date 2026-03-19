from typing import List, Tuple

import nltk
from nltk.tokenize import TreebankWordTokenizer


def download_nltk_data():
    """Ensure required NLTK data is present."""
    # Placeholder for the original download logic
    # In production, this would download necessary tokenizers
    pass


def _normalize_line_endings(text: str) -> str:
    """Normalize Windows line endings to Unix style."""
    return text.replace("\r\n", "\n")


def _tokenize_with_spans(text: str) -> List[Tuple[str, int, int]]:
    """Tokenize text and return tokens with their character spans.

    Returns:
        List of tuples: (token_text, start_index, end_index)
        where text[start_index:end_index] == token_text
    """
    tokenizer = TreebankWordTokenizer()
    spans = list(tokenizer.span_tokenize(text))
    return [(text[start:end], start, end) for start, end in spans]


def _extract_fragments(
    sentence: str,
    tokens: list[str],
    spans: list[tuple[str, int, int]],
    sorted_skills: list[str],
) -> list[str]:
    """Extract text fragments and skills using span-based tracking.

    Args:
        sentence: Original normalized sentence
        tokens: List of token strings
        spans: List of (token, start, end) tuples indexed by token position
        sorted_skills: Skills sorted by length descending

    Returns:
        List of fragments where skills are separated from surrounding text.
    """
    if not tokens:
        # Empty input case: return list containing empty string
        return [sentence]

    result = []
    current_pos = 0
    i = 0

    # Pre-compute token lists for skills for comparison
    skill_sequences = [(skill, skill.split()) for skill in sorted_skills]

    while i < len(tokens):
        matched = False

        # Check for skill match starting at current token
        for skill, skill_tokens in skill_sequences:
            skill_len = len(skill_tokens)
            end_idx = i + skill_len

            if end_idx > len(tokens):
                continue

            # Compare token sequences (ignoring newlines, which are not tokens)
            if tokens[i:end_idx] == skill_tokens:
                # Get character positions from span data
                match_start = spans[i][1]  # start of first token
                match_end = spans[end_idx - 1][2]  # end of last token

                # Add gap between previous position and this match
                # (preserves all whitespace, newlines, tabs)
                gap = sentence[current_pos:match_start]
                result.append(gap)

                # Add skill text (exact substring including newlines between words)
                skill_text = sentence[match_start:match_end]
                result.append(skill_text)

                # Update trackers
                current_pos = match_end
                i = end_idx  # Skip tokens consumed by this skill
                matched = True
                break

        if not matched:
            i += 1

    # Add remaining text after last match
    result.append(sentence[current_pos:])

    return result


def skills_splitter(sentence: str, skills: list[str]) -> list[str]:
    r"""Split a sentence into parts based on a list of skills.

    Preserves exact original text formatting including line breaks, tabs, and
    indentation. Skills are identified even when words are separated by newlines.

    Args:
        sentence: The input sentence to be split.
        skills: A list of skill strings to search for. Skills with more words
                should be listed first (or will be sorted by length).

    Returns:
        A list of strings where reconstruction via ''.join(result) reproduces
        the input (with \r\n normalized to \n). List elements are either skills
        or fragments of text between skills. Empty strings may be present.
    """
    download_nltk_data()

    # Normalize line endings to ensure consistent handling
    normalized_sentence = _normalize_line_endings(sentence)

    # Get tokens with their exact positions in the original text
    tokens_with_spans = _tokenize_with_spans(normalized_sentence)
    tokens = [token for token, _, _ in tokens_with_spans]

    # Sort skills by length (descending) to prioritize longer matches
    sorted_skills = sorted(skills, key=len, reverse=True)

    # Extract fragments preserving exact text formatting
    return _extract_fragments(
        normalized_sentence, tokens, tokens_with_spans, sorted_skills
    )
