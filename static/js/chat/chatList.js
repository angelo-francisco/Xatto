const chatItem = document.querySelector(".chat-item")

chatItem.addEventListener('click', () => {
    const customEvent = new CustomEvent('OpenChat')
    document.body.dispatchEvent(customEvent)
})