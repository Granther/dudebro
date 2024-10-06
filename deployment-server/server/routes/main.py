import os

from flask import Blueprint, abort, render_template, session, jsonify, redirect, url_for, current_app, flash, request

from server.models import GameTypes
from server.manifest import list_games, list_game_versions

deploy = Blueprint('deploy', __name__)

# @main.route("/create", methods=['POST', 'GET'])
# def create():
#     pass

@deploy.route("/get-games", methods=['GET'])
def get_games():
    gameTypes = GameTypes.query.all()
    types = [{game.name, game.id} for game in gameTypes]

    return jsonify({"status":types})
    

@deploy.route("/new-game", methods=['GET', 'POST'])
def new_game():
    # req = request.args.get('gamename')
    print(list_games())

    return jsonify({"status":True})
    
@deploy.route("/get-game-versions/<game_name>", methods=['GET', 'POST'])
def get_game_versions(game_name):
    # req = request.args.get('gamename')
    print(list_game_versions(game_name.lower()))

    return jsonify({"status":True})

# @main.route("/get-game-init-conf/<int:gameId>", methods=['GET'])
# def get_game_init_conf(gameId):
    