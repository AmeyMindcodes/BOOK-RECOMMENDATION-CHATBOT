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
                "1. Search for books by author (e.g., \"Find books by J.K. Rowling\")\n"
                "2. Search for books by genre (e.g., \"Show me fantasy books\")\n"
                "3. Search for books by title (e.g., \"Find books with 'Harry Potter' in the title\")\n"
                "4. Get top-rated books (e.g., \"Show me the highest rated books\")\n"
                "5. Get popular books (e.g., \"What are the most popular books?\")\n"
                "6. Find similar books (e.g., \"Find books similar to Harry Potter\")\n"
                "7. Get book details (e.g., \"Tell me about The Great Gatsby\")\n"
                "8. Get trending books (e.g., \"What's trending now?\")\n"
                "9. Get a random recommendation (e.g., \"Suggest a book for me\")\n\n"
                "You can also just chat with me about books in general!")
    
    # Check for trending books request
    if 'trending' in message or ('what' in message and 'trending' in message):
        books = get_trending_books(5)
        if books:
            response = "Here are some trending books:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
            return response
        return "I couldn't find any trending books at the moment."
    
    # Check for popular books request
    if 'popular' in message and not 'trending' in message:
        books = get_popular_books(5)
        if books:
            response = "Here are some popular books:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
            return response
        return "I couldn't find any popular books at the moment."
    
    # Check for random book request
    if 'random' in message or 'suggest' in message:
        book = get_random_book_recommendation()
        if book:
            return f"How about '{book['title']}' by {book['author']}? It has a rating of {book['rating']}."
        return "I couldn't find a random book recommendation at the moment."
    
    # Check for books by author (specific pattern: "Find books by AUTHOR")
    author_match = re.search(r'(?:find|show|get|display) books? by (.+)', message)
    if author_match:
        author = author_match.group(1).strip()
        books = get_recommendations_by_author(author, 5)
        if books:
            response = f"Here are some books by {author}:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} (Rating: {book['rating']})\n"
            return response
        return f"I couldn't find any books by {author}."
    
    # Check for books with title (specific pattern: "Find books with 'TITLE' in the title")
    title_match = re.search(r'(?:find|show|get|display) books? with [\'"](.+)[\'"] in the title', message)
    if title_match:
        title = title_match.group(1).strip()
        books = search_books(title, 5)
        if books:
            response = f"Here are some books with '{title}' in the title:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
            return response
        return f"I couldn't find any books with '{title}' in the title."
    
    # Check for genre recommendations
    genre_match = re.search(r'(recommend|suggest|find|show) .+ (books?|novels?)', message)
    if genre_match:
        # Extract the genre from the message
        full_match = genre_match.group(0)
        action_words = ['recommend', 'suggest', 'find', 'show', 'me']
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
    
    # Additional pattern for genre recommendations (simpler pattern)
    simple_genre_match = re.search(r'(fantasy|mystery|romance|thriller|horror|science fiction|sci-fi|historical|biography|non-fiction|fiction|adventure|young adult|ya|children|poetry|drama|comedy|action|western|crime|self-help) (books?|novels?)', message)
    if simple_genre_match:
        genre = simple_genre_match.group(1).strip()
        books = get_recommendations_by_genre(genre, 5)
        if books:
            response = f"Here are some {genre} books you might enjoy:\n"
            for i, book in enumerate(books, 1):
                response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
            return response
        return f"I couldn't find any {genre} books at the moment."

    # Even simpler pattern for genre recommendations
    if any(genre in message for genre in ['fantasy', 'mystery', 'romance', 'thriller', 'horror', 'science fiction', 'sci-fi', 'historical', 'biography', 'non-fiction', 'fiction', 'adventure', 'young adult', 'ya', 'children', 'poetry', 'drama', 'comedy', 'action', 'western', 'crime', 'self-help']):
        for genre in ['fantasy', 'mystery', 'romance', 'thriller', 'horror', 'science fiction', 'sci-fi', 'historical', 'biography', 'non-fiction', 'fiction', 'adventure', 'young adult', 'ya', 'children', 'poetry', 'drama', 'comedy', 'action', 'western', 'crime', 'self-help']:
            if genre in message:
                books = get_recommendations_by_genre(genre, 5)
                if books:
                    response = f"Here are some {genre} books you might enjoy:\n"
                    for i, book in enumerate(books, 1):
                        response += f"{i}. {book['title']} by {book['author']} (Rating: {book['rating']})\n"
                    return response
                return f"I couldn't find any {genre} books at the moment."
    
    # Check for author recommendations (alternative pattern)
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
    
    # Even more general search pattern
    if re.search(r'(search|find|look up|get) (.+) books?', message):
        query = re.search(r'(search|find|look up|get) (.+) books?', message).group(2).strip()
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
            "- Suggest a random book\n"
            "- Search for specific books") 