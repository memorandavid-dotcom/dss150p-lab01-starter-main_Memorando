from sqlalchemy import create_engine, text

# Database connection URL: postgresql://USER:PASSWORD@HOST:PORT/DBNAME
DATABASE_URL = "postgresql://dss150p:dss150p_lab@localhost:5432/dss150p_lab"

def test_connection():
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            version = connection.execute(text("SELECT version();")).scalar()
            db_name = connection.execute(text("SELECT current_database();")).scalar()
            
            print("--- Connection Successful ---")
            print(f"PostgreSQL Version: {version}")
            print(f"Current Database:   {db_name}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()