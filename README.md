
# Data Engineering Pipeline Optimization

## 1. Project Overview

This project demonstrates an end-to-end data engineering pipeline using Python and Pandas.

The pipeline processes customer order data, validates records, identifies invalid data, joins datasets, calculates customer sales, and generates output reports.

The project also compares baseline and optimized pipelines to measure execution time and memory usage.

## 2. Technologies Used

- Python
- Pandas
- Pytest
- CSV
- Git

## 3. Project Structure

```text
data_engineering_hackathon/
│
├── data/
│   ├── orders.csv
│   ├── customers.csv
│   ├── large_orders.csv
│   └── large_customers.csv
│
├── output/
│   ├── cleaned_orders.csv
│   ├── customer_sales.csv
│   ├── rejected_orders.csv
│   ├── benchmark_results.csv
│   └── pipeline_logs.csv
│
├── src/
│   ├── main.py
│   ├── generate_data.py
│   └── benchmark.py
│
├── tests/
│   └── test_pipeline.py
│
└── README.md
```

## 4. Pipeline Workflow

1. Read orders and customer datasets.
2. Validate required columns.
3. Check missing values.
4. Identify duplicate order IDs.
5. Validate order amounts.
6. Identify unknown customer IDs.
7. Separate valid and rejected records.
8. Join valid orders with customer information.
9. Calculate total sales by customer.
10. Save output CSV files.
11. Record pipeline execution details.

## 5. Data Validation

The pipeline handles the following data quality issues:

- Missing order IDs.
- Missing customer IDs.
- Missing or invalid amounts.
- Negative and zero amounts.
- Duplicate order IDs.
- Unknown customer IDs.
- Missing required CSV columns.

Invalid records are stored in `rejected_orders.csv` with rejection reasons.

## 6. Performance Optimization

The project compares two approaches:

### Baseline Pipeline
- Reads all columns.
- Performs dataset merging.
- Calculates customer sales.

### Optimized Pipeline
- Reads only required columns using `usecols`.
- Performs dataset merging.
- Calculates customer sales.

### Benchmark Results

| Metric | Result |
|---|---:|
| Baseline execution time | 0.0692 seconds |
| Optimized execution time | 0.0647 seconds |
| Time improvement | 6.57% |
| Baseline memory usage | 26.54 MB |
| Optimized memory usage | 20.45 MB |
| Memory improvement | 22.93% |

*Results are from one local benchmark run and may vary by environment.*

## 7. How to Run the Project

Install dependencies:

```bash
py -m pip install pandas pytest
```

Run the pipeline:

```bash
py src/main.py
```

Run the benchmark:

```bash
py src/benchmark.py
```

Run automated tests:

```bash
py -m pytest -v
```

## 8. Output Files

The pipeline generates:

- `cleaned_orders.csv` – Valid orders combined with customer details.
- `customer_sales.csv` – Total sales by customer.
- `rejected_orders.csv` – Invalid orders with rejection reasons.
- `pipeline_logs.csv` – Pipeline execution status and metrics.
- `benchmark_results.csv` – Performance comparison results.

## 9. Testing

Automated tests cover:

1. Missing values.
2. Duplicate orders.
3. Invalid amounts.
4. Unknown customers.
5. Empty orders.

All 5 current automated tests passed successfully.

## 10. Conclusion

This project demonstrates data ingestion, data quality validation, data transformation, data aggregation, error handling, performance benchmarking, and automated testing using Python and Pandas.
