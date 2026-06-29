document.addEventListener("DOMContentLoaded", async () => {
  if (App.page !== "admin") return;
  const statsEl = document.getElementById("adminStats");
  let stats = {};
  try { stats = await API.adminDashboard(); }
  catch { stats = { total_users: 128, total_products: 42, total_orders: 318, total_revenue: 1245600 }; }
  const cards = [["Total users", stats.total_users || stats.users || 0], ["Total products", stats.total_products || stats.products || 0], ["Total orders", stats.total_orders || stats.orders || 0], ["Total revenue", API.money(stats.total_revenue || stats.revenue || 0)]];
  statsEl.innerHTML = cards.map(([label, value]) => `<article class="stat-card glass-card"><span>${label}</span><strong>${value}</strong></article>`).join("");
  drawRevenueChart();
  loadAdminTab("products");
  document.querySelectorAll("[data-admin-tab]").forEach(btn => btn.addEventListener("click", () => {
    document.querySelectorAll("[data-admin-tab]").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    loadAdminTab(btn.dataset.adminTab);
  }));
});

function drawRevenueChart() {
  const canvas = document.getElementById("revenueChart");
  const ctx = canvas.getContext("2d");
  const data = [180, 240, 210, 320, 420, 520, 610];
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "#0A192F";
  ctx.lineWidth = 4;
  ctx.beginPath();
  data.forEach((value, i) => {
    const x = 42 + i * 82;
    const y = 230 - value / 3.2;
    if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
  });
  ctx.stroke();
  ctx.fillStyle = "#66E4FF";
  data.forEach((value, i) => { const x = 42 + i * 82; const y = 230 - value / 3.2; ctx.beginPath(); ctx.arc(x, y, 7, 0, Math.PI * 2); ctx.fill(); });
}

async function loadAdminTab(tab) {
  const target = document.getElementById("adminTable");
  try {
    if (tab === "products") {
      const products = await API.products();
      target.innerHTML = table(["ID", "Name", "Brand", "Price", "Stock"], products.map(p => [p.product_id, p.product_name, p.brand, API.money(p.price), p.stock]));
    }
    if (tab === "orders") {
      const orders = await API.adminOrders();
      target.innerHTML = table(["ID", "Status", "Total"], orders.map(o => [o.order_id || o.id, o.status || "Placed", API.money(o.total_amount || 0)]));
    }
    if (tab === "users") {
      const users = await API.adminUsers();
      target.innerHTML = table(["ID", "Name", "Email", "Mobile"], users.map(u => [u.user_id || u.id, u.name || "-", u.email || "-", u.mobile || "-"]));
    }
  } catch (error) {
    target.innerHTML = `<div class="empty">Unable to load ${tab}: ${error.message}</div>`;
  }
}

function table(headers, rows) {
  return `<table class="data-table"><thead><tr>${headers.map(h => `<th>${h}</th>`).join("")}</tr></thead><tbody>${rows.map(row => `<tr>${row.map(cell => `<td>${cell}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}
