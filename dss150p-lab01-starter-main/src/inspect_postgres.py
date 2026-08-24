from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://dss150p:dss150p_lab@localhost:5432/dss150p_lab"
engine = create_engine(DATABASE_URL)

TABLE_NAME = "support_tickets"

with engine.connect() as conn:
    print(f"--- COLUMNS ({TABLE_NAME}) ---")
    columns = conn.execute(
        text(
            "SELECT column_name, data_type, is_nullable "
            "FROM information_schema.columns "
            f"WHERE table_name = '{TABLE_NAME}' "
            "ORDER BY ordinal_position;"
        )
    ).fetchall()

    for col in columns:
        print(f"Column: {col[0]:<15} Type: {col[1]:<15} Nullable: {col[2]}")

    print("\n--- ROW COUNT ---")
    count = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME};")).scalar()
    print(f"Total Rows: {count}")

    print("\n--- SAMPLE ROWS (FIRST 5) ---")
    rows = conn.execute(text(f"SELECT * FROM {TABLE_NAME} LIMIT 5;")).fetchall()
    for row in rows:
        print(row)