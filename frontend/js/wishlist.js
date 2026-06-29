document.addEventListener("DOMContentLoaded", () => {
  if (App.page === "wishlist") renderWishlist();
});

async function renderWishlist() {
  const list = await API.wishlist();
  const grid = document.getElementById("wishlistGrid");
  if (!list.length) {
    grid.innerHTML = `<div class="glass-card empty"><h2>No saved watches yet</h2><p>Save watches you love and move them to cart when ready.</p><a class="btn btn-primary" href="products.html">Explore collection</a></div>`;
    return;
  }
  grid.innerHTML = list.map(item => {
    const p = API.normalizeProduct(item.product || item);
    return `<article class="product-card glass-card"><a class="product-card__image" href="product-details.html?id=${p.product_id}">${App.productImageMarkup(p.image_url, p.product_name)}</a><div class="product-card__body"><span class="meta">${p.brand}</span><h3>${p.product_name}</h3><strong class="price">${API.money(p.price)}</strong><div class="card-actions"><button class="btn btn-dark" data-move-cart="${p.product_id}" data-wishlist-id="${item.wishlist_id ?? p.product_id}">Move to cart</button><button class="btn btn-danger" data-remove-wish="${item.wishlist_id ?? p.product_id}">Remove</button></div></div></article>`;
  }).join("");
  document.querySelectorAll("[data-remove-wish]").forEach(btn => btn.addEventListener("click", async () => { await API.removeWishlist(btn.dataset.removeWish); App.toast("Removed from wishlist"); renderWishlist(); }));
  document.querySelectorAll("[data-move-cart]").forEach(btn => btn.addEventListener("click", async () => { await API.addCart(btn.dataset.moveCart, 1); await API.removeWishlist(btn.dataset.wishlistId); App.toast("Moved to cart"); renderWishlist(); }));
}
