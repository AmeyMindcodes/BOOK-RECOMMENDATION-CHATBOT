from flask import Blueprint, render_template, jsonify, request
from app.models.book_service import (
    get_trending_books,
    get_top_rated_books,
    get_popular_books,
    search_books
)
from app.models.chatbot import process_user_message
import random

main_bp = Blueprint('main', __name__)

# AI-powered responses for the chatbot
greetings = ["hello", "hi", "hey", "greetings", "howdy", "hola"]
greeting_responses = [
    "Hello! I'm your AI book recommendation assistant. How can I help you find your next great read?",
    "Hi there! Looking for a good book? I'm here to help!",
    "Hey! I'm excited to help you discover new books. What are you interested in?",
]

thank_you = ["thanks", "thank you", "appreciate it", "thank"]
thank_you_responses = [
    "You're welcome! Happy reading!",
    "Glad I could help! Enjoy your book!",
    "My pleasure! Let me know if you need more recommendations!",
]

farewell = ["bye", "goodbye", "see you", "farewell"]
farewell_responses = [
    "Goodbye! Come back when you need more book recommendations!",
    "See you later! Happy reading!",
    "Farewell! I hope you find a book you love!",
]

help_requests = ["help", "how does this work", "what can you do", "instructions"]
help_response = """
I can help you find books in several ways:
1. Search for books by author (e.g., "Find books by J.K. Rowling")
2. Search for books by genre (e.g., "Show me fantasy books")
3. Search for books by title (e.g., "Find books with 'Harry Potter' in the title")
4. Get top-rated books (e.g., "Show me the highest rated books")
5. Get popular books (e.g., "What are the most popular books?")
6. Find similar books (e.g., "Find books similar to Harry Potter")
7. Get book details (e.g., "Tell me about The Great Gatsby")
8. Get trending books (e.g., "What's trending now?")
9. Get a random recommendation (e.g., "Suggest a book for me")

You can also just chat with me about books in general!
"""

@main_bp.route("/")
def home():
    # Get trending books for the homepage
    trending_books = get_trending_books(6)
    top_rated = get_top_rated_books(6)
    popular = get_popular_books(6)
    
    return render_template(
        "index.html", 
        trending_books=trending_books,
        top_rated_books=top_rated,
        popular_books=popular
    )

@main_bp.route("/chat", methods=["POST"])
def chat():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
        
    user_message = request.json.get("message", "").lower()
    
    # Check for greetings
    if any(greeting in user_message for greeting in greetings):
        return jsonify({"response": random.choice(greeting_responses)})
    
    # Check for thank you
    elif any(thanks in user_message for thanks in thank_you):
        return jsonify({"response": random.choice(thank_you_responses)})
    
    # Check for farewell
    elif any(bye in user_message for bye in farewell):
        return jsonify({"response": random.choice(farewell_responses)})
    
    # Check for help request
    elif any(help_req in user_message for help_req in help_requests):
        return jsonify({"response": help_response})
    
    # Process message using the recommendations system
    response = process_user_message(user_message)
    return jsonify({"response": response})

@main_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    if not query:
        return jsonify({"books": []})
    
    print(f"Search query: {query}")
    books = search_books(query)
    print(f"Search results: {len(books)} books found")
    return jsonify({"books": books}) 