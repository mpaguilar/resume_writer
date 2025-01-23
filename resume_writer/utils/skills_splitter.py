import re

import nltk
from nltk.downloader import Downloader
from nltk.tokenize import sent_tokenize, word_tokenize

_punctuation_re = re.compile(r"\s+([)\]}.,;:!?])")
_open_pair_re = re.compile(r"([\(\[\{])\s+")


def download_nltk_data() -> None:
    """Ensure the nltk data is present."""
    downloader = Downloader()
    if not downloader.is_installed("punkt"):
        nltk.download("punkt")
    if not downloader.is_installed("punkt_tab"):
        nltk.download("punkt_tab")



def normalize_sentence_fragment(fragment: str) -> str:
    """Normalize a sentence by removing extra spaces and punctuation.

    Args:
        fragment: The input sentence.

    Returns:
        The normalized sentence.

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
    """Use a more advanced detokenizer to reassemble fragments."""
    _fragment = fragment.strip()
    _raw_detokenize = sent_tokenize(_fragment)[0]
    _fixed_trailing_punctuation = _punctuation_re.sub(r"\1", _raw_detokenize)
    _fixed_punctuation = _open_pair_re.sub(r"\1", _fixed_trailing_punctuation)

    return _fixed_punctuation


def skills_splitter(sentence: str, skills: list[str]) -> list[str]:
    """Split a sentence into parts based on list of skills.

    Take a sentence, look for the skills in the sentence, and return
    a list with the skills isolated. This is to be able to highlight
    individual skills within a sentence.
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
