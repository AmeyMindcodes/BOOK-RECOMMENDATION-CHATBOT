// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Swiper carousels
    const trendingSwiper = new Swiper('.trending-swiper', {
        slidesPerView: 1,
        spaceBetween: 20,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 30,
            },
            1024: {
                slidesPerView: 5,
                spaceBetween: 30,
            },
        }
    });

    const topRatedSwiper = new Swiper('.top-rated-swiper', {
        slidesPerView: 1,
        spaceBetween: 20,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 30,
            },
            1024: {
                slidesPerView: 5,
                spaceBetween: 30,
            },
        }
    });

    const popularSwiper = new Swiper('.popular-swiper', {
        slidesPerView: 1,
        spaceBetween: 20,
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        breakpoints: {
            640: {
                slidesPerView: 2,
                spaceBetween: 20,
            },
            768: {
                slidesPerView: 3,
                spaceBetween: 30,
            },
            1024: {
                slidesPerView: 5,
                spaceBetween: 30,
            },
        }
    });

    // Initialize AOS (Animate On Scroll)
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true
    });

    // Chatbot functionality
    const chatbotButton = document.querySelector('.chatbotbutton');
    const chatbox = document.querySelector('.chatbox');
    const closeBtn = document.querySelector('.close-btn');
    const sendBtn = document.getElementById('send');
    const messageInput = document.getElementById('message');
    const chatBody = document.querySelector('.chatbox > .body');
    const startChatBtn = document.querySelector('.start-chat-btn');

    // Function to toggle chatbox visibility
    function toggleChatbox() {
        if (chatbox.style.display === 'flex') {
            chatbox.style.display = 'none';
        } else {
            chatbox.style.display = 'flex';
            messageInput.focus();
            // Scroll to the bottom of the chat
            chatBody.scrollTop = chatBody.scrollHeight;
        }
    }

    // Event listeners for chatbot
    if (chatbotButton) {
        chatbotButton.addEventListener('click', toggleChatbox);
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            chatbox.style.display = 'none';
        });
    }

    if (startChatBtn) {
        startChatBtn.addEventListener('click', () => {
            toggleChatbox();
        });
    }

    // Function to add a message to the chat
    function addMessage(message, isUser = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(isUser ? 'isme' : 'isbot');

        const textElement = document.createElement('div');
        textElement.classList.add('text');
        textElement.innerHTML = message;

        messageElement.appendChild(textElement);
        chatBody.appendChild(messageElement);

        // Scroll to the bottom
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.id = 'typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingIndicator.appendChild(dot);
        }
        
        chatBody.appendChild(typingIndicator);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Function to handle sending a message
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message === '') return;

        // Add user message to chat
        addMessage(message, true);
        messageInput.value = '';

        // Show typing indicator
        showTypingIndicator();

        // Send message to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add bot response to chat
            addMessage(data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, there was an error processing your request. Please try again later.');
        });
    }

    // Event listeners for sending messages
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }

    if (messageInput) {
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Handle suggestion clicks
    document.addEventListener('click', function(e) {
        if (e.target && e.target.matches('.suggestion-list li')) {
            messageInput.value = e.target.textContent;
            sendMessage();
        }
    });

    // Search modal functionality
    const searchBtn = document.querySelector('.search-btn');
    const searchModal = document.querySelector('.search-modal');
    const closeSearchBtn = document.querySelector('.close-search-btn');
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchBtn');
    const searchResults = document.querySelector('.search-results');

    if (searchBtn) {
        searchBtn.addEventListener('click', () => {
            searchModal.style.display = 'flex';
            searchInput.focus();
        });
    }

    if (closeSearchBtn) {
        closeSearchBtn.addEventListener('click', () => {
            searchModal.style.display = 'none';
        });
    }

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === searchModal) {
            searchModal.style.display = 'none';
        }
    });

    // Handle search
    if (searchButton && searchInput) {
        searchButton.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }

    function performSearch() {
        const query = searchInput.value.trim();
        if (query === '') return;

        searchResults.innerHTML = '<p>Searching...</p>';

        fetch(`/search?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.books && data.books.length > 0) {
                    let html = '<div class="search-results-grid">';
                    data.books.forEach(book => {
                        html += `
                            <div class="book-card">
                                <div class="book-cover">
                                    <img src="${book.cover_url || '/static/images/default-cover.jpg'}" alt="${book.title}">
                                </div>
                                <div class="book-info">
                                    <h3 class="book-title">${book.title}</h3>
                                    <button class="details-btn" data-book-id="${book.id}">View Details</button>
                                </div>
                            </div>
                        `;
                    });
                    html += '</div>';
                    searchResults.innerHTML = html;
                } else {
                    searchResults.innerHTML = '<p>No books found matching your search.</p>';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                searchResults.innerHTML = '<p>An error occurred while searching. Please try again.</p>';
            });
    }

    // Book details modal functionality
    const bookDetailsModal = document.querySelector('.book-details-modal');
    const closeModalBtn = document.querySelector('.close-modal-btn');
    const modalBookTitle = document.getElementById('modalBookTitle');
    const modalBookCover = document.getElementById('modalBookCover');
    const modalBookDetails = document.getElementById('modalBookDetails');

    // Function to open book details modal
    function openBookDetailsModal(bookId) {
        fetch(`/book/${bookId}`)
            .then(response => response.json())
            .then(book => {
                modalBookTitle.textContent = book.title;
                modalBookCover.src = book.cover_url || '/static/images/default-cover.jpg';
                
                let detailsHtml = `
                    <p><strong>Author:</strong> ${book.author}</p>
                    <p><strong>Published:</strong> ${book.year}</p>
                    <p><strong>Rating:</strong> ${book.rating} / 5</p>
                    <p><strong>Description:</strong> ${book.description}</p>
                `;
                
                modalBookDetails.innerHTML = detailsHtml;
                bookDetailsModal.style.display = 'flex';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error loading book details. Please try again.');
            });
    }

    // Event delegation for book detail buttons
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('details-btn')) {
            const bookId = e.target.getAttribute('data-book-id');
            openBookDetailsModal(bookId);
        }
    });

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => {
            bookDetailsModal.style.display = 'none';
        });
    }

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === bookDetailsModal) {
            bookDetailsModal.style.display = 'none';
        }
    });

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.style.padding = '10px 0';
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.padding = '15px 0';
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        }
    });

    // Add initial greeting message to chatbot
    if (chatBody) {
        addMessage('Hi there! 👋 I\'m BookBuddy, your personal book recommendation assistant. How can I help you today?<br><br>You can ask me things like:<ul class="suggestion-list"><li>Recommend me a fantasy book</li><li>What are the trending books?</li><li>Suggest a random book</li><li>Show me books by Stephen King</li></ul>');
    }
}); 