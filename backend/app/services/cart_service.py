from models.cart import Cart
from models.cart_item import CartItem
from models.product import Product


def get_or_create_cart(db, user_id):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    return cart


def add_to_cart(db, user_id, product_id, quantity):

    cart = get_or_create_cart(db, user_id)

    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id,
        CartItem.product_id == product_id
    ).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItem(
            cart_id=cart.cart_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(item)

    db.commit()


def get_cart(db, user_id):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        return []

    items = db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).all()

    result = []

    for item in items:

        product = db.query(Product).filter(
            Product.product_id == item.product_id
        ).first()

        if not product:
            continue

        result.append({
            "cart_item_id": item.cart_item_id,
            "product_id": product.product_id,
            "product_name": product.product_name,
            "price": float(product.price),
            "quantity": item.quantity,
            "subtotal": float(product.price) * item.quantity
        })

    return result


def clear_cart(db, user_id):

    cart = db.query(Cart).filter(Cart.user_id == user_id).first()

    if not cart:
        return

    db.query(CartItem).filter(
        CartItem.cart_id == cart.cart_id
    ).delete()

    db.commit()

def remove_cart_item(db, cart_item_id):

    item = db.query(CartItem).filter(
        CartItem.cart_item_id == cart_item_id
    ).first()

    if not item:
        return False

    db.delete(item)
    db.commit()

    return True