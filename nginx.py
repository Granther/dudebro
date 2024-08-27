import requests

url = "http://localhost:5000/create_subdomain"
data = {
    "subdomain": "example"
}

response = requests.post(url, json=data)
print(response.json())
