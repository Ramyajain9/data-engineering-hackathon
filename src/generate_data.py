import pandas as pd
import random

customers = []

for i in range(1, 10001):
    customers.append({
        "customer_id": f"C{i:05}",
        "customer_name": f"Customer{i}",
        "city": "Hyderabad"
    })

customers_df = pd.DataFrame(customers)

customers_df.to_csv("data/large_customers.csv", index=False)


orders = []

for i in range(1, 100001):
    orders.append({
        "order_id": i,
        "customer_id": f"C{random.randint(1, 10000):05}",
        "amount": random.randint(100, 5000)
    })

orders_df = pd.DataFrame(orders)

orders_df.to_csv("data/large_orders.csv", index=False)

print("Large datasets created successfully!")