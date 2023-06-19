function getChatId() {
    const pathname = window.location.pathname
    const chatId = pathname.split('/')[2]
    return chatId
}

document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('messages-container');
    const chatId = getChatId()
    
    if (!!chatId) {
        fetch(`/chat_detail/${chatId}/`)
            .then(response => response.json())
            .then(data => {
                const messages = data.messages;
    
                let chatDetailHTML = `
                    <div class="d-flex flex-column messages">
                `;
    
                messages.forEach((message) => {
                    const content = message.content;
                    chatDetailHTML += `
                        <div class="other-message message mt-3">
                            <p>${content}</p>
                        </div>
                    `;
                });
    
                chatDetailHTML += `</div>`;
                messagesContainer.innerHTML = chatDetailHTML;
            })
            .catch(error => console.log(error));
    } else{
        const sendMessageForm = document.getElementById('send-message-form');
        const imageChatGroupMessage = document.getElementById('image-chat-group-message')
        sendMessageForm.style.setProperty('display', 'none', 'important')
        imageChatGroupMessage.style.setProperty('display', 'none', 'important')
    }
   
  


    const sendMessageForm = document.getElementById('send-message-form');
    sendMessageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const data = new FormData(event.target);
        const values =  [...data.entries()]
        //A posição zero é o input hidden CSRFToken
        const token = values[0][1]
        const messageContent = values[1][1]

            if (!!messageContent) {
                fetch(`/send_message/${chatId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': token,
                    },
                    body: JSON.stringify({
                        content: messageContent
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        const newMessage = data.content;
                        const newMessageHTML = `
                            <div class="message">
                                <p>${newMessage}</p>
                            </div>
                        `;
                        messagesContainer.insertAdjacentHTML('beforeend', newMessageHTML);

                        messageInput.value = '';
                    })
                    .catch(error => console.log(error));
            }
    });
});