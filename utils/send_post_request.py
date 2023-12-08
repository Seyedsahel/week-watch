import requests

server = 'https://getinfo.iran.liara.run/record/'
local = 'http://localhost:8000/record/'
data = {
    'link': 'http://example.com',
    'email': 'TahaM8000@gmail.com'
    }
response = requests.post(local, data=data)

print(response.text)
