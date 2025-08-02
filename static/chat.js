document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");
  const chatWindow = document.getElementById("chat-window");
  const loader = document.getElementById("loader");

  const appendMessage = (text, sender) => {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);

    const avatarDiv = document.createElement("div");
    avatarDiv.classList.add("avatar", `${sender}-avatar`);
    avatarDiv.innerHTML = sender === "user" ? '<i class="bi bi-person-fill"></i>' : '<i class="bi bi-robot"></i>';

    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("bubble");
    bubbleDiv.textContent = text;

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(bubbleDiv);
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userInput = input.value.trim();
    if (!userInput) return;

    appendMessage(userInput, "user");
    input.value = "";
    loader.style.display = "block";

    try {
      const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userInput })
      });

      const data = await res.json();
      const responseText = data.results;
      appendMessage(responseText || "Sorry, I couldn't find relevant features.", "bot");
    } catch (error) {
      appendMessage("An error occurred. Please try again.", "bot");
    } finally {
      loader.style.display = "none";
    }
  });
});
