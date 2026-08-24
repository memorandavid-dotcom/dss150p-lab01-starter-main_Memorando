# Source Profile Analysis

## 1. Customers (`customers.csv`)
* **Data Types & Structure:** Contains standard tabular data with scalar data types (`int64`, `object`, `float64`).
* **Missing Values & Duplicates:** Requires validation for null entries across customer contact fields. No complete row-level duplicate records were detected.
* **Observations:** Schema is flat and predictable, suitable for direct ingestion into relational staging tables.

## 2. Orders (`orders.json`)
* **Data Types & Structure:** Contains semi-structured JSON records. Certain fields contain nested dictionaries or array structures representing line items.
* **Missing Values & Duplicates:** Duplicate checking required string casting of unhashable dictionary types. No duplicate raw JSON records were found.
* **Observations:** Nested structures must be flattened or normalized before loading into downstream relational pipelines or analytical models.

## 3. Products (`products.parquet`)
* **Data Types & Structure:** Binary, strongly-typed columnar dataset with explicit schema enforcement.
* **Missing Values & Duplicates:** Zero missing values and zero duplicate rows detected.
* **Observations:** Fast read performance and low storage footprint. Minimal transformation required prior to analytical processing.