function createMessageElement(content, time, isSender) {
    let m = document.createElement('div');
    m.classList.add('message-container', isSender ? 'sent' : 'received');
    m.innerHTML = `
        <div class="message-bubble">
            <p>${content}</p>
            <div class="message-info">
                <span class="time">${time}</span>
            </div>
        </div>`;
    return m;
}

function parseTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function loadRoom() {
    const otherUserUsername = document.querySelector('#js-other-user-username').textContent;
    const chatSlug = document.querySelector('[data-chat-slug]').dataset.chatSlug
    const userSlug = document.querySelector("meta[name='user-slug']").getAttribute('content')
    const userUsername = document.querySelector("meta[name='user-username']").getAttribute('content')

    const firstMessage = document.querySelector('#first-message');

    if (firstMessage) {
        firstMessage.innerText += ' ' + otherUserUsername;
    }

    const ws2 = new WebSocket(`ws://${window.location.host}/chat/chat-consumer/${chatSlug}/${userSlug}/`);

    const chatMessages = document.querySelector('.chat-messages');
    const messageInput = document.getElementById('chat-message-input');

    function sendMessage() {
        const content = messageInput.value.trim();
        if (!content) {
            messageInput.classList.add('shake');
            setTimeout(() => messageInput.classList.remove('shake'), 500);
            return;
        }

        if (ws2.readyState === WebSocket.OPEN) {
            const message = {
                content: content,
            };

            ws2.send(JSON.stringify(message));
            messageInput.value = '';
        }
    }

    ws2.onmessage = (e) => {
        const data = JSON.parse(e.data);
        const time = parseTimestamp(data.timestamp);
        const isSender = data.username === userUsername;

        const messageElement = createMessageElement(data.content, time, isSender);
        chatMessages.appendChild(messageElement);

        messageElement.style.opacity = '0';
        messageElement.style.transform = `translateY(${isSender ? '20px' : '-20px'})`;

        requestAnimationFrame(() => {
            messageElement.style.transition = 'all 0.3s ease-out';
            messageElement.style.opacity = '1';
            messageElement.style.transform = 'translateY(0)';
        });

        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    };

    document.getElementById('js-chat-input-button').addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => e.key === 'Enter' && sendMessage());
}

loadRoom();