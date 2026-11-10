
import pandas as pd
import time
import os
import sys
from datetime import datetime

# Start timer
start_time = time.time()


# Function to save failed pipeline details
def log_failure(error):

    failed_log = pd.DataFrame([{
        "run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_orders": 0,
        "valid_orders": 0,
        "rejected_orders": 0,
        "execution_time_seconds": time.time() - start_time,
        "status": "FAILED",
        "error_message": str(error)
    }])

    failed_log.to_csv(
        "output/pipeline_logs.csv",
        mode="a",
        header=not os.path.exists("output/pipeline_logs.csv"),
        index=False
    )


try:

    # Read datasets
    orders = pd.read_csv("data/orders.csv")
    customers = pd.read_csv("data/customers.csv")
        # Check required columns
    required_order_columns = [
        "order_id", "customer_id", "amount"
    ]

    required_customer_columns = [
        "customer_id", "customer_name", "city"
    ]

    if not all(col in orders.columns for col in required_order_columns):
        raise ValueError("Orders file has missing columns")

    if not all(col in customers.columns for col in required_customer_columns):
        raise ValueError("Customers file has missing columns")

    print("ORDERS DATA")
    print(orders)

    print("CUSTOMERS DATA")
    print(customers)

    # Check missing values
    print("\nCHECKING MISSING VALUES")
    print(orders.isnull().sum())

    # Convert amount into numeric values
    orders["amount"] = pd.to_numeric(
        orders["amount"], errors="coerce"
    )

    # Identify duplicate order IDs
    duplicate_ids = orders["order_id"].duplicated(keep=False)

    # Store valid customer IDs
    valid_customer_ids = set(
        customers["customer_id"].dropna()
    )

    # Find rejection reasons
    def get_rejection_reason(row):

        reasons = []

        if pd.isna(row["order_id"]):
            reasons.append("Missing order ID")

        if pd.isna(row["customer_id"]):
            reasons.append("Missing customer ID")

        if pd.isna(row["amount"]):
            reasons.append("Missing or invalid amount")

        elif row["amount"] <= 0:
            reasons.append("Invalid amount")

        if pd.notna(row["order_id"]) and duplicate_ids.loc[row.name]:
            reasons.append("Duplicate order ID")

        if (
            pd.notna(row["customer_id"])
            and row["customer_id"] not in valid_customer_ids
        ):
            reasons.append("Unknown customer ID")

        return "; ".join(reasons)

    # Add rejection reasons
    orders["rejection_reason"] = orders.apply(
        get_rejection_reason, axis=1
    )

    # Separate valid and rejected orders
    invalid_orders = orders[
        orders["rejection_reason"] != ""
    ].copy()

    valid_orders = orders[
        orders["rejection_reason"] == ""
    ].drop(columns=["rejection_reason"])

    print("\nVALID ORDERS")
    print(valid_orders)

    print("\nREJECTED ORDERS")
    print(invalid_orders)

    # Save rejected orders
    invalid_orders.to_csv(
        "output/rejected_orders.csv", index=False
    )

    # Combine valid orders and customers
    merged = pd.merge(
        valid_orders,
        customers,
        on="customer_id",
        how="inner"
    )

    print("\nCOMBINED ORDERS AND CUSTOMERS")
    print(merged)

    # Calculate total sales by customer
    sales = merged.groupby(
        "customer_name"
    )["amount"].sum()
    

    print("\nTOTAL SALES BY CUSTOMER")
    print(sales)

    # Save output files
    merged.to_csv(
        "output/cleaned_orders.csv", index=False
    )

    sales.to_csv("output/customer_sales.csv")

    # Finish timer
    end_time = time.time()
    execution_time = end_time - start_time

    # Save successful pipeline details
    run_log = pd.DataFrame([{
        "run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_orders": len(orders),
        "valid_orders": len(valid_orders),
        "rejected_orders": len(invalid_orders),
        "execution_time_seconds": execution_time,
        "status": "SUCCESS",
        "error_message": ""
    }])

    run_log.to_csv(
        "output/pipeline_logs.csv",
        mode="a",
        header=not os.path.exists("output/pipeline_logs.csv"),
        index=False
    )

    print("\nPipeline log saved successfully!")
    print("Execution time:", execution_time, "seconds")


except Exception as error:

    # Record pipeline failure
    log_failure(error)

    print("\nPIPELINE FAILED!")
    print("Error:", error)

    sys.exit(1)
