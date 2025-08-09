import re

import nltk
from nltk.downloader import Downloader
from nltk.tokenize import sent_tokenize, word_tokenize

_punctuation_re = re.compile(r"\s+([)\]}.,;:!?])")
_open_pair_re = re.compile(r"([\(\[\{])\s+")


def download_nltk_data() -> None:
    """Ensure the nltk data is present.

    Notes:
        1. Checks if the 'punkt' NLTK data is installed.
        2. If not installed, downloads 'punkt' data.
        3. Checks if the 'punkt_tab' NLTK data is installed.
        4. If not installed, downloads 'punkt_tab' data.
        5. This function performs disk access to download required NLTK data.
    """
    downloader = Downloader()
    if not downloader.is_installed("punkt"):
        nltk.download("punkt")
    if not downloader.is_installed("punkt_tab"):
        nltk.download("punkt_tab")


def normalize_sentence_fragment(fragment: str) -> str:
    """Normalize a sentence by removing extra spaces and punctuation.

    Args:
        fragment: The input sentence fragment to normalize.

    Returns:
        The normalized sentence fragment with consistent spacing and punctuation.

    Notes:
        1. Strips leading and trailing whitespace from the fragment.
        2. Splits the fragment into words and rejoins with single spaces to remove extra spaces.
        3. Strips leading and trailing spaces again.
        4. Fixes spacing before punctuation marks by removing spaces before them.
        5. Fixes spacing after opening punctuation (e.g., '(', '[', '{') by removing spaces after them.
    """
    _fragment = fragment.strip()

    # Remove extra spaces
    sentence = " ".join(_fragment.split())

    # Remove leading/trailing spaces
    sentence = sentence.strip()

    # Fix any spaces before punctuation
    sentence = _punctuation_re.sub(r"\1 ", sentence)

    # Fix any spaces after opening pair, like parenthesis
    sentence = _open_pair_re.sub(r"\1", sentence)

    return sentence


def nltk_normalize_fragment(fragment: str) -> str:
    """Use a more advanced detokenizer to reassemble fragments.

    Args:
        fragment: The input sentence fragment to normalize.

    Returns:
        The normalized sentence fragment after detokenization and punctuation fixes.

    Notes:
        1. Strips leading and trailing whitespace from the fragment.
        2. Uses nltk.sent_tokenize to split the fragment into sentences, taking the first.
        3. Fixes trailing punctuation by removing extra spaces before punctuation.
        4. Fixes punctuation spacing after opening pairs (e.g., '(', '[', '{').
        5. This function performs network access if NLTK data is not present, via nltk.download.
    """
    _fragment = fragment.strip()
    _raw_detokenize = sent_tokenize(_fragment)[0]
    _fixed_trailing_punctuation = _punctuation_re.sub(r"\1", _raw_detokenize)
    _fixed_punctuation = _open_pair_re.sub(r"\1", _fixed_trailing_punctuation)

    return _fixed_punctuation


def skills_splitter(sentence: str, skills: list[str]) -> list[str]:
    """Split a sentence into parts based on a list of skills.

    This function identifies skills within a sentence and separates them into distinct parts,
    allowing for individual highlighting or processing of each skill.

    Args:
        sentence: The input sentence to be split.
        skills: A list of skill strings to search for in the sentence. Skills with more words
                should be listed first for accurate matching.

    Returns:
        A list of strings where each element is either a skill or a fragment of text between skills.

    Notes:
        1. Ensures required NLTK data ('punkt', 'punkt_tab') are downloaded if missing.
        2. Tokenizes the input sentence into individual words and punctuation.
        3. Sorts the skills by length in descending order to prioritize longer, more specific skills.
        4. Iterates through each token in the sentence, checking for matches with any skill.
        5. When a skill is found, adds the current fragment (if any) and the skill to the result.
        6. Skips over tokens that are part of the matched skill.
        7. Continues until all tokens are processed.
        8. Adds any remaining fragment to the result.
        9. Normalizes each part of the result using nltk_normalize_fragment.
        10. Returns the final list of normalized fragments and skills.
        11. This function performs disk access if NLTK data is not present.
    """
    # make sure the nltk data is present
    # TODO: move this to someplace that isn't called all the time
    download_nltk_data()

    # Tokenize the sentence into words and punctuation
    _sentence_tokens = word_tokenize(sentence)

    # Create a list to store the result
    _result = []
    _current_fragment = []

    # sort the skills by length in reverse order
    # this should result in more specific to less specific skills
    _sorted_skills = sorted(skills, key=len, reverse=True)

    _offset = 0
    for i in range(len(_sentence_tokens)):
        _ndx = _offset + i

        if _ndx >= len(_sentence_tokens):
            break

        _match = False

        # Check for multi-word keywords
        for _skill in _sorted_skills:
            _skill_tokens = _skill.split()
            if _sentence_tokens[_ndx : _ndx + len(_skill_tokens)] == _skill_tokens:
                # we have a match

                # add the current fragment to the result
                if _current_fragment:
                    _result.append(" ".join(_current_fragment))

                # add the skill to the result
                _result.append(" ".join(_skill_tokens))

                # skip any words included in the skill
                # -1 to account for the first one
                _offset = _offset + len(_skill_tokens) - 1

                # reset the current fragment
                _current_fragment = []

                # prevent the sentence token from being added
                _match = True

                # stop checking skills
                break

        if not _match:
            _current_fragment.append(_sentence_tokens[_ndx])

    if _current_fragment:
        _result.append(" ".join(_current_fragment))

    _final_result = []
    for _part in _result:
        _normalized = nltk_normalize_fragment(_part)
        _final_result.append(_normalized)

    return _final_result
