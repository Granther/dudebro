import os

from kubernetes import client, config

def create_client():
    config_path = 'kubeconfig.yaml'
    config.load_kube_config(config_file=config_path)
    
    c = client.CoreV1Api()
    if not c:
        return False
    
    return c
