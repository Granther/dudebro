import logging
import os

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from db_factory import db
from models import Users, Containers
from deploy import Deploy
from properties import Properties
from logger import create_logger

app = Flask(__name__)
app.config['SECRET_KEY'] = 'glorp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dudebro.db'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = None
login_manager.login_message_category = 'info'

with app.app_context():
    db.create_all()

properties = Properties()
deploy = Deploy(image=os.getenv("IMAGE_NAME"), db=db, Containers=Containers)

logger = create_logger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

server_props_render = {"class": "bg-gray-900 text-white px-2 py-1 rounded-md"}
server_props_render_int = {"class": "bg-gray-900 text-white px-2 py-1 rounded-md w-16 number-input"}

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"class": "border border-black rounded-lg text-black px-2 py-1 focus:outline-none w-full text-lg", "autocomplete":"off"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "border border-black rounded-lg text-black px-2 py-1 focus:outline-none w-full text-lg", "autocomplete":"off"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "border border-black rounded-lg text-black px-2 py-1 focus:outline-none w-full text-lg", "autocomplete":"off"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "border border-black rounded-lg text-black px-2 py-1 focus:outline-none w-full text-lg", "autocomplete":"off"})
    submit = SubmitField('Sign Up', render_kw={"class": "bg-sky-500 hover:bg-sky-700 text-white py-2 px-5 rounded-full font-bold text-md transition duration-300"})

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"class": "border border-black rounded-lg text-black px-2 py-1 focus:outline-none w-full text-lg", "autocomplete":"off"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "border border-black rounded-lg text-black px-2 py-1 focus:outline-none w-full text-lg", "autocomplete":"off"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login', render_kw={"class": "bg-sky-500 hover:bg-sky-700 text-white py-2 px-5 rounded-full font-bold text-md transition duration-300"})

class CommandForm(FlaskForm):
    command = StringField('Command', validators=[DataRequired()], render_kw={"class": "border border-black rounded-lg text-black px-2 py-1 focus:outline-none w-full text-lg", "autocomplete":"off"})
    submit = SubmitField('Login', render_kw={"class": "bg-sky-500 hover:bg-sky-700 text-white py-2 px-5 rounded-full font-bold text-md transition duration-300"})

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={"class": "bg-sky-500 hover:bg-sky-700 text-white py-2 px-5 rounded-full font-bold text-md transition duration-300"})

