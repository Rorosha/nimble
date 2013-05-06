from flask.ext.wtf import Form, TextField, BooleanField, PasswordField
from flask.ext.wtf import Required

class LoginForm(Form):
  """Provides the functionality for user login via OpenID providers."""
  openid = TextField('openid', validators=[Required()])
  username = TextField('username')
  name = TextField('name')
  password = PasswordField('password', validators=[Required()])
  password_1 = PasswordField('password_1')
  remember_me = BooleanField('remember_me', default=False)
