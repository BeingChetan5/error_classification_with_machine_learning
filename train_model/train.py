import requests

response = requests.post("http://localhost:8080/train")
print("Training model response:", response.json())
