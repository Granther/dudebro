from flask import Flask, request, jsonify
import os
from jinja2 import Template
from dotenv import load_dotenv
import subprocess

nginx_conf_dir = '/etc/nginx/sites-available'
nginx_enabled_dir = '/etc/nginx/sites-enabled'
template_path = 'subdomain_template.conf'

class DudeServer:
    def __init__(self):
        load_dotenv()
        self.zone_id = os.getenv("ZONE_ID")
        self.api_key = os.getenv("API_KEY")
        self.domain = os.getenv("DOMAIN")
        self.public_ip = os.getenv("PUBLIC_IP")
        self.email = os.getenv("EMAIL")

    # Load the Nginx configuration template
    def load_template(self, path):
        with open(path, 'r') as file:
            return Template(file.read())

    def create_dns_entry(self, subdomain):
        url = f'https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records'

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
        }

        data = {
            'type': "A",
            'name': f'{subdomain}.{self.domain}',
            'content': self.public_ip,
            'id': str(uuid4()),
            'proxied': True,
            'ttl': 1, #auto
        }
        create_response = requests.post(url, headers=headers, json=data)
        if create_response.status_code == 200:
            print(f'Record {subdomain}.{self.domain} created successfully.')
        else:
            print(f'Failed to create record: {create_response.json()}')

    # Create a new Nginx configuration file
    def create_nginx_conf(self, subdomain, host):
        self.create_dns_entry(subdomain)
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

app = Flask(__name__)
server = DudeServer()

@app.route('/create_subdomain', methods=['POST'])
def create_subdomain():
    data = request.json
    subdomain = data.get('subdomain')
    host = data.get('host')
    server.create_nginx_conf(subdomain, host)
    return jsonify({"status": "success", "subdomain": subdomain, "host": host})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)