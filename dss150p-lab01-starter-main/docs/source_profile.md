# Source Profile Analysis

## 1. Customers (`customers.csv`)
* **Shape:** 251 rows × 7 columns
* **Columns:** `customer_id`, `first_name`, `last_name`, `email`, `city`, `signup_date`, `customer_segment`
* **Data Types & Structure:** All columns are `object` (string). `signup_date` is stored as a string and requires casting to `datetime` for temporal analysis. `customer_id` follows the pattern `C####`.
* **Missing Values & Duplicates:** No null values detected in any column. At least one pair of rows shares identical `first_name`, `last_name`, and `email` values (e.g., "Paolo Villanueva" appears twice with the same email but different `city` and `customer_segment` values), indicating soft duplicates that are not row-level identical.
* **Observations:** Schema is flat and predictable, suitable for direct ingestion into relational staging tables. `customer_id` is not enforced as unique in the raw CSV — uniqueness must be validated on load.

## 2. Orders (`orders.json`)
* **Data Types & Structure:** Contains semi-structured JSON records. Certain fields contain nested dictionaries or array structures representing line items.
* **Missing Values & Duplicates:** Duplicate checking required string casting of unhashable dictionary types. No duplicate raw JSON records were found.
* **Observations:** Nested structures must be flattened or normalized before loading into downstream relational pipelines or analytical models.

## 3. Products (`products.parquet`)
* **Data Types & Structure:** Binary, strongly-typed columnar dataset with explicit schema enforcement.
* **Missing Values & Duplicates:** Zero missing values and zero duplicate rows detected.
* **Observations:** Fast read performance and low storage footprint. Minimal transformation required prior to analytical processing.

## 4. REST API (`http://localhost:8000/api/orders`)
* **Endpoint:** `GET http://localhost:8000/api/orders` (local classroom server — `local_api_server.py`)
* **Status Code:** 200 OK
* **Content-Type:** `application/json`
* **Top-level structure:** JSON object with keys `count` (integer) and `records` (array)
* **Record Count:** 100 (first 100 orders served from `orders.json`)
* **Sample Record Keys:** `order_id`, `customer_id`, `order_date`, `status`, `items`
* **Missing Values & Duplicates:** Not applicable at the raw HTTP-response level; field-level nulls and duplicates must be validated after flattening the `records` array.
* **Retrieval Timestamp (UTC):** 2026-10-27T10:07:00+00:00
* **Observations:** Schema is consistent with the `orders.json` file. The local server returns a consistent envelope structure. External production APIs would carry higher schema-change risk; this endpoint is stable because it reads from a static local file.

## 5. PostgreSQL (`support_tickets`)
* **Database / Schema:** `dss150p_lab` / `public`
* **Table:** `support_tickets`
* **Shape:** 250 rows × 8 columns
* **Columns & Types:**

| Column | Data Type | Nullable |
|---|---|---|
| `ticket_id` | INTEGER (PK) | NO |
| `customer_id` | VARCHAR(10) | NO |
| `category` | VARCHAR(40) | NO |
| `priority` | VARCHAR(10) | NO |
| `assigned_agent` | VARCHAR(80) | YES |
| `opened_at` | TIMESTAMP | NO |
| `resolved_at` | TIMESTAMP | YES |
| `status` | VARCHAR(20) | NO |

* **Missing Values:** `assigned_agent` and `resolved_at` are intentionally nullable. `resolved_at` is NULL for tickets with `status` of `'Open'` or `'In Progress'`.
* **Constraints:** `ticket_id` is the `PRIMARY KEY`. Five columns carry `NOT NULL` constraints. No foreign-key constraint links `customer_id` to the customers source.
* **Observations:** Schema is well-structured and consistent with the seed DDL. The absence of a foreign key to `customers` means referential integrity must be validated at the application or ETL layer. `priority` values are limited to `'Low'`, `'Medium'`, and `'High'`; a `CHECK` constraint could harden this.