from flask import (
    Blueprint, request, render_template, flash, redirect, url_for, jsonify
)
from flask import session as login_session
from decorators import login_required
from shared import not_authorized
import database as db


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
        db.createCategory(
            name=request.form['name'], user_id=login_session['user_id'])
        flash("New category created!", 'success')
        return redirect(url_for('showCatalog'))
    return render_template('new_category.html')


# EDIT
@app.route('/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def editCategory(category_id):
    """Allows user to edit an existing category"""
    editedCategory = db.findCategory(id=category_id)
    if editedCategory.user_id != login_session['user_id']:
        return not_authorized()
    if request.method == 'POST':
        db.updateCategory(editedCategory, request.form)
        flash(
            'Category Successfully Edited %s' % editedCategory.name, 'success')
        return redirect(url_for('showCatalog'))
    return render_template('edit_category.html', category=editedCategory)


# DELETE
@app.route('/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    """Allows user to delete an existing category"""
    categoryToDelete = db.findCategory(id=category_id)
    if categoryToDelete.user_id != login_session['user_id']:
        return not_authorized()
    if request.method == 'POST':
        db.deleteCategory(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name, 'success')
        return redirect(url_for('showCatalog'))
    return render_template('delete_category.html', category=categoryToDelete)


# READ ALL ITEMS
@app.route('/<int:category_id>')
@app.route('/<int:category_id>/items/')
def showCategoryItems(category_id):
    """Shows items in category"""
    logged = 'username' in login_session
    return render_template(
        'catalog.html', categories=db.getAllCategories(),
        items=db.getAllItems(category_id=category_id), logged=logged,
        category=db.findCategory(id=category_id))


# --------------------------------------
# JSON
# --------------------------------------

@app.route('.json')
def showCategoriesJSON():
    """Returns JSON of all categories in catalog"""
    categories = db.getAllCategories()
    return jsonify(Categories=[r.serialize for r in categories])


@app.route('/<int:category_id>/items.json')
def showCategoryItemsJSON(category_id):
    """Returns JSON of all categories in catalog"""
    items = db.getAllItems(category_id=category_id)
    return jsonify(CategoryItems=[r.serialize for r in items])
