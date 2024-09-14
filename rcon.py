import os

from dotenv import load_dotenv
from mcrcon import MCRcon

from logger import create_logger

class DudeRcon:
    def __init__(self):
        load_dotenv()
        self.logger = create_logger(__name__)

    def command(self, str: command, int: port, str: ip):
        rcon_pass = os.getenv("RCON_PASSWORD")

        with MCRcon(ip, rcon_pass, port=port) as mcr:
            res = mcr.command(command)
            return res

        return False


# Set RCON parameters
rcon_host = 'localhost'  # Or the Docker container IP if running externally
rcon_port = 25575
rcon_password = 'your_secure_password' 
