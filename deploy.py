import docker
import random
import requests
import os
from uuid import uuid4
from dotenv import load_dotenv
from nginx import NginxInteractor
from app import Users, Containers

from db_factory import db
from models import Containers

class Deploy:
    def __init__(self, image, network_name:str="mc-network", timeout:int=5):
        load_dotenv()
        self.image = image
        self.timeout = timeout
        self.client = docker.from_env()
        self.network_name = network_name

        #self.network = self.init_network(network_name)
        self.zone_id = os.getenv("ZONE_ID")
        self.api_key = os.getenv("API_KEY")
        self.domain = os.getenv("DOMAIN")
        self.public_ip = os.getenv("PUBLIC_IP")
        self.email = os.getenv("EMAIL")
        self.default_domain = "doesnickwork.com"
        self.default_target = "mine.doesnickwork.com"

        self.sql_init()

    # def sql_init(self):
    #     self.Base = declarative_base()
    #     self.engine = create_engine('sqlite:///dudebro.db', echo=True)
    #     self.Base.metadata.create_all(self.engine)
    #     # Create a session
    #     Session = sessionmaker(bind=self.engine)
    #     self.session = Session()

    # def create_user(self, username, password):
    #     new_user = Users(username=username, password=password)
    #     self.session.add(new_user)
    #     self.session.commit()

    #     id = self.session.query(Users.id).filter_by(username=username, password=password).first()
    #     return id.id

    def create_container(self, user_id, subdomain):
        # Log all of this data in a DB

        port = self.get_port()
        if not port:
            raise RuntimeError("Error retrieving port")

        container = self.client.containers.run(
            self.image,
            detach=True,
            tty=True,
            name="dudebro-server",
            labels={"user_id": str(user_id), "subdomain": subdomain}
            #network=self.network_name
        )

        new_container = Containers(subdomain=subdomain, domain=self.default_domain, port=port, weight=0, priority=0, name="dudebro-server", userid=user_id)
        db.session.add(new_container)
        db.session.commit()

        self.create_srv_entry(subdomain, self.default_domain, self.default_target, port)

        return container
    
    def get_port(self):
        ports = db.session.query(Containers.port).order_by(db.desc(Containers.port)).first()
        port = None

        if ports:
            port = ports.port
            print("port", port)
        else:
            return False

        return port + 1
    
    def get_container_ip(self, container):
        container.reload()
        network_settings = container.attrs['NetworkSettings']
        ip_address = network_settings['Networks'][self.network_name]['IPAddress']

        return ip_address

    def create_srv_entry(self, subdomain, domain, target_record, port: int, proxied=False, weight:int=0, priority:int=0):
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

    def get_user_containers(self, user_id):
        return self.client.containers.list(all=True, filters={"label": f"user_id={user_id}"})
    
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