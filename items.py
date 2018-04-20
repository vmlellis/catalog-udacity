from flask import (
    Blueprint, request, render_template, flash, redirect, url_for, jsonify
)
from flask import session as login_session
from decorators import login_required
from shared import not_authorized
import database as db

app = Blueprint('items', __name__, template_folder='templates')


# --------------------------------------
# CRUD - Category Items
# --------------------------------------

# READ ONE
@app.route('/<int:category_item_id>/')
def showItem(category_item_id):
    """Shows a category item"""
    return render_template('item.html', item=db.findItem(id=category_item_id))


# CREATE
@app.route('/new', methods=['GET', 'POST'])
@login_required
def newItem():
    """Allow user to  create new catalog item"""
    if request.method == 'POST':
        db.createItem(
            title=request.form['title'],
            description=request.form['description'],
            category_id=request.form['category'],
            user_id=login_session['user_id'])
        flash("New catalog item created!", 'success')
        return redirect(url_for('showCatalog'))
    return render_template('new_item.html', categories=db.getAllCategories())


# UPDATE
@app.route('/<int:category_item_id>/edit', methods=['GET', 'POST'])
@login_required
def editItem(category_item_id):
    """Allows user to edit an existing category item"""
    editedItem = db.findItem(id=category_item_id)
    if editedItem.user_id != login_session['user_id']:
        return not_authorized()
    if request.method == 'POST':
        db.updateItem(editedItem, request.form)
        return redirect(url_for('showCatalog'))
    return render_template(
        'edit_item.html', categories=db.getAllCategories(), item=editedItem)


# DELETE
@app.route('/<int:category_item_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(category_item_id):
    """Allows user to delete an existing category item"""
    itemToDelete = db.findItem(id=category_item_id)
    if itemToDelete.user_id != login_session['user_id']:
        return not_authorized()
    if request.method == 'POST':
        db.deleteItem(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.title, 'success')
        return redirect(url_for('showCatalog'))
    return render_template('delete_item.html', item=itemToDelete)


# --------------------------------------
# JSON
# --------------------------------------
@app.route('.json')
def showItemsJSON():
    """Returns JSON of all items in catalog"""
    items = db.getAllItems()
    return jsonify(CategoryItems=[i.serialize for i in items])
