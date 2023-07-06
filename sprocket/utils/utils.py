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

