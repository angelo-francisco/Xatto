
const userSlug = document.querySelector("meta[name='user-slug']").getAttribute('content')
const loader = document.querySelector('#loader')

document.addEventListener('DOMContentLoaded', () => {
    loader.style.display = "none"
})

function loadUserStatus() {
    const ws = new WebSocket(`ws://${window.location.host}/chat/status/${userSlug}/`)

    document.body.addEventListener('OpenChat', () => {
        ws.onmessage = (e) => {
            const data = JSON.parse(e.data)
            
            const userSlug = document.querySelector("#js-other-user-username").dataset.userSlug
            const statusHTML = document.querySelector("#js-status")
            
            if (userSlug === data.userSlug) {
                statusHTML.innerText = data.status === "on" ? "Online" : data.last_seen
                statusHTML.style.color = data.status === "on" ? "green" : "#333"
            }
        }
    })
    
}

loadUserStatus()
