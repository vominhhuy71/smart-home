import requests, json
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

while True:
    id, text = reader.read()
    key = {"key":id}
    json_key = json.dumps(key)
    new_headers = {'content-type':'application/json'}
    post_key = requests.delete('http://localhost:5000/info/security/keys',data = json_key, headers=new_headers)
    if (post_key.status_code==200):
        print('Successfully deleted!')
        break