class ServerCreateForm(FlaskForm):
    subdomain = StringField('Subdomain', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create')

class ServerPropertiesForm(FlaskForm):
    allow_flight = SelectField("allow_flight", choices=[("false", "false"), ("true", "true")], render_kw=server_props_render)
    allow_nether = SelectField("allow_nether", choices=[("false", "false"), ("true", "true")], render_kw=server_props_render)
    difficulty = SelectField("difficulty", choices=[("hard", "hard"), ("easy", "easy"), ("peaceful", "peaceful")], render_kw=server_props_render)
    enforce_whitelist = SelectField("enforce_whitelist", choices=[("false", "false"), ("true", "true")], render_kw=server_props_render)
    gamemode = SelectField("gamemode", choices=[("creative", "creative"), ("survival", "survival")], render_kw=server_props_render)
    hardcore = SelectField("hardcore", choices=[("false", "false"), ("true", "true")], render_kw=server_props_render)
    level_name = StringField("level_name", render_kw=server_props_render)
    level_seed = StringField("level_seed", render_kw=server_props_render)
    level_type = StringField("level_type", render_kw=server_props_render)
    max_players = IntegerField("max_players", render_kw=server_props_render_int)
    motd = StringField("motd", render_kw=server_props_render)
    pvp = SelectField("pvp", choices=[("false", "false"), ("true", "true")], render_kw=server_props_render)
    # query55port = StringField("query.port")
    # rcon55password = StringField("rcon.password")
    # rcon55port = StringField("rcon.port")
    # server_port = StringField("server_port")
    simulation_distance = IntegerField("simulation_distance", render_kw=server_props_render_int)
    view_distance = IntegerField("view_distance", render_kw=server_props_render_int)
    white_list = SelectField("white_list", choices=[("false", "false"), ("true", "true")], render_kw=server_props_render)

    submit = SubmitField('Save', render_kw={"class": "bg-sky-500 hover:bg-sky-700 text-white py-2 px-5 rounded-full font-bold text-md transition duration-300"})

def user_can_access(id:int, subdomain: str):
    results = Users.query.filter_by(id=id).first().containers

    if results:
        for container in results:
            if subdomain == container.subdomain:
                return True
        
    return False

def reached_creation_limit(id: int):
    results = Users.query.filter_by(id=id).first()

    if results:  
        if len(results.containers) >= results.container_limit:
            return True
    
    return False

def get_container(subdomain: str):
    containers = deploy.get_user_containers(subdomain=subdomain)
    if containers:
        return containers[0]
    
    return False

def get_container_status(subdomain: str):
    states = [{"status": "running", "show": "Running", "color": "bg-green-500"},
                {"status": "exited", "show": "Stopped", "color": "bg-red-500"}]

    container = get_container(subdomain)
    status = deploy.get_status(container.id)

    for state in states:
        if state['status'] == status:
            return state

    return False
        
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email = Users.query.filter_by(email=form.email.data).first()
        if email:
            flash('Register Unsuccessful. Email already associated with account', 'danger')
            return render_template("register.html", title='Register', form=form)

        user = Users(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("validated")
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    # elif not form.validate_on_submit():
    #     flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/home")
@login_required
def home():
    servers = []
    results = Users.query.filter_by(email=current_user.email).first()

    if results:
        containers = results.containers
        for item in containers:
            servers.append(item)

    return render_template("home.html", servers=servers)

@app.route("/home/<subdomain>")
@login_required
def server(subdomain):
    if not user_can_access(id=current_user.id, subdomain=subdomain):
        flash("Sorry, you cannot access that page", "danger")
        return redirect(url_for('home'))

    return render_template("server.html", subdomain=subdomain)
    
@app.route("/edit/<subdomain>", methods=['POST', 'GET'])
@login_required
def edit(subdomain):
    if not user_can_access(id=current_user.id, subdomain=subdomain):
        flash("Sorry, you cannot access that page", "danger")
        return redirect(url_for('home'))

    form = ServerPropertiesForm()
    command_form = CommandForm()
    delete_form = DeleteForm()
    
    results = Containers.query.filter_by(subdomain=subdomain).first()
    props = properties.read_server_properties(results.uuid)

    if request.method == 'GET':
        for key, val in props.items():
            try:
                key = key.replace("-", "_")
                getattr(form, key).data = val
            except:
                pass

    if form.validate_on_submit():
        for key, val in props.items():
            try:
                props[key] = getattr(form, key.replace("-", "_")).data 
            except:
                pass

        properties.write_server_properties(results.uuid, props)
        return redirect(url_for('home'))

    if delete_form.validate_on_submit():
        logger.info(f"Deleting container attached to subdomain: {subdomain}")
        deploy.delete_container(subdomain)

        return redirect(url_for('home'))

    return render_template("edit.html", form=form, command_form=command_form, delete_form=delete_form, subdomain=subdomain, domain=os.getenv("DOMAIN"))

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if reached_creation_limit(id=current_user.id):
        flash("Sorry, you have reached the maximum number of servers you can create", "danger")
        return redirect(url_for('home'))        

    form = ServerCreateForm()
    if form.validate_on_submit():
        try:
            deploy.create_container(user_id=current_user.id, subdomain=form.subdomain.data)
            flash("Successfully created server", "success")
            return redirect(url_for('home'))
        except Exception as e:
            flash(f"Exception occured when creating server: {e}","danger")
            return redirect(url_for('home'))
    
    return render_template("create.html", title="Create", form=form)

@app.route("/get_status/<subdomain>", methods=['GET', 'POST'])
@login_required
def get_status(subdomain):
    if request.method == "GET" and user_can_access(id=current_user.id, subdomain=subdomain):
        status = get_container_status(subdomain)

        print(status)

        if status:
            return jsonify(status)
        else:
            return jsonify({"status": "unknown", "show": "Unknown", "color": "bg-gray-500"})
    
    return "Unauthorized", 401

@app.route("/restart/<subdomain>", methods=['GET', 'POST'])
@login_required
def restart(subdomain):
    if request.method == "GET" and user_can_access(id=current_user.id, subdomain=subdomain):
        status = True

        get_container(subdomain=subdomain).restart()

        return jsonify(status)
    
    return "Unauthorized", 401

@app.route("/shutdown/<subdomain>", methods=['GET', 'POST'])
@login_required
def shutdown(subdomain):
    if request.method == "GET" and user_can_access(id=current_user.id, subdomain=subdomain):
        status = True

        get_container(subdomain=subdomain).kill()

        return jsonify(status)
    
    return "Unauthorized", 401

@app.route("/start/<subdomain>", methods=['GET', 'POST'])
@login_required
def start(subdomain):
    if request.method == "GET" and user_can_access(id=current_user.id, subdomain=subdomain):
        status = True

        get_container(subdomain=subdomain).start()

        return jsonify(status)
    
    return "Unauthorized", 401

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5005)
