document.addEventListener("DOMContentLoaded", async () => {
  if (App.page !== "orders") return;
  const target = document.getElementById("ordersList");
  try {
    const orders = await API.orders();
    target.innerHTML = orders.length
      ? orders.map(orderCard).join("")
      : `<div class="glass-card empty">No orders yet.</div>`;
    document.querySelectorAll("[data-cancel-order]").forEach(btn => {
      btn.addEventListener("click", async () => {
        await API.cancelOrder(btn.dataset.cancelOrder);
        App.toast("Order cancelled");
        location.reload();
      });
    });
  } catch (error) {
    target.innerHTML = `<div class="glass-card empty">${error.message}</div>`;
  }
});

function orderCard(order) {
  const id = order.order_id || order.id;
  const status = String(order.status || "confirmed").toLowerCase();
  const placedDate = parseDate(order.created_at);
  const deliveryDate = estimateDeliveryDate(order.delivery_date || order.expected_delivery_date, placedDate);
  const currentStep = getCurrentStep(status);
  const canCancel = !["cancelled", "delivered"].includes(status);
  return `
    <article class="glass-card order-card">
      <div class="order-top">
        <div>
          <p class="eyebrow">Order confirmed</p>
          <h2>Order #${id}</h2>
          <p class="meta">Placed: ${formatDate(placedDate)} | Delivery date: ${formatDate(deliveryDate)}</p>
        </div>
        <span class="stock ${status === "cancelled" ? "out" : ""}">${titleCase(status)}</span>
      </div>
      <div class="order-stage-list">
        ${["Confirmed", "Processing", "Shipping", "Out for Delivery", "Delivered"].map((label, index) => `
          <div class="order-stage ${index <= currentStep ? "done" : ""} ${index === currentStep ? "current" : ""}">
            <span>${index + 1}</span>
            <strong>${label}</strong>
          </div>
        `).join("")}
      </div>
      <div class="summary-row"><span>Total amount</span><strong>${API.money(order.total_amount || order.total || 0)}</strong></div>
      <p class="meta">${stageMessage(currentStep, deliveryDate, status)}</p>
      ${canCancel ? `<button class="btn btn-danger" data-cancel-order="${id}">Cancel order</button>` : ""}
    </article>`;
}

function getCurrentStep(status) {
  if (status.includes("deliver")) return 4;
  if (status.includes("out")) return 3;
  if (status.includes("ship")) return 2;
  if (status.includes("process") || status.includes("pending")) return 1;
  return 0;
}

function stageMessage(step, deliveryDate, status) {
  if (status.includes("cancel")) return "This order has been cancelled.";
  const messages = [
    "Your order is confirmed and will move to processing shortly.",
    "Your order is being packed and verified.",
    "Your order has been shipped from the warehouse.",
    `Your order is out for delivery. Expected today or by ${formatDate(deliveryDate)}.`,
    "Your order has been delivered successfully."
  ];
  return messages[step] || messages[0];
}

function parseDate(value) {
  const date = value ? new Date(value) : new Date();
  return Number.isNaN(date.getTime()) ? new Date() : date;
}

function estimateDeliveryDate(value, placedDate) {
  if (value) return parseDate(value);
  const date = new Date(placedDate);
  date.setDate(date.getDate() + 5);
  return date;
}

function formatDate(date) {
  return date.toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" });
}

function titleCase(value) {
  return String(value || "Confirmed").replaceAll("_", " ").replace(/\b\w/g, char => char.toUpperCase());
}
