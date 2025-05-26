document.addEventListener('DOMContentLoaded', function() {
    const aiChatOpenBtn = document.getElementById('aiChatOpenBtn');
    const modalAiChat = document.getElementById('modalAiChat');
    const aiChatCloseBtn = document.getElementById('aiChatCloseBtn');
    const aiChatForm = document.getElementById('aiChatForm');
    const aiChatInput = document.getElementById('aiChatInput');
    const aiChatSendBtn = document.getElementById('aiChatSendBtn');
    const aiChatMessages = document.getElementById('aiChatMessages');

    aiChatOpenBtn.onclick = () => {
        modalAiChat.classList.add('active');
        setTimeout(() => {
            aiChatInput.focus();
        }, 100);
    };

    aiChatCloseBtn.onclick = () => { closeModalAiChat(); };
    window.addEventListener('keydown', e => {
        if (e.key === 'Escape' && modalAiChat.classList.contains('active')) closeModalAiChat();
    });
    modalAiChat.addEventListener('click', e => {
        if (e.target === modalAiChat) closeModalAiChat();
    });
    aiChatInput.addEventListener('input', () => {
        aiChatSendBtn.disabled = aiChatInput.value.trim().length === 0;
    });
    aiChatForm.onsubmit = async function(e) {
        e.preventDefault();
        const text = aiChatInput.value.trim();
        if (!text) return;

        addAiMessage(text, 'user');
        aiChatInput.value = '';
        aiChatSendBtn.disabled = true;
        aiChatMessages.scrollTop = aiChatMessages.scrollHeight;

        try {
            const response = await sendToAiApi(text);
            addAiMessage(response, 'bot');
        } catch (error) {
            addAiMessage('Ошибка: не удалось получить ответ от ИИ.', 'error');
        } finally {
            aiChatMessages.scrollTop = aiChatMessages.scrollHeight;
        }
    };

    function closeModalAiChat() {
        modalAiChat.classList.remove('active');
    }

    function addAiMessage(text, who) {
        const msg = document.createElement('div');
        msg.className = 'ai-message ' + who;
        msg.textContent = text;
        aiChatMessages.appendChild(msg);
    }

    async function sendToAiApi(userInput) {
        const apiUrl = "https://openrouter.ai/api/v1/chat/completions";
        const apiKey = "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"; // Используем ключ из Key_API.py

        const payload = {
            model: "deepseek/deepseek-r1:free",
            messages: [
                {
                    role: "user",
                    content: userInput
                }
            ]
        };

        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${apiKey}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error("Ошибка сети");
        }

        const data = await response.json();
        return data.choices[0].message.content;
    }
});
