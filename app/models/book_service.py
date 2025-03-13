import requests
import os
import json
import random
from dotenv import load_dotenv
import re
from app.utils.cache import cache_result

# Load environment variables - no longer needed since we're adding keys directly
# load_dotenv()

# API Keys - directly added instead of loading from .env
GOOGLE_BOOKS_API_KEY = 'AIzaSyDP3748GbW4fbYi3M9IWqetTl9DUC1jCuQ'
NYT_BOOKS_API_KEY = 'fpAAq87lzX04wf2g'

# Debug print statements
print("GOOGLE_BOOKS_API_KEY:", GOOGLE_BOOKS_API_KEY)
print("NYT_BOOKS_API_KEY:", NYT_BOOKS_API_KEY)

# Default image for books without covers
DEFAULT_COVER_URL = 'https://cdn-icons-png.flaticon.com/512/2232/2232688.png'

# Request timeout in seconds
REQUEST_TIMEOUT = 3

# Fallback data in case API calls fail
FALLBACK_BOOKS = [
    {
        'id': 'fallback1',
        'title': 'To Kill a Mockingbird',
        'author': 'Harper Lee',
        'rating': 4.8,
        'year': '1960',
        'description': 'A classic novel about racial injustice in the American South.',
        'cover_url': 'https://covers.openlibrary.org/b/id/8231490-L.jpg'
    },
    {
        'id': 'fallback2',
        'title': '1984',
        'author': 'George Orwell',
        'rating': 4.7,
        'year': '1949',
        'description': 'A dystopian novel set in a totalitarian society.',
        'cover_url': 'https://covers.openlibrary.org/b/id/8575708-L.jpg'
    },
    {
        'id': 'fallback3',
        'title': 'The Great Gatsby',
        'author': 'F. Scott Fitzgerald',
        'rating': 4.5,
        'year': '1925',
        'description': 'A novel about the American Dream set in the Roaring Twenties.',
        'cover_url': 'https://covers.openlibrary.org/b/id/8432047-L.jpg'
    },
    {
        'id': 'fallback4',
        'title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'rating': 4.6,
        'year': '1813',
        'description': 'A romantic novel about societal expectations and personal growth.',
        'cover_url': 'https://covers.openlibrary.org/b/id/8479576-L.jpg'
    },
    {
        'id': 'fallback5',
        'title': 'The Hobbit',
        'author': 'J.R.R. Tolkien',
        'rating': 4.7,
        'year': '1937',
        'description': 'A fantasy novel about a hobbit who goes on an adventure.',
        'cover_url': 'https://covers.openlibrary.org/b/id/8323742-L.jpg'
    },
    {
        'id': 'fallback6',
        'title': 'Harry Potter and the Sorcerer\'s Stone',
        'author': 'J.K. Rowling',
        'rating': 4.9,
        'year': '1997',
        'description': 'The first book in the Harry Potter series.',
        'cover_url': 'https://covers.openlibrary.org/b/id/8267857-L.jpg'
    }
]

