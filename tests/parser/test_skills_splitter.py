from resume_writer.utils.skills_splitter import skills_splitter


def test_single_skill():
    sentence = "I have experience in Python."
    skills = ["Python"]
    expected = ["I have experience in", "Python", "."]
    _result = skills_splitter(sentence, skills)
    assert _result == expected


def test_multiple_skills():
    sentence = "I am proficient in Python and Java."
    skills = ["Python", "Java"]
    expected = ["I am proficient in", "Python", "and", "Java", "."]
    assert skills_splitter(sentence, skills) == expected


def test_skill_with_space():
    sentence = "I am proficient with Spring Boot and Java."
    skills = ["Spring Boot", "Java"]
    expected = ["I am proficient with", "Spring Boot", "and", "Java", "."]
    assert skills_splitter(sentence, skills) == expected


def test_no_skills():
    sentence = "I am a software engineer."
    skills = ["Python", "Java"]
    expected = ["I am a software engineer."]
    assert skills_splitter(sentence, skills) == expected


def test_skills_at_beginning():
    sentence = "Python and Java are my skills."
    skills = ["Python", "Java"]
    expected = ["Python", "and", "Java", "are my skills."]
    assert skills_splitter(sentence, skills) == expected


def test_skills_at_end():
    sentence = "I am skilled in Python and Java."
    skills = ["Python", "Java"]
    expected = ["I am skilled in", "Python", "and", "Java", "."]
    assert skills_splitter(sentence, skills) == expected


def test_multiple_skills_in_sentence():
    sentence = "I have experience in Python, Java, and C++."
    skills = ["Python", "Java", "C++"]
    expected = ["I have experience in", "Python", ",", "Java", ", and", "C++", "."]
    _result = skills_splitter(sentence, skills)
    assert _result == expected


def test_skills_with_punctuation():
    sentence = "I am proficient in Python, Java, and C++."
    skills = ["Python", "Java", "C++"]
    expected = ["I am proficient in", "Python", ",", "Java", ", and", "C++", "."]
    assert skills_splitter(sentence, skills) == expected


def test_empty_sentence():
    sentence = ""
    skills = ["Python", "Java"]
    expected = []
    assert skills_splitter(sentence, skills) == expected


def test_empty_skills():
    sentence = "I am a software engineer."
    skills = []
    expected = ["I am a software engineer."]
    assert skills_splitter(sentence, skills) == expected


def test_fragment_with_parenthesis():
    sentence = "This tests (parenthesis) in sentences"
    skills = ["Python"]
    expected = ["This tests (parenthesis) in sentences"]
    assert skills_splitter(sentence, skills) == expected


def test_fragment_with_skill_and_parenthesis():
    sentence = "This tests (parenthesis) (Python) in sentences"
    skills = ["Python"]
    expected = ["This tests (parenthesis) (", "Python", ") in sentences"]
    _split = skills_splitter(sentence, skills)
    assert _split == expected
