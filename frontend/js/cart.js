document.addEventListener("DOMContentLoaded", () => {
  if (App.page === "cart") renderCart();
});

async function renderCart() {
  const items = await API.cart();
  const normalized = items.map(item => ({ ...item, product: API.normalizeProduct(item.product || item) }));
  const target = document.getElementById("cartItems");
  const summary = document.getElementById("cartSummary");
  if (!normalized.length) {
    target.innerHTML = `<div class="glass-card empty"><h2>Your cart is empty</h2><p>Add a watch from the collection to begin checkout.</p><a class="btn btn-primary" href="products.html">Shop watches</a></div>`;
    summary.innerHTML = `<h2>Total</h2><div class="summary-row"><span>Subtotal</span><strong>Rs 0</strong></div>`;
    return;
  }
  target.innerHTML = normalized.map(item => {
    const p = item.product;
    return `<article class="line-item glass-card">${App.productImageMarkup(p.image_url, p.product_name)}<div><h3>${p.product_name}</h3><p class="meta">${p.brand} - ${API.money(p.price)}</p><div class="qty"><button data-local-qty="${item.cart_item_id ?? item.product_id}" data-product-id="${p.product_id}" data-current="${item.quantity || 1}" data-delta="-1">-</button><strong>${item.quantity || 1}</strong><button data-local-qty="${item.cart_item_id ?? item.product_id}" data-product-id="${p.product_id}" data-current="${item.quantity || 1}" data-delta="1">+</button></div></div><div class="line-actions"><strong>${API.money(p.price * (item.quantity || 1))}</strong><button class="btn btn-danger" data-remove-cart="${item.cart_item_id ?? item.product_id}">Remove</button></div></article>`;
  }).join("");
  const subtotal = normalized.reduce((sum, item) => sum + item.product.price * (item.quantity || 1), 0);
  summary.innerHTML = `<h2>Cart total</h2><div class="summary-row"><span>Subtotal</span><strong>${API.money(subtotal)}</strong></div><div class="summary-row"><span>Delivery</span><strong>Free</strong></div><div class="summary-row"><span>Total</span><strong>${API.money(subtotal)}</strong></div><button id="checkoutBtn" class="btn btn-primary" type="button">Checkout</button>`;
  document.querySelectorAll("[data-remove-cart]").forEach(btn => btn.addEventListener("click", async () => { await API.removeCart(btn.dataset.removeCart); App.toast("Item removed"); renderCart(); }));
  document.querySelectorAll("[data-local-qty]").forEach(btn => btn.addEventListener("click", async () => {
    const next = Math.max(1, Number(btn.dataset.current) + Number(btn.dataset.delta));
    await API.updateCartQuantity(btn.dataset.localQty, btn.dataset.productId, next);
    App.toast("Quantity updated");
    renderCart();
  }));
  document.getElementById("checkoutBtn").addEventListener("click", async () => {
    try { await API.createPaymentOrder(subtotal).catch(() => null); await API.placeOrder(); App.toast("Order placed successfully"); location.href = "orders.html"; }
    catch (error) { App.toast(error.message, "error"); }
  });
}
