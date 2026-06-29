from models.product import Product
from models.product import Product

def create_product(db, product_data):

    product = Product(
        product_name=product_data.product_name,
        brand=product_data.brand,
        description=product_data.description,
        price=product_data.price,
        stock=product_data.stock,
        image_url=product_data.image_url,
        category_id=product_data.category_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_all_products(db):

    return db.query(Product).all()


def get_product_by_id(db, product_id):

    return db.query(Product).filter(
        Product.product_id == product_id
    ).first()


def update_product(db, product_id, product_data):

    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not product:
        return None

    product.product_name = product_data.product_name
    product.brand = product_data.brand
    product.description = product_data.description
    product.price = product_data.price
    product.stock = product_data.stock
    product.image_url = product_data.image_url
    product.category_id = product_data.category_id

    db.commit()
    db.refresh(product)

    return product


def delete_product(db, product_id):

    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not product:
        return False

    db.delete(product)
    db.commit()

    return True

def delete_product(db, product_id):

    product = db.query(Product).filter(
        Product.product_id == product_id
    ).first()

    if not product:
        return False

    db.delete(product)
    db.commit()

    return True



def search_products(db, keyword):

    return db.query(Product).filter(
        Product.product_name.ilike(f"%{keyword}%")
    ).all()

def filter_products(
    db,
    min_price=None,
    max_price=None,
    brand=None
):

    query = db.query(Product)

    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    if brand:
        query = query.filter(
            Product.brand == brand
        )

    return query.all()

from sqlalchemy import or_

def search_products(db, keyword):

    return db.query(Product).filter(
        or_(
            Product.product_name.ilike(f"%{keyword}%"),
            Product.brand.ilike(f"%{keyword}%")
        )
    ).all()


def filter_products(
    db,
    brand=None,
    min_price=None,
    max_price=None
):

    query = db.query(Product)

    if brand:
        query = query.filter(
            Product.brand.ilike(f"%{brand}%")
        )

    if min_price:
        query = query.filter(
            Product.price >= min_price
        )

    if max_price:
        query = query.filter(
            Product.price <= max_price
        )

    return query.all()