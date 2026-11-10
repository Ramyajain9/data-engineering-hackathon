
import pandas as pd
import time


# BASELINE PIPELINE
def baseline_pipeline():

    start_time = time.perf_counter()

    # Read all columns
    orders = pd.read_csv("data/large_orders.csv")
    customers = pd.read_csv("data/large_customers.csv")

    # Join datasets
    merged = pd.merge(
        orders,
        customers,
        on="customer_id",
        how="inner"
    )

    # Calculate total sales
    sales = merged.groupby(
        "customer_name"
    )["amount"].sum()

    # Measure memory usage
    memory_used = (
        orders.memory_usage(deep=True).sum()
        + customers.memory_usage(deep=True).sum()
        + merged.memory_usage(deep=True).sum()
    )

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return execution_time, memory_used, len(merged), len(sales)


# OPTIMIZED PIPELINE
def optimized_pipeline():

    start_time = time.perf_counter()

    # Read only required columns
    orders = pd.read_csv(
        "data/large_orders.csv",
        usecols=["order_id", "customer_id", "amount"]
    )

    customers = pd.read_csv(
        "data/large_customers.csv",
        usecols=["customer_id", "customer_name"]
    )

    # Join datasets
    merged = pd.merge(
        orders,
        customers,
        on="customer_id",
        how="inner"
    )

    # Calculate total sales
    sales = merged.groupby(
        "customer_name"
    )["amount"].sum()

    # Measure memory usage
    memory_used = (
        orders.memory_usage(deep=True).sum()
        + customers.memory_usage(deep=True).sum()
        + merged.memory_usage(deep=True).sum()
    )

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    return execution_time, memory_used, len(merged), len(sales)


# RUN BOTH PIPELINES 5 TIMES
baseline_times = []
optimized_times = []

baseline_memory = []
optimized_memory = []

for i in range(5):

    b_time, b_memory, b_records, b_sales = baseline_pipeline()

    o_time, o_memory, o_records, o_sales = optimized_pipeline()

    baseline_times.append(b_time)
    optimized_times.append(o_time)

    baseline_memory.append(b_memory)
    optimized_memory.append(o_memory)


# CALCULATE AVERAGES
avg_baseline = sum(baseline_times) / 5
avg_optimized = sum(optimized_times) / 5

avg_baseline_memory = sum(baseline_memory) / 5
avg_optimized_memory = sum(optimized_memory) / 5


# CALCULATE IMPROVEMENTS
time_improvement = (
    (avg_baseline - avg_optimized) / avg_baseline
) * 100

memory_improvement = (
    (avg_baseline_memory - avg_optimized_memory)
    / avg_baseline_memory
) * 100


# DISPLAY RESULTS
print("\n===== BENCHMARK RESULTS =====")

print("Baseline time:", avg_baseline, "seconds")
print("Optimized time:", avg_optimized, "seconds")

print("Time improvement:", time_improvement, "%")

print("\nBaseline memory:", avg_baseline_memory / (1024 * 1024), "MB")
print("Optimized memory:", avg_optimized_memory / (1024 * 1024), "MB")

print("Memory improvement:", memory_improvement, "%")

print("\nTotal merged records:", o_records)
print("Total customers in sales:", o_sales)


# SAVE RESULTS
results = pd.DataFrame({
    "Metric": [
        "Baseline Average Time",
        "Optimized Average Time",
        "Time Improvement Percentage",
        "Baseline Memory MB",
        "Optimized Memory MB",
        "Memory Improvement Percentage",
        "Merged Records"
    ],
    "Value": [
        avg_baseline,
        avg_optimized,
        time_improvement,
        avg_baseline_memory / (1024 * 1024),
        avg_optimized_memory / (1024 * 1024),
        memory_improvement,
        o_records
    ]
})

results.to_csv(
    "output/benchmark_results.csv",
    index=False
)

print("\nBenchmark results saved successfully!")
