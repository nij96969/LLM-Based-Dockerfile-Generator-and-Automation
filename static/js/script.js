function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const messages = document.getElementById('messages');
    
    // Append the user's message to the chat
    const userMessage = document.createElement('div');
    userMessage.innerHTML = `You:<br>${userInput}`;
    userMessage.className = 'message user-message ';

    const userContainer = document.createElement('div');
    userContainer.className = 'user-container'
    userContainer.appendChild(userMessage)

    messages.appendChild(userContainer);

    // Clear the input
    document.getElementById('user-input').value = '';

    // Send the user's message to the server
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `user_input=${encodeURIComponent(userInput)}`
    })
    .then(response => response.json())
    .then(data => {
        // Append the bot's response to the chat
        const botMessage = document.createElement('div');
        botMessage.innerHTML = `Jarvis:<br>${data.response.replace(/\n/g, '<br>')}`;
        botMessage.className = 'message bot-message';
        messages.appendChild(botMessage);

        // Scroll to the bottom of the chat
        messages.scrollTop = messages.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getValue() {
    // Get the textarea element
    var textarea = document.getElementById("userInput");

    // Get the value entered by the user
    var text = textarea.value;

    // Display the value (for demonstration)
    alert("The value entered is: " + text);
}

// Function to fetch the updated list of Docker images and update the select element
function refreshList() {
    fetch('/refresh_images')
        .then(response => response.json())
        .then(data => {
            const dockerImagesSelect = document.getElementById('docker-images');
            dockerImagesSelect.innerHTML = ''; // Clear existing options
            data.images.forEach(image => {
                const option = document.createElement('option');
                option.value = image.ID;
                option.textContent = `${image.Repository}:${image.Tag}`;
                dockerImagesSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error refreshing Docker images:', error));
}