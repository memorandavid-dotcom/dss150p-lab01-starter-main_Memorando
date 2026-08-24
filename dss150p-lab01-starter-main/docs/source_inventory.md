# Source Inventory

## 1. Customers (CSV)
* **Source name:** customers
* **Source-system type:** File / Export
* **Data format:** CSV
* **Structured / semi-structured / unstructured:** Structured
* **Expected update pattern:** Daily / Batch
* **Likely acquisition method:** Local file system / SFTP
* **Schema location or schema owner:** `data/raw/customers.csv`
* **Possible primary/business key:** `customer_id`
* **Potential schema-evolution risk:** Low
* **Potential data-quality risk:** Missing values, incorrect data types

## 2. Orders (JSON)
* **Source name:** orders
* **Source-system type:** File / Document
* **Data format:** JSON
* **Structured / semi-structured / unstructured:** Semi-structured
* **Expected update pattern:** Real-time / Hourly
* **Likely acquisition method:** API / File transfer
* **Schema location or schema owner:** `data/raw/orders.json`
* **Possible primary/business key:** `order_id`
* **Potential schema-evolution risk:** High (nested attributes may change)
* **Potential data-quality risk:** Unnested structures, inconsistent date formats

## 3. Products (Parquet)
* **Source name:** products
* **Source-system type:** Analytical Lakehouse / Storage
* **Data format:** Parquet
* **Structured / semi-structured / unstructured:** Structured
* **Expected update pattern:** Batch / Weekly
* **Likely acquisition method:** Data Lake / S3 / Local File
* **Schema location or schema owner:** `data/raw/products.parquet`
* **Possible primary/business key:** `product_id`
* **Potential schema-evolution risk:** Low (strongly typed)
* **Potential data-quality risk:** Type mismatch during reading

## 4. REST API
* **Source name:** External REST API
* **Source-system type:** Web API / External Service
* **Data format:** JSON
* **Structured / semi-structured / unstructured:** Semi-structured
* **Expected update pattern:** On-demand / Real-time
* **Likely acquisition method:** HTTP GET requests
* **Schema location or schema owner:** External API endpoint
* **Possible primary/business key:** `id`
* **Potential schema-evolution risk:** Medium
* **Potential data-quality risk:** Network timeouts, missing payload fields
* **Retrieval Timestamp (UTC):** *(Update after running Task 2.3)*

## 5. PostgreSQL Database
* **Source name:** `inventory_snapshot`
* **Source-system type:** Relational Database (OLTP)
* **Data format:** Relational Table
* **Structured / semi-structured / unstructured:** Structured
* **Expected update pattern:** Transactional / Continuous
* **Likely acquisition method:** SQL Queries / Direct Connection
* **Schema location or schema owner:** `public` schema / PostgreSQL
* **Possible primary/business key:** `inventory_id` / `item_id`
* **Potential schema-evolution risk:** Low (strict DB schema)
* **Potential data-quality risk:** Foreign key constraints, stale snapshots