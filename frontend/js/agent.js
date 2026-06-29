document.addEventListener("DOMContentLoaded", () => {

  if (
    App.page === "login" ||
    App.page === "register" ||
    App.page === "chatbot"
  ) return;

  const fab = document.createElement("button");
  fab.className = "agent-fab";
  fab.type = "button";
  fab.textContent = "AI";
  fab.title = "Watch Store AI";

  const widget = document.createElement("section");
  widget.className = "agent-widget";

  widget.innerHTML = `
    <div class="agent-bar">
      <strong>🤖 Watch Store AI</strong>

      <div>
        <button id="minAgent" type="button">_</button>
        <button id="closeAgent" type="button">×</button>
      </div>
    </div>

    <div id="agentMessages" class="chat-messages"></div>

    <form id="agentForm" class="chat-input">
      <input
        id="agentInput"
        autocomplete="off"
        placeholder="Ask anything..."
      />

      <button
        class="btn btn-primary"
        type="submit">
        Send
      </button>
    </form>
  `;

  document.body.append(fab, widget);

  const messages = widget.querySelector("#agentMessages");

  fab.addEventListener("click", () => {

    widget.classList.add("open");
    fab.classList.add("hidden");

    if (!messages.children.length) {

      addChatMessage(
        messages,
        "assistant",
        "👋 Hi! I'm your Watch Store AI.\n\nI can:\n\n• Recommend watches\n• Search products\n• Add to cart\n• Track orders\n• Place orders\n• Update your profile"
      );

    }

  });

  widget.querySelector("#closeAgent")
    .addEventListener("click", () => {

      widget.classList.remove("open");
      fab.classList.remove("hidden");

    });

  widget.querySelector("#minAgent")
    .addEventListener("click", () => {

      widget.classList.toggle("minimized");

    });

  widget.querySelector("#agentForm")
    .addEventListener("submit", async (event) => {

      event.preventDefault();

      const input = widget.querySelector("#agentInput");

      const question = input.value.trim();

      if (!question) return;

      input.value = "";

      addChatMessage(messages, "user", question);

      const typing = addTyping(messages);

      try {

        const data = await API.ask(question);

        typing.remove();

        let reply =
          data.response ||
          data.message ||
          "No response received.";

        if (typeof reply === "object") {
          reply = JSON.stringify(reply, null, 2);
        }

        addChatMessage(
          messages,
          "assistant",
          reply
        );

        if (Array.isArray(data.products) && data.products.length > 0) {

          data.products.forEach(product => {

            addChatMessage(
              messages,
              "assistant",
`⌚ ${product.product_name}

🏷 Brand: ${product.brand}

💰 Price: ₹${product.price}

📦 Stock: ${product.stock}`
            );

          });

        }

      }
      catch (err) {

        console.error(err);

        typing.remove();

        addChatMessage(
          messages,
          "assistant",
          "❌ Unable to connect to the AI server."
        );

      }

    });

});

function addChatMessage(container, role, text) {

  const div = document.createElement("div");

  div.className = `message ${role}`;

  div.textContent = text;

  container.appendChild(div);

  container.scrollTop = container.scrollHeight;

  return div;

}

function addTyping(container) {

  const div = document.createElement("div");

  div.className = "message assistant typing";

  div.innerHTML = `
    <span></span>
    <span></span>
    <span></span>
  `;

  container.appendChild(div);

  container.scrollTop = container.scrollHeight;

  return div;

}