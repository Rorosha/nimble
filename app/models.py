from app import db

class User(db.Model):
  """Model for a user. User handling is covered by Flask-Login
  and the data piece is handled by Flask-Sqlalchemy."""
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(140))
  username = db.Column(db.String(140), unique=True)
  password = db.Column(db.String(140))
  email = db.Column(db.String(140))
  cards = db.relationship('Card', backref='author', lazy='dynamic')

  def __init__(self, name, username, password, email):
    self.name = name
    self.username = username
    self.password = password
    self.email = email

  def __repr__(self):
    return "<User: %s>" % self.username

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

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

  # Relationship with User
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  # Add author to init.
  def __init__(self, summary):
    self.summary = summary
    self.story = ''
    self.criteria = ''
    self.estimate = 0
    self.deleted = '0'

  def __repr__(self):
    return '<ID: %r, Summary: %r>' % (int(self.id), self.summary)

  def update(self, attrs):
    """Attrs is a list of two item tuples of attributes and values."""
    for key, value in attrs:
      if key in self.__dict__: # Check to see if attr exists
        setattr(self, key, value) # Set class attributes

