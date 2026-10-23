"""Generate data/students.csv: 3 semesters x 3 courses per student."""

import csv
import random
from pathlib import Path

SEMESTER_COURSES = {
    1: ["MATH101", "PHYS101", "CS101"],
    2: ["ENG101", "STAT101", "CS102"],
    3: ["MATH201", "CS201", "ENG201"],
}
NAMES = [
    "Amina",
    "Brian",
    "Chloe",
    "David",
    "Eve",
    "Felix",
    "Grace",
    "Hassan",
    "Ines",
    "Jamal",
    "Kofi",
    "Lina",
    "Moses",
    "Nadia",
    "Omar",
    "Paula",
]
MAJORS = ["CS", "Math", "Physics", "Engineering"]


def main() -> None:
    random.seed(42)
    header = ["student_id", "name", "major", "year"]
    header += [f"s{s}_{c}" for s, courses in SEMESTER_COURSES.items() for c in courses]

    out = Path("data")
    out.mkdir(exist_ok=True)
    with open(out / "students.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(1, 41):
            base = random.gauss(72, 12)
            row = [
                f"S{i:03d}",
                NAMES[i % len(NAMES)],
                random.choice(MAJORS),
                random.randint(1, 4),
            ]
            for courses in SEMESTER_COURSES.values():
                for _ in courses:
                    blank = random.random() < 0.03
                    score = max(0, min(100, round(random.gauss(base, 8), 1)))
                    row.append("" if blank else score)
            writer.writerow(row)
    print("wrote data/students.csv")


if __name__ == "__main__":
    main()
