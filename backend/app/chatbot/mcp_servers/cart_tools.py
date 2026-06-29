from pathlib import Path
import sys
import json

# ==========================
# Project Root
# ==========================
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

# ==========================
# Imports
# ==========================
from mcp.server.fastmcp import FastMCP
from sqlalchemy import text
from database.db import SessionLocal

mcp = FastMCP("cart")


# =====================================================
# Add To Cart
# =====================================================
@mcp.tool()
def add_to_cart(
    user_id: int,
    product_id: int,
    quantity: int = 1
):

    db = SessionLocal()

    try:

        cart = db.execute(
            text("""
                SELECT cart_id
                FROM carts
                WHERE user_id=:user_id
            """),
            {"user_id": user_id}
        ).fetchone()

        if cart is None:

            db.execute(
                text("""
                    INSERT INTO carts(user_id)
                    VALUES(:user_id)
                """),
                {"user_id": user_id}
            )

            db.commit()

            cart = db.execute(
                text("""
                    SELECT cart_id
                    FROM carts
                    WHERE user_id=:user_id
                """),
                {"user_id": user_id}
            ).fetchone()

        cart_id = cart.cart_id

        existing = db.execute(
            text("""
                SELECT quantity
                FROM cart_items
                WHERE cart_id=:cart_id
                AND product_id=:product_id
            """),
            {
                "cart_id": cart_id,
                "product_id": product_id
            }
        ).fetchone()

        if existing:

            db.execute(
                text("""
                    UPDATE cart_items
                    SET quantity=quantity+:quantity
                    WHERE cart_id=:cart_id
                    AND product_id=:product_id
                """),
                {
                    "quantity": quantity,
                    "cart_id": cart_id,
                    "product_id": product_id
                }
            )

        else:

            db.execute(
                text("""
                    INSERT INTO cart_items
                    (
                        cart_id,
                        product_id,
                        quantity
                    )
                    VALUES
                    (
                        :cart_id,
                        :product_id,
                        :quantity
                    )
                """),
                {
                    "cart_id": cart_id,
                    "product_id": product_id,
                    "quantity": quantity
                }
            )

        db.commit()

        return "Product added to cart."

    except Exception as e:

        db.rollback()
        return str(e)

    finally:
        db.close()


# =====================================================
# Show Cart
# =====================================================
@mcp.tool()
def show_cart(user_id: int | str):

    db = SessionLocal()

    try:

        rows = db.execute(
            text("""
                SELECT
                    p.product_id,
                    p.product_name,
                    p.brand,
                    p.price,
                    ci.quantity
                FROM carts c
                JOIN cart_items ci
                    ON c.cart_id=ci.cart_id
                JOIN products p
                    ON p.product_id=ci.product_id
                WHERE c.user_id=:user_id
            """),
            {"user_id": user_id}
        ).fetchall()

        cart = [
            dict(row._mapping)
            for row in rows
        ]

        # IMPORTANT: return string
        return json.dumps(cart, default=str)

    except Exception as e:

        return str(e)

    finally:
        db.close()


# =====================================================
# Remove From Cart
# =====================================================
@mcp.tool()
def remove_from_cart(
    user_id: int,
    product_id: int
):

    db = SessionLocal()

    try:

        cart = db.execute(
            text("""
                SELECT cart_id
                FROM carts
                WHERE user_id=:user_id
            """),
            {"user_id": user_id}
        ).fetchone()

        if cart is None:
            return "Cart not found."

        db.execute(
            text("""
                DELETE
                FROM cart_items
                WHERE cart_id=:cart_id
                AND product_id=:product_id
            """),
            {
                "cart_id": cart.cart_id,
                "product_id": product_id
            }
        )

        db.commit()

        return "Product removed from cart."

    except Exception as e:

        db.rollback()
        return str(e)

    finally:
        db.close()


# =====================================================
# Clear Cart
# =====================================================
@mcp.tool()
def clear_cart(user_id: int):

    db = SessionLocal()

    try:

        cart = db.execute(
            text("""
                SELECT cart_id
                FROM carts
                WHERE user_id=:user_id
            """),
            {"user_id": user_id}
        ).fetchone()

        if cart is None:
            return "Cart not found."

        db.execute(
            text("""
                DELETE
                FROM cart_items
                WHERE cart_id=:cart_id
            """),
            {
                "cart_id": cart.cart_id
            }
        )

        db.commit()

        return "Cart cleared."

    except Exception as e:

        db.rollback()
        return str(e)

    finally:
        db.close()


# =====================================================
# Health Check
# =====================================================
@mcp.tool()
def ping():
    return "cart ok"


if __name__ == "__main__":
    print("Starting Cart MCP Server...")
    mcp.run()