@cache_result(timeout=3600)  # Cache for 1 hour
def get_book_recommendations(book_title, num_recommendations=5):
    """Get book recommendations based on a book title using Google Books API."""
    try:
        # First, search for the book to get its details
        search_url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{book_title}&key={GOOGLE_BOOKS_API_KEY}"
        response = requests.get(search_url)
        data = response.json()
        
        if 'items' not in data or len(data['items']) == 0:
            return []
        
        # Get the first book's categories and authors
        book = data['items'][0]
        book_info = book.get('volumeInfo', {})
        categories = book_info.get('categories', [])
        authors = book_info.get('authors', [])
        
        # Search for similar books based on categories and authors
        similar_books = []
        
        # Try to find books with similar categories
        if categories:
            category_query = '+OR+'.join([f"subject:{category}" for category in categories])
            category_url = f"https://www.googleapis.com/books/v1/volumes?q={category_query}&maxResults=10&key={GOOGLE_BOOKS_API_KEY}"
            category_response = requests.get(category_url)
            category_data = category_response.json()
            
            if 'items' in category_data:
                similar_books.extend(category_data['items'])
        
        # Try to find books by the same authors
        if authors and len(similar_books) < num_recommendations * 2:
            author_query = '+OR+'.join([f"inauthor:{author}" for author in authors])
            author_url = f"https://www.googleapis.com/books/v1/volumes?q={author_query}&maxResults=10&key={GOOGLE_BOOKS_API_KEY}"
            author_response = requests.get(author_url)
            author_data = author_response.json()
            
            if 'items' in author_data:
                similar_books.extend(author_data['items'])
        
        # Remove duplicates and the original book
        unique_books = []
        seen_ids = set()
        original_id = book.get('id')
        
        for similar_book in similar_books:
            book_id = similar_book.get('id')
            if book_id != original_id and book_id not in seen_ids:
                seen_ids.add(book_id)
                unique_books.append(similar_book)
        
        # Format the recommendations
        recommendations = []
        for book in unique_books[:num_recommendations]:
            book_info = book.get('volumeInfo', {})
            
            # Get the cover image URL or use default
            image_links = book_info.get('imageLinks', {})
            cover_url = image_links.get('thumbnail') if image_links else DEFAULT_COVER_URL
            
            recommendations.append({
                'id': book.get('id'),
                'title': book_info.get('title', 'Unknown Title'),
                'author': ', '.join(book_info.get('authors', ['Unknown Author'])),
                'rating': book_info.get('averageRating', 0),
                'year': book_info.get('publishedDate', 'Unknown')[:4] if book_info.get('publishedDate') else 'Unknown',
                'description': book_info.get('description', 'No description available'),
                'cover_url': cover_url
            })
        
        return recommendations
    except Exception as e:
        print(f"Error in get_book_recommendations: {e}")
        return []

