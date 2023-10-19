# Install flask by running command: python -m pip install {package_name}  in an activated terminal.
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#  Set up application, so this just referencing this file.
app = Flask(__name__)


# this app.config['SQLALCHEMY_URL']  part is telling our app where our database is located.
# /// three forward slashs is an relative path (and // two forward slashes is an absolute path). using a relative path here so that we don't have to specify an exact location and want it to reside in the project location.
# set the database name as test.db, then everything is going to be stored in this test.db file.
# import SQL alchemy. and then add a config, this is going to be SQL alchemy.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# initialize the database with the settings form our app.
db = SQLAlchemy(app)

app.app_context().push()


# Create a model. First set an ID column.
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # then create a text column called content which is going to be what holds each list. then set characters as 200 amount.then set nullable = False so that we don't want htis to be left blank. user will not be able to create a new list and just leave the content of that list empty.
    content = db.Column(db.String(200), nullable=False)
    #  time and to do enrty is created. The date_created will automatically be set to the time that it was created.
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # then need a function that is going to return a string every time we create a new element.
    def __repr__(self):
        # it is going to return list that has just been created.
        return "<List %r>" % self.id


#  Careate a index route so that when we browse to the URL, We don't immediately just 404, in Flask.
#  @app.rout("/") Set up routes with the app route decorator. ("/") here we are going to pass in the URL string of your route.
#  adding two methods that this route can accept.
@app.route("/", methods=["POST", "GET"])
# Define the function for that route (@app.rout("/");
def index():
    #  If The request that is set to this route is post, do something here. Then "else", do more things.
    if request.method == "POST":
        list_content = request.form["content"]
        # !!! we have a Todo(db.Model), now create a Todo abject that is going to have its contents equal to the content of that input.
        new_list = Todo(content=list_content)
        # then,push data to the database, do the try below:
        try:
            # add new_list data to database session.
            db.session.add(new_list)
            #  commit the data to database session.
            db.session.commit()
            # finaly, return  a redirect back to index
            return redirect("/")
        # if it failed , create an accept to return error message.
        except:
            return "Something just went wrong, please try again"
    else:
        # create a variable called lists that is going to look ate all of the database contents in the order they were created and it is going to return all of them.
        #  querying database or odering them by the "date_created",then grabbing all of them.
        lists = Todo.query.order_by(Todo.date_created).all()
        # then pass it to template, to set "lists = lists" (the variale just created), below.

        #  Call and return "index.html". using render_template().  Don't need to speicify the folder, beacuse the "app = Flask(__name__)"" is for looking that folder.
        return render_template("index.html", lists=lists)


#  importer render_template at the top of this code page. To get the ID: for integer and call the id.
@app.route("/delete/<int:id>")
# Define a function called id. passing id as the variable.
def delete(id):
    # create variable called list to delete,and then query database,
    # "get" is going to get that list by id, if it doesn't exist, it is going to be 404.
    list_to_delete = Todo.query.get_or_404(id)

    # try to delete
    try:
        db.session.delete(list_to_delete)
        # commit data agian.
        db.session.commit()
        # return the redirect back to the homepage.
        return redirect("/")
    # If it doesn't work ,then print error message.
    except:
        return "Something just went wrong, please check again."


# to update data to database. get the ID: for integer and call the id.
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    # showing the list get list from database and by id.
    list = Todo.query.get_or_404(id)
    if request.method == "POST":
        # if form is requested then list content.
        list.content = request.form["content"]
        # try to commit data to the database sesstion.
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your list"
    else:
        return render_template("update.html", list=list)


# #  Set debuging equal to ture, so if we have any erros, they will pop up the web page and we can see it.
# #  So for this is a very basic flask applicaiton. it should pup pu a page says "Hello, world".
if __name__ == "__main__":
    app.run(debug=True)
