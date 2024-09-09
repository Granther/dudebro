from flask import Flask, request, jsonify
import os
from jinja2 import Template
from dotenv import load_dotenv
import subprocess
from uuid import uuid4
import requests

nginx_conf_dir = '/etc/nginx/sites-available'
nginx_enabled_dir = '/etc/nginx/sites-enabled'
template_path = 'subdomain_template.conf'

class DudeServer:
    def __init__(self):
        pass

    # Load the Nginx configuration template
    def load_template(self, path):
        with open(path, 'r') as file:
            return Template(file.read())

    # Create a new Nginx configuration file
    def create_nginx_conf(self, subdomain, host):
        self.create_dns_entry(subdomain)
        template = self.load_template(template_path)
        config_content = template.render(subdomain=subdomain, host=host)
        conf_filename = f"{subdomain}.conf"

        conf_path = os.path.join(nginx_conf_dir, conf_filename)
        with open(conf_path, 'w') as file:
            file.write(config_content)

        # Create a symlink in the sites-enabled directory
        enabled_conf_path = os.path.join(nginx_enabled_dir, conf_filename)
        if not os.path.exists(enabled_conf_path):
            os.symlink(conf_path, enabled_conf_path)

app = Flask(__name__)
server = DudeServer()

@app.route('/create_subdomain', methods=['POST'])
def create_subdomain():
    data = request.json
    subdomain = data.get('subdomain')
    host = data.get('host')
    server.create_nginx_conf(subdomain, host)
    return jsonify({"status": "success", "subdomain": subdomain, "host": host})

@app.route('/server_properties', methods=['POST', 'GET'])
def server_properties():
    pass
    # If GET, send properties to mother, if POST, receieve properties and submit changes

@app.route('/ops', methods=['POST', 'GET'])
def ops():
    pass
    # Get current ops, update ops

@app.route('/logs', methods=['POST'])
def logs():
    pass
    # This is just the logs mo


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5002)
    pass