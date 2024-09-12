import os
from dotenv import load_dotenv

from mcrcon import MCRcon

class DudeRcon:
    def __init__(self):
        load_dotenv()

    def command(self, str: command, int: port, str: ip):
        rcon_pass = os.getenv("RCON_PASSWORD")

        with MCRcon(ip, rcon_pass, port=port) as mcr:
            res = mcr.command(command)
            return res

        return False

    def op(self, player, ):
        pass


# Set RCON parameters
rcon_host = 'localhost'  # Or the Docker container IP if running externally
rcon_port = 25575
rcon_password = 'your_secure_password'

# Connect to the Minecraft server via RCON
with MCRcon(rcon_host, rcon_password, port=rcon_port) as mcr:
    # Send a command to the Minecraft server
    response = mcr.command("say Hello from RCON!")
    print(response)  # Print the response from the server

    # Execute more commands as needed
    response = mcr.command("list")
    print("Connected players:", response)


from mcrcon import MCRcon
with MCRcon("10.1.1.1", "sekret", port=) as mcr    
    resp = mcr.command("/whitelist add bob"    
