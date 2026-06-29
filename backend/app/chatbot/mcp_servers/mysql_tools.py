from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from mcp.server.fastmcp import FastMCP
from sqlalchemy import text

from database.db import SessionLocal

mcp = FastMCP("mysql")


@mcp.tool()
def execute_query(query: str):

    db = SessionLocal()

    try:

        result = db.execute(text(query))

        if query.lower().strip().startswith("select"):

            return [
                dict(row._mapping)
                for row in result.fetchall()
            ]

        db.commit()

        return "Query Executed"

    except Exception as e:

        db.rollback()
        return str(e)

    finally:
        db.close()


@mcp.tool()
def ping():
    return "mysql ok"


if __name__ == "__main__":
    mcp.run()