import json

data = '{"firstName": "tester", "lastName": "tester", "city": "Vilnius"}'

s = json.loads(data)
print(s)

s['firstName'] = "Augustas"
s['lastName'] = "Paketuras"
s['city'] = "Moletai"
s['age'] = "22"

print(s)