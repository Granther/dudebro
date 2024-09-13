from dotenv import load_dotenv
import configparser
import os

from logger import create_logger

class Properties():
    def __init__(self):
        load_dotenv()
        self.logger = create_logger(__name__)

    def read_server_properties(self, uuid: str):
        path = os.path.join(os.getenv("INSTANCES_DIR"), f"{uuid}/server.properties")
        config = configparser.ConfigParser(allow_no_value=True)
        with open(path, 'r') as f:
            file_content = '[dummy_section]\n' + f.read()
        config.read_string(file_content)
        
        server_properties = {key: value for key, value in config['dummy_section'].items()}
        
        return server_properties

    def write_server_properties(self, uuid: str, properties: dict):
        path = os.path.join(os.getenv("INSTANCES_DIR"), f"{uuid}/server.properties")
        try:
            with open(path, "w") as f:
                for key, value in properties.items():
                    f.write(f"{key}={value}\n")
            return True
        except:
            return False

    def set_property(self, uuid: str, key, value):
        server_props = self.read_server_properties(uuid)
        item = server_props.get(key, False)

        if item:
            server_props[key] = value
            return self.write_server_properties(uuid, server_props)
        else:
            return properties

def set_property(uuid: str, key, value):
    properties = Properties()
    return properties.set_property(uuid, key, value)

if __name__ == "__main__":
    # properties = Properties('server.properties')

    # x = set_property("server-port", 100)
    # print(x)
    pass
    # x = properties.read_server_properties()
    # x['motd'] = "special"
    # properties.write_server_properties(x)
    # print(properties.read_server_properties())
