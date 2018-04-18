from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import session as login_session
from decorators import login_required
from database import session, Category, CategoryItem


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
    return render_template('edit_category.html')


# DELETE
@app.route('/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteCategory(category_id):
    """Allows user to delete an existing category"""
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if categoryToDelete.user_id != login_session['user_id']:
        return not_authorized()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name, 'success')
        session.commit()
        return redirect(url_for('showCatalog', category_id=category_id))
    else:
        return render_template('delete_category.html', category=categoryToDelete)


# --------------------------------------
# CRUD - Category Items
# --------------------------------------

# READ ALL
@app.route('/<int:category_id>')
@app.route('/<int:category_id>/items/')
def showCategoryItems(category_id):
    """Shows items in category"""
    return render_template('category_items.html')


# READ ONE
@app.route('/<int:category_id>/item/<int:category_item_id>/')
def showCategoryItem(category_id, category_item_id):
    """Shows a category item"""
    return render_template('category_item.html')


# CREATE
@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def newCategoryItem():
    """Allow user to  create new catalog item"""
    return render_template('new_category_item.html')


# UPDATE
@app.route(
    '/<int:category_id>/item/<int:category_item_id>/edit',
    methods=['GET', 'POST'])
@login_required
def editCategoryItem(category_id, category_item_id):
    """Allows user to edit an existing category item"""
    return render_template('edit_catalog_item.html')


# DELETE

def not_authorized():
    return "<script>function myFunction() {alert('You are not authorized!')}</script><body onload='myFunction()'>"

