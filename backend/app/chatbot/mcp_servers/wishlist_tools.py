import os
import sys
import json

ROOT_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.insert(0, ROOT_DIR)

from mcp.server.fastmcp import FastMCP
from sqlalchemy import text
from database.db import SessionLocal

mcp = FastMCP("wishlist")


@mcp.tool()
def view_wishlist(user_id: int | str):

    db = SessionLocal()

    try:

        rows = db.execute(
            text("""
                SELECT
                    p.product_name,
                    p.price
                FROM wishlist w
                JOIN products p
                    ON w.product_id = p.product_id
                WHERE w.user_id = :user_id
            """),
            {
                "user_id": user_id
            }
        ).fetchall()

        result = [
            dict(row._mapping)
            for row in rows
        ]

        return json.dumps(
            result,
            indent=2
        )

    except Exception as e:

        return str(e)

    finally:

        db.close()

@mcp.tool()
def add_to_wishlist(
    user_id: int | str,
    product_id: int
):

    db = SessionLocal()

    try:

        db.execute(
            text("""
                INSERT INTO wishlist
                (
                    user_id,
                    product_id
                )
                VALUES
                (
                    :user_id,
                    :product_id
                )
            """),
            {
                "user_id": user_id,
                "product_id": product_id
            }
        )

        db.commit()

        return "Product added to wishlist"

    except Exception as e:

        db.rollback()

        return str(e)

    finally:
        db.close()

@mcp.tool()
def remove_from_wishlist(
    user_id: int | str,
    product_id: int
):

    db = SessionLocal()

    try:

        db.execute(
            text("""
                DELETE FROM wishlist
                WHERE user_id=:user_id
                AND product_id=:product_id
            """),
            {
                "user_id": user_id,
                "product_id": product_id
            }
        )

        db.commit()

        return "Product removed from wishlist"

    except Exception as e:

        db.rollback()

        return str(e)

    finally:
        db.close()

if __name__ == "__main__":
    print("Starting Wishlist MCP Server...")
    mcp.run()