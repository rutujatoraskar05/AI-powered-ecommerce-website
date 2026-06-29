document.addEventListener("DOMContentLoaded", () => {

    const messages = document.getElementById("chatMessages");
    const form = document.getElementById("chatForm");
    const input = document.getElementById("chatInput");

    addChatMessage(
        messages,
        "assistant",
        "👋 Hi! I'm Watch Store AI.\n\nHow can I help you today?"
    );

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

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
                "No response from AI.";

            if (typeof reply === "object") {
                reply = JSON.stringify(reply, null, 2);
            }

            addChatMessage(
                messages,
                "assistant",
                reply
            );

            // Show product cards if backend returns products
            if (Array.isArray(data.products)) {

                data.products.forEach(product => {

                    addProductCard(messages, product);

                });

            }

        }

        catch (error) {

            typing.remove();

            console.error(error);

            addChatMessage(
                messages,
                "assistant",
                "❌ Unable to connect to chatbot."
            );

        }

    });

});

function addChatMessage(container, role, text) {

    const div = document.createElement("div");

    div.className = `message ${role}`;

    // Preserve line breaks
    div.innerHTML = text.replace(/\n/g, "<br>");

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

function addProductCard(container, product) {

    const card = document.createElement("div");

    card.className = "message assistant";

    card.innerHTML = `
        <div style="padding:10px">

            <strong>${product.product_name}</strong>

            <br><br>

            Brand : ${product.brand}<br>

            Price : ₹${product.price}<br>

            ${product.stock !== undefined
                ? `Stock : ${product.stock}<br>`
                : ""}

        </div>
    `;

    container.appendChild(card);

    container.scrollTop = container.scrollHeight;

}