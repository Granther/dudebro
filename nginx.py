import requests
from uuid import uuid4

class NginxInteractor:
    def __init__(self, host, port):
        self.host = host
        self.port = port 

    def create_subdomain(self, subdomain, container_addr):
        url = f"http://{self.host}:{self.port}/create_subdomain"
        data = {
            "subdomain": subdomain,
            "host": container_addr
        }

        return requests.post(url, json=data).json()

        
if __name__ == "__main__":
    pass