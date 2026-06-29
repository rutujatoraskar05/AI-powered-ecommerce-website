document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");

  loginForm?.addEventListener("submit", async event => {
    event.preventDefault();
    const button = loginForm.querySelector("button");
    button.disabled = true;
    try {
      await API.login(Object.fromEntries(new FormData(loginForm)));
      App.toast("Login successful");
      location.href = sessionStorage.getItem("watch_store_redirect") || "index.html";
    } catch (error) {
      App.toast(error.message, "error");
    } finally {
      button.disabled = false;
    }
  });

  registerForm?.addEventListener("submit", async event => {
    event.preventDefault();
    const button = registerForm.querySelector("button");
    button.disabled = true;
    try {
      await API.register(Object.fromEntries(new FormData(registerForm)));
      App.toast("Account created. Please login.");
      setTimeout(() => location.href = "login.html", 700);
    } catch (error) {
      App.toast(error.message, "error");
    } finally {
      button.disabled = false;
    }
  });
});
