from sqlalchemy import create_engine, text


engine = create_engine("postgresql+psycopg2://postgres:@localhost:5432/postgres")

with engine.connect() as conn:
    conn.execute(text("COMMIT"))
    conn.execute(text("CREATE DATABASE task_service_test"))
    print("База task_service_test создана успешно!")