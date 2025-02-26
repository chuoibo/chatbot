import yaml
import logging
import secrets
import hashlib


def read_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)  
        return data
    except FileNotFoundError:
        logging.info(f"Error: The file {file_path} was not found.")
    except yaml.YAMLError as exc:
        logging.info(f"Error parsing YAML file: {exc}")
    except Exception as e:
        logging.info(f"An error occurred: {e}")


def generate_random_string(length):
    return secrets.token_hex(length // 2)  


def generate_request_id(length, max_length):
    random_string = generate_random_string(length)
    h = hashlib.sha256()
    h.update(random_string.encode('utf-8'))
    return h.hexdigest()[:max_length+1]