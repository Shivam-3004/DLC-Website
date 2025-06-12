import requests

url = "https://dlc-website.onrender.com/chat"
data = {"message": "Hello DigiBuddy!"}

response = requests.post(url, json=data)
print(response.json())  # Should return AI response