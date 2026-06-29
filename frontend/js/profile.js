document.addEventListener("DOMContentLoaded", async () => {
  if (App.page !== "profile") return;
  const target = document.getElementById("profilePanel");
  let user = {};
  let orders = [];
  try { user = (await API.me()).user || {}; } catch { user = JSON.parse(localStorage.getItem("watch_store_profile") || "{}"); }
  try { orders = await API.orders(); } catch { orders = []; }
  const spent = orders.reduce((sum, order) => sum + Number(order.total_amount || order.total || 0), 0);
  target.innerHTML = `
    <section class="glass-card profile-card">
      <h2>User information</h2>
      <form id="profileForm" class="stack">
        <label>Name <input name="name" value="${user.name || ""}" required></label>
        <label>Email <input name="email" type="email" value="${user.email || ""}" required></label>
        <label>Mobile <input name="mobile" value="${user.mobile || ""}" required></label>
        <button class="btn btn-primary" type="submit">Update profile</button>
      </form>
    </section>
    <section class="glass-card profile-card">
      <h2>Change password</h2>
      <form id="passwordForm" class="stack">
        <label>Current password <input name="current_password" type="password" required></label>
        <label>New password <input name="new_password" type="password" minlength="6" required></label>
        <button class="btn btn-dark" type="submit">Change password</button>
      </form>
    </section>
    <aside class="glass-card profile-card">
      <h2>Account summary</h2>
      <div class="kpi-row">
        <div class="kpi"><span>Total orders</span><strong>${orders.length}</strong></div>
        <div class="kpi"><span>Total spent</span><strong>${API.money(spent)}</strong></div>
      </div>
    </aside>`;
  document.getElementById("profileForm").addEventListener("submit", async event => {
    event.preventDefault();
    try {
      const payload = Object.fromEntries(new FormData(event.target));
      const result = await API.updateProfile(payload);
      if (result.access_token) API.setToken(result.access_token);
      localStorage.setItem("watch_store_profile", JSON.stringify(result.user || payload));
      App.toast("Profile updated");
    } catch (error) {
      App.toast(error.message, "error");
    }
  });
  document.getElementById("passwordForm").addEventListener("submit", async event => {
    event.preventDefault();
    try {
      await API.changePassword(Object.fromEntries(new FormData(event.target)));
      event.target.reset();
      App.toast("Password changed");
    } catch (error) {
      App.toast(error.message, "error");
    }
  });
});
