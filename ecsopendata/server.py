from flask import Flask, render_template, url_for, redirect, \
     request, abort, jsonify
from flask_security import Security, login_required, \
     SQLAlchemySessionUserDatastore, current_user
import flask_admin
from flask_admin.contrib import sqla
from flask_admin.menu import MenuLink
from database import db_session, init_db
from models import User, Role, RolesUsers, JSONEncoder

# Create app
app = Flask(__name__, template_folder="static/templates")
app.json_encoder = JSONEncoder

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

    # Check if admin role exists, create new role if not
    admin_role = user_datastore.find_or_create_role(name='admin')

    # Check if admin user exists, create new user if not
    if not user_datastore.get_user('admin'):
        print("creating new 'admin' user with password 'password'")
        admin_user = user_datastore.create_user(email='admin',
                                                password='password')
        user_datastore.add_role_to_user(user=admin_user, role=admin_role)

    # Check if user exists, create if not
    if not user_datastore.get_user('user'):
        user_datastore.create_user(email='user', password='password')
    db_session.commit()


# Views
@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/fetchExperiment', methods=['GET'])
def fetchTypes():
    """
    Stand in for now.
    Eventually will retun the unique experiment types from the MasterTable

    """
    experiments = User.query.all()

    exp_types = []
    for experiment in experiments:
        if experiment.password not in exp_types:
            exp_types.append(experiment.password)

    print(exp_types)
    return jsonify(exp_types=exp_types)


@app.route('/fetchData', methods=['GET'])
def fetchData():

    """
    Fetches all of the data from a given data table

    Currently hard coded to the User table, but will move to the MasterTable
    once available
    """

    data = User.query.all()

    return jsonify(data)


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
        Override builtin _handle_view in order to redirect
        users when a view is not accessible.
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
