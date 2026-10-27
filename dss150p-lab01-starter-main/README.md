# DSS150P Lab 01 - Data Source Ingestion & Profiling

**Student Name:** David Hyzxent L. Memorando  
**Student Number:** 2024162312  
**Course:** DSS150P  

---

## Purpose of the Laboratory
This laboratory establishes a reproducible local engineering environment using Python virtual environments, Docker containers, and Git. It covers ingesting, profiling, and inspecting heterogeneous data sources (CSV, JSON, Parquet, REST API, and PostgreSQL) to create data inventories, profile reports, and formalized data contracts.

---

## Software Requirements
* **Python:** 3.10 or higher
* **Container Engine:** Docker Desktop (with Docker Compose)
* **Version Control:** Git
* **Python packages:** `pandas`, `pyarrow`, `requests`, `sqlalchemy`, `psycopg2-binary` (see `requirements.txt`)

---

## Repository Structure

```
dss150p-lab01-starter-main/
├── customers.csv                   # Source: customer records (251 rows, 7 columns)
├── orders.json                     # Source: order records (nested JSON)
├── products.parquet                # Source: product catalogue (Parquet columnar)
├── seed_support_tickets.sql        # PostgreSQL seed: 250 support-ticket rows
├── docker-compose.yml              # PostgreSQL 16 service definition
├── requirements.txt                # Python dependencies
├── local_api_server.py             # Classroom REST API server (port 8000)
├── sql/
│   └── 01_create_schema.sql        # DDL: lab.customers staging table
├── src/
│   ├── profile_sources.py          # Profiles CSV / JSON / Parquet sources
│   ├── inspect_sources.py          # Low-level CSV + JSON field inspection
│   ├── inspect_api.py              # Fetches & snapshots the REST API
│   ├── inspect_postgres.py         # Queries support_tickets via SQLAlchemy
│   └── verify_environment.py       # Checks Python, Docker, and package versions
└── docs/
    ├── source_inventory.md         # Five-source data inventory
    ├── source_profile.md           # Profiling observations per source
    ├── data_contract.yaml          # Formal data contract for customers.csv
    ├── lifecycle_map.md            # End-to-end lifecycle map for all sources
    └── reflection.md               # Personal reflection on the lab
```

---

## Exact Steps to Reproduce the Environment

### Step 1 — Clone the Repository
```powershell
git clone https://github.com/memorandavid-dotcom/dss150p-lab01-starter-main_Memorando.git
cd dss150p-lab01-starter-main_Memorando/dss150p-lab01-starter-main
```

### Step 2 — Create and Activate a Python Virtual Environment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### Step 3 — Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4 — Start the PostgreSQL Database
```powershell
docker compose up -d
```
This launches a PostgreSQL 16 container (`dss150p-postgres`) on port **5432** using credentials `dss150p / dss150p_lab` and database `dss150p_lab`.

### Step 5 — Seed the PostgreSQL Database
Open a shell inside the running container and execute the seed script:
```powershell
docker exec -i dss150p-postgres psql -U dss150p -d dss150p_lab < seed_support_tickets.sql
```
This creates the `public.support_tickets` table and inserts 250 rows.

### Step 6 — Create the Customers Staging Table (Optional)
```powershell
docker exec -i dss150p-postgres psql -U dss150p -d dss150p_lab < sql/01_create_schema.sql
```

### Step 7 — Copy Source Files to the Data Directory
```powershell
mkdir -p data/raw
cp customers.csv data/raw/
cp orders.json   data/raw/
cp products.parquet data/raw/
```

### Step 8 — Run the Local API Server
In a **separate terminal** (keep it running):
```powershell
python local_api_server.py
```
The API is now reachable at `http://localhost:8000/api/orders`.

### Step 9 — Profile the File Sources
```powershell
python src/profile_sources.py
```
Outputs shape, dtypes, null counts, duplicate counts, and numeric summaries for `customers.csv`, `orders.json`, and `products.parquet`.

### Step 10 — Inspect the REST API
```powershell
python src/inspect_api.py
```
Fetches `http://localhost:8000/api/orders`, prints status, record count, sample keys, and UTC retrieval timestamp. Saves snapshot to `data/raw/api_snapshot.json`.

### Step 11 — Inspect the PostgreSQL Database
```powershell
python src/inspect_postgres.py
```
Connects to the Docker PostgreSQL instance via SQLAlchemy, prints column names, data types, nullability, total row count, and the first 5 rows of `support_tickets`.

---

## Data Sources

| # | Source | Format | File / Endpoint | Rows |
|---|---|---|---|---|
| 1 | Customers | CSV | `customers.csv` | 251 |
| 2 | Orders | JSON | `orders.json` | ~1 000 |
| 3 | Products | Parquet | `products.parquet` | varies |
| 4 | REST API | JSON | `http://localhost:8000/api/orders` | 100 (served) |
| 5 | PostgreSQL | Relational | `public.support_tickets` | 250 |

Detailed field lists, update patterns, and quality risks for each source are in [`docs/source_inventory.md`](docs/source_inventory.md).

---

## Key Scripts

| Script | Purpose |
|---|---|
| `src/profile_sources.py` | Pandas profiling of CSV / JSON / Parquet |
| `src/inspect_sources.py` | Low-level CSV and JSON field inspection |
| `src/inspect_api.py` | REST API fetch, snapshot, and timestamp |
| `src/inspect_postgres.py` | PostgreSQL column and row inspection via SQLAlchemy |
| `src/verify_environment.py` | Validates Python and package versions |
| `local_api_server.py` | Serves orders data on `localhost:8000` |

---

## Database Setup

The PostgreSQL database runs in Docker:
* **Image:** `postgres:16`
* **Container name:** `dss150p-postgres`
* **Host:** `localhost:5432`
* **Database:** `dss150p_lab`
* **User / Password:** `dss150p` / `dss150p_lab`
* **Volume:** `dss150p_pgdata` (persisted across restarts)
* **Main table:** `public.support_tickets` (seeded by `seed_support_tickets.sql`)
* **Staging table:** `lab.customers` (created by `sql/01_create_schema.sql`)

To stop and remove all containers and volumes:
```powershell
docker compose down -v
```

---

## Known Limitations

1. **Local API only** — `local_api_server.py` serves a static slice (100 records) of `orders.json`. It is not a production-grade API; it does not support filtering, pagination, or authentication.
2. **No foreign-key enforcement** — `support_tickets.customer_id` is not linked by a database foreign key to `customers.csv`. Referential integrity must be validated at the ETL layer.
3. **customer_id uniqueness** — The raw `customers.csv` does not enforce uniqueness on `customer_id`; soft-duplicate rows with the same email but different `city` / `customer_segment` values are present.
4. **Parquet engine dependency** — Reading `products.parquet` requires `pyarrow`. Ensure it is installed via `requirements.txt` before running `profile_sources.py`.
5. **Windows path separators** — Scripts use `pathlib.Path` for cross-platform compatibility, but some manual `cp` commands in this README use Unix-style separators; substitute `copy` or `robocopy` on Windows if needed.