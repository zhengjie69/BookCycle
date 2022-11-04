from flask import Blueprint
from ..apis.user_api import *

user = Blueprint('users', __name__)


# commented routes are for admin use only

# 'http://localhost:5000/apis/user/create_user'
user.route('/create_user', methods=['POST'])(create_User)

# 'http://localhost:5000/apis/user/login'
user.route('/login', methods=['POST'])(login)

# 'http://localhost:5000/apis/user/logout'
user.route('/logout', methods=['POST'])(logout)

# 'http://localhost:5000/apis/user/get_user_profile'
user.route('/get_user_profile', methods=['GET'])(get_user_profile)

# 'http://localhost:5000/apis/user/update_password'
user.route('/update_password', methods=['POST'])(update_password)


# 'http://localhost:5000/apis/user/update_profile'
user.route('/update_profile', methods=['POST'])(update_profile)

# 'http://localhost:5000/apis/user/send_book_offer'
user.route('/send_book_offer', methods=['POST'])(send_book_offer)

# 'http://localhost:5000/apis/user/get_book_offers'
user.route('/get_book_offers', methods=['GET'])(get_book_offers)

# 'http://localhost:5000/apis/user/get_all_user_book_offers'
user.route('/get_all_user_book_offers', methods=['GET'])(get_all_user_book_offers)

# 'http://localhost:5000/apis/user/accept_book_offer'
user.route('/accept_book_offer', methods=['POST'])(accept_book_offer)

# 'http://localhost:5000/apis/user/edit_book_offer'
user.route('/edit_book_offer', methods=['POST'])(edit_book_offer)

# 'http://localhost:5000/apis/user/delete_book_offer'
user.route('/delete_book_offer', methods=['POST'])(delete_book_offer)

# 'http://localhost:5000/apis/user/get_transaction_details'
user.route('/get_transaction_details', methods=['GET'])(get_transaction_details)

# 'http://localhost:5000/apis/user/get_all_user_transactions'
user.route('/get_all_user_transactions', methods=['GET'])(get_all_user_transactions)

# 'http://localhost:5000/apis/user/forget_password_reset'
user.route('/forget_password_reset',methods=['GET','POST'])(forget_password_reset)

# 'http://localhost:5000/apis/user/forget_password_reset'
user.route('/ForgetResetPassword/<token>',methods=['GET','POST'])(verify_reset_password)

# 'http://localhost:5000/apis/user/forget_password_reset_captcha'
user.route('/forget_password_reset_captcha',methods=['GET','POST'])(verify_captcha)