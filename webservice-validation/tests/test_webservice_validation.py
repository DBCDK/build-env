#!/usr/bin/env python3

import unittest
import unittest.mock
from pathlib import PurePath
import os
import sys

import webservice_validation.webservice_validation


def get_tests_path(module_name: str = __name__, parent_index: int = 0):
    try:
        # get the parent directory of the directory this file is in
        p = PurePath(sys.modules[module_name].__file__)
        return str(p.parents[parent_index])
    except IndexError:
        return os.path(os.getcwd(), "tests")


class MockResponse(object):
    def __init__(self, status_code: int, data: dict):
        self.status_code = status_code
        self.data = data
        self.text = "mock-response"

    def json(self):
        return self.data


class WebserviceValidationTest(unittest.TestCase):
    @unittest.mock.patch("webservice_validation.webservice_validation.requests.post")
    def test_validate(self, mock_requests):
        mock_requests.side_effect = [
            MockResponse(
                200,
                {
                    "response": [
                        {
                            "term": "erindringer",
                            "work": "work:1474702",
                            "weight": 1409,
                            "type": "subject",
                        }
                    ]
                },
            ),
            MockResponse(
                200,
                {
                    "response": [
                        {
                            "term": "Fremmedhad ; mobning ; familien ; barndom ; Danmark ; Nykøbing Falster ; Tyskland ; 1960-1969 ; 1970-1979 ; barndomserindringer ; erindringer",
                            "work": "work:818513",
                            "weight": 1187,
                            "type": "subject",
                        },
                        {
                            "term": "erindring",
                            "work": "work:1408996",
                            "weight": 561,
                            "type": "subject",
                        },
                    ]
                },
            ),
        ]
        tests_path = get_tests_path(__name__)
        spec = webservice_validation.webservice_validation.load_spec(
            f"{tests_path}/data/validation.yml"
        )
        result = webservice_validation.webservice_validation.validate("url", spec)
        self.assertEqual(mock_requests.call_count, 2)
        self.assertEqual(result, True)

    @unittest.mock.patch("webservice_validation.webservice_validation.requests.post")
    def test_validate_empty_response(self, mock_requests):
        mock_requests.side_effect = [
            MockResponse(
                200,
                {
                    "response": [
                        {
                            "term": "erindringer",
                            "work": "work:1474702",
                            "weight": 1409,
                            "type": "subject",
                        }
                    ]
                },
            ),
            MockResponse(200, {"response": []}),
        ]
        tests_path = get_tests_path(__name__)
        spec = webservice_validation.webservice_validation.load_spec(
            f"{tests_path}/data/validation.yml"
        )
        result = webservice_validation.webservice_validation.validate("url", spec)
        self.assertEqual(mock_requests.call_count, 2)
        self.assertEqual(result, False)

    @unittest.mock.patch("webservice_validation.webservice_validation.requests.post")
    def test_validate_failure_status_code(self, mock_requests):
        mock_requests.side_effect = [
            MockResponse(
                200,
                {
                    "response": [
                        {
                            "term": "erindringer",
                            "work": "work:1474702",
                            "weight": 1409,
                            "type": "subject",
                        }
                    ]
                },
            ),
            MockResponse(415, None),
        ]
        tests_path = get_tests_path(__name__)
        spec = webservice_validation.webservice_validation.load_spec(
            f"{tests_path}/data/validation.yml"
        )
        result = webservice_validation.webservice_validation.validate("url", spec)
        self.assertEqual(mock_requests.call_count, 2)
        self.assertEqual(result, False)
