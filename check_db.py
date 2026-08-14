from database_config import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("""
            SELECT
                current_database(),
                current_user,
                inet_server_addr(),
                inet_server_port(),
                version(),
                pg_postmaster_start_time()
        """)
    )

    row = result.fetchone()

    print("DATABASE:", row[0])
    print("USER:", row[1])
    print("SERVER:", row[2])
    print("PORT:", row[3])
    print("VERSION:", row[4])
    print("STARTED:", row[5])

    result = conn.execute(
        text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'users'
            ORDER BY ordinal_position
        """)
    )

    print("COLUMNS:", result.fetchall())