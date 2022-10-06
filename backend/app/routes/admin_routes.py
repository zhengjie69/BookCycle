from flask import Blueprint
from ..apis.admin_api import *

admin = Blueprint('admin', __name__)

# 'http://localhost:5000/apis/admin/search_user'
admin.route('/search_user', methods=['POST'])(search_user)

# 'http://localhost:5000/apis/admin/delete_user_book'
admin.route('/delete_user_book', methods=['POST'])(delete_user_book)

# 'http://localhost:5000/apis/admin/enable_user_account'
admin.route('/enable_user_account', methods=['POST'])(enable_user_account)

# 'http://localhost:5000/apis/admin/disable_user_account'
admin.route('/disable_user_account', methods=['POST'])(disable_user_account)