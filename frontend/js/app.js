const App = (() => {
  const page = document.body.dataset.page;
  const protectedPages = ["cart", "wishlist", "orders", "profile"];

  function toast(message, type = "success") {
    let wrap = document.querySelector(".toast-wrap");
    if (!wrap) {
      wrap = document.createElement("div");
      wrap.className = "toast-wrap";
      document.body.appendChild(wrap);
    }
    const item = document.createElement("div");
    item.className = `toast ${type}`;
    item.textContent = message;
    wrap.appendChild(item);
    setTimeout(() => item.remove(), 3600);
  }

  function image(src) {
    if (!src) return "assets/fossil_grant.jpg";
    if (/^assets\//.test(src)) return src;
    if (/^https?:/.test(src)) return src;
    const clean = String(src).replaceAll("\\", "/");
    const fileName = clean.split("/").pop();
    return fileName ? `assets/${fileName}` : "assets/fossil_grant.jpg";
  }

  function productImageMarkup(src, alt) {
    return `<img src="${image(src)}" alt="${alt}" onerror="this.onerror=null;this.src='assets/fossil_grant.jpg';">`;
  }

  function productCard(product) {
    const p = API.normalizeProduct(product);
    return `
      <article class="product-card glass-card reveal">
        <a class="product-card__image" href="product-details.html?id=${p.product_id}">${productImageMarkup(p.image_url, p.product_name)}</a>
        <div class="product-card__body">
          <span class="meta">${p.brand || "Watch Store Only"}</span>
          <h3><a href="product-details.html?id=${p.product_id}">${p.product_name}</a></h3>
          <p class="meta">${(p.description || "").slice(0, 78)}${(p.description || "").length > 78 ? "..." : ""}</p>
          <strong class="price">${API.money(p.price)}</strong>
          <div class="card-actions">
            <button class="btn btn-dark" data-add-cart="${p.product_id}" type="button">Add to cart</button>
            <button class="btn btn-ghost" data-add-wishlist="${p.product_id}" type="button" title="Add to wishlist">Love</button>
          </div>
        </div>
      </article>`;
  }

  function categoryName(id) {
    return "Watch";
  }

  function header() {
    const target = document.getElementById("site-header");
    if (!target) return;
    const links = [
      ["index.html", "Home", "home"],
      ["products.html", "Products", "products"],
      ["wishlist.html", "Wishlist", "wishlist"],
      ["cart.html", "Cart", "cart"],
      ["orders.html", "Orders", "orders"],
      ["chatbot.html", "AI", "chatbot"]
    ];
    target.innerHTML = `
      <header class="site-header">
        <nav class="nav container">
          <a class="brand" href="index.html">Watch Store Only</a>
          <div id="navLinks" class="nav__links">
            ${links.map(([href, label, key]) => `<a class="${page === key ? "active" : ""}" href="${href}">${label}</a>`).join("")}
          </div>
          <form id="navSearch" class="nav-search">
            <input name="q" type="search" placeholder="Search watches">
            <button type="submit">Search</button>
          </form>
          <div class="nav__actions">
            <a class="btn btn-ghost desktop-only" href="${API.isAuthed() ? "profile.html" : "login.html"}">${API.isAuthed() ? "Profile" : "Login"}</a>
            ${API.isAuthed() ? `<button id="logoutBtn" class="btn btn-ghost desktop-only" type="button">Logout</button>` : ""}
          </div>
        </nav>
      </header>`;
    document.getElementById("navSearch")?.addEventListener("submit", event => {
      event.preventDefault();
      const query = String(new FormData(event.currentTarget).get("q") || "").trim();
      if (query) location.href = `products.html?search=${encodeURIComponent(query)}`;
    });
    document.getElementById("logoutBtn")?.addEventListener("click", () => {
      API.clearToken();
      toast("Logged out");
      setTimeout(() => location.href = "index.html", 500);
    });
  }

  function footer() {
    const target = document.getElementById("site-footer");
    if (!target) return;
    target.innerHTML = `<footer class="site-footer"><div class="container footer-grid"><div><a class="brand" href="index.html">Watch Store Only</a><p>Watch ecommerce frontend powered by FastAPI REST endpoints and vanilla JavaScript.</p></div><div><strong>Shop</strong><p><a href="products.html">Products</a></p><p><a href="wishlist.html">Wishlist</a></p></div><div><strong>Account</strong><p><a href="orders.html">Orders</a></p><p><a href="profile.html">Profile</a></p></div><div><strong>AI</strong><p><a href="chatbot.html">Assistant</a></p><p>Support: hello@watchstore.test</p></div></div></footer>`;
  }

  function protect() {
    if (protectedPages.includes(page) && !API.isAuthed()) {
      sessionStorage.setItem("watch_store_redirect", location.pathname.split("/").pop());
      location.href = "login.html";
    }
  }

  function bindGlobalActions() {
    document.addEventListener("click", async event => {
      const cartButton = event.target.closest("[data-add-cart]");
      const wishButton = event.target.closest("[data-add-wishlist]");
      if (cartButton) {
        cartButton.disabled = true;
        try {
          await API.addCart(cartButton.dataset.addCart, 1);
          toast("Added to cart");
        } catch (error) {
          toast(error.message, "error");
        } finally {
          cartButton.disabled = false;
        }
      }
      if (wishButton) {
        wishButton.disabled = true;
        try {
          await API.addWishlist(wishButton.dataset.addWishlist);
          toast("Saved to wishlist");
        } catch (error) {
          toast(error.message, "error");
        } finally {
          wishButton.disabled = false;
        }
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    protect();
    header();
    footer();
    bindGlobalActions();
  });

  return { page, toast, image, productImageMarkup, productCard, categoryName };
})();
