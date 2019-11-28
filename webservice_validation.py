#!/usr/bin/env python3

import argparse
import json

import requests
import yaml

methods = {
    "get": requests.get,
    "post": requests.post
}

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint")
    parser.add_argument("validation_spec", metavar="validation-spec")
    return parser.parse_args()

def load_spec(path):
    with open(path) as fp:
        return yaml.load(fp, Loader=yaml.Loader)

def get_field(spec, name, default=None):
    return spec[name] if name in spec else default

def validate(endpoint, spec):
    results = []
    for i, validation in enumerate(spec):
        validation_path = validation["path"]
        if validation_path[0] == "/":
            validation_path = validation_path[1:]
        url = f"{endpoint}/{validation_path}"
        headers = get_field(validation, "headers")
        data = get_field(validation, "data")
        requests_parameters = get_field(validation, "requests-parameters", {})
        result = methods[validation["method"]](url, headers=headers,
            data=data, **requests_parameters)
        if result.status_code == validation["response"]["status_code"]:
            response_type_json = get_field(validation["response"], "json", True)
            if response_type_json:
                try:
                    if len(result.json()) > 0:
                        results.append(True)
                except json.JSONDecodeError as e:
                    print(f"validation {i} {validation_path} failed: couldn't parse response as json - {e}")
                    results.append(False)
            else:
                results.append(len(result.text) > 0)
        else:
            print(f"validation {i} {validation_path} failed: result was {result.text}")
            results.append(False)
    return all(results)

if __name__ == "__main__":
    args = setup_args()
    spec = load_spec(args.validation_spec)
    validate(args.endpoint, spec)
