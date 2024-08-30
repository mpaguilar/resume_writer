def block_lines(test_data: str):
    lines = test_data.split("\n")

    return_lines = []
    for line in lines:
        if line.startswith("# "):
            return_lines.append(line[1:])
        else:
            return_lines.append(line)

    return return_lines


def deindenter(lines, count: int = 1):
    """Remove leading '#' from sub-blocks."""

    _lines = []
    for _ in range(count):
        _lines.clear()
        for _line in lines:
            if _line.startswith("##"):
                _line = _line[1:]
                _lines.append(_line)
            else:
                _lines.append(_line)
        lines = _lines.copy()

    return _lines


def get_data_lines(
    test_data: str,
    test_data_start_line: int,
    first_line_number: int,
    last_line_number: int,
) -> list[str]:
    """Get the lines of data from the test data block.

    Calculates based on line numbers of the test.

    test_data: The test data block.

    test_data_start_line: The line number of the first line of the test data
    in the source code.
    In other words, if you have a test file, and test_data starts on line 10,
    then this value is 10.

    first_line_number: The line number of the first line of data to be returned.
    last_line_number: The line number of the last line of data to be returned.

    """
    _data_start = first_line_number - test_data_start_line
    _data_end = last_line_number - test_data_start_line
    _lines = block_lines(test_data)
    _lines = _lines[_data_start : _data_end + 1]  # add one to include the last line
    return _lines
