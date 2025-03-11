import re
import random
from app.models.book_service import (
    get_book_recommendations,
    get_recommendations_by_genre,
    get_recommendations_by_author,
    get_trending_books,
    get_top_rated_books,
    get_popular_books,
    search_books,
    get_random_book_recommendation,
    get_book_details
)

def process_user_message(message):
    """Process user message and return appropriate response."""
    message = message.lower()
    
    # Check for greetings
    if any(greeting in message for greeting in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm your book recommendation assistant. How can I help you today?"
    
    # Check for gratitude
    if any(thanks in message for thanks in ['thank', 'thanks', 'appreciate']):
        return "You're welcome! Let me know if you need more book recommendations!"
    
    # Check for farewell
    if any(bye in message for bye in ['bye', 'goodbye', 'see you']):
        return "Goodbye! Happy reading!"
    
    # Check for help request
    if 'help' in message:
        return ("I can help you find books in several ways:\n"
                "1. Recommend similar books to one you like\n"
                "2. Find books by genre\n"
                "3. Find books by author\n"
                "4. Show trending books\n"
                "5. Suggest a random book\n"
                "Just let me know what you're interested in!")
    
    # Check for trending books request
    if 'trending' in message or 'popular' in message:
        books = get_trending_books(5)
        if books:
            response = "Here are some trending books:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
            return response
        return "I couldn't find any trending books at the moment."
    
    # Check for random book request
    if 'random' in message:
        book = get_random_book_recommendation()
        if book:
            return f"How about '{book['title']}' by {book['author']}? It has a rating of {book['rating']}."
        return "I couldn't find a random book recommendation at the moment."
    
    # Check for genre recommendations
    genre_match = re.search(r'(recommend|suggest|find|show) .+ (books?|novels?)', message)
    if genre_match:
        # Extract the genre from the message
        full_match = genre_match.group(0)
        action_words = ['recommend', 'suggest', 'find', 'show']
        for word in action_words:
            full_match = full_match.replace(word, '')
        genre = full_match.replace('books', '').replace('book', '').replace('novels', '').replace('novel', '').strip()
        
        books = get_recommendations_by_genre(genre, 5)
        if books:
            response = f"Here are some {genre} books you might enjoy:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
            return response
        return f"I couldn't find any {genre} books at the moment."
    
    # Check for author recommendations
    author_match = re.search(r'(books?|novels?) (by|from) (.+)', message)
    if author_match:
        author = author_match.group(3).strip()
        books = get_recommendations_by_author(author, 5)
        if books:
            response = f"Here are some books by {author}:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} (Rating: {book['rating']})\n"
            return response
        return f"I couldn't find any books by {author}."
    
    # Check for similar book recommendations
    similar_match = re.search(r'(similar to|like) (.+)', message)
    if similar_match:
        book_title = similar_match.group(2).strip()
        books = get_book_recommendations(book_title, 5)
        if books:
            response = f"If you liked '{book_title}', you might also enjoy:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
            return response
        return f"I couldn't find any books similar to '{book_title}'."
    
    # Check for top rated books request
    if re.search(r'(top|best|highest) rated', message):
        books = get_top_rated_books(5)
        if books:
            response = "Here are some top-rated books:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
            return response
        return "I couldn't find any top-rated books at the moment."
    
    # General search for books
    if re.search(r'(search|find|look) for (.+)', message):
        query = re.search(r'(search|find|look) for (.+)', message).group(2).strip()
        books = search_books(query, 5)
        if books:
            response = f"Here are some books matching '{query}':\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
            return response
        return f"I couldn't find any books matching '{query}'."
    
    # Default response
    return ("I'm not sure what you're looking for. You can ask me to:\n"
            "- Recommend books similar to a specific book\n"
            "- Find books in a particular genre\n"
            "- Show books by a specific author\n"
            "- Show trending books\n"
            "- Suggest a random book") 