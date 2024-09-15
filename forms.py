from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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
    command = StringField('Command', validators=[DataRequired()], 
                          render_kw={"class": "border border-black rounded-l-lg text-black px-2 py-2 focus:outline-none w-1/2 text-md", "autocomplete":"off"})
    submit = SubmitField('Send', 
                         render_kw={"class": "bg-sky-500 hover:bg-sky-700 text-white py-2 px-5 rounded-r-lg font-bold text-md transition duration-300"})

class BanCommandForm(FlaskForm):
    ban = StringField('/ban', validators=[DataRequired()], render_kw={"class": "border border-black rounded-lg text-black px-2 py-1 focus:outline-none w-1/2 text-lg", "autocomplete":"off"})
    submit = SubmitField('Ban', render_kw={"class": "bg-sky-500 hover:bg-sky-700 text-white py-2 px-5 rounded-full font-bold text-md transition duration-300"})

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete', render_kw={"class": "bg-sky-500 hover:bg-sky-700 text-white py-2 px-5 rounded-full font-bold text-md transition duration-300"})

class ServerCreateForm(FlaskForm):
    subdomain = StringField('Subdomain', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create')

server_props_render = {"class": "bg-gray-900 text-white px-2 py-1 rounded-md"}
server_props_render_int = {"class": "bg-gray-900 text-white px-2 py-1 rounded-md w-16 number-input"}
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
    simulation_distance = IntegerField("simulation_distance", render_kw=server_props_render_int)
    view_distance = IntegerField("view_distance", render_kw=server_props_render_int)
    white_list = SelectField("white_list", choices=[("false", "false"), ("true", "true")], render_kw=server_props_render)

    submit = SubmitField('Save and Restart', render_kw={"class": "bg-sky-500 hover:bg-sky-700 text-white py-2 px-5 rounded-full font-bold text-md transition duration-300"})