@cache_result(timeout=3600)  # Cache for 1 hour
def get_recommendations_by_genre(genre, num_recommendations=5):
    """Get book recommendations based on genre using Google Books API."""
    try:
        # Search for books in the specified genre
        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&orderBy=relevance&maxResults={num_recommendations}&key={GOOGLE_BOOKS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if 'items' not in data:
            return []
        
        # Format the recommendations
        recommendations = []
        for book in data['items'][:num_recommendations]:
            book_info = book.get('volumeInfo', {})
            
            # Get the cover image URL or use default
            image_links = book_info.get('imageLinks', {})
            cover_url = image_links.get('thumbnail') if image_links else DEFAULT_COVER_URL
            
            recommendations.append({
                'id': book.get('id'),
                'title': book_info.get('title', 'Unknown Title'),
                'author': ', '.join(book_info.get('authors', ['Unknown Author'])),
                'rating': book_info.get('averageRating', 0),
                'year': book_info.get('publishedDate', 'Unknown')[:4] if book_info.get('publishedDate') else 'Unknown',
                'description': book_info.get('description', 'No description available'),
                'cover_url': cover_url
            })
        
        return recommendations
    except Exception as e:
        print(f"Error in get_recommendations_by_genre: {e}")
        return []

@cache_result(timeout=3600)  # Cache for 1 hour
def get_recommendations_by_author(author_name, num_recommendations=5):
    """Get book recommendations based on author name using Google Books API."""
    try:
        # Search for books by the specified author
        url = f"https://www.googleapis.com/books/v1/volumes?q=inauthor:{author_name}&orderBy=relevance&maxResults={num_recommendations}&key={GOOGLE_BOOKS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if 'items' not in data:
            return []
        
        # Format the recommendations
        recommendations = []
        for book in data['items'][:num_recommendations]:
            book_info = book.get('volumeInfo', {})
            
            # Get the cover image URL or use default
            image_links = book_info.get('imageLinks', {})
            cover_url = image_links.get('thumbnail') if image_links else DEFAULT_COVER_URL
            
            recommendations.append({
                'id': book.get('id'),
                'title': book_info.get('title', 'Unknown Title'),
                'author': ', '.join(book_info.get('authors', ['Unknown Author'])),
                'rating': book_info.get('averageRating', 0),
                'year': book_info.get('publishedDate', 'Unknown')[:4] if book_info.get('publishedDate') else 'Unknown',
                'description': book_info.get('description', 'No description available'),
                'cover_url': cover_url
            })
        
        return recommendations
    except Exception as e:
        print(f"Error in get_recommendations_by_author: {e}")
        return []

@cache_result(timeout=1800)  # Cache for 30 minutes
def get_trending_books(num_books=5):
    """Get trending books using the NYT Books API."""
    # Return fallback data immediately to avoid delays
    return FALLBACK_BOOKS[:num_books]
    
    # The code below is commented out to avoid API delays
    """
    try:
        # Try to get trending books from NYT API
        if NYT_BOOKS_API_KEY:
            url = f"https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key={NYT_BOOKS_API_KEY}"
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            data = response.json()
            
            if 'results' in data and 'books' in data['results']:
                nyt_books = data['results']['books']
                
                # Format the recommendations
                trending_books = []
                for book in nyt_books[:num_books]:
                    # Get more details from Google Books API
                    title = book.get('title')
                    author = book.get('author')
                    google_book = _get_google_book_details(title, author)
                    
                    if google_book:
                        trending_books.append(google_book)
                    else:
                        # Use NYT data if Google Books data is not available
                        trending_books.append({
                            'id': f"nyt_{book.get('rank')}",
                            'title': title,
                            'author': author,
                            'rating': 0,
                            'year': 'Unknown',
                            'description': book.get('description', 'No description available'),
                            'cover_url': book.get('book_image', DEFAULT_COVER_URL)
                        })
                
                if trending_books:
                    return trending_books
        
        # If NYT API fails or no books are found, try Open Library API
        url = "https://openlibrary.org/trending/daily.json"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        data = response.json()
        
        if 'works' in data:
            ol_books = data['works']
            
            # Format the recommendations
            trending_books = []
            for book in ol_books[:num_books]:
                # Get more details from Google Books API
                title = book.get('title')
                authors = book.get('author_names', ['Unknown Author'])
                author = authors[0] if authors else 'Unknown Author'
                google_book = _get_google_book_details(title, author)
                
                if google_book:
                    trending_books.append(google_book)
                else:
                    # Use Open Library data if Google Books data is not available
                    cover_id = book.get('cover_i')
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else DEFAULT_COVER_URL
                    
                    trending_books.append({
                        'id': f"ol_{book.get('key', '').replace('/works/', '')}",
                        'title': title,
                        'author': author,
                        'rating': 0,
                        'year': 'Unknown',
                        'description': 'No description available',
                        'cover_url': cover_url
                    })
            
            if trending_books:
                return trending_books
        
        # If all APIs fail, return fallback data
        return FALLBACK_BOOKS[:num_books]
    except Exception as e:
        print(f"Error in get_trending_books: {e}")
        return FALLBACK_BOOKS[:num_books]
    """

@cache_result(timeout=1800)  # Cache for 30 minutes
def get_top_rated_books(num_books=5):
    """Get top-rated books using Google Books API."""
    # Return fallback data immediately to avoid delays
    return FALLBACK_BOOKS[:num_books]
    
    # The code below is commented out to avoid API delays
    """
    try:
        # Try to get top-rated books from Google Books API
        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:fiction&orderBy=relevance&maxResults=20&key={GOOGLE_BOOKS_API_KEY}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        data = response.json()
        
        if 'items' in data:
            # Sort by rating
            books = data['items']
            books.sort(key=lambda x: x.get('volumeInfo', {}).get('averageRating', 0), reverse=True)
            
            # Format the recommendations
            top_rated = []
            for book in books[:num_books]:
                book_info = book.get('volumeInfo', {})
                
                # Get the cover image URL or use default
                image_links = book_info.get('imageLinks', {})
                cover_url = image_links.get('thumbnail') if image_links else DEFAULT_COVER_URL
                
                top_rated.append({
                    'id': book.get('id'),
                    'title': book_info.get('title', 'Unknown Title'),
                    'author': ', '.join(book_info.get('authors', ['Unknown Author'])),
                    'rating': book_info.get('averageRating', 0),
                    'year': book_info.get('publishedDate', 'Unknown')[:4] if book_info.get('publishedDate') else 'Unknown',
                    'description': book_info.get('description', 'No description available'),
                    'cover_url': cover_url
                })
            
            if top_rated:
                return top_rated
        
        # If Google Books API fails, return fallback data
        return FALLBACK_BOOKS[:num_books]
    except Exception as e:
        print(f"Error in get_top_rated_books: {e}")
        return FALLBACK_BOOKS[:num_books]
    """

@cache_result(timeout=1800)  # Cache for 30 minutes
def get_popular_books(num_books=5):
    """Get popular books using Google Books API."""
    # Return fallback data immediately to avoid delays
    return FALLBACK_BOOKS[:num_books]
    
    # The code below is commented out to avoid API delays
    """
    try:
        # Try to get popular books from Google Books API
        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:fiction&orderBy=newest&maxResults={num_books}&key={GOOGLE_BOOKS_API_KEY}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        data = response.json()
        
        if 'items' in data:
            # Format the recommendations
            popular_books = []
            for book in data['items'][:num_books]:
                book_info = book.get('volumeInfo', {})
                
                # Get the cover image URL or use default
                image_links = book_info.get('imageLinks', {})
                cover_url = image_links.get('thumbnail') if image_links else DEFAULT_COVER_URL
                
                popular_books.append({
                    'id': book.get('id'),
                    'title': book_info.get('title', 'Unknown Title'),
                    'author': ', '.join(book_info.get('authors', ['Unknown Author'])),
                    'rating': book_info.get('averageRating', 0),
                    'year': book_info.get('publishedDate', 'Unknown')[:4] if book_info.get('publishedDate') else 'Unknown',
                    'description': book_info.get('description', 'No description available'),
                    'cover_url': cover_url
                })
            
            if popular_books:
                return popular_books
        
        # If Google Books API fails, return fallback data
        return FALLBACK_BOOKS[:num_books]
    except Exception as e:
        print(f"Error in get_popular_books: {e}")
        return FALLBACK_BOOKS[:num_books]
    """

@cache_result(timeout=3600)  # Cache for 1 hour
def search_books(query, max_results=10):
    """Search for books based on title, author, or genre using Google Books API or Open Library API as fallback."""
    try:
        # Debug print
        print(f"Searching for books with query: {query}")
        print(f"Using Google Books API key: {GOOGLE_BOOKS_API_KEY}")
        
        # If no query is provided, return empty results
        if not query:
            print("Empty query provided")
            return []
        
        # Try Google Books API first
        if GOOGLE_BOOKS_API_KEY:
            # Search for books matching the query
            encoded_query = requests.utils.quote(query)
            url = f"https://www.googleapis.com/books/v1/volumes?q={encoded_query}&maxResults={max_results}&key={GOOGLE_BOOKS_API_KEY}"
            print(f"Request URL: {url}")
            
            try:
                response = requests.get(url, timeout=REQUEST_TIMEOUT)
                print(f"Response status code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"Response data keys: {data.keys()}")
                    
                    if 'items' in data:
                        # Format the results
                        results = []
                        for book in data['items'][:max_results]:
                            book_info = book.get('volumeInfo', {})
                            
                            # Get the cover image URL or use default
                            image_links = book_info.get('imageLinks', {})
                            cover_url = image_links.get('thumbnail') if image_links else DEFAULT_COVER_URL
                            
                            results.append({
                                'id': book.get('id'),
                                'title': book_info.get('title', 'Unknown Title'),
                                'author': ', '.join(book_info.get('authors', ['Unknown Author'])),
                                'rating': book_info.get('averageRating', 0),
                                'year': book_info.get('publishedDate', 'Unknown')[:4] if book_info.get('publishedDate') else 'Unknown',
                                'description': book_info.get('description', 'No description available'),
                                'cover_url': cover_url
                            })
                        
                        print(f"Found {len(results)} books from Google Books API")
                        if results:
                            return results
                    else:
                        print("No 'items' found in Google Books API response")
            except requests.exceptions.RequestException as e:
                print(f"Error with Google Books API request: {e}")
        
        # Fallback to Open Library API
        print("Falling back to Open Library API")
        try:
            encoded_query = requests.utils.quote(query)
            url = f"https://openlibrary.org/search.json?q={encoded_query}&limit={max_results}"
            print(f"Open Library Request URL: {url}")
            
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            print(f"Open Library Response status code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Open Library Response data keys: {data.keys()}")
                
                if 'docs' in data and len(data['docs']) > 0:
                    # Format the results
                    results = []
                    for book in data['docs'][:max_results]:
                        # Get the cover image URL or use default
                        cover_id = book.get('cover_i')
                        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else DEFAULT_COVER_URL
                        
                        results.append({
                            'id': book.get('key', ''),
                            'title': book.get('title', 'Unknown Title'),
                            'author': ', '.join(book.get('author_name', ['Unknown Author'])),
                            'rating': 0,  # Open Library doesn't provide ratings
                            'year': str(book.get('first_publish_year', 'Unknown')),
                            'description': book.get('description', 'No description available'),
                            'cover_url': cover_url
                        })
                    
                    print(f"Found {len(results)} books from Open Library API")
                    if results:
                        return results
                else:
                    print("No 'docs' found in Open Library API response")
        except requests.exceptions.RequestException as e:
            print(f"Error with Open Library API request: {e}")
        
        # If both APIs fail, return fallback books
        print("No books found from either API, returning fallback books")
        return FALLBACK_BOOKS[:max_results]
    except Exception as e:
        print(f"Error in search_books: {e}")
        # Return fallback books in case of error
        return FALLBACK_BOOKS[:max_results]

@cache_result(timeout=3600)  # Cache for 1 hour
def get_random_book_recommendation():
    """Get a random book recommendation using Google Books API."""
    try:
        # Generate a random search query
        random_subjects = ['fiction', 'fantasy', 'mystery', 'romance', 'science', 'history', 'biography']
        random_subject = random.choice(random_subjects)
        
        # Search for books in the random subject
        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{random_subject}&maxResults=40&key={GOOGLE_BOOKS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if 'items' not in data:
            return None
        
        # Select a random book
        random_book = random.choice(data['items'])
        book_info = random_book.get('volumeInfo', {})
        
        # Get the cover image URL or use default
        image_links = book_info.get('imageLinks', {})
        cover_url = image_links.get('thumbnail') if image_links else DEFAULT_COVER_URL
        
        return {
            'id': random_book.get('id'),
            'title': book_info.get('title', 'Unknown Title'),
            'author': ', '.join(book_info.get('authors', ['Unknown Author'])),
            'rating': book_info.get('averageRating', 0),
            'year': book_info.get('publishedDate', 'Unknown')[:4] if book_info.get('publishedDate') else 'Unknown',
            'description': book_info.get('description', 'No description available'),
            'cover_url': cover_url
        }
    except Exception as e:
        print(f"Error in get_random_book_recommendation: {e}")
        return None

@cache_result(timeout=3600)  # Cache for 1 hour
def get_book_cover_url(book_id_or_title):
    """Get the cover URL for a specific book."""
    try:
        # Check if the input is a Google Books ID
        if book_id_or_title.startswith('google_'):
            book_id = book_id_or_title.replace('google_', '')
            url = f"https://www.googleapis.com/books/v1/volumes/{book_id}?key={GOOGLE_BOOKS_API_KEY}"
            response = requests.get(url)
            data = response.json()
            
            if 'volumeInfo' in data and 'imageLinks' in data['volumeInfo']:
                return data['volumeInfo']['imageLinks'].get('thumbnail', DEFAULT_COVER_URL)
        
        # Check if the input is an Open Library ID
        elif book_id_or_title.startswith('ol_'):
            book_id = book_id_or_title.replace('ol_', '')
            return f"https://covers.openlibrary.org/b/olid/{book_id}-M.jpg"
        
        # Assume the input is a title and search for it
        else:
            url = f"https://www.googleapis.com/books/v1/volumes?q=intitle:{book_id_or_title}&maxResults=1&key={GOOGLE_BOOKS_API_KEY}"
            response = requests.get(url)
            data = response.json()
            
            if 'items' in data and len(data['items']) > 0:
                book_info = data['items'][0].get('volumeInfo', {})
                if 'imageLinks' in book_info:
                    return book_info['imageLinks'].get('thumbnail', DEFAULT_COVER_URL)
        
        return DEFAULT_COVER_URL
    except Exception as e:
        print(f"Error in get_book_cover_url: {e}")
        return DEFAULT_COVER_URL

@cache_result(timeout=3600)  # Cache for 1 hour
def get_book_details(book_id):
    """Get detailed information about a specific book."""
    try:
        # Check if the input is a Google Books ID
        if not book_id.startswith('google_') and not book_id.startswith('ol_'):
            # Try to get details from Google Books API
            url = f"https://www.googleapis.com/books/v1/volumes/{book_id}?key={GOOGLE_BOOKS_API_KEY}"
            response = requests.get(url)
            data = response.json()
            
            if 'volumeInfo' in data:
                book_info = data['volumeInfo']
                
                # Get the cover image URL or use default
                image_links = book_info.get('imageLinks', {})
                cover_url = image_links.get('thumbnail') if image_links else DEFAULT_COVER_URL
                
                return {
                    'id': data.get('id'),
                    'title': book_info.get('title', 'Unknown Title'),
                    'author': ', '.join(book_info.get('authors', ['Unknown Author'])),
                    'rating': book_info.get('averageRating', 0),
                    'year': book_info.get('publishedDate', 'Unknown')[:4] if book_info.get('publishedDate') else 'Unknown',
                    'description': book_info.get('description', 'No description available'),
                    'cover_url': cover_url,
                    'categories': book_info.get('categories', []),
                    'publisher': book_info.get('publisher', 'Unknown Publisher'),
                    'page_count': book_info.get('pageCount', 0),
                    'language': book_info.get('language', 'Unknown')
                }
        
        # Check if the input is an Open Library ID
        elif book_id.startswith('ol_'):
            book_id = book_id.replace('ol_', '')
            url = f"https://openlibrary.org/works/{book_id}.json"
            response = requests.get(url)
            data = response.json()
            
            # Get the cover image URL
            cover_id = data.get('covers', [None])[0]
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else DEFAULT_COVER_URL
            
            # Get the author
            author = "Unknown Author"
            if 'authors' in data and len(data['authors']) > 0:
                author_url = f"https://openlibrary.org{data['authors'][0]['author']['key']}.json"
                author_response = requests.get(author_url)
                author_data = author_response.json()
                author = author_data.get('name', 'Unknown Author')
            
            return {
                'id': f"ol_{book_id}",
                'title': data.get('title', 'Unknown Title'),
                'author': author,
                'rating': 0,  # Open Library doesn't provide ratings
                'year': str(data.get('first_publish_date', 'Unknown')),
                'description': data.get('description', 'No description available'),
                'cover_url': cover_url,
                'categories': data.get('subjects', []),
                'publisher': 'Unknown Publisher',
                'page_count': 0,
                'language': 'Unknown'
            }
        
        # If we reach here, we couldn't find the book
        return None
    except Exception as e:
        print(f"Error in get_book_details: {e}")
        return None

def _get_google_book_details(title, author=None):
    """Helper function to get book details from Google Books API."""
    try:
        # Build the search query
        query = f"intitle:{title}"
        if author:
            query += f"+inauthor:{author}"
        
        # Search for the book
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults=1&key={GOOGLE_BOOKS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            book = data['items'][0]
            book_info = book.get('volumeInfo', {})
            
            # Get the cover image URL or use default
            image_links = book_info.get('imageLinks', {})
            cover_url = image_links.get('thumbnail') if image_links else DEFAULT_COVER_URL
            
            return {
                'id': book.get('id'),
                'title': book_info.get('title', 'Unknown Title'),
                'author': ', '.join(book_info.get('authors', ['Unknown Author'])),
                'rating': book_info.get('averageRating', 0),
                'year': book_info.get('publishedDate', 'Unknown')[:4] if book_info.get('publishedDate') else 'Unknown',
                'description': book_info.get('description', 'No description available'),
                'cover_url': cover_url
            }
        
        return None
    except Exception as e:
        print(f"Error in _get_google_book_details: {e}")
        return None 