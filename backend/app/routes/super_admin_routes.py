from flask import Blueprint
from ..apis.super_admin_api import *

superadmin = Blueprint('superadmin', __name__)

# 'http://localhost:5000/apis/superadmin/search_admin'
superadmin.route('/search_admin', methods=['POST'])(search_admin)

# 'http://localhost:5000/apis/superadmin/create_admin_account'
superadmin.route('/create_admin_account', methods=['POST'])(create_admin_account)

# 'http://localhost:5000/apis/superadmin/delete_admin_account'
superadmin.route('/delete_admin_account', methods=['POST'])(delete_admin_account)

# 'http://localhost:5000/apis/superadmin/disable_admin_account'
superadmin.route('/disable_admin_account', methods=['POST'])(disable_admin_account)