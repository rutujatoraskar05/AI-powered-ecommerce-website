def route_intent(intent: str):
    return {
        "SHOW_PROFILE": "profile_tool",
        "SHOW_CART": "cart_tool",
        "SHOW_ORDERS": "order_tool",
        "ADD_TO_CART": "cart_tool",
        "SEARCH_PRODUCTS": "product_tool",
        "START_CHECKOUT": "checkout_tool",
        "SMALLTALK": "chat_tool"
    }.get(intent, "chat_tool")