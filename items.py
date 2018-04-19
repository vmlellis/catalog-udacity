from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify
from flask import session as login_session
from decorators import login_required
from database import session, Category, CategoryItem, User
from shared import not_authorized


app = Blueprint('items', __name__, template_folder='templates')


# --------------------------------------
# CRUD - Category Items
# --------------------------------------

# READ ONE
@app.route('/<int:category_item_id>/')
def showItem(category_item_id):
    """Shows a category item"""
    item = session.query(CategoryItem).filter_by(id=category_item_id).one()
    return render_template('item.html', item=item)

# CREATE
@app.route('/new', methods=['GET', 'POST'])
@login_required
def newItem():
    """Allow user to  create new catalog item"""
    categories = session.query(Category).all()
    if request.method == 'POST':
        return createItem()
    return render_template('new_item.html', categories=categories)


def createItem():
    newItem = CategoryItem(
        title=request.form['title'],
        description=request.form['description'],
        category_id=request.form['category'],
        user_id=login_session['user_id'])
    session.add(newItem)
    session.commit()
    flash("New catalog item created!", 'success')
    return redirect(url_for('showCatalog'))


# UPDATE
@app.route('/<int:category_item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category_item_id):
    """Allows user to edit an existing category item"""
    editedItem = session.query(
        CategoryItem).filter_by(id=category_item_id).one()
    if editedItem.user_id != login_session['user_id']:
        return not_authorized()
    if request.method == 'POST':
        return updateItem(editedItem)
    categories = session.query(Category).all()
    return render_template('edit_item.html',
        categories=categories, item=editedItem)


def updateItem(editedItem):
    if request.form['title']:
        editedItem.title = request.form['title']
    if request.form['description']:
        editedItem.description = request.form['description']
    if request.form['category']:
        editedItem.category_id = int(request.form['category'])
    session.add(editedItem)
    session.commit()
    return redirect(url_for('showCatalog'))


# DELETE
@app.route('/<int:category_item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(category_item_id):
    """Allows user to delete an existing category item"""
    itemToDelete = session.query(
        CategoryItem).filter_by(id=category_item_id).one()
    if itemToDelete.user_id != login_session['user_id']:
        return not_authorized()
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.title, 'success')
        session.commit()
        return redirect(url_for('showCatalog'))
    return render_template('delete_item.html', item=itemToDelete)


# --------------------------------------
# JSON
# --------------------------------------
@app.route('.json')
def showItemsJSON():
    """Returns JSON of all items in catalog"""
    items = session.query(CategoryItem).order_by(CategoryItem.id.desc())
    return jsonify(CategoryItems=[i.serialize for i in items])
