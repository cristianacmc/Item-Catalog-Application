from flask import Flask
from flask import render_template
app = Flask(__name__)


#Show all categories in my database
@app.route('/')
@app.route('/categories')
def showCategories():
	return "All categories"

#List all items in a specific category
@app.route('/category/<int:category_id>/')
def category_items(category_id):
	return "shows all the items available for the category"

#Sjows the description of the item
@app.route('/category/<int:category_id>/<int:item_id>')
def category_items(category_id, item_id):
	return "shows the information of the item"


#Add a new item info
@app.route('/category/<int:category_id>/new')
def newItemInfo(category_id):
	return "page to create specifications about the items"

#Update item information
@app.route('/category/<int:category_id>/<int:item_id>/edit')
def editCategoryItem(category_id, item_id):
	return "page to update an item information"


#Delete item information
@app.route('/category/<int:category_id>/<int:item_id>/delete')
def deleteCategoryItem(category_id, item_id):
	return "page to delete an item information"	



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)