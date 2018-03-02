
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
from flask import url_for
from flask import flash
from flask import make_response
from flask import session as login_session
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from database import *
from login_dec import login_required
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import random
import string
import httplib2
import json
import requests
import datetime
import os

#------ flask instance ------#

app = Flask(__name__)

#------ google ID ------#
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

#------ Connect to Database and create database session ------#
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Submit request, parse response
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;\
     height: 300px;\
     border-radius: 150px;\
     -webkit-border-radius: 150px;\
     -moz-border-radius: 150px;"> '
    print "done!"
    return output


# functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Disconnect a user and reset their login_session
@app.route('/disconnect')
def disconnect():
    # only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = redirect(url_for('showCategories'))
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show all categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).all()
    latestI = session.query(CategoryItem).order_by(CategoryItem.date).limit(5)
    return render_template(
        'category.html', categories=categories, latests=latestI)


# List all items in a specific category
@app.route('/category/<int:category_id>/')
def categoryItems(category_id):
    category = session.query(
        Category).filter_by(id=category_id).one()
    items = session.query(
        CategoryItem).filter_by(category_id=category.id).all()
    if 'username' not in login_session:
        return render_template('catalog.html', category=category, items=items)
    else:
        return render_template(
            'privatecatalog.html', category=category, items=items)


# Add a new item info
@app.route('/category/<int:category_id>/new', methods=['GET', 'POST'])
@login_required
def newCategoryItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newItem = CategoryItem(
            name=request.form['name'],
            category_id=category.id,
            user_id=login_session['user_id'],
            date=datetime.datetime.now(),
            description=request.form['description'],
            category=category)
        print(newItem)
        session.add(newItem)
        session.commit()
        return redirect(url_for('categoryItems', category_id=category.id))
    else:
        return render_template('newItem.html', category=category)


# Shows the description of the item
@app.route('/category/<int:category_id>/<int:item_id>')
def ItemsDescription(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return render_template(
            'itemdescription.html', category=category, item=item)
    else:
        return render_template(
            'privatedescription.html', category=category, item=item)


# Update item information
@app.route('/category/<int:category_id>/<int:item_id>/edit', methods=[
    'GET', 'POST'])
@login_required
def editItem(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)
    if creator.id != login_session['user_id']:
        flash("You cannot edit this item")
        return redirect(url_for(
            'ItemsDescription', category_id=category_id, item_id=item.id))
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        date = datetime.datetime.now(),
        session.add(item)
        session.commit()
        flash('Modality Successfully Edited')
        return redirect(url_for('categoryItems', category_id=category.id))
    else:
        return render_template('editItem.html', i=item)


# Delete item information
@app.route('/category/<int:category_id>/<int:item_id>/delete', methods=[
    'GET', 'POST'])
@login_required
def deleteCategoryItem(category_id, item_id):
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    creator = getUserInfo(item.user_id)
    if creator.id != login_session['user_id']:
        flash("You cannot delete. The owner is %s" % creator.name)
        return redirect(url_for(
            'ItemsDescription', category_id=category_id, item_id=item.id))
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Modality has been deleted")
        return redirect(url_for('categoryItems', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=item)


# Making an API Endpoint(GET Request)

# Display all the categories
@app.route('/category/JSON')
def showCategoriesJSON():
    category = session.query(Category).all()
    return jsonify(Category=[i.serialize for i in category])


# Display all the modalities from that category
@app.route('/category/<int:category_id>/JSON')
def categoryItemsJSON(category_id):
    items = session.query(
        CategoryItem).filter_by(category_id=category_id).all()
    return jsonify(CategoryItem=[i.serialize for i in items])


# Shows the description of the item selected
@app.route('/category/<int:category_id>/<int:item_id>/JSON')
def ItemsDescriptionJSON(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    return jsonify(CategoryItem=[item.serialize])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
