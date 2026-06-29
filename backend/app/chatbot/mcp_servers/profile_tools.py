from pathlib import Path
import sys
import json

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

from mcp.server.fastmcp import FastMCP
from sqlalchemy import text
from database.db import SessionLocal

mcp = FastMCP("profile")


# =====================================
# Get Profile
# =====================================

@mcp.tool()
def get_profile(user_id: int):

    db = SessionLocal()

    try:

        profile = db.execute(
            text("""
                SELECT
                    user_id,
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
            return json.dumps(
                {
                    "exists": False
                }
            )

        return json.dumps(
            {
                "exists": True,
                "user_id": profile.user_id,
                "customer_name": profile.customer_name,
                "mobile": profile.mobile,
                "address": profile.address,
                "payment_method": profile.payment_method
            },
            indent=4,
            default=str
        )

    finally:
        db.close()


# =====================================
# Create / Update Profile
# =====================================

@mcp.tool()
def update_profile(
    user_id: int,
    customer_name: str,
    mobile: str,
    address: str,
    payment_method: str
):

    db = SessionLocal()

    try:

        profile = db.execute(
            text("""
                SELECT user_id
                FROM user_profiles
                WHERE user_id=:user_id
            """),
            {
                "user_id": user_id
            }
        ).fetchone()

        if profile:

            db.execute(
                text("""
                    UPDATE user_profiles
                    SET
                        customer_name=:customer_name,
                        mobile=:mobile,
                        address=:address,
                        payment_method=:payment_method
                    WHERE user_id=:user_id
                """),
                {
                    "user_id": user_id,
                    "customer_name": customer_name,
                    "mobile": mobile,
                    "address": address,
                    "payment_method": payment_method
                }
            )

        else:

            db.execute(
                text("""
                    INSERT INTO user_profiles
                    (
                        user_id,
                        customer_name,
                        mobile,
                        address,
                        payment_method
                    )
                    VALUES
                    (
                        :user_id,
                        :customer_name,
                        :mobile,
                        :address,
                        :payment_method
                    )
                """),
                {
                    "user_id": user_id,
                    "customer_name": customer_name,
                    "mobile": mobile,
                    "address": address,
                    "payment_method": payment_method
                }
            )

        db.commit()

        return json.dumps(
            {
                "message": "Profile saved successfully.",
                "customer_name": customer_name,
                "mobile": mobile,
                "address": address,
                "payment_method": payment_method
            },
            indent=4
        )

    except Exception as e:

        db.rollback()
        return str(e)

    finally:
        db.close()


# =====================================
# Show Profile
# =====================================

@mcp.tool()
def show_profile(user_id: int):

    return get_profile(user_id)


# =====================================
# Health Check
# =====================================

@mcp.tool()
def ping():

    return "profile ok"


if __name__ == "__main__":
    mcp.run()