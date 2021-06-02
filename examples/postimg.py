import requests
import json

""" post image and return the response """
""" cli command: curl -F "file=@misha2.jpg" http://localhost:5001/"""

url = "http://0.0.0.0:5001/"
path="kovtun.jpg"

files = {'file': open(path, 'rb')}
response = requests.post(url, files=files)
#print(response.text)
names = ""
names = json.loads(response.text)
print(names)
