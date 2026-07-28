"""Day 2 自动检查文件。

运行：
    python day02/test_day02.py

所有检查通过时输出：
    All Day 2 tests passed.
"""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

from student_report import (
    assign_grade,
    build_report,
    calculate_student_average,
    calculate_subject_average,
    load_students,
    parse_score,
    validate_name,
    write_report,
)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def assert_raises(expected_exception, function, *args) -> None:
    try:
        function(*args)
    except expected_exception:
        return
    except Exception as error:
        raise AssertionError(
            f"Expected {expected_exception.__name__}, "
            f"but got {type(error).__name__}: {error}"
        ) from error
    raise AssertionError(f"Expected {expected_exception.__name__}, but no error was raised")


def run_tests() -> None:
    # 1. parse_score：合法值与边界
    assert parse_score("0", "math", 2) == 0
    assert parse_score("100", "python", 2) == 100
    assert parse_score(" 88 ", "ml", 2) == 88

    # 2. parse_score：类型、空值、范围检查
    assert_raises(ValueError, parse_score, "", "math", 3)
    assert_raises(ValueError, parse_score, "88.5", "math", 3)
    assert_raises(ValueError, parse_score, "abc", "python", 3)
    assert_raises(ValueError, parse_score, "-1", "ml", 3)
    assert_raises(ValueError, parse_score, "101", "ml", 3)

    # 3. validate_name
    assert validate_name(" Alice ", 2) == "Alice"
    assert_raises(ValueError, validate_name, "", 2)
    assert_raises(ValueError, validate_name, "   ", 2)
    assert_raises(ValueError, validate_name, "A" * 31, 2)

    # 4. 等级边界
    assert assign_grade(100) == "A"
    assert assign_grade(90) == "A"
    assert assign_grade(89.99) == "B"
    assert assign_grade(80) == "B"
    assert assign_grade(79.99) == "C"
    assert assign_grade(70) == "C"
    assert assign_grade(69.99) == "D"
    assert assign_grade(60) == "D"
    assert assign_grade(59.99) == "F"
    assert assign_grade(0) == "F"

    # 5. 正常 CSV
    students = load_students(DATA_DIR / "students.csv")
    assert len(students) == 10
    assert students[0] == {"name": "Alice", "math": 91, "python": 88, "ml": 93}
    assert students[-1]["name"] == "Jack"
    assert all(isinstance(student["math"], int) for student in students)

    # 6. CSV 异常检查
    invalid_files = [
        "students_invalid_type.csv",
        "students_invalid_range.csv",
        "students_missing_name.csv",
        "students_duplicate_name.csv",
        "students_bad_header.csv",
        "students_missing_score.csv",
        "students_extra_column.csv",
        "students_empty.csv",
    ]
    for filename in invalid_files:
        assert_raises(ValueError, load_students, DATA_DIR / filename)

    assert_raises(FileNotFoundError, load_students, DATA_DIR / "not_found.csv")

    # 7. 平均分
    alice = {"name": "Alice", "math": 91, "python": 88, "ml": 93}
    assert abs(calculate_student_average(alice) - 90.6666666667) < 1e-9
    assert calculate_subject_average(students, "math") == 80.9
    assert calculate_subject_average(students, "python") == 83.4
    assert calculate_subject_average(students, "ml") == 81.8
    assert_raises(ValueError, calculate_subject_average, students, "english")
    assert_raises(ValueError, calculate_subject_average, [], "math")

    # 8. 报告字段与排序
    report = build_report(students)
    assert len(report) == 10
    assert list(report[0].keys()) == [
        "name", "math", "python", "ml", "average", "grade"
    ]
    assert [student["name"] for student in report[:3]] == ["Ivy", "Eva", "Alice"]
    assert report[0]["average"] == 99.0
    assert report[0]["grade"] == "A"

    tie_students = [
        {"name": "Bob", "math": 90, "python": 90, "ml": 90},
        {"name": "Alice", "math": 90, "python": 90, "ml": 90},
    ]
    tie_report = build_report(tie_students)
    assert [student["name"] for student in tie_report] == ["Alice", "Bob"]

    # 9. 输出 CSV
    with tempfile.TemporaryDirectory() as temporary_directory:
        output_path = Path(temporary_directory) / "nested" / "student_report.csv"
        write_report(report, output_path)
        assert output_path.exists()

        with output_path.open("r", newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        assert rows[0]["name"] == "Ivy"
        assert rows[0]["average"] == "99.00"
        assert rows[2]["name"] == "Alice"
        assert rows[2]["average"] == "90.67"
        assert rows[0]["grade"] == "A"

    print("All Day 2 tests passed.")


if __name__ == "__main__":
    run_tests()
