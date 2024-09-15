import os

from dotenv import load_dotenv
from mcrcon import MCRcon

from logger import create_logger

class DudeRcon:
    def __init__(self):
        load_dotenv()
        self.logger = create_logger(__name__)

    def command(self, queue, command: str, port: int, ip: str):
        rcon_pass = os.getenv("RCON_PASSWORD")

        with MCRcon(ip, rcon_pass, port=port) as mcr:
            res = mcr.command(command)
            queue.put(res)

            return True

        return False

