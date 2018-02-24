from flask import Flask #importing flask from the Flask class
from flask import render_template,url_for,redirect,request,flash,jsonify #importing all the required methods from flask
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import  Base,Restraunt,MenuItem
app = Flask(__name__) #creating an instance of this class with the name argument which is the name of the application's module or package.

#setting the database up,session to perform the crud operations
engine = create_engine('sqlite:///restrauntmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

''' 
    Setting up a url path which takes us to the index or the supposedly home page
    the home page takes us to the restraunt followed with the restaurant id
    restraunt method get's invoked when this url is hit as we are binding it to that url
    get the restraunt and menuitem details from the database,use the filterby method to filter the resraunt
    based on the id passed in the url,using the restarunt obtained filter out the menu items of it using
    matching the restraunt_id column of MenuItem table with the restraunt id which is a foreign key column
    then pass the retrieved info to the menuitem.html page which renders it in a decent way,use the render_template
    and pass the restraunt and the items as the context
'''
@app.route('/restraunts')
def default():
    restraunt = session.query(Restraunt).all()
    return render_template('reslist.html',restraunt=restraunt)
@app.route('/restraunts/new',methods=['GET','POST'])
def new_restraunt():
    if request.method == 'POST':
        newres = Restraunt(name = request.form['name'])
        session.add(newres)
        session.commit()
        flash('New Restraunt has been succesfully added')
        return redirect(url_for('default'))
    else:
        return render_template('newres.html')
@app.route('/restraunts/<int:restraunt_id>',methods=['GET','POST'])
def del_restraunt(restraunt_id):
    delres = session.query(Restraunt).filter_by(id=restraunt_id).one()
    if request.method == 'POST':
        session.delete(delres)
        session.commit()
        flash(' Restraunt has been  deleted succesfully')
        return redirect(url_for('default'))
    else:
        return render_template('delres.html',restraunt_id=restraunt_id,item=delres)
@app.route('/restraunts/<int:restraunt_id>/')
def restraunt(restraunt_id):
    restraunt = session.query(Restraunt).filter_by(id =restraunt_id).one()
    items = session.query(MenuItem).filter_by(restraunt_id=restraunt.id)
    return render_template('menu.html', restraunt=restraunt,items=items)

'''
    This Url is for creating a new  menu item  in the restraunt ,we pass in the get and the post methods
    as arguments with out which the corresponding actions can't be performed, the restraunt id from the url is
    passed to the function which let's us add that menu item to the correct restraunt.Perform a check to if the method is post,
    if it is post Create a new item using the name type in the form's input tag with the name attribute,get that value and assign 
    it to the name in the menuitem table,add that and commit that to the database once done redirect the user to the home page
    (i.e restraunt/id page) using the redirect method,if the method is not post then redirect the url to the form which allows him to create a new menu item.
'''
@app.route('/restraunts/<int:restraunt_id>/new/',methods=['GET','POST'])
def newMenuItem(restraunt_id):
    if request.method == 'POST':
        newItem = MenuItem(name = request.form['name'],price =request.form['price'],description = request.form['desc'],restraunt_id=restraunt_id)
        session.add(newItem)
        session.commit()
        flash('New Item has been added to your Menu!!')
        return redirect(url_for('restraunt',restraunt_id=restraunt_id))
    else:
        return render_template('newmenuitem.html', restraunt_id=restraunt_id)
'''
    Edit the menu item of a particular restaurant pass in the restraunt id and the menu id,same as creating a new menu item
    the only difference being that we set the value obtained from name field attribute and set it to the name of the MenuItem.
    flash can be used to provide feedback to the user upon peforming any actions.
'''
@app.route('/restraunts/<int:restraunt_id>/<int:menu_id>/edit/',methods=['GET','POST'])
def editMenuItem(restraunt_id,menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        # if request.form['name']:
        editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash('The item has been edited successfully')
        return redirect(url_for('restraunt',restraunt_id=restraunt_id))
    else:
        return render_template('editmenu.html',restraunt_id=restraunt_id,menu_id=menu_id,item = editedItem)
'''
    Deleting is the same all we do is get the menuitem by using the id provided in the URL and 
    retrieve that item from the database and delete it.
'''
@app.route('/restraunts/<int:restraunt_id>/<int:menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restraunt_id, menu_id):
    delItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(delItem)
        session.commit()
        flash('The item has been deleted')
        return redirect(url_for('restraunt',restraunt_id=restraunt_id))
    else:
        return render_template('deletemenuitem.html',restraunt_id=restraunt_id,menu_id=menu_id,item=delItem)
'''
    Passing the data from the database in a JSON Format.
    We use the jsonify method here,the serialize method from the database is use here to convert it into a JSON
    In this  method we convert the entire menu of a particular restraunt into JSON
    
'''
@app.route('/restraunts/<int:restraunt_id>/JSON')
def restrauntJSON(restraunt_id):
    restraunt = session.query(Restraunt).filter_by(id=restraunt_id).one()
    items = session.query(MenuItem).filter_by(restraunt_id=restraunt_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


'''
    Passing the data from the database in a JSON Format.
    We use the jsonify method here,the serialize method from the database is use here to convert it into a JSON
    In this  method we convert only one item of a  menu of a particular restraunt into JSON

'''
@app.route('/restraunts/<int:restraunt_id>/menu/<int:menu_id>/JSON')
def menuJSON(restraunt_id,menu_id):
    items = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem = items.serialize)

if __name__=='__main__':
    app.secret_key ='harsha'
    app.debug=True
    app.run(host='0.0.0.0',port=5000)