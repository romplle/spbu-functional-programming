from functools import reduce


users = [
    {"name": "Alice", "expenses": [100, 50, 75, 200]},
    {"name": "Bob", "expenses": [50, 75, 80, 100]},
    {"name": "Charlie", "expenses": [200, 300, 50, 150]},
    {"name": "David", "expenses": [100, 200, 300, 400]},
    {"name": "Eve", "expenses": [150, 60, 90, 120]},
    {"name": "Frank", "expenses": [80, 200, 150, 100]},
    {"name": "Grace", "expenses": [300, 400, 250, 500]},
    {"name": "Hannah", "expenses": [120, 60, 70, 90]},
    {"name": "Ivy", "expenses": [500, 300, 250, 150]},
    {"name": "Jack", "expenses": [75, 100, 50, 150]},
    {"name": "Kim", "expenses": [100, 90, 80, 60]},
    {"name": "Liam", "expenses": [120, 200, 180, 160]},
    {"name": "Mia", "expenses": [400, 500, 450, 300]},
    {"name": "Noah", "expenses": [90, 80, 100, 150]},
    {"name": "Olivia", "expenses": [60, 90, 110, 140]},
    {"name": "Paul", "expenses": [200, 300, 150, 100]},
    {"name": "Quincy", "expenses": [100, 120, 130, 140]},
    {"name": "Rachel", "expenses": [90, 60, 50, 80]},
    {"name": "Sam", "expenses": [500, 400, 350, 600]},
    {"name": "Tina", "expenses": [150, 200, 300, 250]},
]


def filter_users_by_expense(users, min_expense):
    return list(filter(lambda user: sum(user['expenses']) >= min_expense, users))

def calculate_total_expenses(users):
    return list(map(lambda user: {
        "name": user["name"],
        "total_expense": reduce(lambda x, y: x + y, user["expenses"])
    }, users))

def get_total_expenses_of_filtered_users(filtered_users):
    total_expenses = calculate_total_expenses(filtered_users)
    return reduce(lambda x, y: x + y["total_expense"], total_expenses, 0)

filtered_users = filter_users_by_expense(users, 1400)
calculated_expenses = calculate_total_expenses(filtered_users)
total_expense_sum = get_total_expenses_of_filtered_users(filtered_users)

print("Отфильтрованные пользователи:", filtered_users)
print("Общая сумма расходов:", calculated_expenses)
print("Общая сумма расходов отфильтрованных пользователей:", total_expense_sum)
