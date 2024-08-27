import docker

class Deploy:
    def __init__(self, image, timeout:int=5):
        self.image = image
        self.client = docker.from_env()
        self.timeout = timeout

    def create_container(self, user_id, subdomain):
        container = self.client.containers.run(
            self.image,
            detach=True,
            tty=True,
            labels={"user_id": user_id, "subdomain": subdomain}
        )

        return container

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
    dep = Deploy("debian")
    # dep.create_container("123", "glorp")
    # x = dep.get_user_containers("123")
    # for i in x:
    #     print(i.id)
    # dep.does_user_own("123", "845cca7f6454d75e1499b0454fbedd6abebae0ab8fb0071e090e165caaaba891")
    print(dep.stop_user_container("123","845cca7f6454d75e1499b0454fbedd6abebae0ab8fb0071e090e165caaaba891"))