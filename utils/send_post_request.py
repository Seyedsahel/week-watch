import requests

url = 'https://getinfo.iran.liara.run/record/'
data = {'link': 'http://example.com'}
response = requests.post(url, data=data)

print(response.text)
