import asyncio

from app.modules.shared.database_conn.database_client import create_tables

if __name__ == "__main__":
    asyncio.run(create_tables())
