from models.review import Review


def add_review(
    db,
    user_id,
    product_id,
    rating,
    comment
):

    review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


def get_reviews(
    db,
    product_id
):

    return db.query(Review).filter(
        Review.product_id == product_id
    ).all()