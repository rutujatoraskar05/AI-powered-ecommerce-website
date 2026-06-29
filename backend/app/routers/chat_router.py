from fastapi import APIRouter
from chatbot.graph import run_chat
from chatbot.session import checkout_sessions
from database.db import SessionLocal
from sqlalchemy import text
from services.order_service import place_order
router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"]
)

@router.get("/")
async def chat(message: str):

    user_id = 1
    msg = message.strip()

    db = SessionLocal()

    try:

        # -------------------------------------------------
        # Update customer name
        # -------------------------------------------------

        if msg.lower().startswith("update name"):

            value = msg.replace("update name", "", 1).strip()

            db.execute(
                text("""
                UPDATE user_profiles
                SET customer_name=:value
                WHERE user_id=:user_id
                """),
                {
                    "value": value,
                    "user_id": user_id
                }
            )

            db.commit()

            return {
                "response":
                f"✅ Name updated to **{value}**.\n\nType **place order**."
            }

        # -------------------------------------------------
        # Update mobile
        # -------------------------------------------------

        if msg.lower().startswith("update mobile"):

            value = msg.replace("update mobile", "", 1).strip()

            db.execute(
                text("""
                UPDATE user_profiles
                SET mobile=:value
                WHERE user_id=:user_id
                """),
                {
                    "value": value,
                    "user_id": user_id
                }
            )

            db.commit()

            return {
                "response":
                f"✅ Mobile updated.\n\nType **place order**."
            }

        # -------------------------------------------------
        # Update address
        # -------------------------------------------------

        if msg.lower().startswith("update address"):

            value = msg.replace("update address", "", 1).strip()

            db.execute(
                text("""
                UPDATE user_profiles
                SET address=:value
                WHERE user_id=:user_id
                """),
                {
                    "value": value,
                    "user_id": user_id
                }
            )

            db.commit()

            return {
                "response":
                "✅ Address updated.\n\nType **place order**."
            }

        # -------------------------------------------------
        # Update payment
        # -------------------------------------------------

        if msg.lower().startswith("update payment"):

            value = msg.replace("update payment", "", 1).strip()

            db.execute(
                text("""
                UPDATE user_profiles
                SET payment_method=:value
                WHERE user_id=:user_id
                """),
                {
                    "value": value,
                    "user_id": user_id
                }
            )

            db.commit()

            return {
                "response":
                f"✅ Payment method updated to **{value}**.\n\nType **place order**."
            }

        # -------------------------------------------------
        # Place Order
        # -------------------------------------------------

        if msg.lower() == "place order":

            profile = db.execute(
                text("""
                SELECT
                    customer_name,
                    mobile,
                    address,
                    payment_method
                FROM user_profiles
                WHERE user_id=:user_id
                """),
                {
                    "user_id": user_id
                }
            ).fetchone()

            if not profile:

                return {
                    "response":
                    "No profile found.\n\nPlease save your profile first."
                }

            checkout_sessions[user_id] = {
                "waiting_confirmation": True
            }

            return {
                "response":
f"""
Please confirm your order.

👤 Name : {profile.customer_name}

📱 Mobile : {profile.mobile}

🏠 Address : {profile.address}

💳 Payment : {profile.payment_method}

Reply:

YES → Place Order

NO → Cancel

You can also update anything:

update name Rutuja

update mobile 9876543210

update address Pune Maharashtra

update payment UPI
"""
            }

        # -------------------------------------------------
        # Confirmation
        # -------------------------------------------------

        if (
            user_id in checkout_sessions
            and checkout_sessions[user_id]["waiting_confirmation"]
        ):

            if msg.lower() == "yes":

                checkout_sessions.pop(user_id)

                order = place_order(db, user_id)

                if order is None:

                    return {
                        "response": "🛒 Your cart is empty."
                    }

                if isinstance(order, dict):

                    return {
                        "response": order["error"]
                    }

                return {
                    "response": f"""
✅ Order placed successfully!

🧾 Order ID : {order.order_id}

📦 Status : {order.status}

💰 Total Amount : ₹{order.total_amount}

Thank you for shopping with us ❤️
"""
                }

            elif msg.lower() == "no":

                checkout_sessions.pop(user_id)

                return {
                    "response": "❌ Order cancelled successfully."
                }

        # -------------------------------------------------
        # Default AI
        # -------------------------------------------------

        response = await run_chat(msg)

        return {
            "response": response
        }

    finally:

        db.close()