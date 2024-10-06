from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField

class MinecraftCreateServerInitForm(FlaskForm):
    subdomain = StringField('Subdomain', validators=[DataRequired(), Length(min=1, max=62)])
    num_players = IntegerField('Num Players', validators=[DataRequired()])
    version = QuerySelectField("Version")