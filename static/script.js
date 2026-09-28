const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const chatMessages = document.getElementById("chatMessages");
const sendButton = document.getElementById("sendButton");

function addMessage(text, className) {
    const message = document.createElement("div");
    message.className = `message ${className}`;
    message.textContent = text;
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return message;
}

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const text = messageInput.value.trim();
    if (!text) {
        return;
    }

    addMessage(text, "user-message");
    messageInput.value = "";
    sendButton.disabled = true;

    const loadingMessage = addMessage("Thinking...", "bot-message");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: text }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        loadingMessage.textContent = data.reply;
    } catch (error) {
        loadingMessage.textContent = error.message;
        loadingMessage.classList.add("error-message");
    } finally {
        sendButton.disabled = false;
        messageInput.focus();
    }
});
