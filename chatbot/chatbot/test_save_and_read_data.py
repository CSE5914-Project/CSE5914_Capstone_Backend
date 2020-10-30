import json

data = {
    "userinfo": {
        'username': 'drago1234',
        'age': 21,
        'language': 'en',
        'session_id': '12345'
    }
}

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
    # outfile.write(json.dumps(data), outfile)