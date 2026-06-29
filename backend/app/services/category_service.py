from models.category import Category


def create_category(db, category_data):

    category = Category(
        category_name=category_data.category_name
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def get_all_categories(db):

    return db.query(Category).all()


def get_category_by_id(db, category_id):

    return db.query(Category).filter(
        Category.category_id == category_id
    ).first()


def update_category(db, category_id, category_data):

    category = db.query(Category).filter(
        Category.category_id == category_id
    ).first()

    if not category:
        return None

    category.category_name = category_data.category_name

    db.commit()
    db.refresh(category)

    return category


def delete_category(db, category_id):

    category = db.query(Category).filter(
        Category.category_id == category_id
    ).first()

    if not category:
        return False

    db.delete(category)
    db.commit()

    return True