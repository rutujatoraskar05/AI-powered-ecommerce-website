from pathlib import Path
import sys
import json
import random
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from mcp.server.fastmcp import FastMCP
from sqlalchemy import text
from database.db import SessionLocal

mcp = FastMCP("orders")


@mcp.tool()
def place_order(
    user_id: int,
    customer_name: str = "Customer",
    address: str = "Not Provided",
    payment_method: str = "COD"
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

        if not cart:
            return "Cart is empty."

        cart_id = cart.cart_id

        items = db.execute(
            text("""
            SELECT
                ci.product_id,
                ci.quantity,
                p.price,
                p.stock
            FROM cart_items ci
            JOIN products p
                ON p.product_id=ci.product_id
            WHERE ci.cart_id=:cart_id
            """),
            {
                "cart_id": cart_id
            }
        ).fetchall()

        if len(items) == 0:
            return "Cart is empty."

        total = 0

        for item in items:

            if item.stock < item.quantity:

                return f"Insufficient stock for product {item.product_id}"

            total += item.price * item.quantity

        tracking_id = "TRK" + str(random.randint(100000,999999))

        db.execute(
            text("""
            INSERT INTO orders
            (
                user_id,
                total_amount,
                status,
                order_date,
                tracking_id,
                expected_delivery,
                payment_method,
                customer_name,
                address
            )
            VALUES
            (
                :user_id,
                :total,
                'Placed',
                NOW(),
                :tracking_id,
                '3-5 days',
                :payment_method,
                :customer_name,
                :address
            )
            """),
            {
                "user_id": user_id,
                "total": total,
                "tracking_id": tracking_id,
                "payment_method": payment_method,
                "customer_name": customer_name,
                "address": address
            }
        )

        db.commit()

        order = db.execute(
            text("""
            SELECT MAX(order_id) AS order_id
            FROM orders
            WHERE user_id=:user_id
            """),
            {
                "user_id": user_id
            }
        ).fetchone()

        order_id = order.order_id

        for item in items:

            db.execute(
                text("""
                INSERT INTO order_items
                (
                    order_id,
                    product_id,
                    quantity,
                    price
                )
                VALUES
                (
                    :order_id,
                    :product_id,
                    :quantity,
                    :price
                )
                """),
                {
                    "order_id": order_id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price
                }
            )

            db.execute(
                text("""
                UPDATE products
                SET stock = stock - :qty
                WHERE product_id = :product_id
                """),
                {
                    "qty": item.quantity,
                    "product_id": item.product_id
                }
            )

        db.execute(
            text("""
            DELETE
            FROM cart_items
            WHERE cart_id=:cart_id
            """),
            {
                "cart_id": cart_id
            }
        )

        db.commit()

        return json.dumps(
            {
                "message": "Order placed successfully.",
                "order_id": order_id,
                "tracking_id": tracking_id,
                "status": "Placed"
            },
            indent=2
        )

    except Exception as e:

        db.rollback()
        return str(e)

    finally:
        db.close()
@mcp.tool()
def track_order(order_id: int | str):

    from datetime import datetime, timedelta

    db = SessionLocal()

    try:

        order = db.execute(
            text("""
            SELECT
                order_id,
                user_id,
                total_amount,
                status,
                order_date,
                tracking_id,
                customer_name,
                payment_method,
                address
            FROM orders
            WHERE order_id=:order_id
            """),
            {
                "order_id": order_id
            }
        ).fetchone()

        if not order:
            return "Order not found."

        # -------------------------------------
        # Calculate order progress
        # -------------------------------------

        hours = (
            datetime.now() - order.order_date
        ).total_seconds() / 3600

        if order.status == "Cancelled":

            status = "Cancelled"
            location = "Order Cancelled"
            expected = "Cancelled"

        else:

            if hours >= 72:

                status = "Delivered"
                location = order.address
                expected = "Delivered"

            elif hours >= 48:

                status = "Out for Delivery"
                location = "Nearest Delivery Hub"
                expected = "Expected Today"

            elif hours >= 24:

                status = "Shipped"
                location = "In Transit"
                expected = "Expected Tomorrow"

            else:

                status = "Placed"
                location = "Seller Warehouse"

                remaining = max(
                    0,
                    72 - int(hours)
                )

                expected = f"Expected in {remaining} hours"

            # Update status in DB
            db.execute(
                text("""
                UPDATE orders
                SET status=:status
                WHERE order_id=:order_id
                """),
                {
                    "status": status,
                    "order_id": order_id
                }
            )

            db.commit()

        expected_date = (
            order.order_date + timedelta(days=3)
        ).strftime("%d %b %Y")

        result = {

            "order_id": order.order_id,

            "tracking_id": order.tracking_id,

            "customer_name": order.customer_name,

            "payment_method": order.payment_method,

            "total_amount": float(order.total_amount),

            "status": status,

            "current_location": location,

            "delivery_address": order.address,

            "ordered_on": order.order_date.strftime("%d %b %Y %I:%M %p"),

            "expected_delivery_date": expected_date,

            "delivery_message": expected

        }

        return json.dumps(
            result,
            indent=4,
            default=str
        )

    except Exception as e:

        return str(e)

    finally:

        db.close()

@mcp.tool()
def view_orders(user_id: int | str):

    db = SessionLocal()

    try:

        rows = db.execute(
            text("""
            SELECT
                order_id,
                tracking_id,
                total_amount,
                status,
                order_date,
                expected_delivery,
                payment_method,
                customer_name,
                address
            FROM orders
            WHERE user_id=:user_id
            ORDER BY order_date DESC
            """),
            {
                "user_id": user_id
            }
        ).fetchall()

        orders = []

        for row in rows:

            order = dict(row._mapping)

            if (
                order["status"] != "Cancelled"
                and order["order_date"] is not None
            ):

                hours = (
                    datetime.now() - order["order_date"]
                ).total_seconds() / 3600

                if hours >= 72:
                    order["status"] = "Delivered"

                elif hours >= 48:
                    order["status"] = "Out for Delivery"

                elif hours >= 24:
                    order["status"] = "Shipped"

                else:
                    order["status"] = "Placed"

            orders.append(order)

        return json.dumps(
            orders,
            indent=4,
            default=str
        )

    except Exception as e:

        return str(e)

    finally:

        db.close()


@mcp.tool()
def cancel_order(order_id: int | str):

    db = SessionLocal()

    try:

        order = db.execute(
            text("""
            SELECT
                status
            FROM orders
            WHERE order_id=:order_id
            """),
            {
                "order_id": order_id
            }
        ).fetchone()

        if not order:

            return "Order not found."

        if order.status == "Cancelled":

            return "Order is already cancelled."

        if order.status == "Delivered":

            return "Delivered orders cannot be cancelled."

        db.execute(
            text("""
            UPDATE orders
            SET status='Cancelled'
            WHERE order_id=:order_id
            """),
            {
                "order_id": order_id
            }
        )

        db.commit()

        return json.dumps(
            {
                "message": "Order cancelled successfully.",
                "order_id": order_id,
                "status": "Cancelled"
            },
            indent=4
        )

    except Exception as e:

        db.rollback()
        return str(e)

    finally:

        db.close()


@mcp.tool()
def ping():
    return "orders ok"


if __name__ == "__main__":
    mcp.run()