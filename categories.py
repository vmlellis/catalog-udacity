from flask import Blueprint
from decorators import login_required


app = Blueprint('categories', __name__, template_folder='templates')


# --------------------------------------
# CRUD - Categories
# --------------------------------------

# CREATE
@app.route('/new', methods=['GET', 'POST'])
@login_required
def newCategory():
    """Allows user to create new category"""
    return render_template('new_category.html')


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
    return render_template('delete_category.html')


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


# UPDATE ITEM
@app.route(
    '/<int:category_id>/item/<int:category_item_id>/edit',
    methods=['GET', 'POST'])
@login_required
def editCategoryItem(category_id, category_item_id):
    """Allows user to edit an existing category item"""
    return render_template('edit_catalog_item.html')
