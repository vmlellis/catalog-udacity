from flask import Flask, render_template, jsonify
from flask import session as login_session
from auth import app as auth
from categories import app as categories
from items import app as items
from database import session, Category, CategoryItem


app = Flask(__name__)
app.register_blueprint(auth)
app.register_blueprint(categories, url_prefix='/categories')
app.register_blueprint(items, url_prefix='/items')


# READ - home page, show latest items and categories
@app.route("/")
@app.route('/catalog/')
def showCatalog():
    """Returns catalog page with all categories and recently added items"""
    categories = session.query(Category).all()
    items = session.query(
        CategoryItem).order_by(CategoryItem.id.desc()).limit(10).all()
    logged = 'username' in login_session
    return render_template(
        'catalog.html', categories=categories, items=items, logged=logged)


# JSON - all categories with all items
@app.route('/catalog.json')
def showCatalogJSON():
    """Returns JSON of all categories with items in catalog"""
    catalog = []
    categories = session.query(Category).all()
    for category in categories:
        data = category.serialize
        data['Items'] = session.query(CategoryItem).filter_by(
            category_id=category.id).all()
        catalog.append(data)
    return jsonify(Categories=catalog)


# JSON - all categories items
@app.route('/category_items.json')
def showCatalogItemsJSON():
    """Returns JSON of all items in catalog"""
    items = session.query(CategoryItem).order_by(CategoryItem.id.desc())
    return jsonify(CategoryItems=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    # app.run(host = '0.0.0.0', port = 5000, ssl_context='adhoc') # To Facebook
