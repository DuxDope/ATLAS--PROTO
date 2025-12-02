document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("send-btn");
    const userInput = document.getElementById("user-input");
    const chatHistory = document.getElementById("chat-history");

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("Usuario", message);

        fetch("/chatbot/response/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({ message }),
        })
            .then(response => response.json())
            .then(data => {
                appendMessage("Atlas", data.response);
                if (data.final_step) {
                    sendBtn.disabled = true;
                    userInput.disabled = true;
                }
            })
            .catch(error => {
                appendMessage("Atlas", "Hubo un error al conectar con el servidor.");
                console.error(error);
            });

        userInput.value = "";
    }

    sendBtn.addEventListener("click", sendMessage);

    userInput.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement("div");
        const isUser = sender === "Usuario";
        messageElement.classList.add("message", isUser ? "user-message" : "bot-message");
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function getCSRFToken() {
        const cookies = document.cookie.split("; ");
        for (let cookie of cookies) {
            const [name, value] = cookie.split("=");
            if (name === "csrftoken") {
                return value;
            }
        }
        return "";
    }
});
