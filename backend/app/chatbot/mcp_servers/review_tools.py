from pathlib import Path
import sys
import json

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from mcp.server.fastmcp import FastMCP
from sqlalchemy import text
from database.db import SessionLocal

mcp = FastMCP("review")


@mcp.tool()
def show_reviews(product_id: int):

    db = SessionLocal()

    try:

        rows = db.execute(
            text("""
                SELECT
                    r.review_id,
                    r.rating,
                    r.comment,
                    u.username
                FROM reviews r
                JOIN users u
                    ON u.user_id = r.user_id
                WHERE r.product_id=:product_id
                ORDER BY r.review_id DESC
            """),
            {
                "product_id": product_id
            }
        ).fetchall()

        return json.dumps(
            [dict(row._mapping) for row in rows],
            default=str
        )

    finally:
        db.close()


@mcp.tool()
def show_my_reviews(
    user_id: int,
    product_id: int
):

    db = SessionLocal()

    try:

        rows = db.execute(
            text("""
                SELECT
                    review_id,
                    rating,
                    comment
                FROM reviews
                WHERE
                    user_id=:user_id
                AND product_id=:product_id
            """),
            {
                "user_id": user_id,
                "product_id": product_id
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