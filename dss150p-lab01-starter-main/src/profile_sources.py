from pathlib import Path
import pandas as pd

RAW = Path("data/raw")  # Or Path("data") depending on where you moved the files

# Load datasets
customers = pd.read_csv(RAW / "customers.csv")
orders = pd.read_json(RAW / "orders.json")
products = pd.read_parquet(RAW / "products.parquet")

sources = {
    "customers.csv": customers,
    "orders.json": orders,
    "products.parquet": products,
}

for name, df in sources.items():
    print(f"\n================ {name} ================")
    print(f"Shape (Rows, Columns): {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nData Types:\n", df.dtypes)
    print("\nNull Values per Column:\n", df.isna().sum())

    # Convert dictionary/list columns to string representation for duplicate checking
    temp_df = df.astype(str)
    print("\nDuplicate Rows:", temp_df.duplicated().sum())

    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) > 0:
        print("\nNumeric Column Summaries (Min/Max):")
        for col in numeric_cols:
            print(f"  {col} -> Min: {df[col].min()}, Max: {df[col].max()}")

    print("\nFirst 5 Records:")
    print(df.head())