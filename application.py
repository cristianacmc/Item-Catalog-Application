from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Category, CategoryItem

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Show all categories 
@app.route('/')
@app.route('/categories/')
def showCategories():
	categories = session.query(Category).all()
	return render_template('category.html', category = categories )

#List all items in a specific category
@app.route('/category/<int:category_id>/')
def categoryItems(category_id):
	category = session.query(Category).filter_by(id = category_id).one()
	items = session.query(CategoryItem).filter_by(category_id = category_id).all()
	return render_template('catalog.html', category = category, items=items)
	

#Shows the description of the item
@app.route('/category/<int:category_id>/<int:item_id>')
def ItemsDescription(category_id, item_id):
	return "shows the information of the item"


#Add a new item info
@app.route('/category/<int:category_id>/<int:item_id>/new', methods=['GET', 'POST'])
def newItemInfo(category_id, item_id):
	if request.method == 'POST':
		newInfo = CategoryItem(name = request.form['name'], category_id = category_id)
		session.add(newInfo)
		session.commit()
		return redirect(url_for('categoryItems', category_id = category_id))
	else:
		return render_template('addinfo.html', category_id = category_id, item_id = item_id)

	

#Update item information
@app.route('/category/<int:category_id>/<int:item_id>/edit', methods = ['GET', 'POST'])
def editItem(category_id, item_id):
	item = session.query(CategoryItem).filter_by(id = item_id).one()
	if request.method == 'POST':
		if request.form['name']:
			item.name = request.form['name']
		if request.form['description']:
			item.description = request.form['description']
		if request.form['Category']:
			item.category = request.form['category']
		session.add(item)
		session.commit()
		return redirect(url_for('categoryItems', category_id = category_id))
	else:
		return render_template('editItem.html', category_id = category_id, item_id = item_id, i = item )
		


#Delete item information
@app.route('/category/<int:category_id>/<int:item_id>/delete', methods = ['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
	item = session.query(CategoryItem).filter_by(id = item_id).one()
	if request.method == 'POST':
		session.delete(item)
		session.commit()
		return redirect(url_for('categoryItems', category_id = category_id))
	else:
		return render_template('deleteItem.html', item = item)

		
if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)