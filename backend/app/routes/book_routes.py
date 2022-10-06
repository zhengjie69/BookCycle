from flask import Blueprint
from ..apis.book_api import *

book = Blueprint('books', __name__)

# 'http://localhost:5000/apis/book/get_all_genres'
book.route('/get_all_genres', methods=['GET'])(get_all_genres)

# 'http://localhost:5000/apis/book/get_all_locations'
book.route('/get_all_locations', methods=['GET'])(get_all_locations)

# 'http://localhost:5000/apis/book/get_all_book_conditions'
book.route('/get_all_book_conditions', methods=['GET'])(get_all_book_conditions)

# 'http://localhost:5000/apis/book/create_book'
book.route('/create_book', methods=['POST'])(create_book)

# 'http://localhost:5000/apis/book/get_all_available_books'
book.route('/get_all_available_books', methods=['GET'])(get_all_available_books)

# 'http://localhost:5000/apis/book/get_all_user_books'
book.route('/get_all_user_books', methods=['GET'])(get_all_user_books)

# 'http://localhost:5000/apis/book/search_book_by_title'
book.route('/search_book_by_title', methods=['GET'])(search_book_by_title)

# 'http://localhost:5000/apis/book/update_book_details'
book.route('/update_book_details', methods=['POST'])(update_book_details)

# 'http://localhost:5000/apis/book/delete_book'
book.route('/delete_book', methods=['POST'])(delete_book)

