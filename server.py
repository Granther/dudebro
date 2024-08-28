from flask import Flask, request, jsonify
import os
from jinja2 import Template
import subprocess

# Define the path to your Nginx configuration directory
nginx_conf_dir = '/etc/nginx/sites-available'
nginx_enabled_dir = '/etc/nginx/sites-enabled'

# Define the path to your configuration template
template_path = 'subdomain_template.conf'

# Load the Nginx configuration template
def load_template(path):
    with open(path, 'r') as file:
        return Template(file.read())

# Create a new Nginx configuration file
def create_nginx_conf(subdomain, host):
    template = load_template(template_path)
    config_content = template.render(subdomain=subdomain, host=host)
    conf_filename = f"{subdomain}.conf"
    
    conf_path = os.path.join(nginx_conf_dir, conf_filename)
    with open(conf_path, 'w') as file:
        file.write(config_content)
    
    # Create a symlink in the sites-enabled directory
    enabled_conf_path = os.path.join(nginx_enabled_dir, conf_filename)
    if not os.path.exists(enabled_conf_path):
        os.symlink(conf_path, enabled_conf_path)
    
    # Test and reload Nginx configuration
    try:
        subprocess.run(['nginx', '-t'], check=True)
        subprocess.run(['systemctl', 'reload', 'nginx'], check=True)
        print("Nginx configuration reloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        print("Configuration test or reload failed.")

app = Flask(__name__)

@app.route('/create_subdomain', methods=['POST'])
def create_subdomain():
    data = request.json 
    subdomain = data.get('subdomain')
    host = data.get('host')
    create_nginx_conf(subdomain, host)
    return jsonify({"status": "success", "subdomain": subdomain, "host": host})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

