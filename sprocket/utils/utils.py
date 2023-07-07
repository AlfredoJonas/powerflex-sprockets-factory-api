import os
import json


def read_json_file(url):
    """
    This function reads a JSON file from a given URL and returns its contents as a Python object.

    :param url: The `url` parameter is a string that represents the path to a JSON file. It is used to
    locate and read the JSON file
    :return: The function `read_json_file` returns the data loaded from a JSON file located at the
    specified URL.
    """
    file_path = os.path.join(url)

    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    return data


def check_keys_on_dict(keys, dictionary):
    """
    The function checks if all the keys in a list are present in a dictionary and returns a list of
    missing keys.

    :param keys: A list of strings representing the keys that should be present in the dictionary
    :param dictionary: A Python dictionary that contains key-value pairs
    :return: The function `check_keys_on_dict` takes in two arguments: `keys` and `dictionary`. It
    returns a list of all the keys in `keys` that are not present in `dictionary`.
    """
    return [field for field in keys if field not in dictionary]


def add_field_to_response(response, key, value):
    # Get the underlying JSON data
    json_data = json.loads(response.content)

    # Add a new field to the JSON data
    json_data[key] = value

    # Set the modified JSON data back to the response
    response.content = json.dumps(json_data)
    return response
