from flask import Flask, render_template, url_for, redirect, request, abort
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore, current_user
import flask_admin
from flask_admin.contrib import sqla
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from database import db_session, init_db
from models import User, Role, RolesUsers

# Create app
app = Flask(__name__, template_folder="static/templates")
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = '0'

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db_session,
                                                User, Role)
security = Security(app, user_datastore)

# Create an admin and normal user to test with
@app.before_first_request
def create_user():
    init_db()
    if not user_datastore.get_user('admin'):
        print("creating new 'admin' user with password 'password'")
        admin_user = user_datastore.create_user(email='admin', password='password')
        user_datastore.add_role_to_user(user=admin_user, role='admin')
    if not user_datastore.get_user('user'):
        user_datastore.create_user(email='user', password='password')
    db_session.commit()

# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')


# Create admin
admin = flask_admin.Admin(
    app,
    'Admin page',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Create customized model view class
class BaseModelView(sqla.ModelView):
    column_display_pk = True

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


admin.add_view(BaseModelView(User, db_session))
admin.add_view(BaseModelView(Role, db_session))
admin.add_view(BaseModelView(RolesUsers, db_session))
admin.add_link(MenuLink(name='Back to ECS OpenData', url='/'))

if __name__ == '__main__':
    app.run()
