#!/usr/bin/env python3

import argparse
import json
import sys

import jsonpath_ng
import requests
import yaml

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint")
    parser.add_argument("validation_spec", metavar="validation-spec")
    parser.add_argument("--from-endpoints-json-file",
        type=argparse.FileType(encoding="utf-8"),
        help="Validate from a list of endpoints instead of the single positional argument endpoint. The format should be a list of object containing an `ip` key with the endpoint. This output can be fetched with the `kube-tools ip-addresses` command.")
    parser.add_argument("-p", "--port", type=int, help="Port to query on the service which is to be validated.")
    return parser.parse_args()

def load_spec(path):
    with open(path) as fp:
        return yaml.load(fp, Loader=yaml.Loader)

def get_field(spec, name, default=None):
    return spec[name] if name in spec else default

def print_failure_message(url, validation_idx, validation_path, message):
    print(f"validation {validation_idx} {validation_path} [{url}] failed: {message}", file=sys.stderr)

def validate(endpoint, spec, port = None):
    # This object is placed here in order to make mocks work. If the object
    # is placed in the global scope like previously, mocking doesn't work
    # because the functions are read on import of the module while mocking
    # only takes effect on each call of the test methods.
    methods = {
        "get": requests.get,
        "post": requests.post
    }

    if endpoint[:4] != "http":
        endpoint = f"http://{endpoint}"
    if port is not None:
        endpoint = f"{endpoint}:{port}"
    results = []
    for i, validation in enumerate(spec):
        validation_path = validation["path"]
        if validation_path[0] == "/":
            validation_path = validation_path[1:]
        url = f"{endpoint}/{validation_path}"
        headers = get_field(validation, "headers")
        data = get_field(validation, "data")
        if data is not None:
            data = data.encode("utf8")
        requests_parameters = get_field(validation, "requests-parameters", {})
        result = methods[validation["method"]](url, headers=headers,
            data=data, **requests_parameters)
        if result.status_code == validation["response"]["status_code"]:
            response_type_json = get_field(validation["response"], "json", True)
            response_len = get_field(validation["response"], "len", 1)
            if response_type_json:
                jsonpath = get_field(validation["response"], "jsonpath")
                if jsonpath is not None:
                    try:
                        exp = jsonpath_ng.parse(jsonpath)
                    except TypeError as e:
                        print_failure_message(endpoint, i, validation_path, f"Error parsing jsonpath {jsonpath}: {e}")
                        results.append(False)
                        continue
                    m = exp.find(result.json())
                    if len(m) == 0:
                        print_failure_message(endpoint, i, validation_path, f"no matches found for jsonpath {jsonpath}")
                        results.append(False)
                        continue
                    o = m[0].value
                else:
                    o = result.json()
                try:
                    if len(o) >= response_len:
                        results.append(True)
                    else:
                        print_failure_message(endpoint, i, validation_path, f"result {o} didn't satisfy the required length {response_len}")
                        results.append(False)
                except json.JSONDecodeError as e:
                    print_failure_message(endpoint, i, validation_path, f"couldn't parse response as json - {e}")
                    results.append(False)
            else:
                res = len(result.text) >= response_len
                results.append(res)
                if not res:
                    print_failure_message(endpoint, i, validation_path, f"expected response length {response_len}, got {len(result.text)}")
        else:
            print_failure_message(endpoint, i, validation_path, f"result was {result.text}")
            results.append(False)
    return all(results)

def main():
    args = setup_args()
    spec = load_spec(args.validation_spec)
    if args.from_endpoints_json_file is not None and args.endpoint != "from-endpoints-json-file":
        print("You cannot specify both --from-endpoints-json-file and a positional endoint. If you use --from-endpoints-json-file, set the positional endpoint argument to be \"from-endpoints-json-file\".")
        sys.exit(1)
    elif args.from_endpoints_json_file is not None:
        try:
            endpoints = json.load(args.from_endpoints_json_file)
            for e in endpoints:
                if not validate(e["ip"], spec, args.port):
                    sys.exit(1)
        except json.JSONDecodeError as e:
            print("Error parsing input given to --from-endpoints-json-file")
            sys.exit(1)
    else:
        if not validate(args.endpoint, spec, args.port):
            sys.exit(1)

if __name__ == "__main__":
    main()
