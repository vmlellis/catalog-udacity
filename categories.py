from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from flask import session as login_session
from decorators import login_required
from database import session, Category, CategoryItem, User
from shared import not_authorized


app = Blueprint('categories', __name__, template_folder='templates')


# --------------------------------------
# CRUD - Categories
# --------------------------------------

# CREATE
@app.route('/new', methods=['GET', 'POST'])
@login_required
def newCategory():
    """Allows user to create new category"""
    if request.method == 'POST':
        return createCategory()
    return render_template('new_category.html')


def createCategory():
    """Creates new category"""
    newCategory = Category(
        name=request.form['name'], user_id=login_session['user_id'])
    session.add(newCategory)
    session.commit()
    flash("New category created!", 'success')
    return redirect(url_for('showCatalog'))


# EDIT
@app.route('/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    """Allows user to edit an existing category"""
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        return not_authorized()
    if request.method == 'POST':
        return updateCategory(editedCategory)
    return render_template('edit_category.html', category=editedCategory)

def updateCategory(editedCategory):
    if request.form['name']:
        editedCategory.name = request.form['name']
    flash('Category Successfully Edited %s' % editedCategory.name,
        'success')
    return redirect(url_for('showCatalog'))


# DELETE
@app.route('/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    """Allows user to delete an existing category"""
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if categoryToDelete.user_id != login_session['user_id']:
        return not_authorized()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name, 'success')
        session.commit()
        return redirect(url_for('showCatalog'))
    return render_template('delete_category.html', category=categoryToDelete)


# READ ALL ITEMS
@app.route('/<int:category_id>')
@app.route('/<int:category_id>/items/')
def showCategoryItems(category_id):
    """Shows items in category"""
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by(
            category_id=category_id).order_by(CategoryItem.id.desc()).all()
    categories = session.query(Category).all()
    logged = 'username' in login_session
    return render_template('catalog.html',
        categories=categories, items=items, logged=logged, category=category)

# --------------------------------------
# JSON
# --------------------------------------
@app.route('.json')
def showCategoriesJSON():
    """Returns JSON of all categories in catalog"""
    categories = session.query(Category).all()
    return jsonify(Categories=[r.serialize for r in categories])


@app.route('/<int:category_id>/items.json')
def showCategoryItemsJSON(category_id):
    """Returns JSON of all categories in catalog"""
    items = session.query(CategoryItem).filter_by(category_id=category_id).all()
    return jsonify(CategoryItems=[r.serialize for r in items])
