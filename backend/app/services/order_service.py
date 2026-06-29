from models.order import Order
from models.order_item import OrderItem
from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product
from models.order import Order
from models.order_item import OrderItem
from models.product import Product
from datetime import datetime
from datetime import timedelta


def place_order(db, user_id):

    cart = db.query(Cart).filter(
        Cart.user_id == user_id
    ).first()

    if not cart:
        return None

    cart_items = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).all()

    if len(cart_items) == 0:
        return None

    total_amount = 0

    for item in cart_items:

        product = db.query(Product).filter(
            Product.product_id == item.product_id
        ).first()

        if product.stock < item.quantity:

            return {
                "error":
                f"{product.product_name} Out Of Stock"
            }

        total_amount += (
            float(product.price)
            * item.quantity
        )

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        status="Placed"
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:

        product = db.query(Product).filter(
            Product.product_id == item.product_id
        ).first()

        order_item = OrderItem(
            order_id=order.order_id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=product.price
        )

        db.add(order_item)

        product.stock -= item.quantity

    db.commit()

    db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).delete()

    db.commit()

    return order



def get_user_orders(db, user_id):

    orders = db.query(Order).filter(
        Order.user_id == user_id
    ).order_by(Order.order_id.desc()).all()

    advance_order_statuses(db, orders)

    return orders

def get_order_by_id(
    db,
    order_id,
    user_id
):

    order = db.query(Order).filter(
        Order.order_id == order_id,
        Order.user_id == user_id
    ).first()

    if order:
        advance_order_statuses(db, [order])

    return order


def cancel_order(
    db,
    order_id,
    user_id
):

    order = db.query(Order).filter(
        Order.order_id == order_id,
        Order.user_id == user_id
    ).first()

    if not order:
        return None

    if order.status == "Cancelled":
        return False

    items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id
    ).all()

    for item in items:

        product = db.query(Product).filter(
            Product.product_id == item.product_id
        ).first()

        product.stock += item.quantity

    order.status = "Cancelled"

    db.commit()

    return order

from models.product import Product


def search_products(db, question):

    question = question.lower()

    products = db.query(Product).all()

    result = []

    for product in products:

        if product.brand.lower() in question:
            result.append({
                "product_name": product.product_name,
                "brand": product.brand,
                "price": float(product.price)
            })

    return result

def update_order_status(
    db,
    order_id,
    status
):

    order = db.query(Order).filter(
        Order.order_id == order_id
    ).first()

    if not order:
        return None

    order.status = status

    db.commit()
    db.refresh(order)

    return order


def advance_order_statuses(db, orders):

    changed = False

    for order in orders:

        tracking = status_for_order_age(order)

        if order.status != tracking["status"]:

            order.status = tracking["status"]
            changed = True

    if changed:
        db.commit()


from datetime import datetime, timedelta


from datetime import datetime, timedelta


def status_for_order_age(order):

    if not order.order_date:
        return {
            "status": order.status,
            "location": "",
            "expected_delivery": "",
            "delivery_date": None
        }

    if order.status == "Cancelled":
        return {
            "status": "Cancelled",
            "location": "Order Cancelled",
            "expected_delivery": "Cancelled",
            "delivery_date": None
        }

    now = (
        datetime.now(order.order_date.tzinfo)
        if order.order_date.tzinfo
        else datetime.now()
    )

    age = now - order.order_date

    delivery_date = order.order_date + timedelta(days=3)

    if age >= timedelta(days=3):

        return {
            "status": "Delivered",
            "location": "Delivered to Customer",
            "expected_delivery": "Delivered",
            "delivery_date": delivery_date
        }

    elif age >= timedelta(days=2):

        return {
            "status": "Out for Delivery",
            "location": "Nearest Delivery Hub",
            "expected_delivery": "Expected Today",
            "delivery_date": delivery_date
        }

    elif age >= timedelta(days=1):

        return {
            "status": "Shipped",
            "location": "In Transit",
            "expected_delivery": "Expected Tomorrow",
            "delivery_date": delivery_date
        }

    else:

        remaining = max(
            0,
            72 - int(age.total_seconds() / 3600)
        )

        return {
            "status": "Placed",
            "location": "Seller Warehouse",
            "expected_delivery": f"Expected in {remaining} hours",
            "delivery_date": delivery_date
        }