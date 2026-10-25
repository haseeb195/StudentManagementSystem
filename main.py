import json
import os
from abc import ABC, abstractmethod


FILE_NAME = "students.json"


# Abstraction: Base class
class Person(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def display(self):
        pass


# Inheritance: Student inherits from Person
class Student(Person):
    def __init__(self, student_id, name, age, course, marks):
        super().__init__(name, age)
        self.student_id = student_id
        self.course = course
        self.__marks = float(marks)

    # Encapsulation: Controlled access to marks
    @property
    def marks(self):
        return self.__marks

    @marks.setter
    def marks(self, value):
        value = float(value)

        if not 0 <= value <= 100:
            raise ValueError("Marks must be between 0 and 100.")

        self.__marks = value

    # Grade calculation
    def calculate_grade(self):
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        elif self.marks >= 40:
            return "D"
        else:
            return "F"

    # Polymorphism: Implementing the abstract display method
    def display(self):
        print("\n--------------------------------")
        print("         STUDENT DETAILS")
        print("--------------------------------")
        print("Student ID :", self.student_id)
        print("Name       :", self.name)
        print("Age        :", self.age)
        print("Course     :", self.course)
        print("Marks      :", self.marks)
        print("Grade      :", self.calculate_grade())
        print("--------------------------------")

    # Convert student object to dictionary for JSON
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "marks": self.marks
        }


# Manage all student records
class StudentManager:
    def __init__(self):
        self.students = []
        self.load_students()

    # Save records to JSON file
    def save_students(self):
        try:
            data = [student.to_dict() for student in self.students]

            with open(FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            print("Student records saved successfully!")

        except OSError as error:
            print("Error saving records:", error)

    # Load records from JSON file
    def load_students(self):
        if not os.path.exists(FILE_NAME):
            return

        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                print("Invalid student data format.")
                return

            loaded_students = []

            for item in data:
                student = Student(
                    item["student_id"],
                    item["name"],
                    item["age"],
                    item["course"],
                    item["marks"]
                )
                loaded_students.append(student)

            self.students = loaded_students
            print("Student records loaded successfully!")

        except (OSError, json.JSONDecodeError, KeyError,
                TypeError, ValueError) as error:
            print("Could not load student records:", error)

    # Add a new student
    def add_student(self):
        try:
            student_id = input("Enter Student ID: ").strip()

            if not student_id:
                print("Student ID cannot be empty.")
                return

            if any(s.student_id == student_id for s in self.students):
                print("Student ID already exists.")
                return

            name = input("Enter Student Name: ").strip()

            if not name:
                print("Name cannot be empty.")
                return

            age = int(input("Enter Age: "))

            if age <= 0:
                print("Age must be positive.")
                return

            course = input("Enter Course: ").strip()

            if not course:
                print("Course cannot be empty.")
                return

            marks = float(input("Enter Marks (0-100): "))

            if not 0 <= marks <= 100:
                print("Marks must be between 0 and 100.")
                return

            student = Student(
                student_id, name, age, course, marks
            )

            self.students.append(student)
            self.save_students()

        except ValueError:
            print("Invalid input. Please enter valid numbers.")

    # View all students
    def view_students(self):
        if not self.students:
            print("No student records found.")
            return

        print("\n========== ALL STUDENTS ==========")

        for student in self.students:
            student.display()

        print("Total students:", len(self.students))

    # Search for a student
    def search_student(self):
        student_id = input(
            "Enter Student ID to search: "
        ).strip()

        for student in self.students:
            if student.student_id == student_id:
                student.display()
                return

        print("Student not found.")

    # Update student information
    def update_student(self):
        student_id = input(
            "Enter Student ID to update: "
        ).strip()

        for student in self.students:
            if student.student_id == student_id:
                try:
                    print("Enter the new details:")

                    name = input("New Name: ").strip()

                    if not name:
                        print("Name cannot be empty.")
                        return

                    age = int(input("New Age: "))

                    if age <= 0:
                        print("Age must be positive.")
                        return

                    course = input("New Course: ").strip()

                    if not course:
                        print("Course cannot be empty.")
                        return

                    marks = float(
                        input("New Marks (0-100): ")
                    )

                    if not 0 <= marks <= 100:
                        print("Marks must be between 0 and 100.")
                        return

                    student.name = name
                    student.age = age
                    student.course = course
                    student.marks = marks

                    self.save_students()
                    print("Student updated successfully!")
                    return

                except ValueError:
                    print("Invalid input. Please enter valid numbers.")
                    return

        print("Student not found.")

    # Delete a student
    def delete_student(self):
        student_id = input(
            "Enter Student ID to delete: "
        ).strip()

        for student in self.students:
            if student.student_id == student_id:
                confirm = input(
                    "Are you sure you want to delete this student? (yes/no): "
                ).strip().lower()

                if confirm == "yes":
                    self.students.remove(student)
                    self.save_students()
                    print("Student deleted successfully!")
                else:
                    print("Deletion cancelled.")

                return

        print("Student not found.")

    # Main menu
    def run(self):
        while True:
            print("\n====================================")
            print("     STUDENT MANAGEMENT SYSTEM")
            print("====================================")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Exit")
            print("====================================")

            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.view_students()

            elif choice == "3":
                self.search_student()

            elif choice == "4":
                self.update_student()

            elif choice == "5":
                self.delete_student()

            elif choice == "6":
                print("Thank you for using Student Management System!")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 6.")


# Program entry point
if __name__ == "__main__":
    manager = StudentManager()
    manager.run()