import os
from flask import Flask 
from flask  import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

class Film(db.Model):
    filmtitle = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    director = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)


    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route('/', methods=["GET", "POST"])
def home():
    books = None
    films = None
    if request.form:
        try:
            if not (request.form.get("title") is None or request.form.get("author") is None):
                book = Book(title=request.form.get("title"), author=request.form.get("author"))
                db.session.add(book)
            if not (request.form.get("filmtitle") is None or request.form.get("director") is None):
                film = Film(filmtitle=request.form.get("filmtitle"), director=request.form.get("director"))
                db.session.add(film)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    films = Film.query.all()
    return render_template("home.html", books=books, films=films)

@app.route("/update", methods=["POST"])
def update():
    try:    
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/updateauthor", methods=["POST"])
def updateauthor():
    try:
        newauthor = request.form.get("newauthor")
        oldauthor = request.form.get("oldauthor")
        book = Book.query.filter_by(author=oldauthor).first()
        book.author = newauthor
        db.session.commit()
    except Exception as e:
        print("Couldn't update book author")
        print(e)
    return redirect("/")

@app.route("/updatefilmtitle", methods=["POST"])
def updatefilmtitle():
    try:
        newfilmtitle = request.form.get("newfilmtitle")
        oldfilmtitle = request.form.get("oldfilmtitle")
        film = Film.query.filter_by(filmtitle=oldfilmtitle).first()
        film.filmtitle = newfilmtitle
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/updatedirector", methods=["POST"])
def updatedirector():
    try:
        newdirector = request.form.get("newdirector")
        olddirector = request.form.get("olddirector")
        film = Film.query.filter_by(director=olddirector).first()
        film.director = newdirector
        db.session.commit()
    except Exception as e:
        print("Couldn't update book author")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

@app.route("/deletefilm", methods=["POST"])
def deletefilm():
    filmtitle = request.form.get("filmtitle")    
    film = Film.query.filter_by(filmtitle=filmtitle).first()
    db.session.delete(film)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)