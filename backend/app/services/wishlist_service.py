from models.wishlist import Wishlist
from models.product import Product

def add_to_wishlist(
    db,
    user_id,
    product_id
):

    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not product:
        return None

    item = Wishlist(
        user_id=user_id,
        product_id=product_id
    )

    db.add(item)
    db.commit()

    return item


def get_wishlist(
    db,
    user_id
):

    return db.query(Wishlist).filter(
        Wishlist.user_id == user_id
    ).all()


def remove_wishlist_item(
    db,
    wishlist_id
):

    item = db.query(Wishlist).filter(
        Wishlist.wishlist_id == wishlist_id
    ).first()

    if not item:
        return False

    db.delete(item)
    db.commit()

    return True