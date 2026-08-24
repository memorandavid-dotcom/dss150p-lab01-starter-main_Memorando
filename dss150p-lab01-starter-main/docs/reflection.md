# Laboratory 01 Reflection

## 1. Easiest Source to Integrate
The Parquet data format (`products.parquet`) is the easiest to integrate into a future data pipeline. Because Parquet is a binary, columnar storage format with embedded schema metadata, data types and column structures are strictly preserved upon write. Unlike CSV files, which require type inferencing or explicit casting during ingestion, Parquet guarantees schema enforcement out of the box, drastically reducing runtime type-mismatch errors.

## 2. Source Presenting Highest Schema/Data-Quality Risk
The REST API payload presents the highest risk to pipeline stability. The profile evidence reveals that API responses return semi-structured JSON payloads with dynamic properties and optional fields. Because web services can alter their schema without prior notice (e.g., adding nested dictionaries or changing nullability rules), downstream ingestion pipelines risk breaking during automatic parsing if schema evolution policies are not strictly enforced.

## 3. Risks of Building Pipelines Without Prior Contracts
Building an ingestion pipeline without prior schema understanding leads to cascading failures across analytical workloads. Unchecked schema changes cause silent data corruption, broken downstream SQL joins, and incorrect aggregation results. Establishing explicit data contracts upfront guarantees that bad records are rejected or quarantined early, preventing unvalidated data from populating analytical models.

## 4. Value of Engineering Tools for Reproducibility
Git, Python virtual environments (`.venv`), Docker containers, and structured documentation form the foundation of modern data reliability. Docker isolates execution environments and database dependencies across platforms, `.venv` prevents local Python dependency drift, Git provides auditable version control, and clear markdown documentation enables team members to deploy, execute, and verify pipelines reliably across any infrastructure.