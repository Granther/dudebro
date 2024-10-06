import os
from functools import wraps
import requests

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file, copy_current_request_context, current_app
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

from app import db, login_manager
from app.models import Users, Games, GameServers, GameServerConfigs, MinecraftConfigs
from app.logger import create_logger
from app.forms import RegistrationForm, LoginForm, CommandForm, DeleteForm, \
                    ServerCreateForm, ServerPropertiesForm, CommandSelectForm, MinecraftCreateServerInitForm

create = Blueprint('create', __name__, template_folder='../../templates')
logger = create_logger(__name__)

@create.route("/create-minecraft-form", methods=['POST', 'GET'])
@login_required
def create_minecraft_form():
    form = MinecraftCreateServerInitForm()
    versions = requests.get(f'http://localhost:10000/get-game-versions/minecraft')
    form.version = versions

    if form.validate_on_submit():
        return render_template("game-create/minecraft-create.html", form=form)

    return render_template("game-create/minecraft-create.html", form=form)

@create.route("/create-minecraft-init", methods=['POST', 'GET'])
@login_required
def create_minecraft_init():
    # form = MinecraftCreateServerInitForm()

    # if form.validate_on_submit():
    #     return render_template("game-create/minecraft-create.html", form=form)

    # return render_template("game-create/minecraft-create.html", form=form)
    return "Hello"