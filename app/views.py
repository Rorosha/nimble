from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm
import models

@lm.user_loader
def load_user(id):
  return models.User.query.get(int(id))

@app.before_request
def before_request():
  g.user = current_user
  if "Anonymous" in str(current_user):
    session['logged_in'] = False
  else:
    session['logged_in'] = True

@oid.after_login
def after_login(resp):
  if resp.email is None or resp.email == '':
    # Ensure email is in the response
    flash('Invalid login, please try again.')
    redirect(url_for('login'))

  # Find the user in the db via email, if possible
  user = models.User.query.filter_by(email=resp.email).first()
  if user is None: # Or create the user if not found
    nickname = resp.nickname
    if nickname is None or nickname == '':
      nickname = resp.email.split('@')[0]
    user = models.User(session['name'], session['username'],
                       session['password'], resp.email)

    db.session.add(user)
    db.session.commit()

  remember_me = False
  if 'remember_me' in session:
    remember_me = session['remember_me']
    session.pop('remember_me', None)

  # Log the user in, regardless if existing or created
  login_user(user, remember=remember_me)
  return redirect(request.args.get('next') or url_for('home'))

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
  if g.user is not None and g.user.is_authenticated():
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    session['remember_me'] = form.remember_me.data
    session['username'] = form.username.data
    session['name'] = form.name.data
    session['password'] = form.password.data
    return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
  return render_template('login.html',
    form = form,
    providers = app.config['AUTH_PROVIDERS'])

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('login'))

@app.route('/')
def home():
    cards = models.Card.query.filter_by(deleted="0").all()
    return render_template('home.html', cards=cards)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_card():
    if request.method == 'GET':
        return render_template("add_card.html")

    if request.method == 'POST':
        newCard = models.Card(request.form['summary'])
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
@login_required
def remove_card():
    if request.method == 'GET':
        return render_template("remove_card.html")

    if request.method == 'POST':
        try:
            card = models.Card.query.filter_by(id=request.form['card_id']).first()
            card.deleted = 1

            db.session.add(card)
            db.session.commit()

            return redirect(url_for('home'))

        except:
            return "<h1>Yeah, that didn't work.</h1>"
        
    else:
        # Someone had a request other than POST or GET
        return "You need to do something here."

@app.route('/recover', methods=['GET', 'POST'])
@login_required
def recover_card():
    if request.method == 'GET':
        deleted_cards = models.Card.query.filter_by(deleted='1').all()
        # change template name to be recover_card.html
        return render_template("recreate_card.html", cards=deleted_cards)

    if request.method == 'POST':
        try:
            recovered_card = models.Card.query.get(request.form['card_id'])
            recovered_card.deleted = '0'

            db.session.add(recovered_card)
            db.session.commit()
            
            return redirect(url_for('home'))

        except:
            return "This is broked."
