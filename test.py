from typing import List, Dict
import json
import os


class Class_Student :
    def __init__(self, student_id: int, name: str):
        self.student_id = student_id
        self.name = name
        self.marks: Dict[str, float] = {}

    def add_mark(self, subject: str, score: float) -> None:
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100.")
        self.marks[subject] = score

    def calculate_average(self) -> float:
        if not self.marks:
            return 0.0
        return sum(self.marks.values()) / len(self.marks)

    def get_grade(self) -> str:
        avg = self.calculate_average()
        if avg >= 90:
            return "A"
        elif avg >= 75:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 40:
            return "D"
        return "F"

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "marks": self.marks
        }

    @staticmethod
    def from_dict(data: dict) -> "Student":
        student = Student(data["student_id"], data["name"])
        student.marks = data["marks"]
        return student


class StudentManager:
    def __init__(self, storage_file: str = "students.json"):
        self.students: List[Student] = []
        self.storage_file = storage_file
        self.load_data()

    def add_student(self, student_id: int, name: str) -> None:
        if self.get_student(student_id):
            raise ValueError("Student ID already exists.")
        self.students.append(Student(student_id, name))

    def get_student(self, student_id: int) -> Student | None:
        return next((s for s in self.students if s.student_id == student_id), None)

    def add_marks(self, student_id: int, subject: str, score: float) -> None:
        student = self.get_student(student_id)
        if not student:
            raise ValueError("Student not found.")
        student.add_mark(subject, score)

    def get_topper(self) -> Student | None:
        if not self.students:
            return None
        return max(self.students, key=lambda s: s.calculate_average())

    def save_data(self) -> None:
        with open(self.storage_file, "w") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def load_data(self) -> None:
        if not os.path.exists(self.storage_file):
            return
        with open(self.storage_file, "r") as f:
            data = json.load(f)
            self.students = [Student.from_dict(s) for s in data]


def main():
    manager = StudentManager()

    while True:
        print("\n===== Student Management System =====")
        print("1. Add Student")
        print("2. Add Marks")
        print("3. View Student")
        print("4. View Topper")
        print("5. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                sid = int(input("Student ID: "))
                name = input("Name: ")
                manager.add_student(sid, name)
                manager.save_data()
                print("Student added successfully!")

            elif choice == "2":
                sid = int(input("Student ID: "))
                subject = input("Subject: ")
                score = float(input("Score: "))
                manager.add_marks(sid, subject, score)
                manager.save_data()
                print("Marks added successfully!")

            elif choice == "3":
                sid = int(input("Student ID: "))
                student = manager.get_student(sid)
                if not student:
                    print("Student not found.")
                else:
                    print(f"\nName: {student.name}")
                    print("Marks:", student.marks)
                    print("Average:", student.calculate_average())
                    print("Grade:", student.get_grade())

            elif choice == "4":
                topper = manager.get_topper()
                if topper:
                    print(f"Topper: {topper.name} (Avg: {topper.calculate_average():.2f})")
                else:
                    print("No students available.")

            elif choice == "5":
                print("Exiting...")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()