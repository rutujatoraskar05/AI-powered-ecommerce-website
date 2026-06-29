from pathlib import Path
import sys
import json

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from mcp.server.fastmcp import FastMCP
from sqlalchemy import text
from database.db import SessionLocal

mcp = FastMCP("product")


@mcp.tool()
def search_products(
    keyword: str = "",
    brand: str = "",
    max_price: float = 999999
):

    db = SessionLocal()

    try:

        rows = db.execute(
            text("""
                SELECT *
                FROM products
                WHERE
                (
                    product_name LIKE :keyword
                    OR brand LIKE :keyword
                )
                AND brand LIKE :brand
                AND price<=:price
            """),
            {
                "keyword": f"%{keyword}%",
                "brand": f"%{brand}%",
                "price": max_price
            }
        ).fetchall()

        return json.dumps(
            [dict(row._mapping) for row in rows],
            default=str
        )

    finally:
        db.close()


if __name__ == "__main__":
    mcp.run()