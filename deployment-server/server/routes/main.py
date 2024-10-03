import os

from flask import Blueprint, abort, render_template, session, jsonify, redirect, url_for, current_app, flash, request

main = Blueprint('main', __name__)

@main.route("/create", methods=['POST', 'GET'])
def create():
    pass

