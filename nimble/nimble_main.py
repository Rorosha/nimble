import os

from flask import Flask, request, url_for, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy

# Basic Config stuff
app = Flask(__name__)
SQL_DATABASE = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:////' + SQL_DATABASE +
                                                                    '/cards.db')

db = SQLAlchemy(app)

# Models

class User(db.Model):
    """Model for a user. User handling is covered by Flask-Login
    and the data piece is handled by Flask-Sqlalchemy."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    username = db.Column(db.String(140), unique=True)
    password = db.Column(db.String(140))

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User: %s>" % self.username

class Card(db.Model):
    """Model for a card. Handles the user story and acceptance criteria.
    Instantiation requires a summary. Everything else is handled by 
    an update."""
    id = db.Column(db.Integer, primary_key=True)
    summary = db.Column(db.String(140))
    story = db.Column(db.String(400))
    criteria = db.Column(db.String(1000))
    estimate = db.Column(db.Integer)
    deleted = db.Column(db.Integer) # Treat this as a bool

    author = db.Column(db.String(50))

    # Relationship with User
   # author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   # author = db.relationship('User',
    #    backref=db.backref('cards', lazy='dynamic'))

    # Add author to init.
    def __init__(self, summary):
        self.summary = summary
        self.story = ''
        self.criteria = ''
        self.estimate = 0
        self.author = 'Mike'
        self.deleted = '0'

    def __repr__(self):
        return '<ID: %r, Summary: %r>' % (int(self.id), self.summary)

    def update(self, attrs):
        """Attrs is a list of two item tuples of attributes and values."""
        for key, value in attrs:
            if key in self.__dict__: # Check to see if attr exists
                setattr(self, key, value) # Set class attributes

# Views
@app.route('/')
def home():
    cards = Card.query.filter_by(deleted="0").all()
    return render_template('home.html', cards=cards)

@app.route('/add', methods=['GET', 'POST'])
def add_card():
    if request.method == 'GET':
        return render_template("add_card.html")

    if request.method == 'POST':
        newCard = Card(request.form['summary'])
        for arg in request.form:
            try:
                # This looks a little wonky, should refactor the method.
                newCard.update([(arg, request.form[arg])])
            except:
                print "Couldn't update the card. Empty Arg = %s " % arg
                pass

        db.session.add(newCard)
        db.session.commit()
        return redirect(url_for('home'))

    else:
        return "You need to do something here."

@app.route('/remove', methods=['GET', 'POST'])
def remove_card():
    if request.method == 'GET':
        return render_template("remove_card.html")

    if request.method == 'POST':
        try:
            card = Card.query.filter_by(id=request.form['card_id']).first()
            card.deleted = 1

            db.session.add(card)
            db.session.commit()

            return redirect(url_for('home'))

        except:
            return "<h1>Yeah, that didn't work.</h1>"
        
    else:

        return "You need to do something here."

@app.route('/recover', methods=['GET', 'POST'])
def recover_card():
    if request.method == 'GET':
        deleted_cards = Card.query.filter_by(deleted='1').all()
        # change template name to be recover_card.html
        return render_template("recreate_card.html", cards=deleted_cards)

    if request.method == 'POST':
        try:
            recovered_card = Card.query.get(request.form['card_id'])
            recovered_card.deleted = '0'

            db.session.add(recovered_card)
            db.session.commit()
            
            return redirect(url_for('home'))

        except:
            return "This is broked."

if __name__ == '__main__':
    app.debug = True
    app.run()
