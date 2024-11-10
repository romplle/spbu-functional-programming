from functools import reduce


students = [
    {"name": "Alice", "age": 20, "grades": [85, 90, 88, 92]},
    {"name": "Bob", "age": 22, "grades": [78, 89, 76, 85]},
    {"name": "Charlie", "age": 21, "grades": [92, 95, 88, 94]},
    {"name": "David", "age": 23, "grades": [65, 75, 70, 68]},
    {"name": "Eve", "age": 20, "grades": [88, 91, 87, 90]},
    {"name": "Frank", "age": 22, "grades": [72, 85, 80, 77]},
    {"name": "Grace", "age": 21, "grades": [93, 90, 89, 92]},
    {"name": "Hannah", "age": 23, "grades": [80, 85, 88, 84]},
    {"name": "Ivy", "age": 19, "grades": [95, 97, 93, 96]},
    {"name": "Jack", "age": 24, "grades": [60, 65, 62, 68]},
    {"name": "Kim", "age": 20, "grades": [89, 91, 87, 92]},
    {"name": "Liam", "age": 22, "grades": [79, 82, 85, 80]},
    {"name": "Mia", "age": 21, "grades": [91, 92, 93, 94]},
    {"name": "Noah", "age": 23, "grades": [67, 72, 70, 68]},
    {"name": "Olivia", "age": 20, "grades": [87, 89, 85, 88]},
    {"name": "Paul", "age": 22, "grades": [82, 85, 79, 83]},
    {"name": "Quincy", "age": 21, "grades": [90, 92, 89, 91]},
    {"name": "Rachel", "age": 23, "grades": [75, 80, 78, 82]},
    {"name": "Sam", "age": 19, "grades": [98, 95, 96, 99]},
    {"name": "Tina", "age": 24, "grades": [63, 68, 65, 66]},
]


def filter_students_by_age(students, age):
    return list(filter(lambda student: student['age'] >= age, students))

def calculate_average_grades(students):
    return list(map(lambda student: {
        "name": student["name"],
        "average_grade": reduce(lambda x, y: x + y, student["grades"]) / len(student["grades"])
    }, students))

def find_top_student(students):
    averages = calculate_average_grades(students)
    return max(averages, key=lambda student: student["average_grade"])

filtered_students = filter_students_by_age(students, 23)
average_grades = calculate_average_grades(filtered_students)
top_student = find_top_student(filtered_students)

print("Отфильтрованные студенты:", filtered_students)
print("Средние баллы:", average_grades)
print("Студент с самым высоким средним баллом:", top_student)
