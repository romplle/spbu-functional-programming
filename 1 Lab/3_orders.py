from functools import reduce


orders = [
    {"order_id": 1, "customer_id": 101, "amount": 150.0},
    {"order_id": 2, "customer_id": 102, "amount": 200.0},
    {"order_id": 3, "customer_id": 101, "amount": 75.0},
    {"order_id": 4, "customer_id": 103, "amount": 100.0},
    {"order_id": 5, "customer_id": 101, "amount": 50.0},
    {"order_id": 6, "customer_id": 104, "amount": 300.0},
    {"order_id": 7, "customer_id": 105, "amount": 250.0},
    {"order_id": 8, "customer_id": 102, "amount": 400.0},
    {"order_id": 9, "customer_id": 103, "amount": 180.0},
    {"order_id": 10, "customer_id": 106, "amount": 500.0},
    {"order_id": 11, "customer_id": 101, "amount": 90.0},
    {"order_id": 12, "customer_id": 107, "amount": 120.0},
    {"order_id": 13, "customer_id": 102, "amount": 60.0},
    {"order_id": 14, "customer_id": 104, "amount": 310.0},
    {"order_id": 15, "customer_id": 105, "amount": 240.0},
    {"order_id": 16, "customer_id": 103, "amount": 130.0},
    {"order_id": 17, "customer_id": 106, "amount": 80.0},
    {"order_id": 18, "customer_id": 101, "amount": 45.0},
    {"order_id": 19, "customer_id": 107, "amount": 170.0},
    {"order_id": 20, "customer_id": 102, "amount": 220.0},
]


def filter_orders_by_customer_id(orders, customer_id):
    return list(filter(lambda order: order['customer_id'] == customer_id, orders))

def calculate_total_amount(orders):
    return reduce(lambda x, y: x + y['amount'], orders, 0)

def calculate_average_order_amount(orders):
    total_amount = calculate_total_amount(orders)
    return total_amount / len(orders)

filtered_orders = filter_orders_by_customer_id(orders, 101)
total_amount = calculate_total_amount(filtered_orders)
average_amount = calculate_average_order_amount(filtered_orders)

print("Отфильтрованные заказы:", filtered_orders)
print("Общая сумма заказов для клиента: ", total_amount)
print("Средняя стоимость заказов для клиента: ", average_amount)