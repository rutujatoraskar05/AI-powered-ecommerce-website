let allProducts = [];
let currentPage = 1;
const pageSize = 8;

document.addEventListener("DOMContentLoaded", async () => {
  if (["home", "products", "product-details", "reviews"].includes(App.page)) {
    try { allProducts = await API.products(); } catch { allProducts = []; }
  }
  if (App.page === "home") renderHome();
  if (App.page === "products") initProducts();
  if (App.page === "product-details") renderDetails();
  if (App.page === "reviews") initReviews();
});

function renderHome() {
  document.getElementById("featured-products").innerHTML = allProducts.slice(0, 4).map(App.productCard).join("");
  document.getElementById("trending-products").innerHTML = allProducts.slice(2, 5).map(App.productCard).join("");
}

function initProducts() {
  const brandFilter = document.getElementById("brandFilter");
  const brands = [...new Set(allProducts.map(p => p.brand).filter(Boolean))].sort();
  brandFilter.innerHTML += brands.map(brand => `<option>${brand}</option>`).join("");
  const params = new URLSearchParams(location.search);
  if (params.get("search")) document.getElementById("searchInput").value = params.get("search");
  ["searchInput", "brandFilter", "priceFilter", "sortSelect"].forEach(id => document.getElementById(id).addEventListener("input", () => { currentPage = 1; renderProducts(); }));
  document.getElementById("clearFilters").addEventListener("click", () => {
    document.getElementById("searchInput").value = "";
    document.getElementById("brandFilter").value = "";
    document.getElementById("priceFilter").value = 50000;
    document.getElementById("sortSelect").value = "featured";
    renderProducts();
  });
  renderProducts();
}

function filteredProducts() {
  const q = document.getElementById("searchInput").value.toLowerCase();
  const brand = document.getElementById("brandFilter").value;
  const max = Number(document.getElementById("priceFilter").value);
  const sort = document.getElementById("sortSelect").value;
  document.getElementById("priceValue").textContent = API.money(max);
  let products = allProducts.filter(p =>
    (!q || `${p.product_name} ${p.brand} ${p.description}`.toLowerCase().includes(q)) &&
    (!brand || p.brand === brand) &&
    Number(p.price) <= max
  );
  if (sort === "price-asc") products.sort((a, b) => a.price - b.price);
  if (sort === "price-desc") products.sort((a, b) => b.price - a.price);
  if (sort === "name") products.sort((a, b) => a.product_name.localeCompare(b.product_name));
  return products;
}

function renderProducts() {
  const products = filteredProducts();
  const totalPages = Math.max(1, Math.ceil(products.length / pageSize));
  currentPage = Math.min(currentPage, totalPages);
  const pageItems = products.slice((currentPage - 1) * pageSize, currentPage * pageSize);
  document.getElementById("resultCount").textContent = `${products.length} products found`;
  document.getElementById("productsGrid").innerHTML = pageItems.length ? pageItems.map(App.productCard).join("") : `<div class="glass-card empty">No watches match the selected filters.</div>`;
  document.getElementById("pagination").innerHTML = Array.from({ length: totalPages }, (_, i) => `<button class="${currentPage === i + 1 ? "active" : ""}" data-page-num="${i + 1}">${i + 1}</button>`).join("");
  document.querySelectorAll("[data-page-num]").forEach(btn => btn.addEventListener("click", () => { currentPage = Number(btn.dataset.pageNum); renderProducts(); }));
}

async function renderDetails() {
  const id = new URLSearchParams(location.search).get("id") || 1;
  const product = await API.product(id);
  const reviews = await API.reviews(id).catch(() => []);
  const imgs = [product.image_url, product.image_url, product.image_url, product.image_url].map(App.image);
  document.getElementById("productDetails").innerHTML = `
    <section class="details-grid">
      <div class="gallery glass-card">
        <div class="gallery-main"><img id="mainProductImage" src="${imgs[0]}" alt="${product.product_name}" onerror="this.onerror=null;this.src='assets/fossil_grant.jpg';"></div>
        <div class="thumbs">${imgs.map(src => `<button type="button" data-thumb="${src}"><img src="${src}" alt="" onerror="this.onerror=null;this.src='assets/fossil_grant.jpg';"></button>`).join("")}</div>
      </div>
      <article class="product-info glass-card">
        <p class="eyebrow">${product.brand || "Watch Store Only"}</p>
        <h1>${product.product_name}</h1>
        <p>${product.description || "Watch crafted for daily elegance."}</p>
        <strong class="price">${API.money(product.price)}</strong>
        <p><span class="stock ${product.stock > 0 ? "" : "out"}">${product.stock > 0 ? `${product.stock} in stock` : "Out of stock"}</span></p>
        <div class="detail-actions">
          <button class="btn btn-primary" data-add-cart="${product.product_id}">Add to Cart</button>
          <button class="btn btn-ghost" data-add-wishlist="${product.product_id}">Add to Wishlist</button>
          <button id="buyNow" class="btn btn-dark">Buy Now</button>
        </div>
      </article>
    </section>
    <section class="section"><div class="section-head"><p class="eyebrow">Reviews</p><h2>Customer ratings</h2></div><div class="stack">${reviews.length ? reviews.map(reviewCard).join("") : `<div class="glass-card empty">No reviews yet. Be the first to review this watch.</div>`}</div></section>`;
  document.querySelectorAll("[data-thumb]").forEach(btn => btn.addEventListener("click", () => document.getElementById("mainProductImage").src = btn.dataset.thumb));
  document.getElementById("buyNow").addEventListener("click", async () => { await API.addCart(product.product_id, 1); location.href = "cart.html"; });
}

function reviewCard(r) {
  return `<article class="glass-card summary"><strong>${"★".repeat(Number(r.rating || 5))}</strong><p>${r.comment || "Excellent watch."}</p><span class="meta">User ${r.user_id || ""}</span></article>`;
}

function initReviews() {
  const load = async () => {
    const id = document.getElementById("reviewProductId").value || 1;
    const list = await API.reviews(id).catch(() => []);
    document.getElementById("reviewsList").innerHTML = list.length ? list.map(reviewCard).join("") : `<div class="glass-card empty">No reviews found.</div>`;
  };
  document.getElementById("loadReviews").addEventListener("click", load);
  document.getElementById("reviewForm").addEventListener("submit", async event => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.target));
    data.product_id = Number(data.product_id);
    data.rating = Number(data.rating);
    try { await API.addReview(data); App.toast("Review added"); event.target.reset(); }
    catch (error) { App.toast(error.message, "error"); }
  });
  load();
}
