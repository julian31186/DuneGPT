import json

def remove_non_ascii(s):
    return "".join(c for c in s if ord(c)<128)

data = "../data/embeds.json"

cleaned_vector = []

with open(data,"r+") as f:
    json_content = json.load(f)
    for obj in json_content:
        obj["id"] = remove_non_ascii(obj["id"])
        cleaned_vector.append(obj)

with open(data, 'w') as f:
    json.dump(cleaned_vector, f ,indent=4)