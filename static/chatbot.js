const chatbotContainer = document.querySelector(".container");
const chatbox = document.getElementById("chatbox");
const chatbody = document.getElementById("chatbody");
const messageTextBox = document.getElementById("userInput");
const sendbutton = document.getElementById("send");
const questions = [
  "Please enter the name of the author whose book you would like to read.",
  "Please enter the name of the publisher whose book you would like to read.",
  "Please enter the partial title of the book you're interested in.",
  "If you'd like, you can select the option to get the top 10 books with the maximum rating.",
  "Alternatively, you can choose to get the book ID based on the title of the book.",
];

// Initialize the chatbot
document.addEventListener("DOMContentLoaded", function() {
  // Add click event listeners to suggestion list items
  const suggestionItems = document.querySelectorAll(".suggestion-list li");
  suggestionItems.forEach(item => {
    item.addEventListener("click", function() {
      messageTextBox.value = this.textContent;
      sendMsg();
    });
  });
});

function openChatBot() {
  if (chatbox.style.display === "flex") {
    chatbox.style.display = "none";
    return;
  }
  chatbox.style.display = "flex";
  chatbody.scrollTop = chatbody.scrollHeight;
  
  // Focus on the input field
  setTimeout(() => {
    messageTextBox.focus();
  }, 300);
}

function closeChatBot() {
  chatbox.style.display = "none";
}

// Event listeners
sendbutton.addEventListener("click", sendMsg);
messageTextBox.addEventListener("keypress", (event) => {
  if (event.key === "Enter" && messageTextBox.value.trim() !== "") {
    sendMsg();
  }
});

// Function to display user message
function displayUserMessage(message) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", "isme");
  
  const messageText = document.createElement("p");
  messageText.classList.add("text");
  messageText.textContent = message;
  
  messageDiv.appendChild(messageText);
  chatbody.appendChild(messageDiv);
  chatbody.scrollTop = chatbody.scrollHeight;
}

// Function to display bot message
function displayBotMessage(message) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", "isbot");
  
  const messageText = document.createElement("p");
  messageText.classList.add("text");
  messageText.textContent = message;
  
  messageDiv.appendChild(messageText);
  chatbody.appendChild(messageDiv);
  chatbody.scrollTop = chatbody.scrollHeight;
}

// Function to display book list
function displayBookList(books) {
  const listElement = document.createElement("ol");
  listElement.classList.add("isbot");
  
  books.forEach(book => {
    const listItem = document.createElement("li");
    listItem.textContent = book;
    listElement.appendChild(listItem);
  });
  
  chatbody.appendChild(listElement);
  chatbody.scrollTop = chatbody.scrollHeight;
}

// Function to display typing indicator
function showTypingIndicator() {
  const typingDiv = document.createElement("div");
  typingDiv.classList.add("message", "isbot", "typing-indicator");
  typingDiv.innerHTML = '<span></span><span></span><span></span>';
  chatbody.appendChild(typingDiv);
  chatbody.scrollTop = chatbody.scrollHeight;
  return typingDiv;
}

// Function to remove typing indicator
function removeTypingIndicator(indicator) {
  if (indicator && indicator.parentNode) {
    indicator.parentNode.removeChild(indicator);
  }
}

// Function to handle sending messages
async function sendMsg() {
  const userMessage = messageTextBox.value.trim();
  
  if (userMessage === "") {
    return;
  }
  
  // Display user message
  displayUserMessage(userMessage);
  
  // Clear input field
  messageTextBox.value = "";
  
  // Show typing indicator
  const typingIndicator = showTypingIndicator();
  
  // Check if it's a legacy format (number, query)
  const splitted = userMessage.split(",");
  if (splitted.length == 2 && !isNaN(splitted[0].trim())) {
    // Legacy format handling
    try {
      const response = await fetch(`/recommendations/${splitted[0].trim()}`, {
        method: "POST",
        body: JSON.stringify({ query: splitted[1].trim() }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      
      const data = await response.json();
      
      // Remove typing indicator
      removeTypingIndicator(typingIndicator);
      
      // Display results
      if (Array.isArray(data)) {
        displayBookList(data);
      } else {
        displayBotMessage(data);
      }
    } catch (error) {
      removeTypingIndicator(typingIndicator);
      displayBotMessage("Sorry, I encountered an error. Please try again.");
      console.error("Error:", error);
    }
  } else {
    // New AI chat format
    try {
      const response = await fetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: userMessage }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      
      const data = await response.json();
      
      // Remove typing indicator
      removeTypingIndicator(typingIndicator);
      
      // Display response message
      displayBotMessage(data.response);
      
      // If there are books to display
      if (data.books && Array.isArray(data.books) && data.books.length > 0) {
        displayBookList(data.books);
      }
    } catch (error) {
      removeTypingIndicator(typingIndicator);
      displayBotMessage("Sorry, I encountered an error. Please try again.");
      console.error("Error:", error);
    }
  }
}

// Add CSS for typing indicator
const style = document.createElement('style');
style.textContent = `
  .typing-indicator {
    display: flex;
    align-items: center;
    padding: 15px 20px;
  }
  
  .typing-indicator span {
    height: 8px;
    width: 8px;
    float: left;
    margin: 0 1px;
    background-color: #9E9EA1;
    display: block;
    border-radius: 50%;
    opacity: 0.4;
  }
  
  .typing-indicator span:nth-of-type(1) {
    animation: 1s blink infinite 0.3333s;
  }
  
  .typing-indicator span:nth-of-type(2) {
    animation: 1s blink infinite 0.6666s;
  }
  
  .typing-indicator span:nth-of-type(3) {
    animation: 1s blink infinite 0.9999s;
  }
  
  @keyframes blink {
    50% {
      opacity: 1;
    }
  }
`;
document.head.appendChild(style);