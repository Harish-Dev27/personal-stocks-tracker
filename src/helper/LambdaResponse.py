import json


def success_response(statusCode, body):
    return {
        "statusCode": statusCode,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"},
    }


def error_response(statusCode, body):
    return {
        "statusCode": statusCode,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"},
    }
