# supervisor.py

from state import EcommerceState

def supervisor_node(
    state: EcommerceState
):

    return {
        "next_agent": "ecommerce_agent"
    }