-- Create schema if it does not exist
CREATE SCHEMA IF NOT EXISTS lab;

-- Create staging table for customers sourced from customers.csv
-- Columns and types mirror the actual CSV source (7 columns):
--   customer_id, first_name, last_name, email, city, signup_date, customer_segment
-- NOTE: customer_id is used as the primary key for this staging table.
--       In the raw CSV the field is not guaranteed unique; uniqueness is enforced here on load.
--       There is no 'created_at' column in the source CSV.
CREATE TABLE IF NOT EXISTS lab.customers (
    customer_id     VARCHAR(10)  PRIMARY KEY,
    first_name      VARCHAR(100) NOT NULL,
    last_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(255) NOT NULL,
    city            VARCHAR(100) NOT NULL,
    signup_date     DATE         NOT NULL,
    customer_segment VARCHAR(50) NOT NULL,
    CONSTRAINT ck_email_format CHECK (email LIKE '%@%')
);