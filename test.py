# from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.sql import func

# # Create an SQLite engine
# engine = create_engine('sqlite:///dudebro.db', echo=True)

# Base = declarative_base()

# # Define a sample model
# class User(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, primary_key=True)
#     created = Column(TIMESTAMP, nullable=False, server_default=func.now())
#     username = Column(String)
#     password = Column(String)
#     containers = relationship("Container", back_populates="user")

#     def __repr__(self):
#         return f"<User(username={self.username}, password={self.password})>"
    
# class Container(Base):
#     __tablename__ = 'containers'
    
#     id = Column(Integer, primary_key=True)
#     created = Column(TIMESTAMP, nullable=False, server_default=func.now())
#     subdomain = Column(String)
#     domain = Column(String)
#     port = Column(Integer)
#     weight = Column(Integer)
#     priority = Column(Integer)
#     name = Column(String)
#     userid = Column(Integer, ForeignKey("users.id"))
#     type = Column(String)

#     user = relationship("User", back_populates="containers")

#     def __repr__(self):
#         return f"<Container(subdomain={self.subdomain}, domain={self.domain}, port={self.port}, weight={self.weight}, priority={self.priority}, name={self.name}, userid={self.userid}, type={self.type})>"

# Base.metadata.create_all(engine)

# # Create a session
# Session = sessionmaker(bind=engine)
# session = Session()

# new_user = User(username='JohnDoe', password="skib")
# new_cont = Container(subdomain="test", domain="test", port=5, weight=5, priority=5, name="test name", type="test type", userid=1)

# session.add(new_user)
# session.add(new_cont)

# session.commit()

# user = session.query(User).filter_by(username='JohnDoe').first()

# if user:
#     containers = user.containers 
#     for container in containers:
#         print(container.name)
# else:
#     print("User not found.")

# import configparser

# def read_server_properties(file_path):
#     config = configparser.ConfigParser(allow_no_value=True)
#     with open(file_path, 'r') as f:
#         file_content = '[dummy_section]\n' + f.read()
#     config.read_string(file_content)
    
#     server_properties = {key: value for key, value in config['dummy_section'].items()}
    
#     return server_properties

# properties = read_server_properties('server.properties')
# print(properties)


import docker

client = docker.from_env()

# Listen to container events
def monitor_events():
    for event in client.events(decode=True):
        if event.get('Type') == 'container':
            container_id = event.get('id')
            action = event.get('Action')
            if action in ['start', 'stop', 'die', 'restart']:
                print(f"Container {container_id} changed state: {action}")

# Start listening for container events
monitor_events()