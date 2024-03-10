import json


def indent_json(file_path, indent=4):
    with open(file_path, 'r') as f:
        data = json.load(f)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=indent)


def print_keys(json_file_path, artifact):
    # Load the JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Get the keys under "observations" -> "default_1"
    artifact = data.get("observations", {}).get(artifact, {}).keys()

    # Print the keys
    for key in artifact:
        print(key)


print_keys("../measured_data/test1.json", "default_1")
