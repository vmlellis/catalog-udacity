from flask import Flask, render_template
from flask import session as login_session
from auth import app as auth
from categories import app as categories
from database import session, Category, CategoryItem


app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(categories, url_prefix='/categories')


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in login_session:
            return redirect(url_for('showLogin'))
        return f(*args, **kwargs)
    return decorated_function


# READ - home page, show latest items and categories
@app.route("/")
@app.route('/catalog/')
def showCatalog():
    """Returns catalog page with all categories and recently added items"""
    categories = session.query(Category).all()
    items = session.query(
        CategoryItem).order_by(CategoryItem.id.desc()).limit(10)
    logged = 'username' in login_session
    return render_template('catalog.html',
        categories=categories, items=items, logged=logged)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    # app.run(host = '0.0.0.0', port = 5000, ssl_context='adhoc')
    app.run(host = '0.0.0.0', port = 5000)
