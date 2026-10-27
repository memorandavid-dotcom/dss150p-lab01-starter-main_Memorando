# Source Inventory

## 1. Customers (CSV)
* **Source name:** customers
* **Source-system type:** File / Export
* **Data format:** CSV
* **Structured / semi-structured / unstructured:** Structured
* **Expected update pattern:** Daily / Batch
* **Likely acquisition method:** Local file system / SFTP
* **Schema location or schema owner:** `customers.csv` (repository root)
* **Columns (actual):** `customer_id`, `first_name`, `last_name`, `email`, `city`, `signup_date`, `customer_segment`
* **Possible primary/business key:** `customer_id` (string, format `C####`; not enforced as UNIQUE in the raw file — duplicates possible)
* **Potential schema-evolution risk:** Low
* **Potential data-quality risk:** Missing values in contact fields; duplicate rows across `first_name`, `last_name`, `email` combinations observed (e.g., rows 6 and 7 share the same email)

## 2. Orders (JSON)
* **Source name:** orders
* **Source-system type:** File / Document
* **Data format:** JSON
* **Structured / semi-structured / unstructured:** Semi-structured
* **Expected update pattern:** Real-time / Hourly
* **Likely acquisition method:** API / File transfer
* **Schema location or schema owner:** `orders.json` (repository root)
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
* **Schema location or schema owner:** `products.parquet` (repository root)
* **Possible primary/business key:** `product_id`
* **Potential schema-evolution risk:** Low (strongly typed)
* **Potential data-quality risk:** Type mismatch during reading

## 4. REST API
* **Source name:** Local classroom REST API (orders endpoint)
* **Source-system type:** Web API / Local HTTP Service
* **Data format:** JSON
* **Structured / semi-structured / unstructured:** Semi-structured
* **Expected update pattern:** On-demand / Real-time
* **Likely acquisition method:** HTTP GET — `http://localhost:8000/api/orders` (served by `local_api_server.py`)
* **Schema location or schema owner:** Response envelope: `{"count": <int>, "records": [<order objects>]}`; top-level record keys: `order_id`, `customer_id`, `order_date`, `status`, `items`
* **Possible primary/business key:** `order_id`
* **Potential schema-evolution risk:** Medium
* **Potential data-quality risk:** Network timeouts, missing payload fields
* **Retrieval Timestamp (UTC):** 2026-10-27T10:07:00+00:00

## 5. PostgreSQL Database
* **Source name:** `support_tickets`
* **Source-system type:** Relational Database (OLTP)
* **Data format:** Relational Table
* **Structured / semi-structured / unstructured:** Structured
* **Expected update pattern:** Transactional / Continuous
* **Likely acquisition method:** SQL Queries / Direct Connection via SQLAlchemy (`psycopg2-binary`)
* **Schema location or schema owner:** `public` schema / PostgreSQL 16 (`dss150p_lab` database)
* **Columns (actual):** `ticket_id` (INTEGER, PK), `customer_id` (VARCHAR(10), NOT NULL), `category` (VARCHAR(40), NOT NULL), `priority` (VARCHAR(10), NOT NULL), `assigned_agent` (VARCHAR(80), nullable), `opened_at` (TIMESTAMP, NOT NULL), `resolved_at` (TIMESTAMP, nullable), `status` (VARCHAR(20), NOT NULL)
* **Constraints / Keys:** `ticket_id` is `PRIMARY KEY`; `customer_id`, `category`, `priority`, `opened_at`, and `status` are `NOT NULL`; `assigned_agent` and `resolved_at` are nullable
* **Possible primary/business key:** `ticket_id`
* **Potential schema-evolution risk:** Low (strict DB schema enforced by DDL)
* **Potential data-quality risk:** `resolved_at` is NULL for unresolved tickets (expected); referential integrity between `customer_id` here and `customers.csv` is not enforced by a foreign key