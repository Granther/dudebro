from kubernetes import client, config

# Specify the path to your kubeconfig file
kubeconfig_path = "kubeconfig.yaml"

# Load the kubeconfig from the specified file
config.load_kube_config(config_file=kubeconfig_path)

# Create an API client (for CoreV1 API, to list pods for example)
v1 = client.CoreV1Api()

# List all pods in the default namespace
print("Listing pods in the default namesppyace:")
pods = v1.list_pod_for_all_namespaces(watch=False)
for pod in pods.items:
    print(f"{pod.metadata.namespace} - {pod.metadata.name}")
