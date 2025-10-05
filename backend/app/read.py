# backend/app/read_db.py
from sqlalchemy import inspect
from database import engine

# Create an inspector
inspector = inspect(engine)

# List all tables
tables = inspector.get_table_names()
print("Tables in database:", tables)

# Optional: show first 5 rows from each table
from sqlalchemy import Table, MetaData, select

metadata = MetaData()
metadata.reflect(bind=engine)

for table_name in tables:
    table = Table(table_name, metadata, autoload_with=engine)
    print(f"\nData from table: {table_name}")
    query = select(table).limit(5)
    with engine.connect() as conn:
        results = conn.execute(query).fetchall()
        for row in results:
            print(row)
