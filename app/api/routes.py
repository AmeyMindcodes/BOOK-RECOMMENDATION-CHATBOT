from flask import Blueprint, jsonify, request
from app.models.book_service import (
    get_book_recommendations,
    get_recommendations_by_genre,
    get_recommendations_by_author,
    get_trending_books,
    get_top_rated_books,
    get_popular_books,
    search_books,
    get_random_book_recommendation,
    get_book_details,
    get_book_cover_url
)
from app.models.chatbot import process_user_message

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/recommendations/similar', methods=['GET'])
def similar_books():
    book_title = request.args.get('title')
    if not book_title:
        return jsonify({'error': 'Book title is required'}), 400
    recommendations = get_book_recommendations(book_title)
    return jsonify(recommendations)

@api_bp.route('/recommendations/genre', methods=['GET'])
def genre_recommendations():
    genre = request.args.get('genre')
    if not genre:
        return jsonify({'error': 'Genre is required'}), 400
    recommendations = get_recommendations_by_genre(genre)
    return jsonify(recommendations)

@api_bp.route('/recommendations/author', methods=['GET'])
def author_recommendations():
    author = request.args.get('author')
    if not author:
        return jsonify({'error': 'Author name is required'}), 400
    recommendations = get_recommendations_by_author(author)
    return jsonify(recommendations)

@api_bp.route('/books/trending', methods=['GET'])
def get_trending():
    limit = request.args.get('limit', 5, type=int)
    books = get_trending_books(limit)
    return jsonify(books)

@api_bp.route('/books/top-rated', methods=['GET'])
def get_top_rated():
    limit = request.args.get('limit', 5, type=int)
    books = get_top_rated_books(limit)
    return jsonify(books)

@api_bp.route('/books/popular', methods=['GET'])
def get_popular():
    limit = request.args.get('limit', 5, type=int)
    books = get_popular_books(limit)
    return jsonify(books)

@api_bp.route('/books/search', methods=['GET'])
def search_book():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Search query is required'}), 400
    results = search_books(query)
    return jsonify(results)

@api_bp.route('/books/random', methods=['GET'])
def random_book():
    book = get_random_book_recommendation()
    if book:
        return jsonify(book)
    return jsonify({'error': 'Could not find a random book'}), 404

@api_bp.route('/books/<book_id>', methods=['GET'])
def book_details(book_id):
    # Check if this is a fallback book ID
    if book_id.startswith('fallback'):
        try:
            # Extract the index from the fallback ID (e.g., fallback1 -> 0)
            index = int(book_id.replace('fallback', '')) - 1
            from app.models.book_service import FALLBACK_BOOKS
            
            if 0 <= index < len(FALLBACK_BOOKS):
                return jsonify(FALLBACK_BOOKS[index])
            else:
                return jsonify({'error': 'Invalid fallback book ID'}), 404
        except (ValueError, IndexError) as e:
            print(f"Error processing fallback book ID: {e}")
            return jsonify({'error': 'Invalid fallback book ID'}), 404
    
    # If not a fallback book, proceed with normal lookup
    try:
        details = get_book_details(book_id)
        if details:
            return jsonify(details)
        return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        print(f"Error in book_details endpoint: {e}")
        return jsonify({'error': f'Error retrieving book details: {str(e)}'}), 500

@api_bp.route('/book-cover/<title>', methods=['GET'])
def book_cover(title):
    cover_url = get_book_cover_url(title)
    if cover_url:
        return jsonify({"url": cover_url})
    return jsonify({'error': 'Cover not found'}), 404

@api_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    response = process_user_message(data['message'])
    return jsonify({'response': response}) 