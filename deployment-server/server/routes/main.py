import os

from flask import Blueprint, abort, render_template, session, jsonify, redirect, url_for, current_app, flash, request

deploy = Blueprint('deploy', __name__)

# @main.route("/create", methods=['POST', 'GET'])
# def create():
#     pass

@deploy.route("/get-games", methods=['GET'])
def get_games():
    return jsonify({"status":True})
    

# @main.route("/get-game-init-conf/<int:gameId>", methods=['GET'])
# def get_game_init_conf(gameId):
    