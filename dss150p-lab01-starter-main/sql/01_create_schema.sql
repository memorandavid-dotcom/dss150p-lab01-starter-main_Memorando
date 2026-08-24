-- Create schema if it does not exist
CREATE SCHEMA IF NOT EXISTS lab;

-- Create table for customers
CREATE TABLE IF NOT EXISTS lab.customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_email_format CHECK (email LIKE '%@%')
);