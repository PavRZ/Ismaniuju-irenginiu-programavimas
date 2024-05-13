import json

def update(data1, data2, new_json):

    #reading and loading json files
    with open(data1, "r") as file:
        users1 = json.load(file)
    
    with open(data2, "r") as file:
        users2 = json.load(file)

    print(users1)
    print(users2)

    #updating data in users1 file
    users1["table"]["users"].update(users2["table"]["users"])

    #writing data to a new json file
    with open(new_json, "w") as file:
        json.dump(users1, file, indent = 4)
        

users1_path = "users1.json"
users2_path = "users2.json"
new_users_path = "users.json"

update(users1_path, users2_path, new_users_path)