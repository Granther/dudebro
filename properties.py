from dotenv import load_dotenv
import configparser
import os

class Properties():
    def __init__(self, path):
        load_dotenv()
        self.path = path

    def read_server_properties(self):
        config = configparser.ConfigParser(allow_no_value=True)
        with open(self.path, 'r') as f:
            file_content = '[dummy_section]\n' + f.read()
        config.read_string(file_content)
        
        server_properties = {key: value for key, value in config['dummy_section'].items()}
        
        return server_properties

    def write_server_properties(self, properties):
        try:
            with open(self.path, "w") as f:
                for key, value in properties.items():
                    f.write(f"{key}={value}\n")
            return True
        except:
            return False

    def set_property(self, key, value):
    server_props = self.read_server_properties()
    item = server_props.get(key, False)

    if item:
        server_props[key] = value
        return self.write_server_properties(server_props)
    else:
        return properties

def set_property(key, value):
    properties = Properties('server.properties')

    server_props = properties.read_server_properties()
    item = server_props.get(key, False)

    if item:
        server_props[key] = value
        return properties.write_server_properties(server_props)
    else:
        return properties

if __name__ == "__main__":
    properties = Properties('server.properties')

    x = set_property("server-port", 100)
    print(x)
    # x = properties.read_server_properties()
    # x['motd'] = "special"
    # properties.write_server_properties(x)
    # print(properties.read_server_properties())
