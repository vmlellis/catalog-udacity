from functools import wraps
from flask import session as login_session
from flask import redirect, url_for

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in login_session:
            return redirect(url_for('auth.showLogin'))
        return f(*args, **kwargs)
    return decorated_function
