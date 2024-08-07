from datetime import datetime

from utils.resume_stats import DateStats


def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%m/%Y") # noqa: DTZ007

def parse_date_range(date_strs : tuple[str, str]) -> tuple[datetime, datetime]:
    # convert 2 strings to 2 datetimes
    _start_date = parse_date(date_strs[0])
    _end_date = parse_date(date_strs[1]) if date_strs[1] else None
    return _start_date, _end_date


def test_simple_date_ranges():
    _range_text = [
        ("02/2014", "02/2016"),
        ("03/2018", "03/2020"),
        ]
    _ranges = [ parse_date_range(r) for r in _range_text ]
    # create a DateStats object
    ds = DateStats()
    for _start, _end in _ranges:
        ds.add_date_range(_start, _end)

    assert ds.days_of_experience == 1461

def test_no_end_date():
    _range_text = [
        ("02/2014", "02/2016"),
        ("03/2018", None),
        ]
    _ranges = [ parse_date_range(r) for r in _range_text ]
    # create a DateStats object
    ds = DateStats()
    for _start, _end in _ranges:
        ds.add_date_range(_start, _end)

    _calcuated_days = 730 + (datetime.now() - parse_date("03/2018")).days

    assert ds.days_of_experience == _calcuated_days

def test_overlapping_date_ranges():
    _range_text = [
        ("02/2014", "02/2016"),
        ("01/2015", "03/2016"),
        ]
    _ranges = [ parse_date_range(r) for r in _range_text ]
    # create a DateStats object
    ds = DateStats()
    for _start, _end in _ranges:
        ds.add_date_range(_start, _end)

    # 2 years + 1 month, with a February in there
    assert ds.days_of_experience == 730 + 29
