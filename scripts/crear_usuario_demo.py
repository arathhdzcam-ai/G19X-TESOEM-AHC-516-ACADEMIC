from app.auth.database import initialize_database, get_db_connection
from app.auth.security import hash_password

DEMO_EMAIL = "demo@supplychain.example.com"
DEMO_PASSWORD = "DemoSupplyChain2026"

def main():
    initialize_database()

    with get_db_connection() as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO users (email, password_hash)
            VALUES (?, ?)
            """,
            (DEMO_EMAIL, hash_password(DEMO_PASSWORD)),
        )

    print(f"Usuario de demostración listo: {DEMO_EMAIL}")

if __name__ == "__main__":
    main()

