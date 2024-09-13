import random
import requests
import os
import shutil

from uuid import uuid4
from dotenv import load_dotenv
import docker

from nginx import NginxInteractor
from properties import set_property
from logger import create_logger

class Deploy:
    def __init__(self, image, Containers, db, network_name:str="mc-network", timeout:int=5):
        load_dotenv()
        self.db = db
        self.Containers = Containers
        self.image = image
        self.timeout = timeout
        self.client = docker.from_env()
        self.network_name = network_name

        self.network = self.init_network(network_name)
        self.zone_id = os.getenv("ZONE_ID")
        self.api_key = os.getenv("API_KEY")
        self.domain = os.getenv("DOMAIN")
        self.public_ip = os.getenv("PUBLIC_IP")
        self.email = os.getenv("EMAIL")
        self.target_fqdn = os.getenv("TARGET_FQDN")

        self.logger = create_logger(__name__)

    def create_container(self, user_id: int, subdomain: str):
        try:
            uuid = str(uuid4())
            path = self._create_instance_dir(uuid)

            port = self._get_port()
            if not port:
                error = "Error retrieving port"
                self.logger.critical(error)
                raise RuntimeError(error)

            if not set_property(uuid, "server-port", port):
                error = "Error setting port property in server.properties"
                self.logger.critical(error)
                raise RuntimeError(error)

            name = f"dude_{subdomain}-{uuid}"
            container = self.client.containers.run(
                self.image,
                detach=True,
                tty=True,
                ports={f"{port}/tcp":port},
                volumes={path: {"bind": "/minecraft", "mode": "rw"}},
                name=name,
                labels={"user_id": str(user_id), "subdomain": subdomain, "uuid": uuid},
                network=self.network_name
            )

            new_container = self.Containers(uuid=uuid, subdomain=subdomain, domain=self.domain, port=port, weight=0, priority=0, name=name, user_id=user_id)
            self.db.session.add(new_container)
            self.db.session.commit()

            self._create_srv_entry(subdomain, self.domain, self.target_fqdn, port)

            return container

        except RuntimeError as e:
            self.logger.critical(str(e), exc_info=True)
            raise

        except Exception as e:
            self.logger.error(f"Unexpected error in create_container: {e}", exc_info=True)
            raise RuntimeError("An unexpected error occurred while creating the container.")
 
    def _create_instance_dir(self, uuid: str):
        try:
            path = os.path.join(os.getenv("INSTANCES_DIR"), uuid)
            shutil.copytree("./minecraft", path)
            return path
        except (OSError, shutil.error) as e:
            self.logger.error(f"Failed to create instance directory: {e}", exc_info=True)
            return None

    def _get_port(self):
        ports = self.db.session.query(self.Containers.port).order_by(self.db.desc(self.Containers.port)).first()
        port = None

        if ports:
            port = ports.port
            print("port", port)
        else:
            port = 1025
            print("port", port)

        return port + 1
    
    def get_container_ip(self, container):
        container.reload()
        network_settings = container.attrs['NetworkSettings']
        ip_address = network_settings['Networks'][self.network_name]['IPAddress']

        return ip_address

    def _create_srv_entry(self, subdomain, domain, target_record, port: int, proxied=False, weight:int=0, priority:int=0):
        url = f'https://api.cloudflare.com/client/v4/zones/{self.zone_id}/dns_records'

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
        }

        data = {
            'type': "SRV",
            "name": f"_minecraft._tcp.{subdomain}.{domain}",
            "service": "_minecraft",
            "proto": "_tcp",
            "data": {
                "weight": weight,
                "port": port,
                "target": target_record,
                "priority": priority,
            },
            'id': str(uuid4()),
            'proxied': proxied,
            'ttl': 1, #auto
        }
        print(data)
        create_response = requests.post(url, headers=headers, json=data)
        if create_response.status_code == 200:
            print(f'Created successfully.')
            return True
        else:
            print(f'Failed to create record: {create_response.json()}')
            return False
    
    def init_network(self, network_name):
        try:
            return self.client.networks.get(network_name)
        except docker.errors.NotFound:
            return self.client.networks.create(network_name, driver="bridge")

    def get_user_containers(self, user_id:str=None, subdomain:str=None, uuid:str=None):
        filter = {"label": ""}
        if user_id:
            filter["label"] = f"user_id={user_id}"
        elif subdomain:
            filter["label"] = f"subdomain={subdomain}"
        elif uuid:
            filter["label"] = f"uuid={uuid}"
        else:
            return False

        return self.client.containers.list(all=True, filters=filter)
    
    def stop_user_container(self, user_id, cid):
        if self.does_user_own(user_id, cid) and self.is_running(cid):
            self.get_container(cid).stop(timeout=self.timeout)
            
    def does_user_own(self, user_id, cid):
        if cid in [container.id for container in self.get_user_containers(user_id)]:
            return True
    
        return False
    
    def get_container(self, cid):
        return self.client.containers.get(cid)
    
    def get_status(self, cid):
        return self.get_container(cid).status
    
    def is_running(self, cid) -> bool:
        if self.get_status(cid) == "running":
            return True
        return False



if __name__ == "__main__":
    dep = Deploy(image="debian")
    # dep.create_container("123", "anotherone")
    userid = dep.create_user(username="Grant", password="pass")
    print("serid", userid)
    cont = dep.create_container(userid, "helo")
    x = dep.get_user_containers(3)
    print(x)
    # x = dep.get_user_containers("123")
    # for i in x:
    #     print(i.id)
    # dep.does_user_own("123", "845cca7f6454d75e1499b0454fbedd6abebae0ab8fb0071e090e165caaaba891")
    # print(dep.stop_user_container("123","845cca7f6454d75e1499b0454fbedd6abebae0ab8fb0071e090e165caaaba891"))