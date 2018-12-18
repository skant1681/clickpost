import requests, json, urllib, json
from requests.models import Response
from flask import make_response, jsonify


SUCCESS = 200
BAD_REQUEST = 400
NOT_FOUND = 404
INVALID_DATA_CONTENT = 409
UNSUPPORTED_TYPE = 415
INVALID_DATA_FORMAT = 422
INTERNAL_SERVER_ERROR = 500


def construct_response(msg : str,code : int):
    json_str = jsonify({'message':msg})
    return make_response(json_str,code)


def get_response(url, headers, params=None):
    try:
        if not params:
            return requests.request("GET", url, headers=headers)
        else:
            return requests.request("GET", url, headers=headers, params=urllib.parse.urlencode(params))
    except requests.exceptions.ConnectionError as e:
        the_response = Response()
        the_response.status_code = INTERNAL_SERVER_ERROR
        the_response._content = b'{"detail": "Track service server is not responding"}'
        return the_response
