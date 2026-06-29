const API = (() => {
  const BASE_URL = localStorage.getItem("watch_store_api_url") || "http://127.0.0.1:8000";
  const TOKEN_KEY = "watch_store_token";
  const CART_KEY = "watch_store_local_cart";
  const WISH_KEY = "watch_store_local_wishlist";
  const IMAGE_BY_BRAND = {
    armani: "assets/armani_chrono.jpg",
    boat: "assets/boat_wave.jpg",
    casio: "assets/casio_edifice.jpg",
    fastrack: "assets/fastrack_black.jpg",
    fire: "assets/fireboltt_ninja.jpg",
    fossil: "assets/fossil_grant.jpg",
    kors: "assets/mk_lexington.jpg",
    noise: "assets/noise_colorfit.jpg",
    titan: "assets/titan_blue.jpg"
  };

  const demoProducts = [
    { product_id: 1, product_name: "Fossil Grant Chronograph", brand: "Fossil", description: "A polished chronograph with Roman markers and premium leather strap.", price: 11995, stock: 12, image_url: "assets/fossil_grant.jpg", category_id: 1 },
    { product_id: 2, product_name: "Titan Blue Ceramic", brand: "Titan", description: "Elegant blue dial dress watch with a slim steel profile.", price: 8495, stock: 18, image_url: "assets/titan_blue.jpg", category_id: 1 },
    { product_id: 3, product_name: "Casio Edifice Motorsport", brand: "Casio", description: "Sport-driven chronograph styling with durable build quality.", price: 10499, stock: 9, image_url: "assets/casio_edifice.jpg", category_id: 4 },
    { product_id: 4, product_name: "Michael Kors Lexington", brand: "Michael Kors", description: "Statement bracelet watch with a bold gold finish.", price: 18995, stock: 5, image_url: "assets/mk_lexington.jpg", category_id: 2 },
    { product_id: 5, product_name: "Noise ColorFit Pro", brand: "Noise", description: "Smart health tracking, crisp display, and all-day comfort.", price: 3499, stock: 25, image_url: "assets/noise_colorfit.jpg", category_id: 3 },
    { product_id: 6, product_name: "Fire-Boltt Ninja", brand: "Fire-Boltt", description: "Everyday smartwatch with workout modes and long battery life.", price: 2499, stock: 30, image_url: "assets/fireboltt_ninja.jpg", category_id: 3 },
    { product_id: 7, product_name: "Armani Exchange Chrono", brand: "Armani", description: "Premium urban chronograph for sharp formal and evening looks.", price: 21995, stock: 6, image_url: "assets/armani_chrono.jpg", category_id: 2 },
    { product_id: 8, product_name: "Fastrack Black Analog", brand: "Fastrack", description: "Minimal black dial with strong everyday wearability.", price: 2199, stock: 22, image_url: "assets/fastrack_black.jpg", category_id: 1 }
  ];

  const getToken = () => localStorage.getItem(TOKEN_KEY);
  const setToken = token => localStorage.setItem(TOKEN_KEY, token);
  const clearToken = () => {
    localStorage.removeItem(TOKEN_KEY);
  };
  const isAuthed = () => Boolean(getToken());
  const money = value => `Rs ${Number(value || 0).toLocaleString("en-IN")}`;

  async function request(path, options = {}) {
    const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
    if (getToken()) headers.Authorization = `Bearer ${getToken()}`;
    const response = await fetch(`${BASE_URL}${path}`, { ...options, headers });
    const text = await response.text();
    const data = text ? JSON.parse(text) : null;
    if (!response.ok) throw new Error(data?.detail || data?.message || data?.error || "Request failed");
    return data;
  }

  async function requestWithFallback(paths, options = {}) {
    let lastError;
    for (const path of paths) {
      try { return await request(path, options); }
      catch (error) { lastError = error; }
    }
    throw lastError;
  }

  const localRead = key => JSON.parse(localStorage.getItem(key) || "[]");
  const localWrite = (key, value) => localStorage.setItem(key, JSON.stringify(value));
  function imageForProduct(product) {
    const provided = product.image_url || product.image;
    if (provided) return provided;

    const haystack = `${product.brand || ""} ${product.product_name || product.name || ""}`.toLowerCase();
    const match = Object.entries(IMAGE_BY_BRAND).find(([key]) => haystack.includes(key));

    return match ? match[1] : "assets/fossil_grant.jpg";
  }

  const normalizeProduct = product => ({
    ...product,
    id: product.product_id ?? product.id,
    product_id: product.product_id ?? product.id,
    product_name: product.product_name ?? product.name ?? "Watch",
    image_url: imageForProduct(product),
    stock: Number(product.stock ?? 0),
    price: Number(product.price ?? 0)
  });
  async function products() {
    try { return (await request("/products/")).map(normalizeProduct); }
    catch { return demoProducts.map(normalizeProduct); }
  }
  async function product(id) {
    try { return normalizeProduct(await request(`/products/${id}`)); }
    catch {
      const item = demoProducts.find(p => String(p.product_id) === String(id)) || demoProducts[0];
      return normalizeProduct(item);
    }
  }
  async function login(payload) {
    const data = await request("/auth/login", { method: "POST", body: JSON.stringify(payload) });
    setToken(data.access_token);
    return data;
  }
  async function register(payload) {
    return request("/auth/register", { method: "POST", body: JSON.stringify(payload) });
  }
  async function me() {
    return request("/auth/me");
  }
  async function updateProfile(payload) {
    return request("/auth/me", { method: "PUT", body: JSON.stringify(payload) });
  }
  async function changePassword(payload) {
    return request("/auth/change-password", { method: "PUT", body: JSON.stringify(payload) });
  }
  async function cart() {
    try { return await request("/cart/"); }
    catch { return localRead(CART_KEY); }
  }
  async function addCart(product_id, quantity = 1) {
    try { return await request("/cart/add", { method: "POST", body: JSON.stringify({ product_id: Number(product_id), quantity }) }); }
    catch {
      const items = localRead(CART_KEY);
      const productData = await product(product_id);
      const existing = items.find(item => String(item.product_id) === String(product_id));
      if (existing) existing.quantity += quantity;
      else items.push({ cart_item_id: Date.now(), product_id: Number(product_id), quantity, product: productData });
      localWrite(CART_KEY, items);
      return { message: "Added to local cart" };
    }
  }
  async function removeCart(cartItemId) {
    try { return await request(`/cart/remove/${cartItemId}`, { method: "DELETE" }); }
    catch {
      localWrite(CART_KEY, localRead(CART_KEY).filter(item => String(item.cart_item_id ?? item.product_id) !== String(cartItemId)));
      return { message: "Removed from local cart" };
    }
  }
  async function updateCartQuantity(cartItemId, productId, quantity) {
    const qty = Math.max(1, Number(quantity || 1));
    const items = localRead(CART_KEY);
    const item = items.find(entry => String(entry.cart_item_id ?? entry.product_id) === String(cartItemId));
    if (item) {
      item.quantity = qty;
      localWrite(CART_KEY, items);
      return { message: "Quantity updated" };
    }
    if (qty > 1) return addCart(productId, 1);
    return { message: "Quantity unchanged" };
  }
  async function wishlist() {
    try { return await request("/wishlist/"); }
    catch { return localRead(WISH_KEY); }
  }
  async function addWishlist(product_id) {
    try { return await request("/wishlist/add", { method: "POST", body: JSON.stringify({ product_id: Number(product_id) }) }); }
    catch {
      const list = localRead(WISH_KEY);
      if (!list.some(item => String(item.product_id) === String(product_id))) list.push({ wishlist_id: Date.now(), product_id: Number(product_id), product: await product(product_id) });
      localWrite(WISH_KEY, list);
      return { message: "Added to local wishlist" };
    }
  }
  async function removeWishlist(id) {
    try { return await request(`/wishlist/${id}`, { method: "DELETE" }); }
    catch {
      localWrite(WISH_KEY, localRead(WISH_KEY).filter(item => String(item.wishlist_id ?? item.product_id) !== String(id)));
      return { message: "Removed from local wishlist" };
    }
  }
  const orders = () => request("/orders/");
  const placeOrder = () => request("/orders/place", { method: "POST" });
  const cancelOrder = id => request(`/orders/cancel/${id}`, { method: "PUT" });
  const reviews = productId => request(`/reviews/${productId}`);
  const addReview = payload => request("/reviews/", { method: "POST", body: JSON.stringify(payload) });
  async function ask(question) {

    const response = await fetch(
        `${BASE_URL}/chatbot/?message=${encodeURIComponent(question)}`,
        {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        }
    );

    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    return {
        response: data.response,
        products: data.products || []
    };
}

  return {
    BASE_URL,
    getToken,
    setToken,
    clearToken,
    isAuthed,
    money,
    products,
    product,
    login,
    register,
    me,
    updateProfile,
    changePassword,
    cart,
    addCart,
    removeCart,
    updateCartQuantity,
    wishlist,
    addWishlist,
    removeWishlist,
    orders,
    placeOrder,
    cancelOrder,
    reviews,
    addReview,
    ask,
    normalizeProduct
}
})();