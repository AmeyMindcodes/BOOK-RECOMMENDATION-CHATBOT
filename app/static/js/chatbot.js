// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
  console.log("Chatbot.js loaded");
  
  // Get DOM elements
  const chatbotContainer = document.querySelector(".chatbot-container");
  const chatbox = document.getElementById("chatbox");
  const chatbody = document.getElementById("chatbody");
  const messageTextBox = document.getElementById("userInput");
  const sendbutton = document.getElementById("send");
  
  console.log("Chatbox element:", chatbox);
  console.log("Chatbody element:", chatbody);
  console.log("Message text box element:", messageTextBox);
  console.log("Send button element:", sendbutton);

  // Add click event listeners to suggestion list items
  const suggestionItems = document.querySelectorAll(".suggestion-list li");
  suggestionItems.forEach(item => {
    item.addEventListener("click", function() {
      messageTextBox.value = this.textContent;
      sendMsg();
    });
  });

  // Define global functions for opening and closing the chatbot
  window.openChatBot = function() {
    console.log("openChatBot called");
    if (chatbox.style.display === "flex") {
      console.log("Closing chatbox");
      chatbox.style.display = "none";
      return;
    }
    console.log("Opening chatbox");
    chatbox.style.display = "flex";
    chatbody.scrollTop = chatbody.scrollHeight;
    
    // Focus on the input field
    setTimeout(() => {
      messageTextBox.focus();
    }, 300);
  };

  window.closeChatBot = function() {
    console.log("closeChatBot called");
    chatbox.style.display = "none";
  };

  // Add direct event listeners to chatbot buttons
  const chatbotButton = document.querySelector(".chatbotbutton");
  const closeBtn = document.querySelector(".close-btn");
  
  if (chatbotButton) {
    console.log("Adding event listener to chatbot button");
    chatbotButton.addEventListener("click", function(e) {
      e.preventDefault();
      console.log("Chatbot button clicked");
      openChatBot();
    });
  }
  
  if (closeBtn) {
    console.log("Adding event listener to close button");
    closeBtn.addEventListener("click", function(e) {
      e.preventDefault();
      console.log("Close button clicked");
      closeChatBot();
    });
  }

  // Event listeners for sending messages
  if (sendbutton) {
    sendbutton.addEventListener("click", sendMsg);
  }
  
  if (messageTextBox) {
    messageTextBox.addEventListener("keypress", (event) => {
      if (event.key === "Enter" && messageTextBox.value.trim() !== "") {
        sendMsg();
      }
    });
  }

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

  // Initialize the chatbot
  console.log("Chatbot initialized");
});