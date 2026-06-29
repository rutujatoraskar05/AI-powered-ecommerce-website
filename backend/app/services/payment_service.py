import razorpay

client = razorpay.Client(
    auth=(
        "YOUR_KEY_ID",
        "YOUR_KEY_SECRET"
    )
)

def create_payment(amount):

    order = client.order.create({
        "amount": amount * 100,
        "currency": "INR",
        "payment_capture": 1
    })

    return order