"""Day 2: CSV student report analyzer.

只能使用 Python 标准库。
完成所有 TODO 后运行：
    python day02/test_day02.py
    python day02/student_report.py
"""

from __future__ import annotations

import csv
from pathlib import Path


SUBJECTS = ("math", "python", "ml")
EXPECTED_HEADERS = ["name", "math", "python", "ml"]


def parse_score(value: str, subject: str, row_number: int) -> int:
    """将分数字符串转换为 0～100 的整数。

    不合法时抛出 ValueError，错误信息必须包含：
    行号、科目名称、原始值。
    """
    original_value = value

    try:
        score = int(value.strip())
    except (AttributeError, ValueError):
        raise ValueError(
            f"Row {row_number}: invalid {subject} score '{original_value}'"
        )
    if not 0 <= score <= 100:
        raise ValueError(
            f"Row {row_number}: {subject} score out of range "
            f"'{original_value}'"
        )
    return int(score)


def validate_name(value: str, row_number: int) -> str:
    """清理并验证姓名。

    姓名去除首尾空格后必须非空，长度为 1～30 个字符。
    """
    cleaned_name = value.strip()

    if not 1 <= len(cleaned_name) <= 30:
        raise ValueError(
            f"Row {row_number}: invalid name '{cleaned_name}'"
        )

    return cleaned_name


def load_students(file_path: Path) -> list[dict]:
    """读取并验证 CSV，返回学生字典列表。

    必须检查：
    1. 表头完全正确；
    2. 每行没有缺失或多余字段；
    3. 姓名合法且不重复；
    4. 三科成绩均为 0～100 的整数；
    5. 至少有一条学生记录。
    """
    rows = []
    with open(file_path, 'r', encoding='utf-8', newline='') as f:
        temp = csv.DictReader(f)
        if temp.fieldnames != ['name', 'math', 'python', 'ml']:
            raise ValueError('Invalid CSV headers')
        dict_name = dict()
        for row_number, row in enumerate(temp, start=2):
            if len(row) != 4:
                raise ValueError
            row['name'] = validate_name(row['name'], row_number)
            if row['name'] in dict_name:
                raise ValueError(f"Row {row_number}: duplicate name '{row['name']}'")
            dict_name[row['name']] = row_number
            row['math'] = parse_score(row['math'], 'math', row_number)
            row['python'] = parse_score(row['python'], 'python', row_number)
            row['ml'] = parse_score(row['ml'], 'ml', row_number)
            rows.append(row)
        if len(rows) == 0:
            raise ValueError('No student records found')
        return rows


def calculate_student_average(student: dict) -> float:
    """返回学生三科原始平均分，不在此函数中格式化字符串。"""
    return (student['math']+student['python']+student['ml']) / 3


def assign_grade(average: float) -> str:
    """按平均分返回 A/B/C/D/F。"""
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    elif average >= 60:
        return 'D'
    else:
        return 'F'


def calculate_subject_average(students: list[dict], subject: str) -> float:
    """计算指定科目的班级平均分。"""
    if len(students) == 0:
        raise ValueError
    if subject not in SUBJECTS:
        raise ValueError(f"Invalid subject '{subject}'")
    sum_score = 0
    for row in students:
        sum_score += row[subject]
    return sum_score / len(students)


def build_report(students: list[dict]) -> list[dict]:
    sorted_students = sorted(
        students,
        key=lambda student: (
            -calculate_student_average(student),
            student["name"],
        ),
    )

    report = []

    for student in sorted_students:
        raw_average = calculate_student_average(student)

        report.append(
            {
                "name": student["name"],
                "math": student["math"],
                "python": student["python"],
                "ml": student["ml"],
                "average": round(raw_average, 2),
                "grade": assign_grade(raw_average),
            }
        )

    return report


def write_report(report: list[dict], output_path: Path) -> None:
    """将报告写入 CSV。

    输出表头固定为：
    name,math,python,ml,average,grade

    average 写入时必须始终显示两位小数。
    输出目录不存在时必须自动创建。
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        fieldnames = ["name", "math", "python", "ml", "average", "grade"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in report:
            output_row = {
                **row,
                "average": f"{row['average']:.2f}",
            }
            writer.writerow(output_row)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "data" / "students.csv"
    output_path = base_dir / "output" / "student_report.csv"

    try:
        students = load_students(input_path)
        report = build_report(students)

        print(f"Loaded students: {len(students)}")
        print(f"Math average: {calculate_subject_average(students, 'math'):.2f}")
        print(f"Python average: {calculate_subject_average(students, 'python'):.2f}")
        print(f"ML average: {calculate_subject_average(students, 'ml'):.2f}")
        print("Top 3 students:")

        for index, student in enumerate(report[:3], start=1):
            print(
                f"{index}. {student['name']} - "
                f"{student['average']:.2f} - {student['grade']}"
            )

        write_report(report, output_path)
        print(f"Report saved to: {output_path}")

    except (FileNotFoundError, ValueError, csv.Error) as error:
        print(f"Error: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
